section("5. Decisions")


@task("If and Else", level="learn", starter="""
height = float(input("Height in cm? "))

if height >= 120:
    print("You can ride")
""")
def if_else(t):
    """
    An `if` runs the lines indented under it **only when its condition is true**.
    An `else` runs its lines when the condition is false:

    ```python
    if mark >= 50:
        print("Pass")
    else:
        print("Not yet")
    ```

    - The `if` line and the `else` line end with a colon `:`.
    - The lines under them are indented 4 spaces (press Tab).
    - `>=` means "greater than or equal to".

    A ride needs riders to be at least 120 cm tall. Add an `else`, so that anyone
    shorter sees `Too short`.
    """
    for height, want in [(150, "You can ride"), (121, "You can ride"), (120, "You can ride"),
                         (119, "Too short"), (100.5, "Too short")]:
        r = t.run(inputs=[height])
        t.test("%s cm: %s" % (height, want), r.check_output([want]),
               hint="At exactly 120 cm you can ride: use >= (at least)." if height == 120 else "")


@task("Comparisons", level="learn", starter="""
mark = float(input("Mark? "))

if mark = 50
print("Pass")
else:
    print("Not yet")
""")
def comparisons(t):
    """
    Python has six ways to compare two values:

    - `==` equal to (two equals signs: one `=` stores a value)
    - `!=` not equal to
    - `<` less than, and `<=` less than or equal to
    - `>` greater than, and `>=` greater than or equal to

    This program should print `Pass` for a mark of 50 or more, and `Not yet` for
    anything less. It has **three** mistakes. Press **Run**, read the error message,
    and fix them one at a time.
    """
    for mark, want in [(50, "Pass"), (51, "Pass"), (80, "Pass"), (49, "Not yet"), (49.5, "Not yet")]:
        r = t.run(inputs=[mark])
        t.test("a mark of %s: %s" % (mark, want), r.check_output([want]),
               hint="A mark of 50 or more passes: which comparison means \"50 or more\"?" if not r.error else "")


@task("Decisions in a Function", level="learn", starter="""
def absolute_value(x):
    if x < 0:
        return -x


print(absolute_value(-5))
print(absolute_value(3))
""")
def absolute_value(t):
    """
    `return` can go inside an `if`. The function stops as soon as it reaches a
    `return`, and gives back that value.

    The absolute value of a number is its distance from 0: |-5| is 5, and |3| is 3.
    This function gets negative numbers right, but for 3 it gives back `None`
    (nothing), because no `return` runs.

    Add an `else`, so that the function gives back the right answer for every number.
    """
    r = t.run()
    for x, want in [(-5, 5), (3, 3), (0, 0), (-2.5, 2.5), (7.25, 7.25)]:
        t.test("absolute_value(%s) gives back %s" % (x, want), r.check_returns("absolute_value", x, want))


@task("Elif", level="learn", starter="""
def sign(number):
    if number > 0:
        return "positive"


print(sign(7))
print(sign(-4))
print(sign(0))
""")
def sign(t):
    """
    `elif` (short for "else if") adds another condition. Python checks the
    conditions from the top, and uses only the **first** one that's true:

    ```python
    if temperature > 25:
        return "hot"
    elif temperature > 10:
        return "warm"
    else:
        return "cold"
    ```

    Finish `sign(number)` so that it gives back `"positive"`, `"negative"` or
    `"zero"`.
    """
    r = t.run()
    for n, want in [(7, "positive"), (-4, "negative"), (0, "zero"), (0.5, "positive"), (-0.1, "negative")]:
        t.test("sign(%s) gives back %r" % (n, want), r.check_returns("sign", n, want))


@task("Speed Check", level="mild", starter="""
def speed_check(speed, limit):
    return ""


print(speed_check(110, 100))
""")
def speed_check(t):
    """
    Make `speed_check(speed, limit)` give back `"Too fast"` if `speed` is over the
    speed limit, and `"OK"` if it isn't. Driving exactly at the limit is OK.
    """
    r = t.run()
    for args, want in [((110, 100), "Too fast"), ((60, 80), "OK"), ((100, 100), "OK"), ((101, 100), "Too fast"),
                       ((50, 50.5), "OK")]:
        t.test("speed_check(%s, %s) gives back %r" % (args + (want,)), r.check_returns("speed_check", args, want),
               hint="Exactly at the limit is OK: use > (over), not >=." if args == (100, 100) else "")


AGE = """
age = int(input("Age? "))
if age >= 16:
    print("You can drive")
else:
    print("Not yet")
"""

SIZES = """
x = int(input("x? "))
if x > 10:
    print("big")
elif x > 5:
    print("medium")
else:
    print("small")
print("done")
"""

WATER = """
t = float(input("Temperature? "))
if t < 0:
    print("Ice")
if t <= 100:
    print("Water")
"""

COMPARE = """
a = int(input("a? "))
b = int(input("b? "))
if a == b:
    print("same")
elif a > b:
    print(a - b)
else:
    print(b - a)
"""


@task("Predict: If and Else", level="medium", predict=[
    question(AGE, 16, 15),
    question(SIZES, 10, 11, hint="Only the first true condition's lines run. Is 10 > 10?"),
    question(WATER, 0, -5, hint="These are two separate ifs, not if and elif: both can run."),
    question(COMPARE, [3, 8], [7, 7]),
])
def predict_if_else(t):
    """
    **Don't run anything.** For each program, work out what it prints when the
    user types the answers shown. Watch the values that land exactly on a
    condition's boundary.
    """


@task("Budget", level="medium", starter="""
income = float(input("Monthly income? "))
expenses = float(input("Monthly expenses? "))
""")
def budget(t):
    """
    If income is more than expenses, there's a surplus; if it's less, there's a
    shortage. Print one of these:

    ```output
    Surplus of $ 180.0
    Shortage of $ 150.0
    Balanced
    ```

    The amount is always positive: the difference between income and expenses.
    For example, income $1500 and expenses $1320 give `Surplus of $ 180.0`.
    """
    for income, expenses, want in [(1500, 1320, "Surplus of $ 180"), (1200, 1350, "Shortage of $ 150"),
                                   (1000, 1000, "Balanced"), (900.5, 900, "Surplus of $ 0.5"),
                                   (0, 45, "Shortage of $ 45")]:
        r = t.run(inputs=[income, expenses])
        t.test("income %s and expenses %s: %s" % (income, expenses, want), r.check_output([want]),
               hint="A shortage is printed as a positive amount: expenses - income." if want.startswith("Short") else "")


@task("Right Triangle?", level="medium", starter="""
a = float(input("Shortest side? "))
b = float(input("Middle side? "))
c = float(input("Longest side? "))
""")
def right_triangle(t):
    """
    A triangle is a right triangle when a² + b² = c², where c is its longest side.

    The program asks for the three sides, from shortest to longest. Print one of these:

    ```output
    Right triangle
    Not a right triangle
    ```
    """
    for sides, right in [((3, 4, 5), True), ((4, 5, 6), False), ((5, 12, 13), True),
                         ((6, 8, 10), True), ((2, 3, 4), False), ((1.5, 2, 2.5), True)]:
        r = t.run(inputs=sides)
        want = "Right triangle" if right else "Not a right triangle"
        t.test("sides %s, %s and %s: %s" % (sides + (want,)), r.check_output([want]))


@task("Fix the Levels", level="medium", starter="""
def level(mark):
    if mark >= 50:
        return "Level 1"
    elif mark >= 60:
        return "Level 2"
    elif mark >= 70:
        return "Level 3"
    elif mark >= 80:
        return "Level 4"
    else:
        return "Not yet"


print(level(85))
""")
def fix_the_levels(t):
    """
    `level(mark)` should give back:

    - `"Level 4"` for 80 and up
    - `"Level 3"` for 70 to 79
    - `"Level 2"` for 60 to 69
    - `"Level 1"` for 50 to 59
    - `"Not yet"` below 50

    But it says a mark of 85 is Level 1! Every condition is right on its own: the
    problem is their **order**. Fix it.
    """
    r = t.run()
    for mark, want in [(85, "Level 4"), (80, "Level 4"), (79, "Level 3"), (70, "Level 3"), (65, "Level 2"),
                       (60, "Level 2"), (59, "Level 1"), (50, "Level 1"), (49, "Not yet"), (0, "Not yet")]:
        t.test("level(%s) gives back %r" % (mark, want), r.check_returns("level", mark, want))


@task("Direct or Partial?", level="hot", starter="""
def variation(m, b):
    return ""


print(variation(3, 0))
""")
def variation(t):
    """
    A line y = mx + b is a **direct variation** if it goes through the origin, and a
    **partial variation** if it doesn't.

    Make `variation(m, b)` give back `"direct"` or `"partial"` for the line
    y = mx + b.
    """
    r = t.run()
    for args, want in [((3, 0), "direct"), ((2, 3), "partial"), ((-1, -2), "partial"), ((0.5, 0), "direct"),
                       ((-4, 0.1), "partial")]:
        t.test("variation(%s, %s) gives back %r" % (args + (want,)), r.check_returns("variation", args, want))


@task("Better Buy", level="hot", starter="""
def better_buy(price_a, size_a, price_b, size_b):
    return ""


print(better_buy(3.99, 500, 6.49, 1000))
""")
def better_buy(t):
    """
    Two sizes of the same cereal: box A costs `price_a` for `size_a` grams, and
    box B costs `price_b` for `size_b` grams.

    Make `better_buy` give back `"A"` or `"B"`, whichever costs less per gram, or
    `"Same"` if they cost the same per gram.
    """
    r = t.run()
    for args, want in [((3.99, 500, 6.49, 1000), "B"), ((2, 1, 5, 2), "A"), ((2, 1, 4, 2), "Same"),
                       ((4.5, 3, 3, 2), "Same"), ((10, 250, 30, 700), "A")]:
        t.test("better_buy%s gives back %r" % (args, want), r.check_returns("better_buy", args, want))


@task("Number Sets", level="hot", starter="""
def smallest_set(number):
    return ""


print(smallest_set(5))
""")
def smallest_set(t):
    """
    Make `smallest_set(number)` give back the **smallest** set the number belongs to:

    - `"natural"`: 1, 2, 3, ...
    - `"whole"`: the natural numbers and 0
    - `"integer"`: the whole numbers and their negatives
    - `"rational"`: any number that can be written as a fraction

    So `smallest_set(5)` is `"natural"`, and `smallest_set(-3)` is `"integer"`.
    (Irrational numbers like π can't be typed in exactly, so the function never
    gets one.)

    Hint: `round(number) == number` is true when `number` has no decimal part.
    """
    r = t.run()
    for n, want in [(5, "natural"), (0, "whole"), (-3, "integer"), (2.5, "rational"), (1, "natural"),
                    (-0.75, "rational"), (7.0, "natural"), (-100, "integer")]:
        t.test("smallest_set(%s) gives back %r" % (n, want), r.check_returns("smallest_set", n, want))


@task("Slope", level="hot", starter="""
def slope(x1, y1, x2, y2):
    return 0


print(slope(1, 5, 3, 9))
""")
def slope(t):
    """
    Make `slope(x1, y1, x2, y2)` give back the slope of the line through the points
    (x1, y1) and (x2, y2): m = (y2 - y1) ÷ (x2 - x1).

    A vertical line has no slope, and the formula would divide by zero. For a
    vertical line, give back `"undefined"` instead.
    """
    r = t.run()
    for args, want in [((1, 5, 3, 9), 2), ((0, 4, 2, 0), -2), ((1, 3, 5, 3), 0), ((0, 0, 4, 1), 0.25),
                       ((2, 1, 2, 7), "undefined"), ((-3, -3, -3, 5), "undefined")]:
        t.test("slope%s gives back %r" % (args, want), r.check_returns("slope", args, want),
               error_hint="For a vertical line, x1 and x2 are the same. Check for that with an if, before dividing."
               if want == "undefined" else "")


@task("Third Angle", level="spicy", starter="""
def third_angle(a, b):
    return 0


print(third_angle(50, 60))
""")
def third_angle(t):
    """
    The angles in a triangle add up to 180°. Make `third_angle(a, b)` give back
    the third angle of a triangle with angles `a` and `b`.

    If there can't be a triangle with those two angles, give back `None` (with no
    quotation marks: it means "nothing").
    """
    r = t.run()
    for args, want in [((50, 60), 70), ((90, 45), 45), ((30.5, 60), 89.5), ((100, 80), None), ((120, 70), None),
                       ((1, 1), 178)]:
        t.test("third_angle(%s, %s) gives back %r" % (args + (want,)), r.check_returns("third_angle", args, want))


@task("Triangle Angles", level="spicy", starter="""
a = float(input("First angle? "))
b = float(input("Second angle? "))
""")
def triangle_angles(t):
    """
    The program asks for two angles of a triangle. Print the third angle, then
    whether the triangle is `acute` (every angle is under 90°), `right` (one is
    90°) or `obtuse` (one is over 90°). For 50 and 60:

    ```output
    Third angle: 70.0
    acute
    ```

    If there can't be a triangle with those two angles, print only
    `Not a triangle`.
    """
    for a, b, lines in [(50, 60, ["Third angle: 70", "acute"]), (30, 60, ["Third angle: 90", "right"]),
                        (20, 30, ["Third angle: 130", "obtuse"]), (100, 50, ["Third angle: 30", "obtuse"]),
                        (90, 45, ["Third angle: 45", "right"]), (100, 90, ["Not a triangle"]),
                        (90, 90, ["Not a triangle"])]:
        r = t.run(inputs=[a, b])
        t.test("%s° and %s°: %s" % (a, b, " / ".join(lines)), r.check_output(lines),
               hint="Check all three angles: any one of them can be the biggest." if a >= 90 or b >= 90 else "")
