import curses
from sys import exit

class ScreenManager:
    def __init__(self):
        self.screen = curses.initscr()
        self.supports_color: bool = curses.has_colors()
        self.content = {}

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
        while True:
            if (key:=self.get_input()) != None: key = key.upper()
            match key:
                case "Q":
                    screen.kill_scr()
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

    def move_content_of_pad(self, direction) -> None:
        pass

if __name__ == "__main__":
    screen = ScreenManager()
