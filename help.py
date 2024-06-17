# add a manual backup maybe or backup and save on change of data (add, change, delete)
help_message = """
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

wrong_input_message = " The provided input doesn't match the wanted pattern.\n\n"

footer_text = ["[H]elp", "[Q]uit"]

step_data = ["To which task do you want to add the task?\nPlease provide the index.\nA `0` means cancel.", "Please provide a name for this step.", "Now a description please.", "Choose an importance for the step.\n[N]one; [L]ow; [M]edium; [H]igh"]

task_data = ["Please provide a name for this task.", "Now a description please.", "Choose an importance for the task.\n[N]one; [L]ow; [M]edium; [H]igh", "What labels should the task have?\nPlease separate them by a `,` e.g. `1, 2, 5`.\nA `0` means no label.", "What groups should the task belong to?\nPlease separate your choice by a `,` e.g. `1, 2, 5`.\nA `0` means no group."]

instructions = {
        "change": {
            "1": "Change Data:\nPlease provide the number or index of the task you want to change.\ne.g. `1` [for a the first task] or `1.2` [for the second step of the first task]",
            "2": {
                "task": task_data,
                "step": step_data
                }
            },
        "add": {
            "1": "Add Data:\nDo you want to add a new [T]ask or [S]tep?",
            "2": {
                "task": task_data,
                "step": step_data
                }
            },
        "delete": "Delete Data:\nWhat do you want to delete?\n[T]ask, [S]tep, [L]abel, [G]roup",
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

if __name__ == "__main__":
    print(help_message)
