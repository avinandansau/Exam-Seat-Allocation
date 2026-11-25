students = [
    {"roll": 101, "name": "Aarav Das", "section": "A", "subject": "Python", "preferred_room": "R2", "special": False},
    {"roll": 102, "name": "Diya Roy", "section": "B", "subject": "DBMS", "preferred_room": "", "special": False},
    {"roll": 103, "name": "Rohan Sen", "section": "C", "subject": "Mathematics", "preferred_room": "", "special": True},
    {"roll": 104, "name": "Mira Dey", "section": "D", "subject": "English", "preferred_room": "R3", "special": False},
    {"roll": 105, "name": "Arjun Pal", "section": "A", "subject": "DBMS", "preferred_room": "", "special": False},
    {"roll": 106, "name": "Isha Ghosh", "section": "B", "subject": "English", "preferred_room": "", "special": False},
    {"roll": 107, "name": "Kabir Bose", "section": "C", "subject": "Python", "preferred_room": "", "special": False},
    {"roll": 108, "name": "Anaya Paul", "section": "D", "subject": "Mathematics", "preferred_room": "", "special": False},
    {"roll": 109, "name": "Aditya Roy", "section": "A", "subject": "English", "preferred_room": "", "special": False},
    {"roll": 110, "name": "Sana Khan", "section": "B", "subject": "Python", "preferred_room": "", "special": False},
    {"roll": 111, "name": "Vivaan Das", "section": "C", "subject": "DBMS", "preferred_room": "", "special": False},
    {"roll": 112, "name": "Myra Sen", "section": "D", "subject": "Python", "preferred_room": "", "special": False},
    {"roll": 113, "name": "Reyansh Dutta", "section": "A", "subject": "Mathematics", "preferred_room": "", "special": False},
    {"roll": 114, "name": "Aditi Nair", "section": "B", "subject": "DBMS", "preferred_room": "", "special": False},
    {"roll": 115, "name": "Krish Saha", "section": "C", "subject": "English", "preferred_room": "", "special": False},
    {"roll": 116, "name": "Pari Roy", "section": "D", "subject": "DBMS", "preferred_room": "", "special": False},
    {"roll": 117, "name": "Dhruv Pal", "section": "A", "subject": "Python", "preferred_room": "", "special": False},
    {"roll": 118, "name": "Tara Bose", "section": "B", "subject": "Mathematics", "preferred_room": "", "special": False},
    {"roll": 119, "name": "Neil Ghosh", "section": "C", "subject": "English", "preferred_room": "", "special": False},
    {"roll": 120, "name": "Riya Das", "section": "D", "subject": "Python", "preferred_room": "", "special": False},
    {"roll": 121, "name": "Atharv Sen", "section": "A", "subject": "DBMS", "preferred_room": "", "special": False},
    {"roll": 122, "name": "Zoya Paul", "section": "B", "subject": "English", "preferred_room": "", "special": False},
    {"roll": 123, "name": "Yash Dey", "section": "C", "subject": "Mathematics", "preferred_room": "R4", "special": False},
    {"roll": 124, "name": "Meera Sen", "section": "D", "subject": "DBMS", "preferred_room": "", "special": True},
]

rooms = [
    {"number": "R1", "capacity": 6, "invigilator": "Mr. Amit", "priority_seats": [1, 6]},
    {"number": "R2", "capacity": 6, "invigilator": "Ms. Rina", "priority_seats": [1, 6]},
    {"number": "R3", "capacity": 6, "invigilator": "Mr. Suman", "priority_seats": [1, 6]},
    {"number": "R4", "capacity": 6, "invigilator": "Ms. Pooja", "priority_seats": [1, 6]},
]

# This dictionary stores the assigned students by room and seat number.
seating = {room["number"]: {} for room in rooms}


def add_student(student):
    """Add one student if the roll number is not already used."""
    for old_student in students:
        if old_student["roll"] == student["roll"]:
            print("Roll number already exists.")
            return False
    students.append(student)
    print("Student added successfully.")
    return True


def remove_student(roll_number):
    """Remove a student before generating the seating plan."""
    for student in students[:]:
        if student["roll"] == roll_number:
            students.remove(student)
            print("Student removed successfully.")
            return True
    print("Student not found.")
    return False


def display_students():
    print("\nREGISTERED STUDENTS")
    print("Roll  Name                 Section  Subject       Preferred  Special")
    for s in students:
        print(f"{s['roll']:<5} {s['name']:<20} {s['section']:<8} {s['subject']:<13} {s['preferred_room'] or '-':<10} {s['special']}")


def validate_students():
    """Check duplicate rolls and required student fields."""
    seen_rolls = []
    for s in students:
        if s["roll"] in seen_rolls:
            print("Validation failed: duplicate roll number", s["roll"])
            return False
        seen_rolls.append(s["roll"])
        if not s["name"] or not s["section"] or not s["subject"]:
            print("Validation failed: missing information for roll", s["roll"])
            return False
    print("Student data validation passed.")
    return True


def calculate_room_capacity():
    return sum(room["capacity"] for room in rooms)


def check_capacity():
    total_capacity = calculate_room_capacity()
    print(f"Total students: {len(students)}")
    print(f"Total room capacity: {total_capacity}")
    if len(students) > total_capacity:
        print("Not enough seats. Add rooms or reduce the student list.")
        return False
    print("Capacity check passed.")
    return True


def group_students():
    """Sort special-requirement students first, then by roll number."""
    return sorted(students, key=lambda s: (not s["special"], s["roll"]))


def check_seating_constraints(student, room_number, seat_number):
    """A student cannot sit beside someone from the same section or subject."""
    room_seats = seating[room_number]
    for neighbor_seat in (seat_number - 1, seat_number + 1):
        if neighbor_seat in room_seats:
            neighbor = room_seats[neighbor_seat]
            if neighbor["section"] == student["section"]:
                return False
            if neighbor["subject"] == student["subject"]:
                return False
    return True


def arrange_students():
    """Return students in a stable order; no random allocation is used."""
    return group_students()


def assign_seats():
    """Allocate students, honoring special seats and preferred rooms when possible."""
    global seating
    seating = {room["number"]: {} for room in rooms}
    room_lookup = {room["number"]: room for room in rooms}
    unassigned = []

    for student in arrange_students():
        # Try the preferred room first, then all other rooms in fixed order.
        room_order = []
        preferred = student["preferred_room"]
        if preferred in room_lookup:
            room_order.append(preferred)
        for room in rooms:
            if room["number"] not in room_order:
                room_order.append(room["number"])

        placed = False
        for room_number in room_order:
            room = room_lookup[room_number]
            occupied = seating[room_number]
            if len(occupied) >= room["capacity"]:
                continue

            # Special-requirement students try priority seats first.
            if student["special"]:
                seat_order = room["priority_seats"] + [n for n in range(1, room["capacity"] + 1) if n not in room["priority_seats"]]
            else:
                seat_order = list(range(1, room["capacity"] + 1))

            for seat_number in seat_order:
                if seat_number in occupied:
                    continue
                if student["special"] and seat_number not in room["priority_seats"]:
                    continue
                if check_seating_constraints(student, room_number, seat_number):
                    occupied[seat_number] = student
                    placed = True
                    break
            if placed:
                break
        if not placed:
            unassigned.append(student)

    if unassigned:
        print("\nWARNING: Some students could not be seated under the current rules:")
        for s in unassigned:
            print(s["roll"], s["name"])
        print("The program will validate the partial plan; adjust the dataset/rooms if needed.")
    else:
        print("All eligible students were allocated.")
    return len(unassigned) == 0


def validate_arrangement():
    """Verify unique student/seat assignment, capacity and all constraints."""
    assigned_rolls = []
    valid = True
    for room in rooms:
        room_number = room["number"]
        room_seats = seating[room_number]
        if len(room_seats) > room["capacity"]:
            print("ERROR: Capacity exceeded in", room_number)
            valid = False
        for seat_number, student in room_seats.items():
            if student["roll"] in assigned_rolls:
                print("ERROR: Student assigned more than once:", student["roll"])
                valid = False
            assigned_rolls.append(student["roll"])
            if student["special"] and seat_number not in room["priority_seats"]:
                print("ERROR: Special student not in priority seat:", student["roll"])
                valid = False
            if not check_seating_constraints(student, room_number, seat_number):
                print("ERROR: Adjacent-seat rule failed for roll", student["roll"])
                valid = False
            if student["preferred_room"] and student["preferred_room"] in [r["number"] for r in rooms]:
                # If their preferred room had a valid seat available, allocator tries it first.
                pass
    if len(assigned_rolls) != len(students):
        print(f"ERROR: {len(students) - len(assigned_rolls)} student(s) are unassigned.")
        valid = False
    if valid:
        print("Final seating arrangement validation passed.")
    else:
        print("Final seating arrangement validation failed.")
    return valid


def display_seating_plan():
    print("\n========== ROOM-WISE SEATING PLAN ==========")
    for room in rooms:
        room_number = room["number"]
        print(f"\nRoom: {room_number} | Invigilator: {room['invigilator']} | Capacity: {room['capacity']}")
        print("Seat  Roll  Student Name         Section  Subject       Special")
        for seat_number in sorted(seating[room_number]):
            s = seating[room_number][seat_number]
            print(f"{seat_number:<5} {s['roll']:<5} {s['name']:<20} {s['section']:<8} {s['subject']:<13} {s['special']}")
        if not seating[room_number]:
            print("No students allocated.")


def generate_room_summary():
    print("\nROOM-WISE SUMMARY")
    print("Room  Invigilator  Occupied  Empty  Capacity")
    for room in rooms:
        occupied = len(seating[room["number"]])
        empty = room["capacity"] - occupied
        print(f"{room['number']:<5} {room['invigilator']:<12} {occupied:<9} {empty:<6} {room['capacity']}")
    print(f"Total allocated: {sum(len(seating[r['number']]) for r in rooms)} / {len(students)} students")


def find_student_seat(roll_number):
    for room in rooms:
        room_number = room["number"]
        for seat_number, student in seating[room_number].items():
            if student["roll"] == roll_number:
                return student, room, seat_number
    return None


def search_student():
    try:
        roll_number = int(input("Enter student roll number: "))
    except ValueError:
        print("Please enter a numeric roll number.")
        return
    result = find_student_seat(roll_number)
    if result:
        student, room, seat_number = result
        print("\nSTUDENT SEAT DETAILS")
        print("Name:", student["name"])
        print("Section:", student["section"])
        print("Subject:", student["subject"])
        print("Examination Room:", room["number"])
        print("Seat Number:", seat_number)
    else:
        print("Student not found in the seating plan.")


def main():
    print("EXAMINATION SEATING ARRANGEMENT SYSTEM")
    if not validate_students() or not check_capacity():
        return
    assign_seats()
    validate_arrangement()

    while True:
        print("\nMENU")
        print("1. Display all students")
        print("2. Display room-wise seating plan")
        print("3. Generate room-wise summary")
        print("4. Search student seat by roll number")
        print("5. Add student (requires rerunning allocation)")
        print("6. Remove student (requires rerunning allocation)")
        print("7. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            display_students()
        elif choice == "2":
            display_seating_plan()
        elif choice == "3":
            generate_room_summary()
        elif choice == "4":
            search_student()
        elif choice == "5":
            try:
                roll = int(input("Roll number: "))
                name = input("Student name: ").strip()
                section = input("Section: ").strip().upper()
                subject = input("Subject: ").strip()
                preferred = input("Preferred room (or press Enter): ").strip().upper()
                special = input("Special requirement? (y/n): ").strip().lower() == "y"
                if add_student({"roll": roll, "name": name, "section": section, "subject": subject, "preferred_room": preferred, "special": special}):
                    if validate_students() and check_capacity():
                        assign_seats()
                        validate_arrangement()
            except ValueError:
                print("Roll number must be numeric.")
        elif choice == "6":
            try:
                roll = int(input("Enter roll number to remove: "))
                if remove_student(roll):
                    assign_seats()
                    validate_arrangement()
            except ValueError:
                print("Roll number must be numeric.")
        elif choice == "7":
            print("Thank you for using the system.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
