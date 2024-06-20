from os.path import exists, dirname, split, splitext
from os import chdir
from sys import argv
from json import load, dumps
from uuid import uuid4

class FileManager:
    """
    A class that manages a JSON file and the respective backup file
    """
    def __init__(self, path_to_file: str) -> None:
        if not exists(path_to_file): raise Exception("File not found in given directory.")
        self.path_to_file: str = path_to_file
        self.backup_path: str = splitext(path_to_file)[0] + ".backup"
        self.data: dict = self.read_file_data()

    @classmethod
    def for_new_file(cls, path_with_filename_and_extension: str) -> None:
        """
        Alternative constructor for when the JSON file doesn't exist yet
        """
        with open(path_with_filename_and_extension, "w") as f:
            f.write('{"order of tasks in group":{},'
                      '"tasks":{}}')
        return cls(path_with_filename_and_extension)

    def read_file_data(self) -> dict:
        """
        Read JSON file and move contents into dictionary
        """
        with open(self.path_to_file, "r") as f:
            return load(f)

    def update_data(self, data: dict) -> None:
        """
        Overwrite old data with new data
        """
        self.data = data
        with open(self.path_to_file, "w") as f:
            f.write(str(dumps(self.data)))

    def write_backup(self) -> None:
        with open(self.backup_path, "w") as f:
            f.write(str(dumps(self.data)))

    def load_backup_data(self) -> None:
        """
        Load backup data as the dict
        """
        with open(self.backup_path, "r") as f:
            self.data = load(f)

    def overwrite_main_data_with_backup(self) -> None:
        with open(self.backup_path, "r") as f:
            update_data(load(f))

class DataManager:
    """
    A class that manages a dict that was created from a JSON file of the following scheme:
    {
        "order of tasks in group": {"group name": ["hash of first task", "..."]},
        "tasks": {
            "task_hash": {
                "name": str,
                "description": str,
                "steps": {
                    "name": str,
                    "description": str,
                    "importance": str,
                    "index": int
                },
                "importance": str,
                "index": int,
                "labels": list,
                "groups": list
            }
        }
    }
    """
    def __init__(self, data: dict):
        self.data: dict = data
        self.TAB_INDENT = 8
        self.current_order = ["standard", ""]

    def change_current_order_to(self, order: str) -> None:
        print("current_order changed", order)
        self.current_order = order

    def gen_unique_hash(self) -> str:
        """
        Generates the task hash
        """
        return uuid4().hex

    # ADDING, CHANGING AND REMOVING DATA
    def modify_task(self, data: dict, is_new_task=False, task_hash="") -> None:
        if is_new_task:
            id = self.gen_unique_hash()
            data["index"] = len(self.data["tasks"])
            self.update_groups(id, data["groups"])
            self.data["tasks"].update({id: data})
        else:
            try:
                self.data["tasks"][task_hash].update(data)
            except:
                pass

    def add_step(self, task_hash: str, data: dict) -> None:
        id = self.gen_unique_hash()
        data["index"] = len(self.data["tasks"][task_hash]["steps"])
        self.data["tasks"][task_hash]["steps"].update({id: data})

    def add_label(self, task_hash: str, label: str) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        self.data["tasks"][task_hash]["labels"].append(label)

    def add_group(self, task_hash: str, group: str) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        self.data["tasks"][task_hash]["groups"].append(group)
        try:
            self.data["order of tasks in group"][group].append(task_hash)
        except:
            self.data["order of tasks in group"].update({group: [task_hash]})

    def change_data_step(self, task_hash: str, step_hash: str,data: dict) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        self.data["tasks"][task_hash]["steps"][step_hash].update(data)

    def change_order_tasks_global_insertion(self, task_hash: str, new_idx: int) -> None:
        pass

    def change_order_of_steps_insertion(self, task_hash: str, step_hash: str, new_idx: int) -> None:
        pass

    def change_order_tasks_group_insertion(self, group_name: str, task_hash: str, new_idx: int) -> None:
        pass

    def change_global_order_of_tasks(self, new_order: dict) -> None:
        # new order consist of task_hash: number
        for hash, value in new_order.items():
            if hash not in self.data["tasks"].keys(): continue
            self.data["tasks"][hash]["index"] = value

    def change_order_of_steps(self, task_hash: str, new_order: dict) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        for hash, value in new_order.items():
            if hash not in self.data["tasks"][task_hash].keys(): continue
            self.data["tasks"][task_hash][hash]["index"] = value

    def change_group_order_of_tasks(self, group_name: str, order: list[str]) -> None:
        if group_name not in self.data["order of tasks in group"]: return
        self.data["order of tasks in group"][group_name] = order

    def do_deletion(self, data_to_delete: list) -> None:
        match data_to_delete[0]:
            case "task":
                self.delete_task(data_to_delete[1])
            case "step":
                self.delete_step(data_to_delete[1][0], data_to_delete[1][1])
            case "label":
                self.delete_label(data_to_delete[1])
            case "group":
                self.delete_group(data_to_delete[1])

    def delete_task(self, task_hash: str) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        del self.data["tasks"][task_hash]

    def delete_step(self, task_hash: str, step_hash: str) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        if step_hash not in self.data["tasks"][task_hash]["steps"].keys(): return
        del self.data["tasks"][task_hash]["steps"][step_hash]

    def delete_label(self, label: str) -> None:
        for value in self.data["tasks"].values():
            if label in value["labels"]: value["labels"].remove(label)

    def delete_group(self, group_name: str) -> None:
        hashes = self.data["order of tasks in group"].pop(group_name, None)
        if hashes == None: return
        for hash in hashes:
            self.data["tasks"][hash]["groups"].remove(group_name)

    # GET DATA (MAINLY FOR FILTER FUNCTION)
    def get_all_tasks_without(self, key: str) -> dict:
        data = {}
        for i in self.data["tasks"].items():
            if not i[1][key]: data.update({i[0]: i[1]})
        return data

    def get_hash_of_task_with_index(self, idx: int, type_of_idx_with_args: list) -> str:
        hash = ""
        match type_of_idx_with_args[0]:
            case "standard":
                data = self.data["tasks"].items() if type_of_idx_with_args[1] == None else type_of_idx_with_args[1].items()
                sorted_data = dict(sorted(data, key=lambda item: item[1]['index']))
                for index, key in enumerate(sorted_data):
                    if index == idx-1: return key
            case "group":
                try:
                    hash = self.data["order of tasks in group"][type_of_idx_with_args[1]][idx-1]
                except:
                    pass
        return hash

    def get_hash_of_step_with_index(self, idx: str, type_of_idx_with_args: list) -> tuple[str]:
        task_idx, step_idx = idx.split(".")
        task_hash = self.get_hash_of_task_with_index(int(task_idx), type_of_idx_with_args)
        if task_hash == "": return "", ""
        step_hash = ""
        sorted_data = dict(sorted(self.data["tasks"][task_hash]["steps"].items(), key=lambda item: item[1]["index"]))
        for idx, step in enumerate(sorted_data):
            if idx == int(step_idx)-1: step_hash = step
        return (task_hash, step_hash)

    def get_hash_of_step_with_task_hash_and_idx(self, task_hash: str, step_idx: str, type_of_idx_with_args: list) -> tuple[str]:
        if task_hash == "": return "", ""
        step_hash = ""
        sorted_data = dict(sorted(self.data["tasks"][task_hash]["steps"].items(), key=lambda item: item[1]["index"]))
        for idx, step in enumerate(sorted_data):
            if idx == int(step_idx)-1: step_hash = step
        return step_hash

    def get_labels(self) -> tuple[str | list]:
        output = "\n"
        labels_names = sorted(list(set((i for j in self.data["tasks"].values() for i in j["labels"]))))
        for idx, name in enumerate(labels_names):
            output += f"{idx+1}. {name} | "
        if output=="\n": return "\nThere are no labels defined. Input any number to continue"
        return output, labels_names

    def get_data_with_label(self, label: str) -> dict | None:
        dictionary = {}
        for key, values in self.data["tasks"].items():
            if label in values["labels"]: dictionary.update({key: values})
        return dictionary

    def get_groups(self) -> str:
        group_names = "\n"
        list_of_groups = []
        for idx, name in enumerate(self.data["order of tasks in group"].keys()):
            group_names += f"{idx+1}. {name} | "
            list_of_groups.append(name)
        if group_names=="\n": return "\nThere are no groups defined. Input any number to continue."
        return group_names, list_of_groups

    def get_data_of_group(self, group_name: str) -> dict:
        dictionary = {}
        for key, values in self.data["tasks"].items():
            if group_name in values["groups"]: dictionary.update({key: values})
        return dictionary

    def get_data_of_importance(self, importance_lvl: str) -> dict:
        dictionary = {}
        for key, values in self.data["tasks"].items():
            if values["importance"] == importance_lvl: dictionary.update({key: values})
        return dictionary

    def get_all_data(self, *args, **kwargs) -> dict:
        return self.data["tasks"]

    # Beautify Data for display purposes
    def display_task_details(self, data: dict, task_hash="") -> str:
        """
        A function that displays all tasks passed to it and the details of a specific one
        Only pass the tasks dict or part of it to this function otherwise it wont work
        The function returns a list so the ScreenManager can add color based on the tasks importance.
        """
        output = []
        if data == {}: return [["You did not create a task yet. Press A to change that.", "None"]]
        if self.current_order[0] == "group":
            index_map = {v: i for i, v in enumerate(self.data["order of tasks in group"][self.current_order[1]])}
            print(index_map)
            data = dict(sorted(data.items(), key=lambda pair: index_map[pair[0]]))
        else:
            data = dict(sorted(data.items(), key=lambda item: item[1]['index']))
        for idx, items in enumerate(data.items()):
            output.append([f"{idx+1}. {items[1]['name']} {''.join(f'[{label}]' for label in items[1]['labels'])}{''.join(f'{{{group}}}' for group in items[1]['groups'])}", items[1]["importance"]])
            # display details
            if items[0] == task_hash:
                if items[1]["description"] != "": output.append([items[1]["description"], "None"])
                output.append(["\n", "None"])
                # display steps with details
                sorted_steps = dict(sorted(items[1]["steps"].items(), key=lambda item: item[1]["index"]))
                for idx_2, values in enumerate(sorted_steps.values()):
                    output.append([f"{' '*self.TAB_INDENT}{idx+1}.{idx_2+1} {values['name']}", values["importance"]])
                    if values["description"] != "": output.append([f"{' '*self.TAB_INDENT}{values['description']}", "None"])
                    output.append(["\n", "None"])
        return output

    def get_longest_entry_beautified(self) -> tuple[int]:
        """
        Function returns the length of the longest beautified entry (height and width)
        """
        output = []
        number_of_tasks = len(self.data["tasks"])
        min_height = number_of_tasks
        # generate all outputs for all step hashes and determine the max len and height than
        data = dict(sorted(self.data["tasks"].items(), key=lambda item: item[1]['index']))
        for idx, items in enumerate(data.items()):
            output.append(f"{idx+1}. {items[1]['name']} {''.join(f'[{label}]' for label in items[1]['labels'])}{''.join(f'{{{group}}}' for group in items[1]['groups'])}")
            # display details
            if items[1]["description"] != "": output.append(items[1]["description"])
            output.append("\n")
            # display steps with details
            start_len = len(output)
            sorted_steps = dict(sorted(items[1]["steps"].items(), key=lambda item: item[1]["index"]))
            for idx_2, values in enumerate(sorted_steps.values()):
                output.append(f"{' '*self.TAB_INDENT}{idx+1}.{idx_2+1} {values['name']}")
                if values["description"] != "": output.append(f"{' '*self.TAB_INDENT}{values['description']}")
                output.append("\n")
            end_len = len(output) - start_len
            if end_len + number_of_tasks > min_height: min_height = end_len + number_of_tasks

        return (min_height+2, len(max(output, key=lambda x: len(x)))) # min_height + 2 bc of the outline top and bottom

    # Update and validate data automaticly
    def update_groups(self, task_hash: str, groups: list) -> None:
        for group in groups:
            try:
                if not task_hash in self.data["order of tasks in group"][group]: self.data["order of tasks in group"][group].append(id)
            except:
                self.data["order of tasks in group"].update({group: [task_hash]})

    def validata_data_and_update_necessary(self, type_of_deletion_with_args: list[str]) -> None:
        """
        Currently only makes the index is continues to avoid problems
        """
        match type_of_deletion_with_args[0]:
            case "task":
                sorted_data = dict(sorted(self.data["tasks"].items(), key=lambda item: item[1]["index"]))
                for idx, task in enumerate(sorted_data.values()):
                    task["index"] = idx
            case "step":
                sorted_data = dict(sorted(self.data["tasks"][type_of_deletion_with_args[1][0]]["steps"].items(), key=lambda item: item[1]["index"]))
                for idx, step in enumerate(sorted_data.values()):
                    step["index"] = idx

if __name__ == "__main__":
    from os import getcwd
    cwd = getcwd()
    filepath = split(argv[0])[0] + "\\" + "data.backup"
    f = FileManager(f"{cwd}\\data.json")
    data = DataManager(f.data)
    print(data.display_tasks(data.data["tasks"]))
