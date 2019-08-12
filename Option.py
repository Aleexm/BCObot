class Option:

    def __init__(self, user_info, params=None, object=None, name="", function=None):
        self.function = function
        self.name = "({})".format(name)
        self.user_info = user_info
        self.params = params
        self.object = object

    def __repr__(self):
        return "{}: {}".format(self.name, self.user_info)
