import curses
from time import sleep
from sys import exit
from re import match
from textwrap import wrap
from os.path import exists
from help import footer_text, help_message, instructions, wrong_input_message
from FileManager import FileManager, DataManager

class ScreenManager:
    def __init__(self, file: str, content=None, content_beautified=None) -> None:
        self.screen = curses.initscr()
        self.file = file
        self.data = DataManager(self.file.data)
        self.running = True
        self.current_order_with_args = ["standard"] # other would be group, label and importance

        # DETERMINE THE SIZE OF THE MAIN PAD
        max_dimensions = self.data.get_longest_entry_beautified()
        if max_dimensions[0]+2 > self.screen.getmaxyx()[0]-3:
            y = max_dimensions[0]+2
        else:
            y = self.screen.getmaxyx()[0]-3
        if max_dimensions[1]+2 > self.screen.getmaxyx()[1]:
            x = max_dimensions[1]+2
        else:
            x = self.screen.getmaxyx()[1]

        help_lines = help_message.split("\n")
        self.window_dimensions = [self.screen.getmaxyx(),
                                  (y, x),
                                  (len(help_lines)+1, max(len(line) for line in help_lines)+1)]
        self.windows = [self.screen, # footer
                        curses.newpad(self.window_dimensions[1][0], self.window_dimensions[1][1]), # main todo
                        curses.newpad(self.window_dimensions[2][0], self.window_dimensions[2][1])] # help message popup

        self.scroll_y, self.scroll_x = 0, 0
        self.last_scroll_pos_main_scr = (0, 0)
        self.main_start_x_y = (2, 0)
        self.main_end_x_y = (self.window_dimensions[0][0]-2, self.window_dimensions[0][1]-1)
        self.active_window = 1
        self.content = self.data.get_all_data() if content==None else content
        self.content_beautified = self.data.display_task_details(self.content) if content_beautified==None else content_beautified

        # COLOR STUFF FOR IMPORTANCE
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.low_importance = curses.color_pair(1)
        self.medium_importance = curses.color_pair(2)
        self.high_importance = curses.color_pair(3)

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
        self.beautify_output()
        while self.running:
            sleep(0.01) # so program doesn't use 100% cpu
            key=self.get_input()
            self.event_handler(key)

    def scroll_pad(self, pad_id: int) -> None:
        start_x, start_y, end_x, end_y = self.get_coordinates_for_centered_pad(pad_id)
        self.windows[pad_id].refresh(self.scroll_x, self.scroll_y, start_x, start_y, end_x, end_y)

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
                if abs(self.scroll_y - self.window_dimensions[self.active_window][1]) <= self.window_dimensions[0][1]:
                    return
                self.scroll_y += 1
                self.scroll_pad(self.active_window)
            case "KEY_LEFT":
                self.scroll_y -= 1
                if self.scroll_y <= 0:
                    self.scroll_y = 0
                self.scroll_pad(self.active_window)
            # Main operations
            case "S" | "s":
                input_length = 12
                input = self.get_input_string(instructions["show"], input_length, r"\d+")
                if input=="0":
                    self.update_content(self.content)
                    self.beautify_output()
                else:
                    task_hash = self.data.get_hash_of_task_with_index(int(input), self.current_order_with_args)
                    self.update_content(self.content, task_hash)
                    self.beautify_output()
            case "A" | "a":
                input = self.get_input_string(instructions["add"]["1"], 1, r"[TtSs]")
                match input.lower():
                    case "t":
                        pass
                    case "s":
                        pass
            case "C" | "c":
                pass
            case "D" | "d":
                input = self.get_input_string(instructions["display"]["1"], 1, r"[GgLlIi0]")
                match input.lower():
                    case "0":
                        self.current_order_with_args = ["standard"]
                        self.update_content(self.data.get_all_data())
                        self.beautify_output()
                    case "g":
                        groups = self.data.get_groups()
                        input = self.get_input_string(instructions["display"]["2"]["group"] + groups[0], 12, r"\d+")
                        try:
                            if input == "0":
                                self.update_content(self.data.get_all_tasks_without("groups"))
                                self.current_order_with_args = ["standard", self.content]
                            else:
                                self.update_content(self.data.get_data_of_group(list(self.data.data["order of tasks in group"].keys())[int(input)-1]))
                                self.current_order_with_args = ["group", groups[1][int(input)-1]]
                        except:
                            pass
                        self.beautify_output()
                    case "l":
                        labels = self.data.get_labels()
                        input = self.get_input_string(instructions["display"]["2"]["label"] + labels[0], 12, r"\d+")
                        try:
                            if input=="0":
                                self.update_content(self.data.get_all_tasks_without("labels"))
                                self.current_order_with_args = ["standard", self.content]
                            else:
                                self.update_content(self.data.get_data_with_label(labels[1][int(input)-1]))
                                self.current_order_with_args = ["standard", self.content]
                        except:
                            pass
                        self.beautify_output()
                    case "i":
                        input = self.get_input_string(instructions["display"]["2"]["importance"], 1, r"[LlMmHhNn]")
                        match input.lower():
                            case "n":
                                self.update_content(self.data.get_data_of_importance("None"))
                            case "l":
                                self.update_content(self.data.get_data_of_importance("low"))
                            case "m":
                                self.update_content(self.data.get_data_of_importance("medium"))
                            case "h":
                                self.update_content(self.data.get_data_of_importance("high"))
                        self.current_order_with_args = ["standard", self.content]
                        self.beautify_output()
            case "X" | "x":
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
            case "KEY_RESIZE":
                self.kill_scr()
                ScreenManager(self.file, self.content, self.content_beautified)

    def get_input(self) -> str:
        try:
            return self.screen.getkey()
        except:
            return None

    def kill_scr(self) -> None:
        self.running = False
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def update_content(self, content: dict, task_hash="") -> None:
        """
        A method that updates both content and content_beautified at the same time for the user
        """
        self.content = content
        self.content_beautified = self.data.display_task_details(content, task_hash)

    def get_coordinates_for_centered_text(self, text: str) -> tuple[int]:
        height, width = self.window_dimensions[0]
        start_y = height // 2
        start_x = (width // 2) - (len(text) // 2)
        return start_x, start_y-1

    def get_coordinates_for_centered_pad(self, win: int) -> list[int]:
        """
        Function returns top-left and bottom-right corner of pad so that it is centered (if possible)
        Should only center pop-ups like the help one
        """
        start_coords = [2, 0]
        end_coords = list(self.main_end_x_y)
        if self.window_dimensions[0][0]-3 > self.window_dimensions[win][0]:
            start_coords[0] = (self.window_dimensions[0][0]-1)//2 - self.window_dimensions[win][0]//2 + start_coords[0]
            end_coords[0] = start_coords[0] + self.window_dimensions[win][0]
        if self.window_dimensions[0][1] > self.window_dimensions[win][1]:
            start_coords[1] = (self.window_dimensions[0][1]-1)//2-self.window_dimensions[win][1]//2
            end_coords[1] = start_coords[1] + self.window_dimensions[win][1] - 1
        start_coords.extend(end_coords)
        return start_coords

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
            start_x, start_y, end_x, end_y = self.get_coordinates_for_centered_pad(win)
            self.windows[win].refresh(self.scroll_x, self.scroll_y, start_x, start_y, end_x, end_y)

    def beautify_output(self, start_y=1, start_x=1) -> None:
        self.windows[1].clear()
        for line, importance in self.content_beautified:
            if importance != "None":
                self.output_text_to_window(1, line, start_y, start_x, self.__dict__[f"{importance}_importance"])
            else:
                self.output_text_to_window(1, line, start_y, start_x)
            start_y += 1

    def make_message_fit_width(self, message: str, width: int) -> str:
        paras = ["dbc71b7fc9e348da85ae5e095bd80855" if i == "" else i for i in message.splitlines()] # using a uuid4 here to preserve the custom linespacing via `\n`
        lines = [" "+j for i in paras for j in wrap(i,width)]
        return "\n".join(["" if i==" dbc71b7fc9e348da85ae5e095bd80855" else i for i in lines])

    def get_input_string(self, message: str, input_length: int, p_regex=None) -> str:
        regex = r"[\S\s]" if p_regex==None else p_regex
        message = self.make_message_fit_width(message, self.window_dimensions[0][1]-2)
        message_is_updated = False
        while True:
            # Init new window and change some settings
            win = curses.newwin(self.main_end_x_y[0]-1, self.main_end_x_y[1]+1, self.main_start_x_y[0], self.main_start_x_y[1])
            curses.echo()
            curses.curs_set(1)

            # Output info and get input
            win.addstr(1, 0, message)
            height_of_msg = len(message.splitlines())+1
            win.box()
            win.refresh()
            input = win.getstr(height_of_msg, 1, input_length).decode('utf-8', 'backslashreplace')

            # Clean up the window and settings changed
            del win
            curses.noecho()
            curses.curs_set(0)
            self.windows[1].refresh(self.scroll_x, self.scroll_y,
                                    self.main_start_x_y[0], self.main_start_x_y[1],
                                    self.main_end_x_y[0], self.main_end_x_y[1])
            if match(regex, input):
                break
            elif not message_is_updated:
                message_is_updated = True
                message = wrong_input_message + message
        return input

def main(cwd: str) -> None:
    filepath = f"{cwd}\\data.json"
    if exists(filepath):
        file = FileManager(filepath)
    else:
        file = FileManager.for_new_file(filepath)
    screen = ScreenManager(file)
    print("Do backup stuff here")
    exit()

if __name__ == "__main__":
    from os import getcwd
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="ToDo",
                            description="A minimalistic terminal-based todo-manager written with curses.",
                            epilog="Have fun using it.")

    args = parser.parse_args()

    main(getcwd())
