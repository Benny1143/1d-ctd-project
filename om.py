import colors


class Option:
    def __init__(self, option, name, function):
        self.option = option
        self.name = name
        self.function = function


class OptionManager:
    def __init__(self):
        self._options = []
        self._dict_options = {}
        pass

    def add_option(self, option, name, function = None):
        if function is None:
            function = name
        option = str(option)
        self._options.append(Option(option, name, function))
        self._dict_options[option] = function

    def option_printer(self, question: str = "Enter Option") -> str:
        ls = list(map(lambda option: (option.option, option.name), self._options))
        return "{color}Options:\n{options_string}\n{question}: {white}".format(
            options_string='\n'.join(
                f"{option:>4}   {name}" for option, name in ls),
            color=colors.Yellow, white=colors.White,
            question=question)

    def get_option(self, option):
        if option in self._dict_options:
            return self._dict_options.get(option)

    def input(self, string, print_function, error_function):
        while True:
            option = print_function(string, True)
            if option in self._dict_options:
                return option
            else:
                error_function("Invalid Option")
