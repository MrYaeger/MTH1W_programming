section("1. Printing and Calculating")


@task("Hello World", starter="""
# Type your code under this line, then press Run.
""")
def hello_world(t):
    """
    Make Python print this line:

        Hello World

    `print("...")` prints whatever is between the quotation marks.
    """
    r = t.run()
    t.test("prints Hello World", r.check_output(["Hello World"]))


@task("Python as a Calculator", starter="""
print(15 + 27)
""")
def calculator(t):
    """
    Python can do arithmetic: `+` adds, `-` subtracts, `*` multiplies and `/` divides.

    The program already prints the answer to 15 + 27. Add two more lines, so that
    it prints the answers to all three of these, in this order:

    - 15 + 27
    - 12 × 8
    - 100 ÷ 4

    Dividing always gives a decimal, so the last answer prints as `25.0`.
    """
    r = t.run()
    t.test("prints the three answers", r.check_output([42, 96, 25]))
    t.test("Python does the calculating", t.uses("+", "*", "/"),
           "Let Python work the answers out: use + , * and / in your code instead of typing the answers.")


@task("Order of Operations", starter="""
print(2 + 3 * 4)
""")
def order_of_operations(t):
    """
    Python follows BEDMAS, so this program multiplies first and prints `14`.

    Add **one pair of brackets** so that it adds first and prints `20`.
    Don't change the numbers.
    """
    r = t.run()
    t.test("prints 20", r.check_output([20]))
    t.test("still calculates with 2, 3 and 4", t.uses("2", "3", "4", "+", "*"),
           "Keep  2 + 3 * 4  in the program, and add brackets to it.")
