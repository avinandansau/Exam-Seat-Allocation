# Exam Seat Allocation

A command-line Python program that assigns students to examination rooms and seats, while checking seating rules and providing room and student lookup tools.

## Features

- Validates student records for duplicate roll numbers and missing names, sections, or subjects.
- Checks that the total room capacity can accommodate the student list.
- Assigns students in a deterministic order, placing students with special requirements first.
- Tries a student's preferred room first when it exists; if seating constraints or capacity prevent placement, it tries the other rooms.
- Places students with special requirements in designated priority seats.
- Prevents students with the same section or subject from occupying adjacent seats in the same room.
- Validates the completed plan for capacity, duplicate assignments, priority-seat use, and unassigned students.
- Displays the student list, room seating plans, and room occupancy summaries.
- Searches for a student's assigned room and seat by roll number.
- Allows students to be added or removed during the session and reallocates seats after changes.

## Requirements

- Python 3.8 or later
- No third-party packages are required.

## Run the program

Clone or download this repository, open a terminal in the project folder, and run:

```powershell
py exam.py
```

If the `py` launcher is not available, use:

```powershell
python exam.py
```

The program validates the initial data and creates a seating plan before showing the interactive menu.

## Menu

| Option | Action |
| --- | --- |
| 1 | Display all registered students |
| 2 | Display the room-wise seating plan |
| 3 | Display occupied and empty seats for each room |
| 4 | Search for a student's room and seat using their roll number |
| 5 | Add a student and recalculate the seating plan |
| 6 | Remove a student and recalculate the seating plan |
| 7 | Exit |

Student and room changes made through the menu exist only for the current run.

## Default data and customization

The program starts with 24 sample students and four rooms (`R1`–`R4`), each with six seats. Student and room data are defined near the top of [`exam.py`](exam.py). Edit those lists to use your own data.

Each student record has these fields:

| Field | Description |
| --- | --- |
| `roll` | Unique numeric student identifier |
| `name` | Student name |
| `section` | Student's section |
| `subject` | Examination subject |
| `preferred_room` | Preferred room number, or an empty string for no preference |
| `special` | `True` if the student requires a priority seat; otherwise `False` |

Each room record has:

| Field | Description |
| --- | --- |
| `number` | Room identifier |
| `capacity` | Number of seats in the room |
| `invigilator` | Invigilator name shown in room output |
| `priority_seats` | Seat numbers reserved for students with special requirements |

The allocation is deterministic: it does not use randomization. Students with special requirements are processed first, then students are ordered by roll number. The allocator tries to place each student while satisfying the adjacent-seat rule and any applicable priority-seat requirement. Preferred rooms are best-effort; a student may be assigned to another room if needed. If the rules prevent a complete allocation, the program reports unassigned students and the final validation reports the incomplete plan.

## Limitations

- Student and room data are held in memory; changes are not saved after the program exits.
- There is no file import/export, database, or graphical interface.
- The program checks for duplicate rolls and required student fields, but does not validate all possible data issues (for example, room configuration errors).
