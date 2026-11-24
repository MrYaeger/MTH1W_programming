section("4. Functions")


@task("Formula Machines", level="learn", starter="""
def square_area(side):
    return side ** 2


print(square_area(5))
""")
def formula_machines(t):
    """
    A **function** is a formula machine: you give it a value, and it gives back an
    answer, like f(x) in math.

    ```python
    def square_area(side):
        return side ** 2
    ```

    - `def` makes the machine, and names it `square_area`.
    - `side` is its **parameter**: the value it's given. Here it's like the x in f(x).
    - `return` gives back the answer.
    - The indented lines are the machine's insides. They need the colon `:` above them.

    Making the machine doesn't run it. It runs when it's **called**:
    `square_area(5)` runs it with `side` set to 5, and gives back 25.

    Add two lines that print the areas of squares with sides of **7** and **2.5**,
    by calling `square_area`.
    """
    r = t.run()
    t.test("prints 25, 49 and 6.25", r.check_output([25, 49, 6.25]))
    t.test("calls square_area each time", t.count("square_area") >= 4,
           "Print square_area(7) and square_area(2.5), so that the function does the work.")


@task("Write a Function", level="learn", starter="""
def triangle_area(base, height):
    return 0


print(triangle_area(6, 4))
""")
def write_a_function(t):
    """
    A function can have more than one parameter. `triangle_area` has two: `base`
    and `height`. When it's called as `triangle_area(6, 4)`, base is 6 and height is 4.

    Right now it always gives back 0. Change its `return` line so that it gives back
    the area of the triangle: base × height ÷ 2. The last line should then print `12.0`.

    Use the parameters in the formula, not the numbers 6 and 4: the function has to
    work for **any** triangle.
    """
    r = t.run()
    for args, area in [((6, 4), 12), ((5, 3), 7.5), ((10, 0.5), 2.5), ((1, 1), 0.5)]:
        t.test("triangle_area(%s, %s) gives back %s" % (args + (area,)), r.check_returns("triangle_area", args, area))


@task("Return, Not Print", level="learn", starter="""
def double(n):
    print(n * 2)


answer = double(5) + 1
print(answer)
""")
def return_not_print(t):
    """
    `print( )` only **shows** a value on the screen. `return` **gives it back**, so
    that the rest of the program can use it.

    This program should print 11 (double 5 is 10, plus 1). Press **Run**: it stops
    with an error, because `double` shows its answer but gives back nothing.

    Fix the function so that it gives back its answer instead of printing it.
    """
    r = t.run()
    t.test("prints 11", r.check_output([11]))
    for n, want in [(5, 10), (0.5, 1), (-3, -6)]:
        t.test("double(%s) gives back %s" % (n, want), r.check_returns("double", n, want))


@task("Use the Parameters", level="learn", starter="""
length = 8
width = 3


def rectangle_area(l, w):
    return length * width


print(rectangle_area(8, 3))
print(rectangle_area(5, 2))
""")
def use_the_parameters(t):
    """
    This function looks like it works: the first line prints 24, which is right.
    But the second line should print 10, and it prints 24 again!

    Inside the function, `l` and `w` are the values it was given. Fix the function
    so that it uses them, and works for every rectangle.
    """
    r = t.run()
    t.test("prints 24, then 10", r.check_output([24, 10]))
    for args, area in [((5, 2), 10), ((2.5, 4), 10), ((1, 1), 1)]:
        t.test("rectangle_area(%s, %s) gives back %s" % (args + (area,)), r.check_returns("rectangle_area", args, area),
               hint="Use the function's own parameters, l and w, in its return line.")


@task("Rectangle Perimeter", level="mild", starter="""
def rectangle_perimeter(length, width):
    return 0


print(rectangle_perimeter(8, 3))
""")
def rectangle_perimeter(t):
    """
    Change the `return` line, so that `rectangle_perimeter(length, width)` gives
    back the perimeter of a rectangle. The last line should then print `22`.
    """
    r = t.run()
    for args, p in [((8, 3), 22), ((2.5, 4), 13), ((10, 10), 40), ((0.5, 0.25), 1.5)]:
        t.test("rectangle_perimeter(%s, %s) gives back %s" % (args + (p,)), r.check_returns("rectangle_perimeter", args, p))


@task("Predict: Functions", level="medium", predict=[
    question("""
    def f(x):
        return 3 * x - 1

    print(f(2))
    """),
    question("""
    def f(x):
        return x ** 2 + 1

    print(f(3) + f(0))
    """, hint="Work out each call on its own first: f(3), then f(0)."),
    question("""
    def area(length, width):
        return length * width

    print(area(2, 5), area(5, 2))
    """),
    question("""
    def g(n):
        print(n + 1)
        return n * 10

    result = g(4)
    print(result)
    """, hint="Calling g runs every line inside it, including its print( ). Then it gives back a value."),
])
def predict_functions(t):
    """
    **Don't run anything.** For each program, work out what it prints. Remember
    that a function only runs when it's called, and that `return` gives a value
    back to the line that called it.
    """


@task("Unit Price Machine", level="medium", starter="""
def unit_price(price, quantity):
    return 0


print(unit_price(8.99, 12))
""")
def unit_price_function(t):
    """
    Make `unit_price(price, quantity)` give back the price of one item, **rounded
    to 2 decimal places**. A pack of 12 for $8.99 is $0.75 each, so the last line
    should print `0.75`.
    """
    r = t.run()
    for args, each in [((8.99, 12), 0.75), ((5, 1), 5), ((10, 3), 3.33), ((12, 7), 1.71), ((0.99, 3), 0.33)]:
        t.test("unit_price(%s, %s) gives back %s" % (args + (each,)), r.check_returns("unit_price", args, each))


@task("Inscribed Angles", level="medium", starter="""
def inscribed_angle(central):
    return 0


print(inscribed_angle(110))
""")
def inscribed_angle(t):
    """
    In a circle, an inscribed angle is half of the central angle on the same arc.

    Make `inscribed_angle(central)` give back the inscribed angle for a central
    angle of `central` degrees. The last line should print `55.0`.
    """
    r = t.run()
    for central, angle in [(110, 55), (90, 45), (37, 18.5), (180, 90)]:
        t.test("inscribed_angle(%s) gives back %s" % (central, angle), r.check_returns("inscribed_angle", central, angle))


@task("Cylinder Volume", level="hot", starter="""
import math


def circle_area(radius):
    return math.pi * radius ** 2


def cylinder_volume(radius, height):
    return 0


print(cylinder_volume(2, 5))
""")
def cylinder_volume(t):
    """
    The volume of a cylinder is the area of its circle times its height.

    `circle_area` already works. Make `cylinder_volume(radius, height)` give back
    the volume of a cylinder, by **calling `circle_area`** inside it. The last line
    should print about 62.83.
    """
    r = t.run()
    pi = 3.141592653589793
    for args, v in [((2, 5), 20 * pi), ((1, 1), pi), ((3, 0.5), 4.5 * pi), ((10, 2), 200 * pi)]:
        t.test("cylinder_volume(%s, %s) gives back %.4f" % (args + (v,)), r.check_returns("cylinder_volume", args, v))
    t.test("cylinder_volume calls circle_area", t.count("circle_area") >= 2,
           "Use circle_area(radius) inside cylinder_volume, instead of writing the circle's formula again.")


@task("Distance Between Points", level="spicy", starter="""
import math


def distance(x1, y1, x2, y2):
    return 0


print(distance(0, 0, 3, 4))
""")
def distance(t):
    """
    Make `distance(x1, y1, x2, y2)` give back the distance between the points
    (x1, y1) and (x2, y2). The last line should print `5.0`.

    Hint: draw a right triangle whose hypotenuse joins the two points. How long are
    its other two sides?
    """
    r = t.run()
    for args, d in [((0, 0, 3, 4), 5), ((1, 2, 4, 6), 5), ((-1, -1, 2, 3), 5), ((0, 0, 1, 1), 2 ** 0.5),
                    ((5, 1, 2, -3), 5), ((2, 2, 2, 9), 7)]:
        t.test("distance(%s, %s, %s, %s) gives back %s" % (args + (round(d, 4),)), r.check_returns("distance", args, d))
