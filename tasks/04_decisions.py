section("4. Making Decisions")


@task("Positive, Negative or Zero", starter="""
number = float(input("Number? "))

if number > 0:
    print("Positive")
""")
def positive_negative_zero(t):
    """
    An `if` runs the indented lines under it only when its condition is true.

    This program says `Positive` for numbers above zero. Finish it, so that it
    prints exactly one of these for any number:

        Positive
        Negative
        Zero

    Useful: `elif` (else if) and `else`.
    """
    for number, word in [(5, "Positive"), (-3, "Negative"), (0, "Zero"), (0.5, "Positive"), (-0.1, "Negative")]:
        r = t.run(inputs=[number])
        t.test("%s is %s" % (number, word), r.check_output([word]))


@task("Is It a Right Triangle?", starter="""
a = float(input("Shortest side? "))
b = float(input("Middle side? "))
c = float(input("Longest side? "))
""")
def right_triangle(t):
    """
    A triangle is a right triangle when a² + b² = c², where c is its longest side.

    The program asks for the three sides, from shortest to longest. Print one
    of these:

        Right triangle
        Not a right triangle

    Useful: `==` checks whether two values are equal.
    """
    for sides, right in [((3, 4, 5), True), ((2, 3, 4), False), ((5, 12, 13), True),
                         ((6, 8, 10), True), ((1, 1, 1), False)]:
        r = t.run(inputs=sides)
        want = "Right triangle" if right else "Not a right triangle"
        t.test("sides %s, %s and %s: %s" % (sides + (want,)), r.check_output([want]))
