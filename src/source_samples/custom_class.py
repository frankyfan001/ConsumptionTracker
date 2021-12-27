class CustomClass:

    def __init__(self):
        self.x = 0
        print(self.x)

    def setX(self, x):
        self.x = x
        print(self.x)

    def getX(self):
        print(self.x)
        return self.x


def foo():
    a = 666
    print(a)


def bar():
    b = "string"
    print(b)


def main():
    foo()
    bar()

    custom_class = CustomClass()
    custom_class.setX(1)
    x = custom_class.getX()


main()
