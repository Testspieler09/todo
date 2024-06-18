# add a manual backup maybe or backup and save on change of data (add, change, delete)
HELP_MESSAGE = """
 Key cheat sheet
 ===============

 Arrow-Keys -> navigation/scrolling content
 S -> [S]how more information of task

 A -> [A]dd task/step
 C -> [C]hange data/order
 D -> [D]isplay tasks of specific group, label or importance
 X -> delete task/step

 H -> toggle this [H]elpmessage
 Q -> [Q]uit program"""

WRONG_INPUT_MESSAGE = "The provided input doesn't match the wanted pattern.\n\n"

FOOTER_TEXT = ["[H]elp", "[Q]uit"]

STEP_DATA = ["To which task do you want to add the task?\nPlease provide the index.\nA `0` means cancel.", "Please provide a name for this step.", "Now a description please.", "Choose an importance for the step.\n[N]one; [L]ow; [M]edium; [H]igh"]

TASK_DATA = ["Please provide a name for this task.", "Now a description please.", "Choose an importance for the task.\n[N]one; [L]ow; [M]edium; [H]igh", ["Do you want to add [E]xisting labels or create a [N]ew one?", "What labels should the task have?\nPlease separate them by a `,` e.g. `1, 2, 5`.\nA `0` means no label.", "Please provide a name for the new label"], ["Do you want to add [E]xisting groups or create a [N]ew one?", "What groups should the task belong to?\nPlease separate your choice by a `,` e.g. `1, 2, 5`.\nA `0` means no group.", "Please provide a name for the new label"]]

INSTRUCTIONS = {
        "change": {
            "1": "Change Data:\nPlease provide the number or index of the task you want to change.\ne.g. `1` [for a the first task] or `1.2` [for the second step of the first task]",
            "2": {
                "task": TASK_DATA,
                "step": STEP_DATA
                }
            },
        "add": {
            "1": "Add Data:\nDo you want to add a new [T]ask or [S]tep?",
            "2": {
                "task": TASK_DATA,
                "step": STEP_DATA
                }
            },
        "delete": {
            "1": "Delete Data:\nWhat do you want to delete?\n[T]ask, [S]tep, [L]abel, [G]roup",
            "task": "Which task do you want to delete?\nPlease provide it's index",
            "step": "Which step do you want to delete?\nPlease provide the index.\ne.g. `1.2` [for the second step of the first task]",
            "label": "Which label would you like to delete?\nPlease provide the index",
            "group": "Which group would you like to delete?\nPlease provide the index",
            "validation": "Are you shure you want to delete it?\n[Y]es; [N]o"
            },
        "show": "Show more details:\nPlease provide the number or index of the task you want to expand.\ne.g. `1` [for a the first task]\nTIPP: `0` -> close details of given task",
        "display": {
            "1": "Display Data:\nDo you want to display all tasks of a [G]roup, [L]abel or [I]mportance?\nTo disable the current filter use `0`",
            "2": {
                "group": "Display tasks of group:\nPlease provide the number/index of the group.\nInput `0` for all tasks that do not belong to a group\n",
                "label": "Display tasks of label:\nPlease provide the number/index of the label.\nInput `0` for all tasks that do not have a label\n",
                "importance": "Display tasks of importance:\nPlease choose between [L]ow, [M]edium, [H]igh or [N]one.\n"
                }
            }
        }

# FIXED INPUT LENGTHS
CHOICE_LEN = 1
STEP_IDX_LEN = 30
NAME_LEN = 35
DESCRIPTION_LEN = 80
INDEX_LEN = 12
MULTIINDEX_LEN = 40

# SOME REPEATING REGEX
MULTIINDEX_REGEX = r"\d+(,\s*\d)*"
INDEX_REGEX = r"\d+"
NAME_REGEX = r"[\S\s]+"
STEP_IDX_REGEX = r"\d+\.\d+"

if __name__ == "__main__":
    print(HELP_MESSAGE)
