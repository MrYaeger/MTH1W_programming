section("5. Repeating")


@task("Count to Ten", starter="""
for number in range(1, 4):
    print(number)
""")
def count_to_ten(t):
    """
    A `for` loop repeats the indented lines under it. `range(1, 4)` starts at 1
    and stops **before** 4, so this loop prints 1, 2 and 3.

    Change the program so that it prints the numbers from 1 to 10, one on each line.
    """
    r = t.run()
    t.test("prints 1 to 10", r.check_output(list(range(1, 11))))
    t.test("uses a loop", (t.uses("for") or t.uses("while")) and t.count("print") <= 2,
           "Let a loop do the counting, instead of writing a print for every number.")


TABLE = """
m = 2
b = 3

for x in range(0, 6):
    print(x)
"""


@task("Table of Values", starter=TABLE)
def table_of_values(t):
    """
    The line y = 2x + 3 has a slope of `m = 2` and a y-intercept of `b = 3`.

    This program prints x for x = 0 to 5. Change it so that each line shows x
    and then y, to make a table of values:

        0 3
        1 5
        2 7
        3 9
        4 11
        5 13

    Use `m` and `b` in your calculation, so that the table works for any line.
    `print(x, y)` prints two values with a space between them.
    """
    def table(m, b):
        return ["%s %s" % (x, m * x + b) for x in range(0, 6)]

    r = t.run()
    t.test("table for y = 2x + 3", r.check_output(table(2, 3)))
    r = t.run(m=-1, b=10)
    t.test("table for y = -x + 10", r.check_output(table(-1, 10)))
    r = t.run(m=0.5, b=0)
    t.test("table for y = 0.5x", r.check_output(table(0.5, 0)))


@task("Add Them Up", starter="""
n = int(input("Add up to which number? "))
total = 0
""")
def add_them_up(t):
    """
    Ask for a whole number `n`, then print the sum of all the whole numbers
    from 1 to n. If the answer is 10, that's 1 + 2 + 3 + ... + 10:

        Sum: 55

    Useful: inside a loop, `total = total + number` adds `number` to a running total.
    """
    for n, total in [(10, 55), (100, 5050), (1, 1), (4, 10)]:
        r = t.run(inputs=[n])
        t.test("adding up to %d gives %d" % (n, total), r.check_output(["Sum: %d" % total]))
