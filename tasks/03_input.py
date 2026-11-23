section("3. Asking Questions")


@task("Greeting", starter="""
name = input("What is your name? ")
""")
def greeting(t):
    """
    `input("...")` asks a question and waits for an answer. Here the answer is
    stored in the variable `name`.

    Add a line that says hello to that person. If the answer is Sam:

        Hello, Sam!

    Join pieces of text with `+`, like this: `"Hello, " + name`
    """
    for name in ["Sam", "Priya"]:
        r = t.run(inputs=[name])
        t.test("answering %s prints Hello, %s!" % (name, name), r.check_output(["Hello, %s!" % name]))
    t.test("asks one question", len(r.prompts) == 1,
           "Your program asked %d questions. Ask just one." % len(r.prompts))


@task("Area of a Triangle", starter="""
base = float(input("Base? "))
""")
def triangle_area(t):
    """
    `input()` always gives text. `float(...)` turns that text into a number, so
    you can calculate with it.

    Ask for the base of a triangle, then its height, and print its area.
    If the answers are 6 and 4:

        Area: 12.0
    """
    for base, height, area in [(6, 4, 12), (5, 3, 7.5), (2.5, 4, 5)]:
        r = t.run(inputs=[base, height])
        t.test("base %s and height %s give Area: %s" % (base, height, float(area)),
               r.check_output(["Area: %s" % area]))


@task("Pythagorean Theorem", starter="""
a = float(input("a? "))
b = float(input("b? "))
""")
def pythagorean(t):
    """
    The two shorter sides of a right triangle are `a` and `b`. Work out the
    longest side `c`, and print it **rounded to 2 decimal places**.

    If the answers are 3 and 4:

        c = 5.0

    If the answers are 2 and 3:

        c = 3.61

    Useful: `x ** 2` squares x, `x ** 0.5` is the square root of x, and
    `round(x, 2)` rounds x to 2 decimal places.
    """
    for a, b, c in [(3, 4, 5), (2, 3, 3.61), (5, 12, 13), (1, 1, 1.41)]:
        r = t.run(inputs=[a, b])
        t.test("a = %s and b = %s give c = %s" % (a, b, c), r.check_output(["c = %s" % c]))
