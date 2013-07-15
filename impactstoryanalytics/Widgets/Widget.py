class Widget:
    def get_name(self):
        return self.__class__.__name__.lower()

    def get_data(self):
        raise NotImplementedError