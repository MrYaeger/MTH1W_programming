section("2. Variables")


@task("Variables", level="learn", starter="""
length = 8
width = 3
area = length * width
print("area")
""")
def variables(t):
    """
    A **variable** is a name for a value. `=` stores the value on its right in the
    name on its left. After that, the name can be used in place of the value:

    ```python
    side = 5
    perimeter = 4 * side
    print(perimeter)
    ```

    ```output
    20
    ```

    To print what a variable holds, write its name **without** quotation marks.
    `print("perimeter")` would print the word perimeter.

    This program should print the rectangle's area, but it prints the word **area**.
    Fix it.
    """
    r = t.run()
    t.test("prints the area, 24", r.check_output([24]),
           hint="Text in quotation marks is printed exactly as typed. Take the quotation marks away to print "
                "what the variable holds." if r.output == ["area"] else "")
    r = t.run(length=10, width=4.5)
    t.test("prints 45 when length is 10 and width is 4.5", r.check_output([45]),
           hint="Print the variable area, so that the answer changes when length and width change.")


@task("Changing a Variable", level="learn", starter="""
savings = 50
savings = savings + 15
print(savings)
""")
def changing_a_variable(t):
    """
    A variable holds one value at a time, and it can be changed. The right side of
    `=` is worked out first, using the old value:

    ```python
    savings = savings + 15
    ```

    means "work out savings + 15, then store that in savings". So this program
    prints 65.

    You save $15 every week. Add lines so that `savings` goes up by 15 **two more
    times**, and is printed after each time:

    ```output
    65
    80
    95
    ```
    """
    r = t.run()
    t.test("prints 65, 80 and 95", r.check_output([65, 80, 95]))
    r = t.run(savings=100)
    t.test("starting with 100, prints 115, 130 and 145", r.check_output([115, 130, 145]),
           hint="Each time, add 15 to savings (savings = savings + 15) and print savings. Don't type the totals.")


@task("Top to Bottom", level="learn", starter="""
area = side ** 2
side = 6
print("Area:", area)
""")
def top_to_bottom(t):
    """
    Python runs a program one line at a time, from the top down. A variable has to
    be given a value **before** a line can use it.

    This program should print the area of a square with sides of 6, but it stops
    with an error. Press **Run** and read the error message, then fix the program
    so it prints:

    ```output
    Area: 36
    ```
    """
    r = t.run()
    t.test("prints Area: 36", r.check_output(["Area: 36"]))
    r = t.run(side=2.5)
    t.test("prints Area: 6.25 when side is 2.5", r.check_output(["Area: 6.25"]),
           hint="Work the area out from side (side ** 2), so that it changes when side changes.")


@task("Using math", level="learn", starter="""
import math

radius = 5
""")
def circle(t):
    """
    `import math` (at the top of a program) gives you more maths:

    - `math.pi` is π (3.14159...)
    - `math.sqrt(x)` is the square root of x

    The circumference of a circle is C = 2πr. Write `2πr` in Python as
    `2 * math.pi * radius`: Python needs the `*` signs.

    Print the circumference of a circle with this radius. For a radius of 5, it's
    about 31.42.
    """
    r = t.run()
    t.test("prints about 31.42 for a radius of 5", r.check_prints(2 * 3.141592653589793 * 5, tol=0.01),
           hint="Use math.pi for π: it's more accurate than 3.14." if not t.uses("pi") else "")
    r = t.run(radius=2.5)
    t.test("prints about 15.71 for a radius of 2.5", r.check_prints(2 * 3.141592653589793 * 2.5, tol=0.01),
           hint="Use the variable radius in your formula, so that the answer changes when radius changes.")


RECTANGLE = """
length = 8
width = 5

area = length * width
print("Area:", area)
"""


@task("Rectangle", level="mild", starter=RECTANGLE)
def rectangle(t):
    """
    This program stores a rectangle's length and width, then works out its area.

    Add to it, so that it also works out the perimeter, stores it in a variable
    called `perimeter`, and prints it. For a length of 8 and a width of 5:

    ```output
    Area: 40
    Perimeter: 26
    ```

    Then try other numbers for `length` and `width`. Both answers should change.
    """
    r = t.run()
    t.test("prints the area and the perimeter", r.check_output(["Area: 40", "Perimeter: 26"]))
    t.test("has a variable called perimeter", r.check_var("perimeter", 26))
    r = t.run(length=10, width=2.5)
    t.test("works for other rectangles (length 10, width 2.5)", r.check_output(["Area: 25", "Perimeter: 25"]),
           hint="Work the perimeter out from length and width, so that it changes when they change.")


@task("Predict: Variables", level="mild", predict=[
    question("""
    x = 3
    y = 6 * x + 5
    print(y)
    """),
    question("""
    a = 10
    b = a / 4
    print(a, b)
    """, hint="print( ) puts a space between the values it's given, and / always gives a decimal."),
    question("""
    x = 5
    x = x + 2
    print(x * 2)
    """, hint="A variable holds one value at a time. x = x + 2 replaces x's value with a new one."),
    question("""
    p = 4
    q = p ** 2 - 1
    p = 1
    print(p, q)
    """, hint="q was worked out when its line ran. Changing p afterwards doesn't change q."),
])
def predict_variables(t):
    """
    **Don't run anything.** Read each program and work out what it prints, keeping
    track of each variable's value as you go, line by line. Type your answers, then
    press **Check my answers**.
    """


AVERAGE = """
a = 70
b = 80
c = 90

average = a + b + c / 3
print("Average:", average)
"""


@task("Fix the Average", level="mild", starter=AVERAGE)
def fix_the_average(t):
    """
    Three test marks are 70, 80 and 90, so their average is 80.
    This program says the average is 180.0!

    Find the mistake and fix it, so that it prints:

    ```output
    Average: 80.0
    ```

    Hint: BEDMAS. Which operation happens first?
    """
    r = t.run()
    t.test("the average of 70, 80 and 90 is 80", r.check_output(["Average: 80"]))
    r = t.run(a=50, b=60, c=100)
    t.test("the average of 50, 60 and 100 is 70", r.check_output(["Average: 70"]),
           hint="Work the average out from a, b and c, so that it changes when they change.")


@task("Order the Lines", level="medium", starter="""
print("Area:", area)
a = 6
area = (a + b) / 2 * h
h = 4
b = 10
""")
def order_the_lines(t):
    """
    A trapezoid has parallel sides `a` and `b` and height `h`. Its area is

    ```output
    area = (a + b) ÷ 2 × h
    ```

    These lines work out the area of a trapezoid, but they're in the wrong order.
    Put them in an order that works, so that the program prints:

    ```output
    Area: 32.0
    ```

    Move lines with cut and paste (Ctrl+X, then Ctrl+V). Don't change, add or
    remove any lines.
    """
    r = t.run()
    t.test("prints Area: 32.0", r.check_output(["Area: 32"]))
    t.test("uses only the given lines", t.check_same_lines())


@task("Ball Height", level="medium", starter="""
h = -4.9t^2 + 20t + 2
t = 3
print(round(h, 1))
""")
def ball_height(t):
    """
    A ball is thrown upward. Its height in metres, `t` seconds later, is

    ```output
    h = -4.9t² + 20t + 2
    ```

    This program should print the height after 3 seconds, rounded to 1 decimal
    place, but it has **three** mistakes. Fix them, so that it prints `17.9`.

    Press **Run** after each fix, and read the error message.
    """
    r = t.run()
    t.test("prints 17.9 when t is 3", r.check_output([17.9]))
    r = t.run(t=1)
    t.test("prints 17.1 when t is 1", r.check_output([17.1]),
           hint="Work h out from t, so that it changes when t changes.")
    r = t.run(t=0)
    t.test("prints 2 when t is 0", r.check_output([2]))


@task("Race Times", level="medium", starter="""
t1 = 14.2
t2 = 13.87
t3 = 14.05
t4 = 13.9
t5 = 14.31
""")
def race_times(t):
    """
    These are a runner's times, in seconds, for five 100 m races.

    Print the mean (average) time, **rounded to 1 decimal place**:

    ```output
    Mean: 14.1
    ```

    Use the variables in your calculation, so that it still works if a time changes.
    """
    r = t.run()
    too_big = any(word.replace(".", "", 1).isdigit() and float(word) > 20 for word in r.text.split())
    t.test("prints Mean: 14.1", r.check_output(["Mean: 14.1"]),
           hint="Add all five times first: the adding needs brackets around it, like (t1 + t2 + t3 + t4 + t5) / 5."
           if too_big else "")
    r = t.run(t1=10, t2=11, t3=12, t4=13, t5=15.5)
    t.test("works for other times (mean 12.3)", r.check_output(["Mean: 12.3"]),
           hint="Use t1, t2, t3, t4 and t5 in the calculation, instead of typing the times.")
    r = t.run(t1=10, t2=10, t3=10, t4=10, t5=10.26)
    t.test("rounds to 1 decimal place (mean 10.052 prints as 10.1)", r.check_output(["Mean: 10.1"]))


@task("Celsius to Fahrenheit", level="medium", starter="""
celsius = 25

# Work out the temperature in °F, then print it.
""")
def celsius_to_fahrenheit(t):
    """
    To change a temperature from °C to °F, multiply by 9, divide by 5, then add 32:

    ```output
    F = C × 9 ÷ 5 + 32
    ```

    Print the temperature in °F. For 25 °C, the program should print `77.0`.
    """
    for c, f in [(25, 77), (100, 212), (0, 32), (-40, -40), (37, 98.6)]:
        r = t.run(celsius=c)
        t.test("%s °C is %s °F" % (c, f), r.check_output([f]),
               hint="Use the variable celsius in your formula, so that the answer changes when it changes.")


@task("Fahrenheit to Celsius", level="hot", starter="""
temperature = 25
answer = temperature * 9 / 5 + 32
print(answer)
""")
def fahrenheit_to_celsius(t):
    """
    This program changes a temperature from °C into °F.

    **Change one line** (the one that works out `answer`) so that the program
    changes °F into °C instead: `temperature` is now in °F.

    You'll need to rearrange F = C × 9 ÷ 5 + 32 to find C. Check: 212 °F is 100 °C,
    and 32 °F is 0 °C.
    """
    for f, c in [(212, 100), (32, 0), (-40, -40), (98.6, 37), (50, 10)]:
        r = t.run(temperature=f)
        t.test("%s °F is %s °C" % (f, c), r.check_output([c]))
    t.test("changes just one line", t.check_changed(1))


@task("Hours, Minutes, Seconds", level="spicy", starter="""
total_seconds = 3725
""")
def hours_minutes_seconds(t):
    """
    Two more operations help here:

    - `//` divides and drops the remainder: `17 // 5` is `3`
    - `%` gives just the remainder: `17 % 5` is `2`

    Change `total_seconds` into hours, minutes and seconds, and print them like
    this. For 3725 seconds:

    ```output
    1 h 2 min 5 s
    ```
    """
    for total, (h, m, s) in [(3725, (1, 2, 5)), (3600, (1, 0, 0)), (59, (0, 0, 59)), (86399, (23, 59, 59)),
                             (7260, (2, 1, 0))]:
        r = t.run(total_seconds=total)
        t.test("%d seconds is %d h %d min %d s" % (total, h, m, s), r.check_output(["%d h %d min %d s" % (h, m, s)]))
