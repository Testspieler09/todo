# ToDo (terminal app)

The ToDo Manager is a minimalistic terminal based todo list, which has support for groups, labels and 3 different importance levels (low, medium, high). The program was developed on Windows 11 but should be portable. If there are any problems please open an issue or send a pull request.

## Features

1. Support for groups
    - e.g. Project 1, Project 2, etc
1. Support for labels
    - e.g. bug, till tomorrow, etc
1. Support for importance levels
    - if terminal can display color the task will be shown in different colors based on importance
    - colors are based on terminal/shell's color pallet (None->White, Low->Green, Medium->Blue, High->Red)
1. Support for task steps (just 1 layer for now)
    - e.g. Big Task -> Step 1, Step 2, etc
1. Some advanced functionality
    - reorder task, filter by label, importance etc.
1. Some backup functions
    - to see them add the -h flag when calling the program

## How does the program even look?

<div align="center">

![ToDo](assets/program.png)

**Image is outdated as the help message changed (correct help message further below).**

</div>

## Usage

When toggeling the help menu via the `h` key one gets the following help message:

```txt
Key cheat sheet
===============

Arrow-Keys -> navigation/scrolling content
S -> [S]how more information of task

A -> [A]dd task/step/label/group
C -> [C]hange data/order/rename label or group
F -> [F]ilter tasks of specific group, label or importance
D -> [D]elete task/step/label/group

H -> toggle this [H]elpmessage
Q -> [Q]uit program
```

**The program does not care about the letter being capitalized**

Further instructions will follow when the key is pressed.

### On Windows

Curses is not installed by default on Windows, so you need to run

```pwsh
pip install windows-curses
```

or

```pwsh
pip install -r requirements.txt
```
