import colors


class Option:
    def __init__(self, option, name, function):
        self.option = option
        self.name = name
        self.function = function

    def __str__(self):
        return f"{self.option:>4}   {self.name}"


class OptionManager:
    def __init__(self):
        self._options = []
        self._dict_options = {}

    def add_option(self, option, name, function=None):
        if function is None:
            function = name
        option = str(option)
        self._options.append(Option(option, name, function))
        self._dict_options[option] = function

    def option_printer(self, question: str = "Enter Option") -> str:
        options_string = ""
        for option in self._options:
            options_string += str(option) + "\n"
        return "{color}Options:\n{options_string}{question}: {white}".format(
            options_string=options_string,
            color=colors.Yellow, white=colors.White,
            question=question)

    def get_option(self, option):
        if option in self._dict_options:
            return self._dict_options.get(option)

    def input(self, string, input_function, error_function):
        while True:
            option = input_function(string)
            if option in self._dict_options:
                return option
            else:
                error_function("Invalid Option")
