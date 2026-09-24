import json

# STUDENT CLASS 
class Student:

    def __init__(self, name, roll, python, sql, maths):
        self.name = name
        self.roll = roll
        self.python = python
        self.sql = sql
        self.maths = maths

    # Calculate total marks
    def calculate_total(self):
        return self.python + self.sql + self.maths

    # Calculate average
    def calculate_average(self):
        return self.calculate_total() / 3

    # Calculate grade
    def calculate_grade(self):

        average = self.calculate_average()

        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"

    # Pass or fail
    def get_status(self):

        if (
            self.python >= 40
            and self.sql >= 40
            and self.maths >= 40 ):
            return "PASS"
        else:
            return "FAIL"

    # Display student information
    def display(self):

        print("\n========== STUDENT INFORMATION ==========")
        print("Name:", self.name)
        print("Roll:", self.roll)
        print("Python:", self.python)
        print("SQL:", self.sql)
        print("Maths:", self.maths)
        print("Total:", self.calculate_total())
        print("Average:", self.calculate_average())
        print("Grade:", self.calculate_grade())
        print("Status:", self.get_status())

# STUDENT MANAGER CLASS
class StudentManager:

    def __init__(self):
        self.students = []

    # Get valid roll number
    def get_roll(self):
        while True:

            try:
                roll = int(input("Enter roll number: "))
                return roll
            
            except ValueError:
                print("Invalid roll number! Enter numbers only.")

    # Get valid name
    def get_name(self):
        while True:

            name = input("Enter student name: ")

            if name.strip() == "":
                print("Name cannot be empty!")

            elif not name.replace(" ", "").isalpha():
                print("Name should contain letters only!")

            else:
                return name
            
    # Get valid marks
    def get_mark(self, subject):
        while True:

            try:
                mark = int(input(f"Enter {subject} mark (0-100): "))

                if 0 <= mark <= 100:
                    return mark

                else:
                    print("Invalid mark! Enter a mark between 0-100.")

            except ValueError:
                print("Invalid mark! Enter numbers only.")

    # Check roll number
    def roll_exists(self, roll):

        for student in self.students:

            if student.roll == roll:
                return True

        return False

    # Add student
    def add_student(self):

        print("\n========== ADD STUDENT ==========")

        name = self.get_name()
        roll = self.get_roll()

        while self.roll_exists(roll):

            print("Roll number already exists!")
            roll = self.get_roll()

        python = self.get_mark("Python")
        sql = self.get_mark("SQL")
        maths = self.get_mark("Maths")

        student = Student(
            name,
            roll,
            python,
            sql,
            maths
        )

        self.students.append(student)

        print("\nStudent enrolled successfully!")

    # View all students
    def view_students(self):

        if len(self.students) == 0:

            print("\nNo students found!")
            return

        print("\n========== STUDENT LIST ==========")

        print(
            "Name\t\tRoll\tPython\tSQL\tMaths"
        )

        print("-----------------------------------------------")

        for student in self.students:

            print(
                student.name,
                "\t\t",
                student.roll,
                "\t",
                student.python,
                "\t",
                student.sql,
                "\t",
                student.maths
            )

    # Search student
    def search_student(self):

        roll = self.get_roll()

        for student in self.students:

            if student.roll == roll:

                student.display()
                return

        print("Student not found!")

    # Update student
    def update_student(self):

        roll = self.get_roll()

        for student in self.students:

            if student.roll == roll:

                print("\nStudent found!")

                student.python = self.get_mark(
                    "new Python"
                )

                student.sql = self.get_mark(
                    "new SQL"
                )

                student.maths = self.get_mark(
                    "new Maths"
                )

                print("Student updated successfully!")
                return

        print("Student not found!")

    # Delete student
    def delete_student(self):

        roll = self.get_roll()

        for student in self.students:

            if student.roll == roll:

                print("\n========== STUDENT FOUND ==========")

                print("Name:", student.name)
                print("Roll:", student.roll)

                confirm = input(
                    "Are you sure you want to delete? (yes/no): "
                ).lower()

                if confirm == "yes":

                    self.students.remove(student)

                    print(
                        "Student deleted successfully!"
                    )

                else:

                    print("Student was not deleted.")

                return

        print("Student not found!")

    # Student result
    def student_result(self):

        roll = self.get_roll()

        for student in self.students:

            if student.roll == roll:

                student.display()
                return

        print("Student not found!")

    # Find topper
    def find_topper(self):

        if len(self.students) == 0:

            print("\nNo students found!")
            return

        topper = self.students[0]

        for student in self.students:

            if (
                student.calculate_total()
                > topper.calculate_total()
            ):

                topper = student

        print("\n========== TOP RANK STUDENT ==========")

        topper.display()

    # Save students to JSON
    def save_data(self):

        data = []

        for student in self.students:

            student_data = {
                "name": student.name,
                "roll": student.roll,
                "python": student.python,
                "sql": student.sql,
                "maths": student.maths
            }

            data.append(student_data)

        with open("students.json", "w") as file:

            json.dump(data, file, indent=4)

        print("\nStudent data saved successfully!")

    # Load students from JSON
    def load_data(self):

        try:

            with open("students.json", "r") as file:

                data = json.load(file)

            for item in data:

                student = Student(
                    item["name"],
                    item["roll"],
                    item["python"],
                    item["sql"],
                    item["maths"]
                )

                self.students.append(student)

            print("Student data loaded successfully!")

        except FileNotFoundError:

            print("No previous student data found.")

# MAIN PROGRAM
manager = StudentManager()

# Load previous data
manager.load_data()

while True:

    print("\n")
    print("==========================================")
    print("       STUDENT MANAGEMENT SYSTEM")
    print("==========================================")

    print("ADD    - Add Student")
    print("VIEW   - View Students")
    print("SEARCH - Search Student")
    print("UPDATE - Update Student")
    print("DELETE - Delete Student")
    print("RESULT - Student Result")
    print("TOPPER - Find Topper")
    print("SAVE   - Save Data")
    print("EXIT   - Exit")

    choice = input("\nEnter your choice: ").upper()

    if choice == "ADD":

        manager.add_student()

    elif choice == "VIEW":

        manager.view_students()

    elif choice == "SEARCH":

        manager.search_student()

    elif choice == "UPDATE":

        manager.update_student()

    elif choice == "DELETE":

        manager.delete_student()

    elif choice == "RESULT":

        manager.student_result()

    elif choice == "TOPPER":

        manager.find_topper()

    elif choice == "SAVE":

        manager.save_data()

    elif choice == "EXIT":

        manager.save_data()

        print( "\nThank you for using Student Management System!")

        break

    else:

        print("Invalid choice! Please try again.")