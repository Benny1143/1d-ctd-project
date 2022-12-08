import colors as colors


class TerminalManager():
    def __init__(self) -> None:
        self.error = None
        self.length = 18
        self.inplace = True  # Change inplace to True to print inplace
        if self.inplace:
            print("\n"*self.length, flush=True)

    def switch_inplace(self):
        self.inplace = not self.inplace

    def clear(self):
        print(f"\x1B[{self.length}A" + "\033[K\n" *
              (self.length), end="", flush=True)

    def print(self, text: str, get_input: bool = False) -> str | None:
        length = self.length
        if self.error and self.inplace:
            length -= 1

        text_ls = text.split("\n")
        len_text = len(text_ls)
        if len_text > length:
            raise Exception(
                f"{text}\n\nThe print string is longer than space assigned")

        if self.inplace:
            text = "\x1B[{length}A{empty_space}{text}\033[K".format(
                length=length,
                empty_space="\033[K\n"*(length - len_text),
                text="\033[K\n".join(text.split("\n")))
            print((self.error + "\033[K")
                  if self.error else "\033[K", end="", flush=True)
        else:
            if self.error:
                if get_input:
                    text = "\n".join(text_ls[:-1] + [self.error, text_ls[-1]])
                else:
                    text = f"{self.error}\n{text}"
            text = "\n"*(length - len_text) + text

        self.error = None
        if get_input:
            return input(text)
        print(text, flush=True)

    def input(self, text: str) -> str:
        return self.print(text, True)

    def set_error(self, error: str) -> None:
        self.error = colors.Red + error + colors.White


if __name__ == "__main__":
    tm = TerminalManager()
    while True:
        error = tm.input("Input Error (0 - Exit): ")
        if error == "0":
            break
        if error:
            tm.set_error(error)
