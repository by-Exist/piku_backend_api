class Test2:
    pass


class Test:
    def __init__(self):
        test2 = Test2()
        test2.test = "2"
        self.test = test2


test = Test()

print(test.test.test)

print(getattr(test, "test.test"))