help_message = """
 Key cheat sheet
 ===============

 Arrow-Keys -> navigation/scrolling content
 S -> [s]how more information of task

 G -> display tasks of specific [G]roup
 L -> display tasks of specific [L]abel
 I -> display tasks of specific [I]mportance
 C -> [C]hange data
 D -> [D]elete task/step
 A -> [A]dd task/step

 H -> toggle this [H]elpmessage
 Q -> [Q]uit program"""

footer_text = ["[H]elp", "[Q]uit"]

step_data = ["Please provide a name for this step.", "Now a description please.", "Choose an importance for the task.\n0 -> None; 1 -> Low; 2 -> Medium; 3 -> High"]

task_data = ["Please provide a name for this task.", "Now a description please.", "Choose an importance for the task.\n0 -> None; 1 -> Low; 2 -> Medium; 3 -> High", "What labels should the task have?\nPlease separate them by a `,` e.g. `1, 2, 5`. If you want to create new labels do...", "What groups should the task belong to?\nPlease separate your choice by a `,` e.g. `1, 2, 5`. If you want to create new group do..."]

instructions = {
        "change": {
            "1": "Change Data:\nPlease provide the number or index of the task you want to change.\ne.g. `1` [for a the first task] or `1.2` [for the second step of the first task]",
            "2": {
                "task": task_data,
                "step": step_data
                }
            },
        "add": {
            "1": "Add Data:\nDo you want to add a new [t]ask or [s]tep?",
            "2": {
                "task": task_data,
                "step": step_data
                }
            },
        "delete": "Delete Data:\nWhat do you want to delete?\n[t]ask, [s]tep, [l]abel, [g]roup",
        "show": "Show more details:\nPlease provide the number or index of the task you want to expand.\ne.g. `1` [for a the first task] or `1.2` [for the second step of the first task]"
        }

if __name__ == "__main__":
    print(help_message)
