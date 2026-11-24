# Python Mini Tasks (web)

A web page where students write Python, run it, and check it against a task's
tests, all inside the browser. Nothing is installed and no files are needed, so it
works on a locked-down Chromebook. It is the Python counterpart of the JavaScript
Mini Task tester, and is published the same way: as a GitHub Pages site.

## What students see

- A list of tasks, grouped in sections, with a tick beside each one they've finished.
- The chosen task's description, and an editor that starts with the task's starter
  code. The editor colours keywords, numbers and text, shows line numbers, and
  indents the way Python expects (Tab types 4 spaces; Enter after a `:` indents).
- **Run** runs the program and shows what it prints. `input()` works: the page asks
  for each answer under the output. Ctrl + Enter also runs.
- **Check my code** runs the task's tests and lists each one as PASS or FAIL, with
  a reason for each failure.
- **Predict** tasks show programs to read instead of an editor, with a box under
  each for what it prints.
- Each task is labelled **Learn** (a lesson step) or **Mild**, **Medium**, **Hot**
  or **Spicy** (practice).
- **Scratchpad**, at the top of the list, is a blank program that nothing checks.
- **Copy my code** copies the program, to paste into a D2L submission or a document.

Each student's code and ticks are kept by the browser they used (`localStorage`).
They are not sent anywhere, and they don't follow a student to another device.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The page. |
| `py-worker.js` | Starts Python in the background and passes requests to it. |
| `harness.py` | Runs a student's program and a task's tests. All the checking is here. |
| `tasks/manifest.json` | The task files the site shows, in order. |
| `tasks/*.py` | The tasks. Each file holds one or more. |
| `teacher/` | Your tools and the model solutions. Never published (see `.gitignore`). |

## Writing a task

A task is a Python function in a file in `tasks/`. The decorator gives it a title,
a level and starter code, the docstring is the description students read, and the
body is the tests.

```python
section("2. Variables")

RECTANGLE = """
length = 8
width = 5

area = length * width
print("Area:", area)
"""


@task("Rectangle", level="mild", starter=RECTANGLE)
def rectangle(t):
    """
    Add to the program, so that it also works out the perimeter, stores it in
    a variable called `perimeter`, and prints it:

    ```output
    Area: 40
    Perimeter: 26
    ```
    """
    r = t.run()
    t.test("prints the area and the perimeter", r.check_output(["Area: 40", "Perimeter: 26"]))
    t.test("has a variable called perimeter", r.check_var("perimeter", 26))
    r = t.run(length=10, width=2.5)
    t.test("works for other rectangles", r.check_output(["Area: 25", "Perimeter: 25"]),
           hint="Work the perimeter out from length and width, so that it changes when they change.")
```

To add a file of tasks: put it in `tasks/`, add its name to `tasks/manifest.json`,
and put a model solution for each task in `teacher/solutions/` (see Checking).

- `section("...")` names the section for the tasks below it. Without it, the
  section is named after the file (`03_input.py` becomes "Input").
- `level=` is `"learn"` (a lesson step, done in order), or `"mild"`, `"medium"`,
  `"hot"` or `"spicy"` (practice, matching levels 1-2, 3, 4, and beyond). It shows
  as a coloured label beside the task.
- The function's name identifies the task: in links, in the solutions folder, and
  for students' saved code and ticks. Renaming it starts those afresh. The title
  can change freely.
- In a description, leave a blank line between paragraphs, start list lines with
  `- `, and use `` `code` `` and `**bold**`. Fence Python with ```` ```python ````
  (shown in colour) and what a program prints with ```` ```output ```` (shown like
  the dark box under Run).

### Predict tasks

A Predict task shows programs instead of an editor. Students type what each one
prints, and the answers are checked by running the programs, so the test function
needs nothing but the description.

```python
@task("Predict: If and Else", level="medium", predict=[
    question("print(2 + 3 * 4)"),
    question(AGE_PROGRAM, 16, 15),                  # run twice: typing 16, then typing 15
    question(COMPARE_PROGRAM, [3, 8], [7, 7]),      # two answers typed on each run
    question("print(10 / 4)", hint="Dividing gives an answer with a decimal point."),
])
def predict_if_else(t):
    """Read each program and work out what it prints."""
```

Each run gets its own answer box. A wrong answer is told which line is wrong (and
the `hint`), but not the right answer. Answers are compared the way output is (see
below), so `2.5` matches `2.50`. After a student has checked once, a **Run it**
button under each program shows what it really prints.

### Alter, Fix and Order tasks

These start from code that's already written. A Fix task needs nothing special:
the starter code is broken, and the tests check the output. For the others:

| Call | Passes when |
| --- | --- |
| `t.check_changed(1)` | At most 1 line differs from the starter code (and at least one does). |
| `t.check_only_added("()")` | The code is the starter code with only brackets added. |
| `t.check_same_lines()` | The code uses exactly the starter's lines, in any order and indentation (for putting scrambled lines in order). |

### What `t` can do

| Call | What it does |
| --- | --- |
| `t.run()` | Runs the student's program from the top and returns the run, `r`. |
| `t.run(inputs=[6, 4])` | The same, typing these answers for each `input()`, in order. |
| `t.run(length=10)` | Runs it as if the line `length = ...` said `length = 10`. This is how to check that a program uses its variables instead of typed-in answers. |
| `t.run(seed=1)` | Makes `random` give the same values every time. |
| `t.test(name, result)` | Records one test. `result` is `True`/`False`, or what a check below returns. |
| `t.test(name, passed, message)` | The same, with your own message for the student. |
| `t.test(name, result, hint="...")` | Adds a hint to the message if the test fails because the answer is wrong. |
| `t.test(name, result, error_hint="...")` | Adds a hint if it fails because the program stopped early (an error, the time limit, or asking for the wrong number of inputs). |
| `t.uses("for", "**")` | Is every one of these words or symbols in the code? Comments and text in quotes don't count. |
| `t.count("print")` | How many times a word or symbol is in the code. |
| `t.code`, `t.starter` | The student's code, and the task's starter code, as text. |

### What `r` (a run) can do

Each check returns a pass/fail and a message written for the student, ready to
hand to `t.test`. If the program stopped with an error, every check fails and its
message is the error, with the line number and a hint.

| Call | Passes when |
| --- | --- |
| `r.check_output(["Area: 40", "Perimeter: 26"])` | The program printed these lines, and nothing else. |
| `r.check_prints(26, "perimeter")` | Each value was printed somewhere. Other printing is allowed. |
| `r.check_var("perimeter", 26)` | The program has that variable, with that value. Leave the value out to check only that it exists. |
| `r.check_returns("area", (8, 5), 40)` | The student's function `area(8, 5)` gives back 40. |
| `r.ok` | The program ran to the end without an error. |

Output is compared leniently: capitals and spaces don't matter, and numbers are
compared by value, so `20` matches `20.0` and `0.30000000000000004` matches `0.3`.
This suits a math class: `float(input())` answers print with a decimal point, and
`print("Hello,", name, "!")` prints `Hello, Sam !`. Add `exact=True` to
`check_output` when the exact form matters. Rounding does matter: an expected
`3.61` is not matched by `3.605551275463989`. To accept an unrounded answer, add
`tol=0.01` (to `check_output`, `check_prints`, `check_var` or `check_returns`) and
numbers within 0.01 match.

For anything else, a run has `r.output` (the printed lines), `r.text` (the same as
one string), `r.prompts` (the questions `input()` asked), `r.vars` (the variables
afterwards), `r.error` (why it stopped, or `None`) and `r.call("name", args...)`,
which calls one of the student's functions and returns a run with `.value`.

### Hints students get without asking

The error messages explain the common slips from the outline: `^` used for a
power (noted whenever `^` appears, even though it runs), `2x` with no `*`, `x` or
`×` for multiplying, curly quotation marks pasted from a document, `=` in an `if`,
a missing colon, a variable used before the line that sets it (naming both lines),
`Area` where `area` was meant, `sqrt` or `pi` without `math.`, forgetting `float()`
around `input()`, `print` instead of `return`, a loop that never stops, and
`print( )` left outside a loop.

### Limits on a student's program

- Run stops a program after 5 seconds, and a test's run after 2 seconds, with a
  message that names the line it was on. Printing more than 1000 lines also stops it.
  Both usually mean a loop that never ends.
- `input()` works by running the program again from the top with the answers typed
  so far. Students won't notice, but a program that takes seconds to reach its
  second question takes that long again.
- `time.sleep()` doesn't wait.
- There are no files, and no `turtle`, `tkinter` or `pygame`: text programs only.

## Checking and previewing (on your computer)

- **`teacher/Check Tasks.cmd`** runs every task's tests on its model solution,
  which must pass, and on its starter code, which must not. A model solution is the
  file `teacher/solutions/<task file name>/<function name>.py`, for example
  `teacher/solutions/02_variables/rectangle.py`. To try some other code against a task:
  `python teacher/check_tasks.py rectangle path/to/code.py`. A Predict task needs no
  solution: its programs just have to run. `python teacher/check_tasks.py --answers`
  prints the answers to every Predict task.
- **`teacher/Preview Site.cmd`** opens the site from this folder, so you can try a
  task as a student before publishing. (Opening `index.html` by double-clicking
  doesn't work: a browser won't start Python from a file.)

The checker uses the Python on this computer, and the site uses the Python in the
browser. They run the same `harness.py`, so tests behave the same; the wording of
Python's own error messages can differ slightly between versions.

## Publishing

This folder is the website. As with the JavaScript tester: make it a git
repository, push it to a GitHub repository of its own, and turn on GitHub Pages for
the main branch (Settings, Pages, "Deploy from a branch"). `.gitignore` keeps
`teacher/` out, so the model solutions are never published. The tests in `tasks/`
are public, as they are for the JavaScript tester.

After that, publishing a change is a commit and a push.

### Links for D2L

- `.../index.html?section=Variables` lists only the sections whose names match.
  Several can be given, separated by commas.
- `.../index.html?task=rectangle` opens on that task. Use the function's name or
  the title. Choosing a task puts this in the address bar, ready to copy.

## Hosting the libraries yourself

The page needs two libraries, named at the top of `index.html`:

- **Pyodide**, which is Python built to run inside a browser (about 13 MB, fetched
  once and then kept by the browser).
- **CodeMirror**, the code editor (well under 1 MB).

They are loaded from `cdn.jsdelivr.net`. If the school's filter blocks that
address, Python won't start, and the page says so. (If only the editor can't load,
the page falls back to a plain text box with no colours.) The fix is to put both
libraries in this folder, so that everything comes from the same address as the page:

1. Pyodide: from the `pyodide` package on npm, at the version in `PYODIDE_URL`, copy
   `pyodide.mjs`, `pyodide.asm.mjs`, `pyodide.asm.wasm`, `python_stdlib.zip` and
   `pyodide-lock.json` into `vendor/pyodide/`.
2. CodeMirror: from the `codemirror` package, version 5, copy `lib/codemirror.js`,
   `lib/codemirror.css`, `mode/python/python.js`, `addon/edit/matchbrackets.js`,
   `addon/selection/active-line.js` and `addon/runmode/runmode.js` into
   `vendor/codemirror/`, keeping those folders.
3. In `index.html`, set `PYODIDE_URL = "vendor/pyodide/"` and
   `CODEMIRROR_URL = "vendor/codemirror/"`.
