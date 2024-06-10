from os.path import exists, dirname, split, splitext
from os import chdir
from sys import argv
from json import load, dumps
from uuid import uuid4

class FileManager:
    def __init__(self, path_to_file: str) -> None:
        if not exists(path_to_file): raise Exception("File not found in given directory.")
        self.path_to_file: str = path_to_file
        self.backup_path: str = splitext(path_to_file)[0] + ".backup"
        self.data: dict = self.read_file_data()

    @classmethod
    def for_new_file(cls, path_with_filename_and_extension: str) -> None:
        with open(path_with_filename_and_extension, "w") as f:
            f.write('{"order of tasks in group":{},'
                      '"tasks":{}}')
        return cls(path_with_filename_and_extension)

    def read_file_data(self) -> dict:
        with open(self.path_to_file, "r") as f:
            return load(f)

    def update_data(self, data: dict) -> None:
        self.data = data
        with open(self.path_to_file, "w") as f:
            f.write(str(dumps(self.data)))

    def load_backup_data(self) -> None:
        with open(self.backup_path, "r") as f:
            self.data = load(f)

    def overwrite_main_data_with_backup(self) -> None:
        with open(self.backup_path, "r") as f:
            update_data(load(f))

    def write_backup(self) -> None:
        with open(self.backup_path, "w") as f:
            f.write(str(dumps(self.data)))

class DataManager:
    def __init__(self, data: dict):
        self.data: dict = data

    def gen_unique_hash(self) -> str:
        return uuid4().hex

    # ADDING, CHANGING AND REMOVING DATA
    def modify_task(self, data: dict) -> None:
        self.data["tasks"].update(data)

    def delete_task(self, task_hash: str) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        self.data["tasks"].remove(task_hash)

    def add_step(self, task_hash: str, data: dict) -> None:
        self.data["tasks"][task_hash]["steps"].update(data)

    def delete_step(self, task_hash: str, step_hash: str) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        if step_hash not in self.data["tasks"][task_hash]["steps"].keys(): return
        self.data["tasks"][task_hash]["steps"].remove(step_hash)

    def change_data_step(self, task_hash: str, data: dict) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        self.data["tasks"][task_hash].update(data)

    def add_label(self, task_hash: str, label: str) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        self.data["tasks"][task_hash]["labels"].append(label)

    def delete_task_hash_from_label(self, task_hash: str, label: str) -> None:
        if label not in self.data["labels"].keys(): return
        self.data["labels"][label].remove(task_hash)

    def delete_label(self, label: str) -> None:
        for value in self.data["tasks"].values():
            if label in value["labels"]: value["labels"].remove(label)

    def change_importance(self, task_hash, importance: str | None) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        self.data["tasks"][task_hash].update({"importance": importance})

    def change_order_of_tasks(self, new_order: dict) -> None:
        # new order consist of task_hash: number
        for hash, value in new_order.items():
            if hash not in self.data["tasks"].keys(): continue
            self.data["tasks"][hash]["index"] = value

    def change_order_of_steps(self, task_hash: str, new_order: dict) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        for hash, value in new_order.items():
            if hash not in self.data["tasks"][task_hash].keys(): continue
            self.data["tasks"][task_hash][hash]["index"] = value

    # GET DATA (MAINLY FOR FILTER FUNCTION)
    def get_data_with_label(self, label: str) -> dict | None:
        dictionary = {}
        for key, values in self.data["tasks"].items():
            if values["labels"] == label: dictionary.update({key: values})
        return dictionary

    def get_data_of_group(self, group_name: str) -> dict:
        dictionary = {}
        for key, values in self.data["tasks"].items():
            if values["groups"] == group_name: dictionary.update({key: values})
        return dictionary

    def get_data_of_importance(self, importance_lvl: str) -> dict:
        dictionary = {}
        for key, values in self.data["tasks"].items():
            if values["importance"] == importance_lvl: dictionary.update({key: values})
        return dictionary

    def get_all_data(self) -> dict:
        return self.data["tasks"]

    # Beautify Data for display purposes
    def display_tasks(self, data: dict) -> list:
        """
        A function to display the tasks in a nice way.
        e.g. Task 1 [label][label_2]
        Only pass the tasks dict or part of it to this function otherwise it wont work
        The function returns a list so the ScreenManager can add color based on the tasks importance.
        """
        output = []
        data = dict(sorted(data.items(), key=lambda item: item[1]['index']))
        for idx, values in enumerate(data.values()):
            output.append(f"{idx+1}. {values['name']} {''.join(f'[{label}]' for label in values['labels'])}")
        return output

    def display_task_details(self, data: dict, task_hash: str) -> str:
        return str(data)

if __name__ == "__main__":
    from os import getcwd
    cwd = getcwd()
    filepath = split(argv[0])[0] + "\\" + "data.backup"
    f = FileManager(f"{cwd}\\data.json")
    data = DataManager(f.data)
    print(data.display_tasks(data.data["tasks"]))
