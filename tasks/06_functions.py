section("6. Functions")

PERIMETER = """
def perimeter(length, width):
    return 0


print(perimeter(8, 5))
"""


@task("Perimeter Function", starter=PERIMETER)
def perimeter_function(t):
    """
    A function is a named set of steps. `return` is how it gives back its answer.

    `perimeter(length, width)` should give back the perimeter of a rectangle,
    but right now it always gives back 0. Fix it.

    The last line tries it out, and should print `26`.
    """
    r = t.run()
    for args, want in [((8, 5), 26), ((10, 2.5), 25), ((1, 1), 4)]:
        t.test("perimeter(%s, %s) gives back %s" % (args + (want,)), r.check_returns("perimeter", args, want))
