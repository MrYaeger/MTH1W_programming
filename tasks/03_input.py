section("3. Asking Questions")


@task("Greeting", level="learn", starter="""
name = input("What is your name? ")
""")
def greeting(t):
    """
    `input("...")` asks a question and waits for an answer. The answer is stored
    in a variable, just like a value:

    ```python
    food = input("Favourite food? ")
    print("I like", food, "too")
    ```

    ```output
    Favourite food? pizza
    I like pizza too
    ```

    This program asks for a name and stores it in `name`. Add a line that says
    hello to that person. If the answer is Sam:

    ```output
    Hello, Sam!
    ```

    Press **Run**, then type an answer in the box that appears and press Enter.
    """
    for name in ["Sam", "Priya"]:
        r = t.run(inputs=[name])
        t.test("answering %s prints Hello, %s!" % (name, name), r.check_output(["Hello, %s!" % name]),
               hint="Print the variable name (no quotation marks around it), so the greeting uses the answer.")
    t.test("asks one question", len(r.prompts) == 1,
           "Your program asked %d questions. Ask just one." % len(r.prompts))


@task("Numbers from input", level="learn", starter="""
side = input("Side length? ")
print("Perimeter:", 4 * side)
""")
def square(t):
    """
    `input( )` always gives **text**, even when the answer is a number. Python
    can't do arithmetic with text, so turn it into a number first:

    - `float(input("..."))` for any number, like 2.5
    - `int(input("..."))` for whole numbers only

    Press **Run** and type 5. The perimeter comes out as 5555! That's because
    `side` holds the text "5", and 4 times a piece of text repeats it.

    Fix the program, then add a line that prints the square's area. For a side
    of 5:

    ```output
    Perimeter: 20.0
    Area: 25.0
    ```
    """
    hint = ("" if t.uses("float") or t.uses("int")
            else "Turn the answer into a number: side = float(input(\"Side length? \"))")
    for side in [5, 2.5, 10]:
        r = t.run(inputs=[side])
        t.test("a side of %s gives a perimeter of %s and an area of %s" % (side, 4 * side, side ** 2),
               r.check_output(["Perimeter: %s" % (4 * side), "Area: %s" % (side ** 2)]), hint=hint, error_hint=hint)


@task("Area of a Triangle", level="mild", starter="""
base = float(input("Base? "))
""")
def triangle_area(t):
    """
    Ask for the base of a triangle, then its height, and print its area.
    If the answers are 6 and 4:

    ```output
    Area: 12.0
    ```

    The area of a triangle is base × height ÷ 2.
    """
    for base, height, area in [(6, 4, 12), (5, 3, 7.5), (2.5, 4, 5)]:
        r = t.run(inputs=[base, height])
        t.test("base %s and height %s give Area: %s" % (base, height, float(area)),
               r.check_output(["Area: %s" % area]))


@task("Predict: input", level="mild", predict=[
    question("""
    n = int(input("Number? "))
    print(n * 2 + 1)
    """, 4, 10),
    question("""
    name = input("Name? ")
    print("Hi", name)
    print(name, name)
    """, "Ali"),
    question("""
    a = input("Number? ")
    print(a + a)
    """, 5, hint="Without int( ) or float( ), the answer is text, and + joins text together."),
    question("""
    x = float(input("x? "))
    y = float(input("y? "))
    print(y - x)
    """, [2, 10]),
])
def predict_input(t):
    """
    **Don't run anything.** For each program, work out what it prints when the
    user types the answers shown. Write only what `print( )` shows: the question
    `input( )` asks isn't part of it.
    """


@task("Hypotenuse", level="medium", starter="""
import math

a = float(input("a? "))
b = float(input("b? "))
""")
def pythagorean(t):
    """
    The two shorter sides of a right triangle are `a` and `b`. By the Pythagorean
    theorem, the longest side (the hypotenuse) is c = √(a² + b²).

    Work out c and print it **rounded to 3 decimal places**. `math.sqrt(x)` is the
    square root of x. If the answers are 3 and 4:

    ```output
    c = 5.0
    ```

    If the answers are 1 and 1:

    ```output
    c = 1.414
    ```
    """
    for a, b, c in [(3, 4, 5), (5, 12, 13), (1, 1, 1.414), (2.5, 6, 6.5), (2, 3, 3.606)]:
        r = t.run(inputs=[a, b])
        t.test("a = %s and b = %s give c = %s" % (a, b, c), r.check_output(["c = %s" % c]))


@task("Unit Price", level="medium", starter="""
# Ask for the price of the pack, then the number of items in it.
""")
def unit_price(t):
    """
    A pack of 12 pens costs $8.99. How much is that for each pen?

    Write a program that asks for the price of a pack, then the number of items in
    it. Print the price of one item, **rounded to 2 decimal places**:

    ```output
    Price per item: $ 0.75
    ```
    """
    for price, items, each in [(8.99, 12, 0.75), (5, 1, 5), (10, 3, 3.33), (12, 7, 1.71)]:
        r = t.run(inputs=[price, items])
        t.test("$%s for %d items is $%s each" % (price, items, each), r.check_output(["Price per item: $ %s" % each]),
               hint="Ask for the price first, then the number of items.",
               error_hint="Ask for the price first, then the number of items.")


@task("Proportions", level="medium", starter="""
# Ask for a, then b, then c.
""")
def proportions(t):
    """
    In the proportion a/b = c/x, the missing value is

    ```output
    x = b × c ÷ a
    ```

    Write a program that asks for a, then b, then c, and prints x. If the answers
    are 2, 3 and 8 (so 2/3 = 8/x):

    ```output
    x = 12.0
    ```
    """
    for a, b, c, x in [(2, 3, 8, 12), (4, 6, 10, 15), (5, 2, 7, 2.8), (3, 9, 1.5, 4.5)]:
        r = t.run(inputs=[a, b, c])
        t.test("%s/%s = %s/x gives x = %s" % (a, b, c, x), r.check_output(["x = %s" % x]),
               hint="Ask for the values in this order: a, then b, then c.",
               error_hint="Ask for the values in this order: a, then b, then c.")


@task("Radius from Area", level="hot", starter="""
import math
""")
def radius_from_area(t):
    """
    The area of a circle is A = πr². Ask for a circle's area, and print its
    radius **rounded to 1 decimal place**. If the answer is 50:

    ```output
    Radius: 4.0
    ```

    Rearrange A = πr² to find r first.
    """
    for area, radius in [(50, 4.0), (100, 5.6), (3.14, 1.0), (1000, 17.8)]:
        r = t.run(inputs=[area])
        t.test("an area of %s gives Radius: %s" % (area, radius), r.check_output(["Radius: %s" % radius]))


@task("Scientific Notation", level="hot", starter="""
""")
def scientific_notation(t):
    """
    A number in scientific notation looks like a × 10ⁿ, for example 3.2 × 10⁴.

    Write a program that asks for a, then for n, and prints the number in standard
    form. If the answers are 3.2 and 4:

    ```output
    32000.0
    ```

    If they're 5 and -3, it prints `0.005`. In Python, 10ⁿ is `10 ** n`.

    Python writes very big and very small numbers its own way: `6.02e+23` means
    6.02 × 10²³. That's fine.
    """
    for a, n, value in [(3.2, 4, 32000), (5, -3, 0.005), (1.5, 0, 1.5), (7.25, 2, 725), (6.02, 23, 6.02e23)]:
        r = t.run(inputs=[a, n])
        t.test("%s × 10 to the power %s is %s" % (a, n, value), r.check_prints(value),
               hint="Ask for a first, then n.", error_hint="Ask for a first, then n.")


@task("Line Through Two Points", level="spicy", starter="""
""")
def line_through_points(t):
    """
    Write a program that asks for two points on a line, (x1, y1) and (x2, y2), as
    four answers in that order: x1, y1, x2, y2. Print the line's equation in the
    form y = mx + b. For the points (1, 5) and (3, 9):

    ```output
    y = 2.0x + 3.0
    ```

    The slope is m = (y2 - y1) ÷ (x2 - x1). Then use one of the points to find b.
    (You can assume the line isn't vertical, and that b isn't negative.)
    """
    for points, m, b in [((1, 5, 3, 9), 2, 3), ((0, 4, 2, 0), -2, 4), ((1, 1, 3, 2), 0.5, 0.5),
                         ((-1, 2, 1, 6), 2, 4), ((2, 7, 6, 7), 0, 7)]:
        r = t.run(inputs=list(points))
        t.test("(%s, %s) and (%s, %s) give y = %sx + %s" % (points + (m, b)), r.check_output(["y = %sx + %s" % (m, b)]))
