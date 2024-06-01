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
        self.data: dict = {}

    @classmethod
    def for_new_file(cls, path_with_filename_and_extension: str) -> None:
        with open(path_with_filename_and_extension, "w") as f:
            f.write('{"labels":{},'
                      '"groups":{},'
                      '"tasks":{}}')
        return cls(path_with_filename_and_extension)

    def read_file_to_dict(self) -> None:
        with open(self.path_to_file, "r") as f:
            self.data = load(f)

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
        return uuid4()

    # ADDING, CHANGING AND REMOVING DATA
    def modify_task(self, data: dict) -> None:
        self.data["tasks"].update(data)

    def delete_task(self, task_hash: str) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        self.data["tasks"].pop(task_hash)

    def add_step(self, task_hash: str, data: dict) -> None:
        self.data["tasks"][task_hash]["steps"].update(data)

    def delete_step(self, task_hash: str, step_hash: str) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        if step_hash not in self.data["tasks"][task_hash]["steps"].keys(): return
        self.data["tasks"][task_hash]["steps"].pop(step_hash)

    def change_data_step(self, task_hash: str, data: dict) -> None:
        if task_hash not in self.data["tasks"].keys(): return
        self.data["tasks"][task_hash].update(data)

    def add_label(self, task_hash: str, label: str) -> None:
        if label in self.data["labels"].keys():
            self.data["labels"][label].append(task_hash)
        else:
            self.data["labels"].update({label:[task_hash]})

    def delete_task_hash_from_label(self, task_hash: str, label: str) -> None:
        if label not in self.data["labels"].keys(): return
        self.data["labels"][label].remove(task_hash)

    def delete_label(self, label: str) -> None:
        if label not in self.data["labels"].keys(): return
        self.data["labels"].pop(label)

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
        if label not in self.data["labels"].keys(): return
        task_hashes = self.data["labels"][label]
        dictionary = {}
        for hash in task_hashes:
            if hash not in self.data["tasks"].keys(): continue
            dictionary.update(self.data["tasks"][hash])
        return dictionary

    def get_data_of_group(self, group_name: str) -> dict:
        if group_name not in self.data["groups"].keys(): return
        task_hashes = self.data["groups"][group_name]
        dictionary = {}
        for hash in task_hashes:
            if hash not in self.data["tasks"].keys(): continue
            dictionary.update(self.data["tasks"][hash])
        return dictionary

    def get_data_of_importance(self, importance_lvl: str) -> dict:
        dictionary = {}
        for item in self.data["tasks"].values():
            if item["importance"] == importance_lvl: dictionary.update(item)
        return dictionary

    def get_all_data(self) -> dict:
        return self.data["tasks"]

if __name__ == "__main__":
    from os import getcwd
    cwd = getcwd()
    filepath = split(argv[0])[0] + "\\" + "data.backup"
    f = FileManager(f"{cwd}\\data.json")
    f.read_file_to_dict()
    print(f.path_to_file, "\n", f.backup_path)
