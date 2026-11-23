"""
harness.py - runs a student's Python program and a task's tests.

Used by py-worker.js (the website, where Python is Pyodide running in the
browser) and by teacher/check_tasks.py (the Python on the teacher's computer).

A task file in tasks/ sees two names from here, section and task, and each of
its test functions is handed a Tester, which the task files call t:

    section("2. Variables")

    @task("Rectangle", starter=RECTANGLE)
    def rectangle(t):
        '''The description students read, written as the function's docstring.'''
        r = t.run()
        t.test("prints the area", r.check_output(["Area: 40"]))

README.md lists everything t and r can do.

Kept to Python 3.9 syntax, so the checker runs on the teacher's computer too.
"""
import ast
import builtins
import contextlib
import difflib
import inspect
import io
import json
import math
import random
import re
import sys
import textwrap
import time
import tokenize
import traceback
import warnings

STUDENT_FILE = "<your code>"  # the file name the student's program is compiled under

RUN_SECONDS = 5     # how long the Run button lets a program run
TEST_SECONDS = 2    # how long each run made by a test may take...
QUICK_SECONDS = 0.5 # ...once one of that task's runs has been stopped for taking too long
MAX_LINES = 1000    # printing more than this stops the program...
MAX_CHARS = 20000   # ...and so does printing more characters than this


# ----------------------------------------------------------------------------
# Stopping a program from the inside
# ----------------------------------------------------------------------------
class _Stop(BaseException):
    """Ends the student's program. Not an Exception, so `except Exception` can't catch it."""


class _NeedInput(_Stop):
    pass


class _TooLong(_Stop):
    pass


class _TooMuch(_Stop):
    pass


class _Screen:
    """Stands in for sys.stdout while a program runs: what's printed goes to the Run."""

    def __init__(self, run):
        self.run = run

    def write(self, text):
        text = str(text)
        self.run._printed(text)
        return len(text)

    def flush(self):
        pass

    def isatty(self):
        return False


@contextlib.contextmanager
def _sandbox(run, seconds):
    """While this is open: print() and input() belong to `run`, sleep() doesn't
    wait, and the program is stopped once it has run for `seconds`."""
    deadline = time.monotonic() + seconds
    count = [0]

    def on_line(frame, event, arg):
        if event == "line":
            count[0] += 1
            if count[0] % 200 == 0 and time.monotonic() > deadline:
                raise _TooLong(frame.f_lineno)
        return on_line

    def on_call(frame, event, arg):
        # Only the student's own lines are counted; library code runs at full speed.
        return on_line if frame.f_code.co_filename == STUDENT_FILE else None

    saved = sys.stdout, builtins.input, time.sleep
    sys.stdout, builtins.input, time.sleep = _Screen(run), run._input, lambda seconds=0: None
    sys.settrace(on_call)
    try:
        yield
    finally:
        sys.settrace(None)
        sys.stdout, builtins.input, time.sleep = saved


# ----------------------------------------------------------------------------
# Explaining an error
# ----------------------------------------------------------------------------
_INPUT_IS_TEXT = ("One of these values is text, not a number. input() always gives text: "
                  "wrap it like int(input(...)) or float(input(...)).")

# (pattern found in "ErrorName: message", hint) - the first match is used.
_HINTS = [
    (r"NameError", "Check the spelling and the capital letters. If it's meant to be text, it needs \"quotes\"."),
    (r"expected ':'", "Lines that start with if, elif, else, for, while or def end with a colon  :"),
    (r"expected an indented block", "The lines inside an if, a loop or a def must be indented (4 spaces)."),
    (r"IndentationError|TabError", "Check the spaces at the start of this line. Lines that belong together start at the same position."),
    (r"was never closed|unexpected EOF|EOF in multi-line", "A bracket is missing its partner: every ( needs a )."),
    (r"unterminated string|EOL while scanning", "A quotation mark is missing its partner: text needs \" at both ends."),
    (r"Maybe you meant '=='|cannot assign to", "To compare two values use ==  (two equals signs). One = stores a value in a variable."),
    (r"Missing parentheses in call to 'print'", "print needs brackets:  print(\"Hello\")"),
    (r"can only concatenate str|must be str, not", "Text and a number can't be joined with +. Separate them with a comma inside print( ), or turn the number into text with str( )."),
    (r"unsupported operand type.*'str'|can't multiply sequence by non-int|not supported between instances of.*'str'", _INPUT_IS_TEXT),
    (r"invalid literal for int\(\)", "int( ) only understands whole numbers. For decimals use float( )."),
    (r"could not convert string to float", "float( ) needs a number, and it was given something else."),
    (r"ZeroDivisionError", "Dividing by zero isn't possible. Check the value you're dividing by."),
    (r"object is not callable", "Brackets straight after a number or a variable mean \"call this\". To multiply, write the star:  2 * (x + 1)"),
    (r"ModuleNotFoundError", "That module isn't available on this page."),
    (r"RecursionError", "A function keeps calling itself and never stops."),
    (r"SyntaxError", "Python couldn't read this line. Check for a missing bracket, quotation mark, comma or colon, here or on the line above."),
]


def _hint(summary):
    for pattern, hint in _HINTS:
        if re.search(pattern, summary):
            return hint
    return ""


def _explain(exc, source):
    """(message, line number or None, error name) for an exception from the student's program."""
    kind = type(exc).__name__
    line = None
    if isinstance(exc, SyntaxError):
        if exc.filename == STUDENT_FILE:
            line = exc.lineno
    else:
        for frame in traceback.extract_tb(exc.__traceback__):
            if frame.filename == STUDENT_FILE:
                line = frame.lineno  # the last of the student's lines the error passed through
    # The last line Python prints for the error, e.g.
    #   NameError: name 'pritn' is not defined. Did you mean: 'print'?
    summary = "".join(traceback.format_exception_only(type(exc), exc)).strip().split("\n")[-1].strip()
    lines = source.split("\n")
    message = summary
    if line and 1 <= line <= len(lines):
        message = "Error on line %d:\n    %s\n%s" % (line, lines[line - 1].strip(), summary)
    hint = _hint(summary)
    return message + ("\n" + hint if hint else ""), line, kind


# ----------------------------------------------------------------------------
# Comparing values and printed lines
# ----------------------------------------------------------------------------
_NUMBER = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
_ANY = object()


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _close(a, b):
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)


def _same(a, b):
    """Equal, where 20 and 20.0 are the same number and 0.1 + 0.2 is 0.3."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if _is_number(a) and _is_number(b):
        return _close(a, b)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    return type(a) == type(b) and a == b


def _show_number(v):
    return repr(int(v)) if isinstance(v, float) and v.is_integer() and abs(v) < 1e15 else repr(v)


def _split_lines(text):
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def _as_lines(x):
    """Lines from one string (with \\n between lines) or from a list of lines."""
    if isinstance(x, str):
        return _split_lines(x)
    return [str(v) for v in x]


def _tidy_lines(x):
    lines = [line.rstrip() for line in _as_lines(x)]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def _indent(lines):
    return "\n".join("  " + line for line in lines) if lines else "  (nothing)"


def _same_line(want, got, exact):
    if want == got:
        return True
    if exact or _NUMBER.split(want) != _NUMBER.split(got):
        return False
    return all(_close(float(a), float(b)) for a, b in zip(_NUMBER.findall(want), _NUMBER.findall(got)))


def _decimals(number_text):
    return len(number_text.split(".")[1]) if "." in number_text and "e" not in number_text.lower() else 0


def _line_hint(want, got):
    """A likely reason two lines differ, or ""."""
    def squash(s):
        return re.sub(r"\s+", "", s)

    def bare(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())

    if want.lower() == got.lower():
        return "Check the capital letters."
    if squash(want) == squash(got):
        return "Check the spaces."
    if got in ('"' + want + '"', "'" + want + "'"):
        return "The quotation marks were printed too."
    if _NUMBER.split(want) == _NUMBER.split(got):
        pairs = list(zip(_NUMBER.findall(want), _NUMBER.findall(got)))
        if all(_close(float(a), float(b)) for a, b in pairs):
            return "The number is right, but it has to be written exactly this way."
        if all(_close(float(a), round(float(b), _decimals(a))) for a, b in pairs):
            return "Check the rounding. round(number, 2) keeps 2 decimal places."
        return "The words match, but a number is different. Check the calculation."
    if bare(want) == bare(got):
        return "Check the punctuation."
    if "None" in got and "None" not in want:
        return "None usually means printing something that has no value, like print(print(...)) or a function with no return."
    return ""


def compare_output(expected, actual, exact=False):
    """(passed, message) for the lines `actual` against the lines `expected`.

    Spaces at the end of a line and blank lines at the end don't count. Unless
    `exact`, numbers are compared by value: 20 matches 20.0."""
    want, got = _tidy_lines(expected), _tidy_lines(actual)
    if len(want) == len(got) and all(_same_line(w, g, exact) for w, g in zip(want, got)):
        return True, "Printed:\n" + _indent(got)
    if not got:
        return False, "Nothing was printed. Expected:\n" + _indent(want) + "\nPrint each line with print(...)."
    both = ""
    if len(want) > 1 or len(got) > 1:
        both = "\n\nExpected:\n" + _indent(want) + "\nPrinted:\n" + _indent(got)
    for i, (w, g) in enumerate(zip(want, got)):
        if not _same_line(w, g, exact):
            hint = _line_hint(w, g)
            return False, "Line %d should be:\n  %s\nbut it was:\n  %s%s%s" % (i + 1, w, g, "\n" + hint if hint else "", both)
    if len(got) < len(want):
        missing = len(want) - len(got)
        return False, "%s from the end. Next expected:\n  %s%s" % (
            "A line is missing" if missing == 1 else "%d lines are missing" % missing, want[len(got)], both)
    extra = len(got) - len(want)
    return False, "%s:\n  %s%s" % (
        "One extra line was printed" if extra == 1 else "%d extra lines were printed, starting with" % extra,
        got[len(want)], both)


# ----------------------------------------------------------------------------
# One run of the student's program
# ----------------------------------------------------------------------------
class Run:
    """What happened when the program ran. Tests get one from t.run().

    output   the lines print() wrote            prompts  the questions input() asked
    text     the same, as one string            vars     the program's variables afterwards
    error    why it stopped early, or None      value    what a function gave back (after r.call)
    """

    def __init__(self, source, inputs=(), interactive=False):
        self.source = source
        self.text = ""
        self.prompts = []
        self.error = None
        self.error_line = None
        self.error_kind = None
        self.vars = {}
        self.value = None
        self.waiting = False     # interactive only: stopped at an input() nobody has answered yet
        self.transcript = []     # [kind, text] pairs, in order: "out", "prompt" or "in"
        self._answers = [str(x) for x in inputs]
        self._given = len(self._answers)
        self._interactive = interactive
        self._tester = None      # the Tester this run belongs to, if a test made it
        self._globals = {"__name__": "__main__"}
        self._chars = 0
        self._newlines = 0

    @property
    def output(self):
        return _split_lines(self.text)

    # ---- what the sandbox calls ----
    def _show(self, kind, text):
        if self.transcript and self.transcript[-1][0] == kind == "out":
            self.transcript[-1][1] += text
        else:
            self.transcript.append([kind, text])

    def _printed(self, text):
        self.text += text
        self._show("out", text)
        self._chars += len(text)
        self._newlines += text.count("\n")
        if self._chars > MAX_CHARS or self._newlines > MAX_LINES:
            raise _TooMuch()

    def _input(self, prompt=""):
        prompt = str(prompt)
        self.prompts.append(prompt)
        self._show("prompt", prompt)
        if not self._answers:
            raise _NeedInput()
        answer = self._answers.pop(0)
        self._show("in", answer)
        return answer

    def _fail(self, kind, message, line=None):
        self.error, self.error_kind, self.error_line = message, kind, line

    def _execute(self, seconds, action):
        """Do `action` inside the sandbox and record how it ended. Returns what it returned."""
        try:
            with _sandbox(self, seconds):
                return action()
        except _NeedInput:
            if self._interactive:
                self.waiting = True
            elif self._given == 0:
                self._fail("input", "Your program asked for input (%r), but nothing is typed in for this test. "
                                    "Take out the input() line, or check that you chose the right task." % self.prompts[-1])
            else:
                self._fail("input", "Your program asked for input %d times, but this test only types %d answer%s. "
                                    "Check how many input() lines run." % (len(self.prompts), self._given, "" if self._given == 1 else "s"))
        except _TooLong as stop:
            line = stop.args[0] if stop.args else None
            if self._tester:
                self._tester._slow = True
            self._fail("time", "Your program ran for more than %g seconds, so it was stopped%s. A loop that never ends "
                               "is the usual cause: check that the loop's condition can become False."
                               % (seconds, " (at line %d)" % line if line else ""), line)
        except _TooMuch:
            self._fail("output", "Your program printed more than %d lines, so it was stopped. "
                                 "A loop that never ends is the usual cause." % MAX_LINES)
        except SystemExit:
            pass  # exit() or quit(): the program chose to stop
        except BaseException as exc:
            message, line, kind = _explain(exc, self.source)
            self._fail(kind, message, line)
        return None

    def _run_program(self, seconds):
        def action():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                code = compile(self.source, STUDENT_FILE, "exec")
            exec(code, self._globals)

        self._execute(seconds, action)
        self.vars = {k: v for k, v in self._globals.items() if not k.startswith("__")}

    # ---- checks: each returns (passed, message), ready to hand to t.test ----
    def _stopped(self):
        if self.error:
            return False, ("Your program stopped with an error.\n" if self.error_kind not in ("input", "time", "output", "setup") else "") + self.error
        return None

    def _input_note(self):
        """A note for a failed check when the program asked fewer questions than the test answers."""
        if self._answers and not self.error:
            asked = len(self.prompts)
            return "\n\nYour program asked for input %s, and this test expects %d." % (
                "once" if asked == 1 else "%d times" % asked, self._given)
        return ""

    @property
    def ok(self):
        """(passed, message): did the program run to the end without an error?"""
        return self._stopped() or (True, "Ran without errors")

    def check_output(self, expected, exact=False):
        """Did the program print these lines, and nothing else? `expected` is a list of
        lines or one string. Numbers match by value (20 and 20.0) unless exact=True."""
        stopped = self._stopped()
        if stopped:
            return stopped
        passed, message = compare_output(expected, self.output, exact)
        return passed, message if passed else message + self._input_note()

    def check_prints(self, *values):
        """Was each of these printed somewhere? A number matches that number anywhere in
        the output; text matches that text in any capitals. Other printing is allowed."""
        stopped = self._stopped()
        if stopped:
            return stopped
        numbers = [float(n) for n in _NUMBER.findall(self.text)]
        printed = "\nPrinted:\n" + _indent(self.output)
        for value in values:
            if _is_number(value):
                if not any(_close(value, n) for n in numbers):
                    return False, "Expected the number %s to be printed.%s%s" % (_show_number(value), printed, self._input_note())
            elif str(value).lower() not in self.text.lower():
                return False, "Expected \"%s\" to be printed.%s%s" % (value, printed, self._input_note())
        return True, printed.strip()

    def check_var(self, name, expected=_ANY):
        """Does the program have a variable with this name (and, if given, this value)?"""
        stopped = self._stopped()
        if stopped:
            return stopped
        if name not in self.vars:
            near = difflib.get_close_matches(name.lower(), [k.lower() for k in self.vars], 1, 0.75)
            found = [k for k in self.vars if near and k.lower() == near[0]]
            return False, "Couldn't find a variable called %s.%s" % (
                name, " (There is one called %s. The spelling and capital letters have to match.)" % found[0] if found else "")
        value = self.vars[name]
        if expected is _ANY or _same(value, expected):
            return True, "%s = %r" % (name, value)
        if isinstance(value, str) and _is_number(expected):
            return False, "%s holds the text %r, not a number. input() always gives text: wrap it in int( ) or float( )." % (name, value)
        return False, "%s should be %r, but it is %r." % (name, expected, value)

    def call(self, name, *args, inputs=()):
        """Call one of the program's functions. Returns a Run for the call: .value is
        what it gave back, .output what it printed, .error why it stopped (or None)."""
        call = Run(self.source, inputs)
        call._globals, call._tester = self._globals, self._tester
        fn = self._globals.get(name)
        if not callable(fn):
            call._fail("setup", "Couldn't find a function called %s. Define it with:  def %s(...):" % (name, name))
            return call
        call.value = call._execute(_seconds(self._tester), lambda: fn(*args))
        return call

    def check_returns(self, name, args, expected):
        """Does the program's function name(*args) give back `expected`?"""
        stopped = self._stopped()
        if stopped:
            return stopped
        if not isinstance(args, (list, tuple)):
            args = (args,)
        shown = "%s(%s)" % (name, ", ".join(repr(a) for a in args))
        call = self.call(name, *args)
        if call.error_kind == "setup":
            return False, call.error
        if call.error:
            return False, "%s stopped with an error.\n%s" % (shown, call.error)
        if _same(call.value, expected):
            return True, "%s gave back %r" % (shown, call.value)
        if call.value is None:
            return False, ("%s gave back nothing (None), and it should give back %r. Does the function end with return? "
                           "print() shows a value, but it doesn't give it back." % (shown, expected))
        return False, "%s should give back %r, but it gave back %r." % (shown, expected, call.value)


def _with_values(source, values):
    """The source with `name = ...` rewritten for each name in `values`: the first
    such line at the left edge of the program. Returns (source, None), or
    (None, name) if there's no line that gives `name` a value."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source, None  # the run will report the syntax error itself
    data = source.encode("utf-8")
    starts = [0]
    for line in data.split(b"\n"):
        starts.append(starts[-1] + len(line) + 1)
    edits = []
    for name, value in values.items():
        for node in tree.body:
            target = None
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                target = node.target
            if isinstance(target, ast.Name) and target.id == name:
                v = node.value
                edits.append((starts[v.lineno - 1] + v.col_offset, starts[v.end_lineno - 1] + v.end_col_offset, repr(value)))
                break
        else:
            return None, name
    for start, end, text in sorted(edits, reverse=True):
        data = data[:start] + text.encode("utf-8") + data[end:]
    return data.decode("utf-8"), None


def _seconds(tester):
    """How long a test's run may take: less once the program has shown it can hang,
    so a loop that never ends doesn't cost 2 seconds for every test."""
    return QUICK_SECONDS if tester and tester._slow else TEST_SECONDS


def run_program(source, inputs=(), interactive=False, seconds=None, seed=None, values=None, tester=None):
    """Run a program from the top and return its Run."""
    if isinstance(inputs, (str, int, float)):
        inputs = [inputs]
    if seconds is None:
        seconds = _seconds(tester)
    run = Run(source, inputs, interactive)
    run._tester = tester
    if values:
        changed, missing = _with_values(source, values)
        if missing:
            run._fail("setup", "This test changes the variable %s, so your code needs a line that starts with  %s =  "
                               "(at the left edge, not inside a loop or an if)." % (missing, missing))
            return run
        run.source = changed
    random.seed(seed)
    run._run_program(seconds)
    return run


# ----------------------------------------------------------------------------
# What a task's test function is given
# ----------------------------------------------------------------------------
class Tester:
    def __init__(self, source):
        self.code = source      # the student's code, as text
        self.results = []       # [{name, passed, message}]
        self._tokens = None
        self._slow = False      # a run was stopped for taking too long

    def run(self, inputs=(), seed=None, **values):
        """Run the student's program from the top and return the Run.

        inputs       what to type for each input(), in order
        seed         a number that makes random give the same values every time
        name=value   run it as if the line  name = ...  said  name = value
        """
        return run_program(self.code, inputs, seed=seed, values=values, tester=self)

    def test(self, name, result=True, message=""):
        """Record one test. `result` is True/False or the (passed, message) a check gives."""
        if isinstance(result, tuple):
            passed = bool(result[0])
            message = result[1] if len(result) > 1 and not message else message
        else:
            passed = bool(result)
        self.results.append({"name": str(name), "passed": passed, "message": str(message or "")})
        return passed

    def count(self, word):
        """How many times a word or symbol is in the code, e.g. "for", "print", "**".
        Text inside quotation marks and comments doesn't count."""
        if self._tokens is None:
            self._tokens = []
            try:
                for tok in tokenize.generate_tokens(io.StringIO(self.code).readline):
                    if tok.type in (tokenize.NAME, tokenize.OP, tokenize.NUMBER):
                        self._tokens.append(tok.string)
            except (tokenize.TokenError, SyntaxError):
                pass  # unfinished code: count what was read before the problem
        return self._tokens.count(str(word))

    def uses(self, *words):
        """Is every one of these words or symbols in the code?"""
        return all(self.count(w) > 0 for w in words)


# ----------------------------------------------------------------------------
# The list of tasks
# ----------------------------------------------------------------------------
_tasks = {}                                 # key -> task, in the order they were added
_loading = {"file": "", "section": ""}


def section(name):
    """The section the tasks below this line belong to."""
    _loading["section"] = str(name)


def _tidy_code(text):
    text = textwrap.dedent(text or "").strip("\n")
    return text + "\n" if text else ""


def task(title, starter=""):
    """Decorator that adds a task. The function is the task's tests, its docstring
    is the description students read, and its name identifies the task."""
    def register(fn):
        key = "%s:%s" % (_loading["file"], fn.__name__)
        if key in _tasks:
            raise ValueError("two tasks in this file use the function name %s" % fn.__name__)
        _tasks[key] = {
            "key": key, "file": _loading["file"], "id": fn.__name__, "section": _loading["section"],
            "title": str(title), "description": inspect.cleandoc(fn.__doc__ or ""),
            "starter": _tidy_code(starter), "fn": fn,
        }
        return fn
    return register


def _section_from_file(file):
    words = re.sub(r"\.py$", "", file)
    words = re.sub(r"^\d+[_\-\s]*", "", words)
    return " ".join(w.capitalize() for w in re.split(r"[_\-\s]+", words) if w)


def load_task_file(file, source):
    """Add the tasks one file in tasks/ defines. Returns "" or what went wrong."""
    for key in [k for k, t in _tasks.items() if t["file"] == file]:
        del _tasks[key]
    _loading["file"], _loading["section"] = file, _section_from_file(file)
    try:
        exec(compile(source, "tasks/" + file, "exec"), {"__name__": "tasks", "section": section, "task": task})
    except BaseException as exc:
        return "%s (%s)" % (file, "".join(traceback.format_exception_only(type(exc), exc)).strip().split("\n")[-1])
    return ""


def all_tasks():
    return list(_tasks.values())


def check(key, source):
    """Run one task's tests on a student's code. Returns the list of results."""
    t = Tester(source)
    try:
        _tasks[key]["fn"](t)
    except Exception as exc:
        where = [f.lineno for f in traceback.extract_tb(exc.__traceback__) if f.filename.startswith("tasks/")]
        t.test("The rest of the tests", False, "The tests stopped early: %s: %s%s" % (
            type(exc).__name__, exc, " (line %d of the task file)" % where[-1] if where else ""))
    return t.results


# ----------------------------------------------------------------------------
# For py-worker.js: everything crosses to JavaScript as JSON text
# ----------------------------------------------------------------------------
def catalog_json():
    return json.dumps([{k: v for k, v in t.items() if k != "fn"} for t in _tasks.values()])


def run_json(source, inputs_json="[]", seed=None):
    """The Run button: run the program, typing `inputs`. If it asks for more input
    than that, "waiting" is true and the page asks the student for the next answer."""
    run = run_program(source, json.loads(inputs_json), interactive=True, seconds=RUN_SECONDS, seed=seed)
    return json.dumps({"transcript": run.transcript, "error": run.error, "errorLine": run.error_line, "waiting": run.waiting})


def check_json(key, source):
    if key not in _tasks:
        return json.dumps({"missing": True, "results": []})
    return json.dumps({"results": check(key, source)})
