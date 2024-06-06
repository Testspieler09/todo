import curses
from time import sleep
from sys import exit
from os.path import exists
from help import footer_text, help_message
from FileManager import FileManager, DataManager

class ScreenManager:
    def __init__(self, file: str) -> None:
        self.screen = curses.initscr()
        self.file = file
        self.data = DataManager(self.file.data)

        lines = help_message.split("\n")
        self.window_dimensions = [self.screen.getmaxyx(),
                                  (100, 100),
                                  (len(lines)+1, max(len(line) for line in lines)+1)]
        self.windows = [self.screen, # footer
                        curses.newpad(self.window_dimensions[1][0], self.window_dimensions[1][1]), # main todo
                        curses.newpad(self.window_dimensions[2][0], self.window_dimensions[2][1])] # help message popup

        self.scroll_y, self.scroll_x = 0, 0
        self.last_scroll_pos_main_scr = (0, 0)
        self.main_start_x_y = (2, 1)
        self.main_end_x_y = (self.window_dimensions[0][0]-2, self.window_dimensions[0][1]-1)
        self.active_window = 1
        self.content = {}# self.load_content(file)

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
        self.output_text_to_window(0, self.space_footer_text(footer_text), self.window_dimensions[0][0]-1, 0)
        y, _ = self.get_coordinates_for_centered_text(headline)
        self.output_text_to_window(0, headline, 1, y, curses.A_UNDERLINE)
        self.output_text_to_window(1, str(self.data.get_data_of_group("Project 1")), 1, 1)
        while True:
            sleep(0.01) # so program doesn't use 100% cpu
            key=self.get_input()
            self.event_handler(key)

    def scroll_pad(self, pad_id: int) -> None:
        self.windows[pad_id].refresh(self.scroll_x, self.scroll_y,
                                     self.main_start_x_y[0], self.main_start_x_y[1],
                                     self.main_end_x_y[0], self.main_end_x_y[1])

    def event_handler(self, event: str) -> None:
        match event:
            # Scroll operations
            case "KEY_DOWN":
                if abs(self.scroll_x - self.window_dimensions[self.active_window][0]-3) <= self.window_dimensions[0][0]:
                    return
                self.scroll_x += 1
                self.scroll_pad(self.active_window)
            case "KEY_UP":
                self.scroll_x -= 1
                if self.scroll_x <= 0:
                    self.scroll_x = 0
                self.scroll_pad(self.active_window)
            case "KEY_RIGHT":
                if abs(self.scroll_y - self.window_dimensions[self.active_window][1]-1) <= self.window_dimensions[0][1]:
                    return
                self.scroll_y += 1
                self.scroll_pad(self.active_window)
            case "KEY_LEFT":
                self.scroll_y -= 1
                if self.scroll_y <= 0:
                    self.scroll_y = 0
                self.scroll_pad(self.active_window)
            # Main operations
            case "G" | "g":
                pass
            case "L" | "l":
                pass
            case "I" | "i":
                pass
            case "C" | "c":
                pass
            case "D" | "d":
                pass
            case "A" | "a":
                pass
            # Default operations
            case "H" | "h":
                if self.active_window == 2:
                    self.active_window = 1
                    self.scroll_x, self.scroll_y = self.last_scroll_pos_main_scr
                    self.windows[1].refresh(self.scroll_x, self.scroll_y,
                                            self.main_start_x_y[0], self.main_start_x_y[1],
                                            self.main_end_x_y[0], self.main_end_x_y[1])
                else:
                    self.active_window = 2
                    self.last_scroll_pos_main_scr = (self.scroll_x, self.scroll_y)
                    self.scroll_x, self.scroll_y = 0, 0
                    self.output_text_to_window(2, help_message, 0, 0)
            case "Q" | "q":
                self.kill_scr()
                exit()
            case "KEY_RESIZE":
                self.kill_scr()
                ScreenManager(self.file.path_to_file)

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
        height, width = self.window_dimensions[0]
        start_y = height // 2
        start_x = (width // 2) - (len(text) // 2)
        return start_x, start_y-1

    def space_footer_text(self, footer_text: list) -> str:
        char_amount = len("".join(footer_text))
        width = (self.window_dimensions[0][1]-1 - char_amount) // (len(footer_text) - 1)
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
        try:
            self.windows[win].refresh()
        except Exception:
            self.windows[win].box()
            self.windows[win].refresh(self.scroll_x, self.scroll_y,
                                      self.main_start_x_y[0], self.main_start_x_y[1],
                                      self.main_end_x_y[0], self.main_end_x_y[1])

def main(cwd: str) -> None:
    filepath = f"{cwd}\\data.json"
    if exists(filepath):
        file = FileManager(filepath)
    else:
        file = FileManager.for_new_file(filepath)
    screen = ScreenManager(file)

if __name__ == "__main__":
    from os import getcwd
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="ToDo",
                            description="A minimalistic terminal-based todo-manager written with curses.",
                            epilog="Have fun using it.")

    args = parser.parse_args()

    main(getcwd())
