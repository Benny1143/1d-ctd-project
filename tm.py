import colors as colors
# https://stackoverflow.com/questions/70480375/python-text-color-is-not-working-in-cmd-but-it-is-working-in-windows-terminal
from colorama import init
init()


class TerminalManager():
    def __init__(self) -> None:
        self.error = None
        self.length = 15
        # Change inplace to True to print inplace
        self.inplace = False
        if self.inplace:
            print("\n"*self.length, flush=True)

    def print(self, text: str, get_input: bool = False):
        length = self.length
        if self.inplace:
            print(f"\x1B[{length}A" + f"\033[K\n" *
                  (self.length), end="", flush=True)
        if self.error and self.inplace:
            length -= 1
        text_ls = text.split("\n")
        len_text = len(text_ls)
        if not self.inplace and self.error:
            if get_input:
                # print one line above input string
                text = "\n".join(text_ls[:-1] + [self.error, text_ls[-1]])
            else:
                # print above all the text
                text = f"{self.error}\n{text}"
            self.error = None
        if len_text > length:
            raise Exception("The print string is longer than space assigned")
        text = "\n"*(length - len_text) + text
        if self.inplace:
            text = f"\x1B[{length}A" + text
            if self.error:
                print(self.error, end="", flush=True)
                self.error = None
            else:
                print("\033[K", end="", flush=True)
        if get_input:
            return input(text)
        print(text, flush=True)

    def set_error(self, error: str):
        self.error = colors.Red + error + colors.White
