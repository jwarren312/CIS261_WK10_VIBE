"""Student Grade Calculator

This program manages student records with three test scores, calculates averages
and letter grades, displays a formatted list, computes class statistics, and
loads/saves records from/to a pipe-delimited text file.

Data structure choice: Option B - using a Student class.
"""

import os

DATA_FILE = "student_grades.txt"


class Student:
    def __init__(self, name: str, student_id: str, test1: float, test2: float, test3: float):
        self.name = name.strip()
        self.student_id = student_id.strip()
        self.test1 = test1
        self.test2 = test2
        self.test3 = test3
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self) -> float:
        return (self.test1 + self.test2 + self.test3) / 3.0

    def calculate_grade(self) -> str:
        average = self.average
        if average >= 90:
            return "A"
        if average >= 80:
            return "B"
        if average >= 70:
            return "C"
        if average >= 60:
            return "D"
        return "F"

    def to_pipe_line(self) -> str:
        return (
            f"{self.name}|{self.student_id}|{self.test1:.2f}|{self.test2:.2f}|"
            f"{self.test3:.2f}|{self.average:.2f}|{self.grade}"
        )

    @classmethod
    def from_pipe_line(cls, line: str):
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 7:
            raise ValueError("Invalid record format")

        name, student_id, test1, test2, test3, _, _ = parts
        return cls(name, student_id, float(test1), float(test2), float(test3))


def load_records(filename: str) -> list[Student]:
    students = []
    if not os.path.exists(filename):
        return students

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    students.append(Student.from_pipe_line(line))
                except Exception as error:
                    print(f"Warning: could not read line {line_number}: {error}")
    except OSError as error:
        print(f"Error loading file '{filename}': {error}")

    return students


def save_records(filename: str, students: list[Student]) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in students:
                file.write(student.to_pipe_line() + "\n")
        print(f"Saved {len(students)} student record(s) to '{filename}'.")
    except OSError as error:
        print(f"Error saving file '{filename}': {error}")


def prompt_input(prompt: str) -> str | None:
    value = input(prompt).strip()
    if value.upper() == "ESC":
        return None
    return value


def prompt_float(prompt: str) -> float | None:
    while True:
        value = prompt_input(prompt)
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please enter a valid float, or type ESC to cancel.")


def add_student(students: list[Student]) -> None:
    print("\nAdd New Student Record (type ESC to cancel at any prompt)")
    name = prompt_input("Student name: ")
    if name is None:
        print("Canceled adding a new student.")
        return

    student_id = prompt_input("Student ID: ")
    if student_id is None:
        print("Canceled adding a new student.")
        return

    test1 = prompt_float("Test 1 score: ")
    if test1 is None:
        print("Canceled adding a new student.")
        return

    test2 = prompt_float("Test 2 score: ")
    if test2 is None:
        print("Canceled adding a new student.")
        return

    test3 = prompt_float("Test 3 score: ")
    if test3 is None:
        print("Canceled adding a new student.")
        return

    student = Student(name, student_id, test1, test2, test3)
    students.append(student)
    print(f"Added {student.name} with average {student.average:.2f} and grade {student.grade}.")


def display_students(students: list[Student]) -> None:
    if not students:
        print("No student records available.")
        return

    print("\nStudent Records")
    print("-" * 88)
    header = f"{'Name':<20} {'ID':<12} {'Test1':>7} {'Test2':>7} {'Test3':>7} {'Average':>8} {'Grade':>6}"
    print(header)
    print("-" * 88)
    for student in students:
        print(
            f"{student.name:<20} {student.student_id:<12} "
            f"{student.test1:7.2f} {student.test2:7.2f} {student.test3:7.2f} "
            f"{student.average:8.2f} {student.grade:>6}"
        )
    print("-" * 88)


def display_statistics(students: list[Student]) -> None:
    if not students:
        print("No student records to calculate statistics.")
        return

    averages = [student.average for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)

    print("\nClass Statistics")
    print("-" * 36)
    print(f"Highest average : {highest:.2f}")
    print(f"Lowest average  : {lowest:.2f}")
    print(f"Class average   : {class_average:.2f}")
    print("-" * 36)


def search_student(students: list[Student]) -> None:
    if not students:
        print("No student records available to search.")
        return

    term = prompt_input("Enter student name to search: ")
    if term is None:
        print("Search canceled.")
        return

    term_lower = term.lower()
    matches = [student for student in students if term_lower in student.name.lower()]

    if not matches:
        print(f"No students found matching '{term}'.")
        return

    print(f"\nFound {len(matches)} matching student(s):")
    print("-" * 88)
    header = f"{'Name':<20} {'ID':<12} {'Test1':>7} {'Test2':>7} {'Test3':>7} {'Average':>8} {'Grade':>6}"
    print(header)
    print("-" * 88)
    for student in matches:
        print(
            f"{student.name:<20} {student.student_id:<12} "
            f"{student.test1:7.2f} {student.test2:7.2f} {student.test3:7.2f} "
            f"{student.average:8.2f} {student.grade:>6}"
        )
    print("-" * 88)


def main() -> None:
    students = load_records(DATA_FILE)
    print("Student Grade Calculator")
    print("Loaded", len(students), "student record(s).")

    while True:
        print("\nMenu")
        print("1. Add new student record")
        print("2. Display all student records")
        print("3. Display class statistics")
        print("4. Search student by name")
        print("5. Save student records")
        print("ESC. Exit program")

        choice = input("Enter option number or type ESC to exit: ").strip()
        if choice.upper() == "ESC":
            break

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            display_statistics(students)
        elif choice == "4":
            search_student(students)
        elif choice == "5":
            save_records(DATA_FILE, students)
        else:
            print("Invalid selection. Please pick 1-5 or ESC.")

    save_records(DATA_FILE, students)
    print("Exiting the program. Goodbye!")


if __name__ == "__main__":
    main()
