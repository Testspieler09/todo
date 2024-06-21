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
    
![ToDo](https://github.com/Testspieler09/todo/assets/142326461/5d25d5d6-a66d-4948-976d-d425d17a8ac1)
    
</div>

## Usage

When toggeling the help menu via the `h` key one gets the following help message:

```txt
Key cheat sheet
===============

Arrow-Keys -> navigation/scrolling content
S -> [S]how more information of task

A -> [A]dd task/step
C -> [C]hange data/order
F -> [F]ilter tasks of specific group, label or importance
D -> [D]elete task/step

H -> toggle this [H]elpmessage
Q -> [Q]uit programey cheat sheet
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
