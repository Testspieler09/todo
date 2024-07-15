# add a manual backup maybe or backup and save on change of data (add, change, delete)
HELP_MESSAGE = """
 Key cheat sheet
 ===============

 Arrow-Keys -> navigation/scrolling content
 S -> [S]how more information of task

 A -> [A]dd task/step
 C -> [C]hange data/order
 F -> [F]ilter tasks of specific group, label or importance
 D -> [D]elete task/step

 H -> toggle this [H]elpmessage
 Q -> [Q]uit program"""

WRONG_INPUT_MESSAGE = "The provided input doesn't match the wanted pattern.\n\n"

FOOTER_TEXT = ["[H]elp", "[Q]uit"]

STEP_DATA = ["To which task do you want to add the task?\nPlease provide the index.\nA `0` means cancel.", "Please provide a name for this step.", "Now a description please.", "Choose an importance for the step.\n[N]one; [L]ow; [M]edium; [H]igh"]

TASK_DATA = ["Please provide a name for this task.", "Now a description please.", "Choose an importance for the task.\n[N]one; [L]ow; [M]edium; [H]igh", ["Do you want to add [E]xisting labels or create a [N]ew one?", "What labels should the task have?\nPlease separate them by a `,` e.g. `1, 2, 5`.\nA `0` means no label.", "Please provide a name for the new label"], ["Do you want to add [E]xisting groups or create a [N]ew one?", "What groups should the task belong to?\nPlease separate your choice by a `,` e.g. `1, 2, 5`.\nA `0` means no group.", "Please provide a name for the new group"]]

INSTRUCTIONS = {
    "change": {
        "1": "Change Data:\nWhat would you like to change?\n[T]ask; [S]tep; [O]rder; [R]ename label/group",
        "task": {
            "1": "What would you like to change?\ne.g. `1, 2, 4`\n1. Name | 2. Desciption | 3. Importance | 4. Labels | 5. Groups |",
            "2": ["Please provide a new name for this task.",
                  "Please provide the new description.",
                  "Choose a new importance for the task.\n[N]one; [L]ow; [M]edium; [H]igh",
                  [
                      "Do you want to add [E]xisting labels or create a [N]ew one?",
                      "What labels should the task have?\nPlease separate them by a `,` e.g. `1, 2, 5`.\nA `0` means no label.\nNote that the labels won't be added to the existing ones but overwrite the old choice.",
                      "Please provide a name for the new label.\nIt will be added to the other labels of this task."
                    ],
                  [
                      "Do you want to add [E]xisting groups or create a [N]ew one?",
                      "What groups should the task belong to?\nPlease separate your choice by a `,` e.g. `1, 2, 5`.\nA `0` means no group.\nNote that the groups won't be added to the existing ones but overwrite the old choice.",
                      "Please provide a name for the new group.\nIt will be added to the other groups of this task."
                    ]
                  ],
            "task_hash": "Please provide the index of the task you want to change the data of.\nA `0` means cancel."
        },
        "step": {
            "1": "What would you like to change?\ne.g. `1, 2, 4`\n1. Name | 2. Desciption | 3. Importance |",
            "2": ["Which step do you want to change?\nPlease provide the index.\ne.g. `1.2` [for the second step of the first task]\nInput `0.0` to cancel the process.", "Please provide a name for this step.", "Now a description please.", "Choose an importance for the step.\n[N]one; [L]ow; [M]edium; [H]igh"]

        },
        "order": {
            "what": "What do you want to reorder?\n[T]asks; [S]teps",
            "tasks": "TIPP: Filter the tasks by group before reordering and you will sort them within the group.\nChoose how you want to order the data.\n[I]nsert specific task/step at index; provide all indices as [N]ew order",
            "steps": "Please provide the index of the tasks the steps belong to.\nA `0` means cancel the process.",
            "order_type": "Choose how you want to order the data.\n[I]nsert specific task/step at index; provide all indices as [N]ew order",
            "insert": "Please provide the index of the task/step you want to move and then the index it should be in separate by a `,`.\ne.g. `4, 1` to move the 4th task/step to the top (index 1)",
            "new order": "Please provide the new order of tasks/steps. Do it by providing a new arrangement of the old indices.\ne.g. `2, 1, 3` if you have 3 tasks/steps and want to reorder them so the first and second tasks/steps are switched\nA `0` means cancel the process"
        },
        "rename": ["Do you want to rename a [L]abel or [G]roup?\nA `0` means cancel", "Please provide the index of the label/group", "Please provide the new name for the label/group named "]
    },
    "add": {
        "1": "Add Data:\nDo you want to add a new [T]ask, [S]tep, [L]abel or [G]roup?",
        "task": TASK_DATA,
        "step": STEP_DATA,
        "label": "Please provide the name for the new label.",
        "group": "Please provide the name for the new group."
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
        "1": "Filter Data:\nDo you want to display all tasks of a [G]roup, [L]abel or [I]mportance?\nTo disable the current filter use `0`",
        "group": "Display tasks of group:\nPlease provide the number/index of the group.\nInput `0` for all tasks that do not belong to a group\n",
        "label": "Display tasks of label:\nPlease provide the number/index of the label.\nInput `0` for all tasks that do not have a label\n",
        "importance": "Display tasks of importance:\nPlease choose between [L]ow, [M]edium, [H]igh or [N]one.\n"
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
MULTIINDEX_REGEX = r"^\d+(,\s*\d)*$"
INDEX_REGEX = r"^\d+$"
NAME_REGEX = r"^[\S\s]+$"
STEP_IDX_REGEX = r"^\d+\.\d+$"

if __name__ == "__main__":
    print(HELP_MESSAGE)
