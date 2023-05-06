# defines custom classes

class Thingy(object):
    def __init__(self, num):
        self.number = num

    def __str__(self):
        return "<Thingy @" + str(id(self)) + ", number=" + str(self.number) + ">"
