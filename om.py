import colors


class Option:
    def __init__(self, option: str, name: str, value: any):
        self.option = option
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f"{self.option:>4}   {self.name}"


class OptionManager:
    def __init__(self, option_dict: dict = {}):
        self.counter = 1
        self._options = []
        self._dict_options = {}
        for name, value in option_dict.items():
            self.add_option(name, value)

    def add_option(self, name: str, value: any = None, option: str = None) -> None:
        if value is None:
            value = name
        option = option if option else str(self.counter)
        self._options.append(Option(option, name, value))
        self._dict_options[option] = value
        self.counter += 1

    def option_printer(self, question: str = "Enter Option") -> str:
        options_string = ""
        for option in self._options:
            options_string += str(option) + "\n"
        return "{color}Options:\n{options_string}{question}: {white}".format(
            options_string=options_string,
            color=colors.Yellow, white=colors.White,
            question=question)

    def get_option(self, option: str):
        if option in self._dict_options:
            return self._dict_options.get(option)

    def input(self, string, input_function, error_function):
        while True:
            option = input_function(string)
            if option in self._dict_options:
                return option
            else:
                error_function("Invalid Option")


if __name__ == "__main__":
    om = OptionManager({"Test": 1})
    om.add_option("Exit", "0", "0")
    print(om.option_printer())
