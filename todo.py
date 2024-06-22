from curses import newwin, newpad, initscr, init_pair, color_pair, start_color, curs_set, cbreak, noecho, nocbreak, echo, endwin, COLOR_BLACK, COLOR_BLUE, COLOR_GREEN, COLOR_RED, A_UNDERLINE, A_NORMAL
from time import sleep
from sys import exit
from re import match
from textwrap import wrap
from os.path import exists
from help import FOOTER_TEXT, HELP_MESSAGE, INSTRUCTIONS, WRONG_INPUT_MESSAGE, CHOICE_LEN, NAME_LEN, DESCRIPTION_LEN, INDEX_LEN, MULTIINDEX_LEN, STEP_IDX_LEN, MULTIINDEX_REGEX, INDEX_REGEX, NAME_REGEX, STEP_IDX_REGEX
from FileManager import FileManager, DataManager

class ScreenManager:
    def __init__(self, file: str, content=None, content_beautified=None) -> None:
        self.screen = initscr()
        self.file = file
        self.data = DataManager(self.file.data)
        self.running = True

        # DETERMINE THE SIZE OF THE MAIN PAD
        y, x = self.get_main_dimensions()

        help_lines = HELP_MESSAGE.split("\n")
        self.window_dimensions = [self.screen.getmaxyx(),
                                  (y, x),
                                  (len(help_lines)+1, max(len(line) for line in help_lines)+1)]
        self.windows = [self.screen, # footer
                        newpad(self.window_dimensions[1][0], self.window_dimensions[1][1]), # main todo
                        newpad(self.window_dimensions[2][0], self.window_dimensions[2][1])] # help message popup

        self.scroll_y, self.scroll_x = 0, 0
        self.last_scroll_pos_main_scr = (0, 0)
        self.main_start_x_y = (2, 0)
        self.main_end_x_y = (self.window_dimensions[0][0]-2, self.window_dimensions[0][1]-1)
        self.active_window = 1
        self.content = self.data.get_all_data() if content==None else content
        self.content_beautified = self.data.display_task_details(self.content) if content_beautified==None else content_beautified
        self.current_order_with_args = ["standard", self.content] # other would be group, label and importance
        self.opened_task_hash = ""
        self.current_filter = ["self.data.get_all_data", ()]

        # COLOR STUFF FOR IMPORTANCE
        start_color()
        init_pair(1, COLOR_GREEN, COLOR_BLACK)
        init_pair(2, COLOR_BLUE, COLOR_BLACK)
        init_pair(3, COLOR_RED, COLOR_BLACK)
        self.low_importance = color_pair(1)
        self.medium_importance = color_pair(2)
        self.high_importance = color_pair(3)

        # ADJUST SETTINGS
        curs_set(0)
        cbreak()
        noecho()
        self.screen.nodelay(True)
        self.screen.keypad(True)

        # CLEAR SCREEN AND RUN IT
        self.screen.clear()
        self.screen.refresh()
        self.run_scr()

    def run_scr(self) -> None:
        headline = "ToDo Manager"
        self.output_text_to_window(0, self.space_footer_text(FOOTER_TEXT), self.window_dimensions[0][0]-1, 0)
        y, _ = self.get_coordinates_for_centered_text(headline)
        self.output_text_to_window(0, headline, 1, y, A_UNDERLINE)
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
                self.show_procedure()
            case "A" | "a":
                self.add_procedure()
            case "C" | "c":
                self.change_procedure()
            case "F" | "f":
                self.filter_procedure()
            case "D" | "d":
                self.delete_procedure()
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
                    self.output_text_to_window(2, HELP_MESSAGE, 0, 0)
            case "Q" | "q":
                self.file.update_data(self.data.data)
                self.kill_scr()
            case "KEY_RESIZE":
                self.kill_scr()
                ScreenManager(self.file, self.content, self.content_beautified)

    def show_procedure(self) -> None:
        index = self.get_input_string(INSTRUCTIONS["show"], INDEX_LEN, INDEX_REGEX)
        if index=="0":
            self.opened_task_hash = ""
            self.current_order_with_args = ["standard", self.content]
        else:
            self.opened_task_hash = self.data.get_hash_of_task_with_index(int(index), self.current_order_with_args)
        self.update_content(self.content)
        self.beautify_output()

    def add_procedure(self) -> None:
        input = self.get_input_string(INSTRUCTIONS["add"]["1"], CHOICE_LEN, r"[TtSs]")
        match input.lower():
            case "t":
                data = {}
                data["name"] = self.get_input_string(INSTRUCTIONS["add"]["task"][0], NAME_LEN, NAME_REGEX)
                data["description"] = self.get_input_string(INSTRUCTIONS["add"]["task"][1], DESCRIPTION_LEN)
                input = self.get_input_string(INSTRUCTIONS["add"]["task"][2], CHOICE_LEN, r"[LlMmHhNn]")
                match input.lower():
                    case "n":
                        data["importance"] = "None"
                    case "l":
                        data["importance"] = "low"
                    case "m":
                        data["importance"] = "medium"
                    case "h":
                        data["importance"] = "high"
                data["steps"] = {}
                input = self.get_input_string(INSTRUCTIONS["add"]["task"][3][0], CHOICE_LEN, r"[EeNn]")
                match input.lower():
                    case "e":
                        labels = self.data.get_labels()
                        index = self.get_input_string(INSTRUCTIONS["add"]["task"][3][1] + labels[0], MULTIINDEX_LEN, MULTIINDEX_REGEX)
                        data["labels"] = self.get_all_possible_items(index, labels)
                    case "n":
                        name = self.get_input_string(INSTRUCTIONS["add"]["task"][3][2], NAME_LEN, NAME_REGEX)
                        data["labels"] = [name]
                input = self.get_input_string(INSTRUCTIONS["add"]["task"][4][0], CHOICE_LEN, r"[EeNn]")
                match input.lower():
                    case "e":
                        groups = self.data.get_groups()
                        index = self.get_input_string(INSTRUCTIONS["add"]["task"][4][1] + groups[0], MULTIINDEX_LEN, MULTIINDEX_REGEX)
                        data["groups"] = self.get_all_possible_items(index, groups)
                    case "n":
                        name = self.get_input_string(INSTRUCTIONS["add"]["task"][4][2], NAME_LEN, NAME_REGEX)
                        data["groups"] = [name]
                self.data.modify_task(data, True)
            case "s":
                data = {}
                idx = self.get_input_string(INSTRUCTIONS["add"]["step"][0], INDEX_LEN, INDEX_REGEX)
                task_hash = self.data.get_hash_of_task_with_index(int(idx) , self.current_order_with_args)
                if not idx=="0" and task_hash!="":
                    data["name"] = self.get_input_string(INSTRUCTIONS["add"]["step"][1], NAME_LEN, NAME_REGEX)
                    data["description"] = self.get_input_string(INSTRUCTIONS["add"]["step"][2], DESCRIPTION_LEN)
                    input = self.get_input_string(INSTRUCTIONS["add"]["step"][3], CHOICE_LEN, r"[LlMmHhNn]")
                    match input.lower():
                        case "n":
                            data["importance"] = "None"
                        case "l":
                            data["importance"] = "low"
                        case "m":
                            data["importance"] = "medium"
                        case "h":
                            data["importance"] = "high"
                    self.data.add_step(task_hash, data)
        self.update_content(eval(self.current_filter[0])(self.current_filter[1]))
        self.file.update_data(self.data.data)
        self.update_main_dimensions()
        self.beautify_output()

    def change_procedure(self) -> None:
        input = self.get_input_string(INSTRUCTIONS["change"]["1"], CHOICE_LEN, r"[TtSsOo]")
        match input.lower():
            case "t":
                input = self.get_input_string(INSTRUCTIONS["change"]["task"]["1"], MULTIINDEX_LEN, MULTIINDEX_REGEX)
                idx = [int(i)-1 for i in sorted(set(input.replace(" ", "").split(",")))]
                task_idx = self.get_input_string(INSTRUCTIONS["change"]["task"]["task_hash"], INDEX_LEN, INDEX_REGEX)
                task_hash = self.data.get_hash_of_task_with_index(int(task_idx), self.current_order_with_args)
                if task_idx == "0" or task_hash == "": return
                data = {}
                if 0 in idx:
                    data["name"] = self.get_input_string(INSTRUCTIONS["change"]["task"]["2"][0], NAME_LEN, NAME_REGEX)
                if 1 in idx:
                    data["description"] = self.get_input_string(INSTRUCTIONS["change"]["task"]["2"][1], DESCRIPTION_LEN)
                if 2 in idx:
                    input = self.get_input_string(INSTRUCTIONS["change"]["task"]["2"][2], CHOICE_LEN, r"[LlMmHhNn]")
                    match input.lower():
                        case "n":
                            data["importance"] = "None"
                        case "l":
                            data["importance"] = "low"
                        case "m":
                            data["importance"] = "medium"
                        case "h":
                            data["importance"] = "high"
                if 3 in idx:
                    input = self.get_input_string(INSTRUCTIONS["change"]["task"]["2"][3][0], CHOICE_LEN, r"[EeNn]")
                    match input.lower():
                        case "e":
                            labels = self.data.get_labels()
                            index = self.get_input_string(INSTRUCTIONS["change"]["task"]["2"][3][1] + labels[0], MULTIINDEX_LEN, MULTIINDEX_REGEX)
                            data["labels"] = self.get_all_possible_items(index, labels)
                        case "n":
                            name = self.get_input_string(INSTRUCTIONS["change"]["task"]["2"][3][2], NAME_LEN, NAME_REGEX)
                            self.data.add_label(task_hash, name)
                if 4 in idx:
                    input = self.get_input_string(INSTRUCTIONS["change"]["task"]["2"][4][0], CHOICE_LEN, r"[EeNn]")
                    match input.lower():
                        case "e":
                            groups = self.data.get_groups()
                            index = self.get_input_string(INSTRUCTIONS["change"]["task"]["2"][4][1] + groups[0], MULTIINDEX_LEN, MULTIINDEX_REGEX)
                            data["groups"] = self.get_all_possible_items(index, groups)
                        case "n":
                            name = self.get_input_string(INSTRUCTIONS["change"]["task"]["2"][4][2], NAME_LEN, NAME_REGEX)
                            self.data.add_group(task_hash, name)
                self.data.modify_task(data, False, task_hash)
            case "s":
                input = self.get_input_string(INSTRUCTIONS["change"]["step"]["1"], MULTIINDEX_LEN, MULTIINDEX_REGEX)
                idx = [int(i)-1 for i in sorted(set(input.replace(" ", "").split(",")))]
                data = {}
                task_step_idx = self.get_input_string(INSTRUCTIONS["change"]["step"]["2"][0], STEP_IDX_LEN, STEP_IDX_REGEX)
                task_hash, step_hash = self.data.get_hash_of_step_with_index(task_step_idx, self.current_order_with_args)
                if not idx=="0" and task_hash!="" and step_hash!="":
                    if 0 in idx:
                        data["name"] = self.get_input_string(INSTRUCTIONS["change"]["step"]["2"][1], NAME_LEN, NAME_REGEX)
                    if 1 in idx:
                        data["description"] = self.get_input_string(INSTRUCTIONS["change"]["step"]["2"][2], DESCRIPTION_LEN)
                    if 2 in idx:
                        input = self.get_input_string(INSTRUCTIONS["change"]["step"]["2"][3], CHOICE_LEN, r"[LlMmHhNn]")
                        match input.lower():
                            case "n":
                                data["importance"] = "None"
                            case "l":
                                data["importance"] = "low"
                            case "m":
                                data["importance"] = "medium"
                            case "h":
                                data["importance"] = "high"
                    self.data.change_data_step(task_hash, step_hash, data)
            case "o":
                input = self.get_input_string(INSTRUCTIONS["change"]["order"]["what"], CHOICE_LEN, r"[TtSs]")
                match input.lower():
                    case "t":
                        args = [self.get_input_string(INSTRUCTIONS["change"]["order"]["tasks"], CHOICE_LEN, r"[IiNn]")]
                    case "s":
                        index = self.get_input_string(INSTRUCTIONS["change"]["order"]["steps"], INDEX_LEN, INDEX_REGEX)
                        task_hash = self.data.get_hash_of_task_with_index(int(index), self.current_order_with_args)
                        if task_hash=="": return
                        type_of_reorder = self.get_input_string(INSTRUCTIONS["change"]["order"]["order_type"], CHOICE_LEN, r"[IiNn]")
                        args = [type_of_reorder, task_hash]
                try:
                    self.call_order_methods(input.lower(), args)
                except:
                    return
        self.update_content(eval(self.current_filter[0])(self.current_filter[1]))
        self.file.update_data(self.data.data)
        self.update_main_dimensions()
        self.beautify_output()

    def filter_procedure(self) -> None:
        input = self.get_input_string(INSTRUCTIONS["display"]["1"], CHOICE_LEN, r"[GgLlIi0]")
        match input.lower():
            case "0":
                self.current_filter = ["self.data.get_all_data", ()]
                self.update_content(self.data.get_all_data())
                self.current_order_with_args = ["standard", self.content]
                self.data.change_current_order_to(self.current_order_with_args)
                self.beautify_output()
            case "g":
                groups = self.data.get_groups()
                index = self.get_input_string(INSTRUCTIONS["display"]["group"] + groups[0], INDEX_LEN, INDEX_REGEX)
                try:
                    if index == "0":
                        self.current_filter = ["self.data.get_all_tasks_without", ("groups")]
                        self.update_content(self.data.get_all_tasks_without("groups"))
                        self.current_order_with_args = ["standard", self.content]
                        self.data.change_current_order_to(self.current_order_with_args)
                    else:
                        self.current_filter = ["self.data.get_data_of_group", (list(self.data.data["order of tasks in group"].keys())[int(index)-1])]
                        self.update_content(self.data.get_data_of_group(list(self.data.data["order of tasks in group"].keys())[int(index)-1]))
                        self.current_order_with_args = ["group", groups[1][int(index)-1]]
                        self.data.change_current_order_to(self.current_order_with_args)
                except:
                    pass
                self.beautify_output()
            case "l":
                labels = self.data.get_labels()
                index = self.get_input_string(INSTRUCTIONS["display"]["label"] + labels[0], INDEX_LEN, INDEX_REGEX)
                try:
                    if index == "0":
                        self.current_filter = ["self.data.get_all_tasks_without", ("labels")]
                        self.update_content(self.data.get_all_tasks_without("labels"))
                        self.current_order_with_args = ["standard", self.content]
                    else:
                        self.current_filter = ["self.data.get_data_with_label", (labels[1][int(index)-1])]
                        self.update_content(self.data.get_data_with_label(labels[1][int(index)-1]))
                        self.current_order_with_args = ["standard", self.content]
                except:
                    pass
                self.beautify_output()
            case "i":
                input = self.get_input_string(INSTRUCTIONS["display"]["importance"], CHOICE_LEN, r"[LlMmHhNn]")
                match input.lower():
                    case "n":
                        self.current_filter = ["self.data.get_data_of_importance", ("None")]
                        self.update_content(self.data.get_data_of_importance("None"))
                    case "l":
                        self.current_filter = ["self.data.get_data_of_importance", ("low")]
                        self.update_content(self.data.get_data_of_importance("low"))
                    case "m":
                        self.current_filter = ["self.data.get_data_of_importance", ("medium")]
                        self.update_content(self.data.get_data_of_importance("medium"))
                    case "h":
                        self.current_filter = ["self.data.get_data_of_importance", ("high")]
                        self.update_content(self.data.get_data_of_importance("high"))
                self.current_order_with_args = ["standard", self.content]
                self.beautify_output()

    def delete_procedure(self) -> None:
        data_to_delete = [] # 0 -> type, 1 -> hash (task|step) or name (label|group)
        input = self.get_input_string(INSTRUCTIONS["delete"]["1"], CHOICE_LEN, r"[TtSsLlGg]")
        match input.lower():
            case "t":
                index = self.get_input_string(INSTRUCTIONS["delete"]["task"], INDEX_LEN, INDEX_REGEX)
                data_to_delete = ["task", self.data.get_hash_of_task_with_index(int(index), self.current_order_with_args)]
            case "s":
                index = self.get_input_string(INSTRUCTIONS["delete"]["step"], STEP_IDX_LEN, STEP_IDX_REGEX)
                data_to_delete = ["step", self.data.get_hash_of_step_with_index(index, self.current_order_with_args)]
            case "l":
                labels = self.data.get_labels()
                index = self.get_input_string(INSTRUCTIONS["delete"]["label"] + labels[0], INDEX_LEN, INDEX_REGEX)
                data_to_delete = ["label", labels[1][int(index)-1]]
            case "g":
                groups = self.data.get_groups()
                index = self.get_input_string(INSTRUCTIONS["delete"]["group"] + groups[0], INDEX_LEN, INDEX_REGEX)
                data_to_delete = ["group", groups[1][int(index)-1]]
        input = self.get_input_string(INSTRUCTIONS["delete"]["validation"], CHOICE_LEN, r"[YyNn]")
        match input.lower():
            case "y":
                self.data.do_deletion(data_to_delete)
                self.data.validata_data_and_update_necessary(data_to_delete)
                self.update_content(self.data.get_all_data())
                self.beautify_output()
                self.file.update_data(self.data.data)
            case "n":
                pass

    def call_order_methods(self, items_to_reorder: str, args: list[str]) -> None:
        match args[0].lower():
            case "i":
                input = self.get_input_string(INSTRUCTIONS["change"]["order"]["insert"], MULTIINDEX_LEN, r"^\d+,\s*\d+$")
                old_idx, new_idx = input.replace(" ", "").split(",")
                match items_to_reorder:
                    case "t":
                        task_hash = self.data.get_hash_of_task_with_index(int(old_idx), self.current_order_with_args)
                        if self.current_order_with_args[0]=="group":
                            self.data.change_order_tasks_group_insertion(self.current_order_with_args[1], task_hash, int(new_idx)-1)
                        elif self.current_order_with_args[0]=="standard":
                            self.data.change_order_tasks_global_insertion(task_hash, int(new_idx)-1)
                    case "s":
                        step_hash = self.data.get_hash_of_step_with_task_hash_and_idx(args[1], old_idx, self.current_order_with_args)
                        if args[1]=="" or step_hash=="": return
                        self.data.change_order_of_steps_insertion(args[1], step_hash, int(new_idx)-1)
            case "n":
                new_order = self.get_input_new_order(INSTRUCTIONS["change"]["order"]["new order"], items_to_reorder, args)
                if new_order==None: return
                match items_to_reorder:
                    case "t":
                        if self.current_order_with_args[0]=="group":
                            self.data.change_group_order_of_tasks(self.current_order_with_args[1], new_order)
                        elif self.current_order_with_args[0]=="standard":
                            self.data.change_global_order_of_tasks(new_order)
                    case "s":
                        self.data.change_order_of_steps(args[1], new_order)

    def get_input(self) -> str:
        try:
            return self.screen.getkey()
        except:
            return None

    def get_input_string(self, p_message: str, input_length: int, p_regex=None) -> str:
        regex = r"[\S\s]*" if p_regex==None else p_regex
        message = self.make_message_fit_width(p_message, self.window_dimensions[0][1]-2)
        height_of_msg = len(message.splitlines())+1
        message_is_updated = False
        while True:
            # Init new window and change some settings
            win = newwin(self.main_end_x_y[0]-1, self.main_end_x_y[1]+1, self.main_start_x_y[0], self.main_start_x_y[1])
            echo()
            curs_set(1)

            # Output info and get input
            win.addstr(1, 0, message)
            win.box()
            win.refresh()
            input = win.getstr(height_of_msg, 1, input_length).decode('utf-8', 'backslashreplace')

            # Clean up the window and settings changed
            del win
            noecho()
            curs_set(0)
            self.windows[1].refresh(self.scroll_x, self.scroll_y,
                                    self.main_start_x_y[0], self.main_start_x_y[1],
                                    self.main_end_x_y[0], self.main_end_x_y[1])
            if match(regex, input):
                break
            elif not message_is_updated:
                message_is_updated = True
                message = self.make_message_fit_width(WRONG_INPUT_MESSAGE + p_message, self.window_dimensions[0][1]-2)
                height_of_msg = len(message.splitlines())+1
        return input

    def get_input_new_order(self, p_message: str, items_to_reorder: str, args: list[str]) -> None:
        message = self.make_message_fit_width(p_message, self.window_dimensions[0][1]-2)
        height_of_msg = len(message.splitlines())+1
        message_is_updated = False
        if items_to_reorder == "t" and self.current_order_with_args[0] == "standard":
            content = self.content
        elif items_to_reorder == "t" and self.current_order_with_args[0] == "group":
            content = self.data.data["order of tasks in group"][self.current_order_with_args[1]]
        elif items_to_reorder == "s":
            content = self.data.data["tasks"][args[1]]["steps"]
        input_length = len("".join(f"{i+1}, " for i in range(len(content))))
        while True:
            # Init new window and change some settings
            win = newwin(self.main_end_x_y[0]-1, self.main_end_x_y[1]+1, self.main_start_x_y[0], self.main_start_x_y[1])
            echo()
            curs_set(1)

            # Output info and get input
            win.addstr(1, 0, message)
            win.box()
            win.refresh()
            input = win.getstr(height_of_msg, 1, input_length).decode('utf-8', 'backslashreplace')

            # Clean up the window and settings changed
            del win
            noecho()
            curs_set(0)
            self.windows[1].refresh(self.scroll_x, self.scroll_y,
                                    self.main_start_x_y[0], self.main_start_x_y[1],
                                    self.main_end_x_y[0], self.main_end_x_y[1])

            all_indices_given = False
            if match(r"^\d+(,\s*\d+)*$", input):
                new_order_idx = [int(i)-1 for i in input.replace(" ", "").split(",")]
                all_indices_given = all(i in range(len(content)+1) for i in new_order_idx)

            if all_indices_given:
                break
            elif input.replace(" ", "")=="0":
                return
            elif not message_is_updated:
                message_is_updated = True
                message = self.make_message_fit_width("You need to provide all indices and separate them by a `,`!!!\n\n" + p_message, self.window_dimensions[0][1]-2)
                height_of_msg = len(message.splitlines())+1

        if items_to_reorder == "t" and self.current_order_with_args[0] == "group":
            new_order = [self.data.get_hash_of_task_with_index(idx+1, self.current_order_with_args) for idx in new_order_idx]
        elif items_to_reorder == "t" and self.current_order_with_args[0] == "standard":
            new_order = {self.data.get_hash_of_task_with_index(i+1, self.current_order_with_args): idx for idx, i in enumerate(new_order_idx)}
        elif items_to_reorder == "s":
            new_order = {self.data.get_hash_of_step_with_task_hash_and_idx(args[1], f"{i+1}", self.current_order_with_args): idx for idx, i in enumerate(new_order_idx)}

        return new_order

    def kill_scr(self) -> None:
        self.running = False
        nocbreak()
        self.screen.keypad(False)
        echo()
        endwin()

    # Update attributes automaticly
    def update_main_dimensions(self) -> None:
        y, x = self.get_main_dimensions()
        del self.window_dimensions[1]
        self.window_dimensions.insert(1, (y, x))
        del self.windows[1]
        self.windows.insert(1, newpad(self.window_dimensions[1][0], self.window_dimensions[1][1]))

    def update_content(self, content: dict) -> None:
        """
        A method that updates both content and content_beautified at the same time for the user
        """
        self.content = content
        self.content_beautified = self.data.display_task_details(content, self.opened_task_hash)

    # Some getter methods
    def get_main_dimensions(self) -> tuple:
        try:
            max_dimensions = self.data.get_longest_entry_beautified()
        except ValueError:
            y, x = self.screen.getmaxyx()
            return y-3, x
        if max_dimensions[0]+2 > self.screen.getmaxyx()[0]-3:
            y = max_dimensions[0]+2
        else:
            y = self.screen.getmaxyx()[0]-3
        if max_dimensions[1]+2 > self.screen.getmaxyx()[1]:
            x = max_dimensions[1]+2
        else:
            x = self.screen.getmaxyx()[1]
        return y, x

    @staticmethod
    def get_all_possible_items(idx: list, items: list) -> list:
        output = []
        for i in idx.replace(" ", "").split(","):
            try:
                if int(i)==0: continue
                output.append(items[1][int(i)-1])
            except:
                pass
        return output

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

    # Text manipulation and output methods
    def space_footer_text(self, footer_text: list) -> str:
        char_amount = len("".join(footer_text))
        width = (self.window_dimensions[0][1]-1 - char_amount) // (len(footer_text) - 1)
        return "".join([arg + " "*width for arg in footer_text]).strip()

    def output_text_to_window(self, win: int, text: str, y=0, x=0, *args) -> None:
        error_msg = "Couldn't print string to window."
        attributes = A_NORMAL
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

def main(cwd: str, flags) -> None:
    if flags.manualBackup:
        filepath = f"{cwd}\\data.json"
        if exists(filepath):
            file = FileManager(filepath)
        else:
            file = FileManager.for_new_file(filepath)
        file.write_backup()
        exit()

    if flags.overwriteMainFile:
        filepath = f"{cwd}\\data.json"
        if exists(filepath):
            file = FileManager(filepath)
        else:
            file = FileManager.for_new_file(filepath)
        file.overwrite_main_data_with_backup()
        exit()

    if flags.useBackup:
        filepath = f"{cwd}\\data.backup"
    else:
        filepath = f"{cwd}\\data.json"
    filepath = f"{cwd}\\data.json"
    if exists(filepath):
        file = FileManager(filepath)
    else:
        file = FileManager.for_new_file(filepath)
    file.write_backup()
    screen = ScreenManager(file)
    print("Thank you for using ToDo. If there is any issue with the project open an issue on github [ https://github.com/Testspieler09/todo ]")
    exit()

if __name__ == "__main__":
    from sys import argv
    from os.path import split
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="ToDo",
                            description="A minimalistic terminal-based todo-manager written with curses.",
                            epilog="Have fun using it.")

    parser.add_argument("-ub", "--useBackup",
                        default=False,
                        nargs="?",
                        const=False,
                        type=bool,
                        help="Use the backup data (e.g. if something went wrong with the main file).")
    parser.add_argument("-om", "--overwriteMainFile",
                        default=False,
                        nargs="?",
                        const=False,
                        type=bool,
                        help="Overwrite the data of the main file with the backup data.")
    parser.add_argument("-mb", "--manualBackup",
                        default=False,
                        nargs="?",
                        const=False,
                        type=bool,
                        help="Do a manual backup.")

    args = parser.parse_args()

    main(split(argv[0])[0], args)
