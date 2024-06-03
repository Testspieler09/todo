import curses
from time import sleep
from sys import exit
from help import footer_text, help_message

class ScreenManager:
    def __init__(self, content: dict) -> None:
        self.screen = curses.initscr()
        curses.start_color()
        self.dimensions = self.screen.getmaxyx()
        self.windows = [self.screen, # footer
                        curses.newpad(100,100), # main todo
                        curses.newwin(1, self.dimensions[1]-2, self.dimensions[0]-2, 0)] # help message popup
        self.active_window = 1
        self.content = content

        # ADJUST SETTINGS
        curses.curs_set(0)
        curses.cbreak()
        curses.noecho()
        self.screen.nodelay(True)
        self.screen.keypad(True)

        # CLEAR SCREEN AND RUN IT
        self.screen.clear()
        self.screen.refresh()
        self.run_scr()

    def run_scr(self) -> None:
        headline = "ToDo Manager"
        self.output_text_to_window(0, self.space_footer_text(footer_text), self.dimensions[0]-1, 0)
        _, x = self.get_coordinates_for_centered_text(headline)
        self.output_text_to_window(0, headline, 1, x, curses.A_UNDERLINE)
        while True:
            sleep(0.1) # so program doesn't use 100% cpu
            key=self.get_input()
            self.event_handler(key)

    def event_handler(self, event: str) -> None:
            match event:
                case "H" | "h":
                    pass
                case "Q" | "q":
                    self.kill_scr()
                    exit()
                case "KEY_RESIZE":
                    self.kill_scr()
                    ScreenManager()

    def get_input(self) -> str:
        try:
            return self.screen.getkey()
        except:
            return None

    def kill_scr(self) -> None:
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def get_coordinates_for_centered_text(self, text: str) -> tuple[int]:
        height, width = self.dimensions
        start_y = height // 2
        start_x = (width // 2) - (len(text) // 2)
        return start_x, start_y-1

    def space_footer_text(self, footer_text: list) -> str:
        char_amount = len("".join(footer_text))
        width = (self.dimensions[1]-1 - char_amount) // (len(footer_text) - 1)
        return "".join([arg + " "*width for arg in footer_text]).strip()

    def output_text_to_window(self, win: int, text: str, y=0, x=0, *args) -> None:
        error_msg = "Couldn't print string to window."
        attributes = curses.A_NORMAL
        for attr in args:
            attributes |= attr
        try:
            self.windows[win].addstr(y, x, text, attributes)
        except Exception:
            print(error_msg)
        self.windows[win].refresh()

    def move_content_of_pad(self, direction) -> None:
        pass

if __name__ == "__main__":
    screen = ScreenManager({})
