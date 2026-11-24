section("6. Loops")


def _loop_used(t):
    return t.uses("for") or t.uses("while")


@task("Count to Ten", level="learn", starter="""
for number in range(1, 4):
    print(number)
""")
def count_to_ten(t):
    """
    A `for` loop repeats the lines indented under it, once for each value:

    ```python
    for number in range(1, 4):
        print(number)
    ```

    ```output
    1
    2
    3
    ```

    `range(1, 4)` starts at 1 and stops **before** 4. Each time around the loop,
    `number` holds the next value. (`range(4)` on its own starts at 0: 0, 1, 2, 3.)

    Change the program so that it prints the numbers from 1 to 10, one on each line.
    """
    r = t.run()
    t.test("prints 1 to 10", r.check_output(list(range(1, 11))),
           hint="range(1, 10) stops before 10. To include 10, use range(1, 11)." if r.output == [str(i) for i in range(1, 10)] else "")
    t.test("uses a loop", _loop_used(t) and t.count("print") <= 2,
           "Let a loop do the counting, instead of writing a print for every number.")


@task("Inside and After the Loop", level="learn", starter="""
for x in range(1, 6):
    print(x)
""")
def countdown(t):
    """
    The lines **indented** under the `for` line are inside the loop, and repeat.
    The first line that isn't indented runs once, after the loop has finished.

    The loop variable can be used in a calculation: when `x` is 1, `6 - x` is 5.

    Change the program so that it counts down, then prints `Liftoff!` once:

    ```output
    5
    4
    3
    2
    1
    Liftoff!
    ```
    """
    r = t.run()
    lift = sum(1 for line in r.output if "liftoff" in line.lower())
    t.test("counts down from 5, then prints Liftoff!", r.check_output([5, 4, 3, 2, 1, "Liftoff!"]),
           hint="Liftoff! should print once, after the loop: don't indent its line." if lift > 1 else "")
    t.test("uses a loop", _loop_used(t) and t.count("print") <= 2,
           "Let the loop print the numbers, instead of writing a print for each one.")


@task("Running Total", level="learn", starter="""
n = 10

for x in range(1, n + 1):
    print(x ** 2)
""")
def add_them_up(t):
    """
    To add up values in a loop, keep a **running total**: start it at 0 **before**
    the loop, add to it **inside** the loop, and print it **after** the loop.

    ```python
    total = 0
    for x in range(1, 4):
        total = total + x * 10
    print(total)
    ```

    ```output
    60
    ```

    This program prints the squares 1, 4, 9, ... up to n². Change it so that it adds
    them up instead, and prints only the total. For n = 10:

    ```output
    Total: 385
    ```
    """
    def hint(run, last_square):
        if len(run.output) > 1:
            return "Print the total once, after the loop: its line shouldn't be indented."
        if run.output == ["Total: %d" % last_square]:
            return ("total = 0 is inside the loop, so the total starts again at 0 every time. "
                    "Move it above the for line.")
        return ""

    r = t.run()
    t.test("adds the squares up to 10² (385)", r.check_output(["Total: 385"]), hint=hint(r, 100))
    r = t.run(n=3)
    t.test("adds the squares up to 3² (14)", r.check_output(["Total: 14"]),
           hint=hint(r, 9) or "Use n in the range, so that the program works for any n.")
    r = t.run(n=1)
    t.test("adds the squares up to 1² (1)", r.check_output(["Total: 1"]))


@task("While Loops", level="learn", starter="""
savings = 50
goal = 200
weeks = 0

# Add a while loop here.

print("Weeks:", weeks)
""")
def while_loops(t):
    """
    A `while` loop repeats **as long as its condition is true**. Something inside
    the loop has to change, so that the condition becomes false and the loop stops:

    ```python
    n = 1
    while n < 100:
        n = n * 2
    print(n)
    ```

    ```output
    128
    ```

    You have $50 and save $15 every week. Add a `while` loop that adds 15 to
    `savings` and 1 to `weeks`, for as long as `savings` is less than `goal`. Then
    the program prints how many weeks it takes to save at least $200:

    ```output
    Weeks: 10
    ```
    """
    r = t.run()
    t.test("takes 10 weeks to save $200", r.check_output(["Weeks: 10"]))
    for goal, weeks in [(500, 30), (51, 1), (50, 0)]:
        r = t.run(goal=goal)
        t.test("takes %s to save $%d" % ("1 week" if weeks == 1 else "%d weeks" % weeks, goal),
               r.check_output(["Weeks: %d" % weeks]),
               hint="Use goal in the while condition, so that the loop works for any goal.")
    t.test("uses a while loop", t.uses("while"), "Use a while loop for this one.")


@task("Multiples of Seven", level="mild", starter="""
""")
def multiples_of_seven(t):
    """
    Use a `for` loop to print the multiples of 7 from 7 to 84, one on each line:

    ```output
    7
    14
    21
    ```

    ...and so on, up to 84.
    """
    r = t.run()
    want = [7 * x for x in range(1, 13)]
    t.test("prints 7, 14, ..., 84", r.check_output(want))
    t.test("uses a loop", _loop_used(t) and t.count("print") <= 2,
           "Let a loop do the work, instead of writing a print for every number.")


TABLE = """
m = 3
b = 2

for x in range(0, 11):
    print(x)
"""


@task("Table of Values", level="medium", starter=TABLE)
def table_of_values(t):
    """
    The line y = 3x + 2 has a slope of `m = 3` and a y-intercept of `b = 2`.

    This program prints x for x = 0 to 10. Change it so that each line shows x and
    then y, to make a table of values:

    ```output
    0 2
    1 5
    2 8
    ```

    ...and so on, up to `10 32`. Use `m` and `b` in your calculation, so that the
    table works for any line. `print(x, y)` prints two values with a space between them.
    """
    def table(m, b):
        return ["%s %s" % (x, m * x + b) for x in range(0, 11)]

    r = t.run()
    t.test("table for y = 3x + 2", r.check_output(table(3, 2)))
    r = t.run(m=-1, b=10)
    t.test("table for y = -x + 10", r.check_output(table(-1, 10)),
           hint="Work y out from m and b, so that the table changes when they change.")
    r = t.run(m=0.5, b=0)
    t.test("table for y = 0.5x", r.check_output(table(0.5, 0)))


@task("Predict: Loops", level="medium", predict=[
    question("""
    for x in range(4):
        print(x)
    """, hint="range(4) starts at 0, and stops before 4."),
    question("""
    for x in range(2, 5):
        print(x * x)
    print("end")
    """),
    question("""
    total = 100
    for x in range(3):
        total = total - 10
        print(total)
    """),
    question("""
    n = 3
    while n < 20:
        n = n * 2
    print(n)
    """, hint="Write down n each time around the loop, and check the condition each time."),
    question("""
    count = 0
    for x in range(1, 6):
        if x > 2:
            count = count + 1
    print(count)
    """),
])
def predict_loops(t):
    """
    **Don't run anything.** For each program, work out what it prints. It helps to
    write down each variable's value every time around the loop.
    """


@task("Mean of Five", level="medium", starter="""
total = 0
""")
def mean_of_five(t):
    """
    Write a program that asks for 5 numbers, then prints their mean. If the numbers
    are 70, 80, 90, 60 and 75:

    ```output
    Mean: 75.0
    ```

    Use a loop, with **one** `input( )` line inside it, and add each number to a
    running total.
    """
    for numbers, mean in [([70, 80, 90, 60, 75], 75), ([1, 2, 3, 4, 5.5], 3.1), ([0, 0, 0, 0, 10], 2)]:
        r = t.run(inputs=numbers)
        t.test("the mean of %s is %s" % (", ".join(str(n) for n in numbers), mean), r.check_output(["Mean: %s" % mean]))
    t.test("asks inside a loop", _loop_used(t) and t.count("input") == 1,
           "Ask with one input( ) line inside a loop, instead of writing five input( ) lines.")


@task("Fix the Endless Loop", level="medium", starter="""
n = 1
while n < 100:
    print(n)
print("Done")
""")
def fix_endless_loop(t):
    """
    This loop should print 1, 2, 4, 8, ... (doubling each time) while `n` is less
    than 100, then print `Done`:

    ```output
    1
    2
    4
    8
    16
    32
    64
    Done
    ```

    Press **Run**: it never stops! Fix it.
    """
    r = t.run()
    t.test("prints 1, 2, 4, ..., 64, then Done", r.check_output([1, 2, 4, 8, 16, 32, 64, "Done"]))
    r = t.run(n=5)
    t.test("starting at 5, prints 5, 10, 20, 40, 80, then Done", r.check_output([5, 10, 20, 40, 80, "Done"]))


@task("Order the Loop", level="medium", starter="""
print("Total:", total)
total = total + x * x
total = 0
print(x, total)
for x in range(1, 6):
""")
def order_the_loop(t):
    """
    These lines add up the squares 1² + 2² + ... + 5², printing the running total
    each time around the loop. They're in the wrong order, and the lines inside
    the loop need to be **indented**. Fix them, so the program prints:

    ```output
    1 1
    2 5
    3 14
    4 30
    5 55
    Total: 55
    ```

    Don't change, add or remove any lines.
    """
    r = t.run()
    t.test("prints the running totals, then Total: 55",
           r.check_output(["1 1", "2 5", "3 14", "4 30", "5 55", "Total: 55"]))
    t.test("uses only the given lines", t.check_same_lines())


@task("Halving", level="hot", starter="""
def halvings(target):
    value = 1
    count = 0
    # Halve value until it's below target, counting each halving.
    return count


print(halvings(0.001))
""")
def halving(t):
    """
    Start at 1 and keep halving: 0.5, 0.25, 0.125, ...

    Make `halvings(target)` give back how many halvings it takes for the value to
    get **below** `target`. It takes 10 halvings to get below 0.001, so the last
    line should print `10`.
    """
    r = t.run()
    for target, n in [(0.001, 10), (0.1, 4), (0.5, 2), (2, 0), (0.0001, 14)]:
        t.test("halvings(%s) gives back %d" % (target, n), r.check_returns("halvings", target, n))


@task("Adding Halves", level="hot", starter="""
def add_halves(n):
    return 0


print(add_halves(3))
""")
def adding_halves(t):
    """
    Make `add_halves(n)` give back the sum of the first `n` terms of

    ```output
    1 + 1/2 + 1/4 + 1/8 + ...
    ```

    For example, `add_halves(3)` is 1 + 0.5 + 0.25 = 1.75. Use a loop. What happens
    to the sum as n gets bigger?
    """
    r = t.run()
    for n, total in [(3, 1.75), (1, 1), (2, 1.5), (20, 2 - 0.5 ** 19), (0, 0)]:
        t.test("add_halves(%d) gives back %s" % (n, total), r.check_returns("add_halves", n, total))
    t.test("uses a loop", _loop_used(t), "Use a loop to add up the terms.")


@task("Compound Interest", level="hot", starter="""
def years_to_double(rate):
    money = 1000
    years = 0
    # Grow money by the rate each year, until it's at least 2000.
    return years


print(years_to_double(0.05))
""")
def compound_interest(t):
    """
    $1000 is invested at an interest rate of 5% a year (`rate` is 0.05). Each year,
    the money grows by 5% of itself.

    Make `years_to_double(rate)` give back how many years it takes for the $1000 to
    grow to **at least** $2000. At 5% it takes 15 years, so the last line should
    print `15`.
    """
    r = t.run()
    for rate, years in [(0.05, 15), (0.10, 8), (0.07, 11), (1, 1), (0.02, 36)]:
        t.test("years_to_double(%s) gives back %d" % (rate, years), r.check_returns("years_to_double", rate, years))


@task("Powers of Two", level="spicy", starter="""
def smallest_power(target):
    return 0


print(smallest_power(1000000))
""")
def powers_of_two(t):
    """
    Make `smallest_power(target)` give back the smallest whole number n for which
    2ⁿ is **greater than** `target`. Since 2¹⁹ = 524 288 and 2²⁰ = 1 048 576,
    `smallest_power(1000000)` is 20.
    """
    r = t.run()
    for target, n in [(1000000, 20), (1000, 10), (1, 1), (0.5, 0), (1024, 11)]:
        t.test("smallest_power(%s) gives back %d" % (target, n), r.check_returns("smallest_power", target, n))


@task("Triangular Numbers", level="spicy", starter="""
def triangular(n):
    return 0


print(triangular(4))
""")
def triangular_numbers(t):
    """
    The triangular numbers count the dots in triangles like these:

    ```output
                            •
                  •        • •
          •      • •      • • •
    •    • •    • • •    • • • •
    1     3       6       10
    ```

    Make `triangular(n)` give back the nth triangular number, **using a loop**.
    `triangular(4)` is 10. What is `triangular(750)`?
    """
    r = t.run()
    for n, value in [(4, 10), (1, 1), (5, 15), (750, 281625)]:
        t.test("triangular(%d) gives back %d" % (n, value), r.check_returns("triangular", n, value))
    t.test("uses a loop", _loop_used(t),
           "Use a loop for this one. (If you know a formula for it, that's great: check your loop with it!)")


@task("Doubling Paycheque", level="spicy", starter="""
pay_a = 500
""")
def doubling_paycheque(t):
    """
    Two jobs:

    - **Job A** pays $500 a day, so its total is $500 after day 1, $1000 after
      day 2, and so on.
    - **Job B** pays a total of $1 after day 1, $2 after day 2, $4 after day 3, and
      keeps doubling.

    Write a program that prints the first day on which Job B's total is **more than**
    Job A's:

    ```output
    Day 14
    ```

    Use the variable `pay_a` for Job A's daily pay, so the program still works if it changes.
    """
    for pay, day in [(500, 14), (1000, 15), (1, 3), (100, 12)]:
        r = t.run(pay_a=pay)
        t.test("with Job A paying $%d a day: Day %d" % (pay, day), r.check_output(["Day %d" % day]),
               hint="Use pay_a in your calculation, so that the answer changes when it changes." if pay != 500 else "")
    t.test("uses a loop", _loop_used(t), "Use a loop to go through the days.")
