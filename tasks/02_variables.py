section("2. Variables")

RECTANGLE = """
length = 8
width = 5

area = length * width
print("Area:", area)
"""


@task("Rectangle", starter=RECTANGLE)
def rectangle(t):
    """
    A variable is a name for a value. This program stores a rectangle's length
    and width, then works out its area.

    Add to it, so that it also works out the perimeter, stores it in a variable
    called `perimeter`, and prints it. For a length of 8 and a width of 5:

        Area: 40
        Perimeter: 26

    Then try other numbers for `length` and `width`. Both answers should change.
    """
    r = t.run()
    t.test("prints the area and the perimeter", r.check_output(["Area: 40", "Perimeter: 26"]))
    t.test("has a variable called perimeter", r.check_var("perimeter", 26))
    r = t.run(length=10, width=2.5)
    t.test("works for other rectangles (length 10, width 2.5)", r.check_output(["Area: 25", "Perimeter: 25"]))


AVERAGE = """
a = 70
b = 80
c = 90

average = a + b + c / 3
print("Average:", average)
"""


@task("Fix the Average", starter=AVERAGE)
def fix_the_average(t):
    """
    Three test marks are 70, 80 and 90, so their average is 80.
    This program says the average is 180.0!

    Find the mistake and fix it, so that it prints:

        Average: 80.0

    Hint: BEDMAS. Which operation happens first?
    """
    r = t.run()
    t.test("the average of 70, 80 and 90 is 80", r.check_output(["Average: 80"]))
    r = t.run(a=50, b=60, c=100)
    t.test("the average of 50, 60 and 100 is 70", r.check_output(["Average: 70"]))


TAXI = """
distance = 12

# Work out the cost of the trip, then print it.
"""


@task("Taxi Fare", starter=TAXI)
def taxi_fare(t):
    """
    A taxi charges a flat fee of $3.50, plus $2 for every kilometre.

    Work out the cost of a trip, store it in a variable called `cost`, and print
    it. For a trip of 12 km:

        Cost: 27.5

    Use the variable `distance` in your calculation, so that the program works
    for any distance.
    """
    r = t.run()
    t.test("a 12 km trip costs 27.5", r.check_output(["Cost: 27.5"]))
    t.test("has a variable called cost", r.check_var("cost", 27.5))
    for distance, cost in [(20, 43.5), (0, 3.5)]:
        r = t.run(distance=distance)
        t.test("a %d km trip costs %s" % (distance, cost), r.check_output(["Cost: %s" % cost]))
