section("1. Print and Calculate")


@task("Hello World", level="learn", starter="""
# Lines that start with # are comments. Python skips them.
# Type your code under this line, then press Run.
""")
def hello_world(t):
    """
    `print( )` shows something on the screen. Text goes inside quotation marks:

    ```python
    print("Good morning")
    ```

    ```output
    Good morning
    ```

    Make Python print this line. Press **Run** to try it, then **Check my code**.

    ```output
    Hello World
    ```
    """
    r = t.run()
    t.test("prints Hello World", r.check_output(["Hello World"]),
           hint="Put the words in quotation marks inside the brackets:  print(\"...\")")


@task("Python as a Calculator", level="learn", starter="""
print(15 + 27)
""")
def calculator(t):
    """
    Python can do arithmetic. Numbers don't go in quotation marks.

    - `+` adds and `-` subtracts
    - `*` multiplies (not x)
    - `/` divides

    The program already prints the answer to 15 + 27. Add two more lines, so that it
    also prints the answers to **12 × 8** and **100 ÷ 8**, in that order.

    Dividing always gives an answer with a decimal point, so 100 ÷ 8 prints as `12.5`.
    """
    r = t.run()
    t.test("prints the three answers", r.check_output([42, 96, 12.5]))
    t.test("Python does the calculating", t.uses("*", "/"),
           "Let Python work the answers out: use * and / in your code instead of typing the answers.")


@task("Powers", level="learn", starter="""
print(5 ** 2)
""")
def powers(t):
    """
    `**` means "to the power of". This program prints 5², which is 25.

    **Careful:** `^` is not a power in Python. `5 ^ 2` runs, but gives 7!

    Add two lines, so that the program prints 5², then **2¹⁰**, then **3⁴**.
    """
    r = t.run()
    t.test("prints 25, 1024 and 81", r.check_output([25, 1024, 81]))
    t.test("uses ** for each power", t.count("**") >= 3,
           "Use ** for each power, instead of typing the answers or multiplying.")


@task("Order of Operations", level="learn", starter="""
print(2 + 3 * 4)
""")
def order_of_operations(t):
    """
    Python follows BEDMAS: **B**rackets, **E**xponents, **D**ivision and
    **M**ultiplication, then **A**ddition and **S**ubtraction. So this program
    multiplies first, and prints `14`.

    Add **one pair of brackets** so that it adds first and prints `20`.
    Don't change anything else.
    """
    r = t.run()
    t.test("prints 20", r.check_output([20]))
    t.test("only brackets were added", t.check_only_added("()"))


@task("Text and Numbers Together", level="learn", starter="""
print("5 squared is", 5 ** 2)
""")
def text_and_numbers(t):
    """
    `print( )` can show several things at once: separate them with commas, and
    Python puts a space between them.

    ```python
    print("5 squared is", 5 ** 2)
    ```

    ```output
    5 squared is 25
    ```

    Text in quotation marks is printed exactly as it is typed. Maths outside the
    quotation marks is worked out first.

    A rectangle is 8 cm long and 3 cm wide. Change the program so that it prints

    ```output
    The area is 24
    ```

    and let Python do the multiplying: write `8 * 3`, not 24.
    """
    r = t.run()
    t.test("prints The area is 24", r.check_output(["The area is 24"]),
           hint="Maths inside quotation marks is just text. Put 8 * 3 after a comma, outside the quotation marks.")
    t.test("Python does the multiplying", t.uses("8", "3", "*"),
           "Write 8 * 3 outside the quotation marks, so that Python works out the area.")


@task("Rounding", level="learn", starter="""
print(22 / 7)
""")
def rounding(t):
    """
    `round(number, places)` rounds a number to that many decimal places. Leave out
    the places to round to a whole number.

    ```python
    print(round(3.14159, 2))
    print(round(3.14159))
    ```

    ```output
    3.14
    3
    ```

    22 ÷ 7 is close to π. Change the program so that it prints 22 ÷ 7 **rounded to
    3 decimal places**. Then add a line that prints 100 ÷ 3 **rounded to a whole number**.
    """
    r = t.run()
    t.test("prints 3.143, then 33", r.check_output([3.143, 33]))
    t.test("uses round( ) for both", t.count("round") >= 2,
           "Use round( ) for both answers, instead of typing them.")


@task("Predict: Calculations", level="mild", predict=[
    question("print(2 + 3 * 4)", hint="BEDMAS: multiplying comes before adding."),
    question("print(10 / 4)", hint="Dividing gives an answer with a decimal point."),
    question("print((7 - 3) ** 2 + 1)"),
    question("print(2 * 3 ** 2)", hint="BEDMAS: the exponent comes before the multiplying."),
    question('print("3 + 4 =", 3 + 4)',
             hint="Text in quotation marks is printed exactly as typed. Maths outside them is worked out."),
])
def predict_calculations(t):
    """
    **Don't run anything.** Read each program and work out what it prints. Type
    your answer in the box under it, then press **Check my answers**.

    Remember BEDMAS, and that `/` always gives an answer with a decimal point.
    """


@task("Fix the Mistakes", level="mild", starter="""
print(3 x 4)
print(4^2)
print("10 + 5 =", "10 + 5")
""")
def fix_the_mistakes(t):
    """
    Each line of this program has a mistake. Fix them so that it prints:

    ```output
    12
    16
    10 + 5 = 15
    ```

    Press **Run** after each fix: the error messages tell you which line to look at.
    """
    r = t.run()
    text_sum = len(r.output) == 3 and r.output[2].replace(" ", "") == "10+5=10+5"
    t.test("prints 12, 16 and 10 + 5 = 15", r.check_output([12, 16, "10 + 5 = 15"]),
           hint="Let Python work out 10 + 5: take away the quotation marks around it." if text_sum else "")
    t.test("Python does the calculating", t.uses("*", "**", "+"),
           "Use * to multiply, ** for the power, and let Python add 10 + 5.")


@task("Brackets Only", level="medium", starter="""
print(3 + 4 * 2 ** 2)
print(3 + 4 * 2 ** 2)
""")
def brackets_only(t):
    """
    Both lines work out `3 + 4 * 2 ** 2`, so right now the program prints 19 twice.

    **Add only brackets** (don't change, move or remove anything else) so that the
    first line prints **28** and the second line prints **196**.
    """
    r = t.run()
    t.test("prints 28, then 196", r.check_output([28, 196]))
    t.test("only brackets were added", t.check_only_added("()"))
