# ToDo (terminal app)

The ToDo Manager is a minimalistic terminal based todo list, which has support for groups, labels and 3 different importance levels (low, medium, high). The program was developed on Windows 11 but should be portable. If there are any problems please open an issue or send a pull request.

## Features

1. Support for groups
    - e.g. Project 1, Projekt 2, etc
1. Support for labels
    - e.g. bug, till tomorrow, etc
1. Support for importance levels
    - defaults to None if not specified
    - if terminal can display color the task will be shown in different colors based on importance
1. Support for task steps (just 1 layer for now)
    - e.g. Big Task -> Step 1, Step 2, etc

## Usage

When toggeling the help menu via the `h` key one gets the following help message:

```txt
Key cheat sheet
===============

Arrow-Keys -> navigation/scrolling content

G -> display tasks of specific [G]roup
L -> display tasks of specific [L]abel
I -> display tasks of specific [I]mportance
C -> [C]hange data
D -> [D]elete task/step
A -> [A]dd task/step

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
