import streamlit as st
import json
import os


# STUDENT CLASS

class Student:

    def __init__(self, name, roll, python, sql, maths):
        self.name = name
        self.roll = roll
        self.python = python
        self.sql = sql
        self.maths = maths

    def calculate_total(self):
        return self.python + self.sql + self.maths

    def calculate_average(self):
        return self.calculate_total() / 3


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

    def get_status(self):
        if (
            self.python >= 40
            and self.sql >= 40
            and self.maths >= 40
        ):
            return "PASS"
        else:
            return "FAIL"


# STUDENT MANAGER CLASS

class StudentManager:

    def __init__(self):
        self.students = []

    # Check roll number

    def roll_exists(self, roll):

        for student in self.students:

            if student.roll == roll:
                return True

        return False

    # Add student

    def add_student(self, name, roll, python, sql, maths):

        if self.roll_exists(roll):
            return False

        student = Student(
            name,
            roll,
            python,
            sql,
            maths)

        self.students.append(student)

        return True


    # Search student

    def search_student(self, roll):

        for student in self.students:

            if student.roll == roll:
                return student

        return None

    # Delete student

    def delete_student(self, roll):

        student = self.search_student(roll)

        if student:

            self.students.remove(student)

            return True

        return False

    # Update student

    def update_student(
        self,
        roll,
        python,
        sql,
        maths):

        student = self.search_student(roll)

        if student:

            student.python = python
            student.sql = sql
            student.maths = maths

            return True

        return False

    # Find topper


    def find_topper(self):

        if len(self.students) == 0:
            return None

        topper = self.students[0]

        for student in self.students:

            if ( student.calculate_total() > topper.calculate_total() ):
                topper = student

        return topper

    # Save data
  
    def save_data(self):

        data = []

        for student in self.students:

            student_data = {

                "name": student.name,
                "roll": student.roll,
                "python": student.python,
                "sql": student.sql,
                "maths": student.maths}

            data.append(student_data)

        with open("students.json", "w") as file:

            json.dump(
                data,
                file,
                indent=4)

    # --------------------------------------
    # Load data
    # --------------------------------------

    def load_data(self):

        if not os.path.exists("students.json"):
            return

        with open("students.json", "r") as file:

            data = json.load(file)

        self.students = []

        for item in data:

            student = Student(
                item["name"],
                item["roll"],
                item["python"],
                item["sql"],
                item["maths"] )

            self.students.append(student)

# STREAMLIT SETUP

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide")

# CREATE MANAGER

if "manager" not in st.session_state:

    manager = StudentManager()

    manager.load_data()

    st.session_state.manager = manager


manager = st.session_state.manager

# TITLE

st.title("🎓 Student Management System")

st.write(
    "Manage student records, marks, results and topper information.")

# SIDEBAR MENU

st.sidebar.title("📚 MENU")

choice = st.sidebar.selectbox(

    "Choose an option",

    [
        "ADD",
        "VIEW",
        "SEARCH",
        "UPDATE",
        "DELETE",
        "RESULT",
        "TOPPER",
        "SAVE"])

# ADD STUDENT


def reset_student_fields():
    st.session_state.student_name = ""
    st.session_state.student_roll = 1
    st.session_state.student_python = 0
    st.session_state.student_sql = 0
    st.session_state.student_maths = 0

if choice == "ADD":

    st.header("➕ Add Student")

    if "student_name" not in st.session_state:
        st.session_state.student_name = ""
        st.session_state.student_roll = 1
        st.session_state.student_python = 0
        st.session_state.student_sql = 0
        st.session_state.student_maths = 0

    name = st.text_input("Student Name", key="student_name")
    roll = st.number_input("Roll Number", 1, step=1, key="student_roll")
    python = st.number_input("Python Mark", 0, 100, step=1, key="student_python")
    sql = st.number_input("SQL Mark", 0, 100, step=1, key="student_sql")
    maths = st.number_input("Maths Mark", 0, 100, step=1, key="student_maths")

    col1, col2 = st.columns(2)

    with col1:
        add = st.button("➕ Add Student")

    with col2:
        st.button(
        "➡️ Add Next Student",
        on_click=reset_student_fields)

    if add:
        if not name.strip():
            st.error("Name cannot be empty!")
        elif not name.replace(" ", "").isalpha():
            st.error("Name should contain letters only!")
        elif manager.roll_exists(roll):
            st.error("Roll number already exists!")
        else:
            manager.add_student(name, roll, python, sql, maths)
            manager.save_data()
            st.success(f"Student '{name}' added successfully! 🎉")

# VIEW STUDENTS

elif choice == "VIEW":

    st.header("👥 Student List")

    if len(manager.students) == 0:

        st.info("No students found!")

    else:

        data = []

        for student in manager.students:

            data.append({

                "Name": student.name,
                "Roll": student.roll,
                "Python": student.python,
                "SQL": student.sql,
                "Maths": student.maths,
                "Total": student.calculate_total(),
                "Average": round(
                    student.calculate_average(),
                    2
                ),
                "Grade": student.calculate_grade(),
                "Status": student.get_status()})

        st.dataframe(
            data,
            use_container_width=True)


# SEARCH STUDENT

elif choice == "SEARCH":

    st.header("🔍 Search Student")

    roll = st.number_input(
        "Enter Roll Number",
        min_value=1,
        step=1)

    if st.button("Search"):

        student = manager.search_student(roll)

        if student:

            st.success(
                f"Student Found: {student.name}")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Python",
                student.python)

            col2.metric(
                "SQL",
                student.sql )

            col3.metric(
                "Maths",
                student.maths)

            st.write(
                "### 📊 Result")

            st.write(
                f"**Total:** {student.calculate_total()}")

            st.write(
                f"**Average:** "
                f"{student.calculate_average():.2f}")

            st.write(
                f"**Grade:** "
                f"{student.calculate_grade()}")

            st.write(
                f"**Status:** "
                f"{student.get_status()}")

        else:
            st.error("Student not found!")

# UPDATE STUDENT

elif choice == "UPDATE":

    st.header("✏️ Update Student")

    roll = st.number_input(
        "Enter Roll Number",
        min_value=1,
        step=1)

    python = st.number_input(
        "New Python Mark",
        min_value=0,
        max_value=100,
        step=1)

    sql = st.number_input(
        "New SQL Mark",
        min_value=0,
        max_value=100,
        step=1)

    maths = st.number_input(
        "New Maths Mark",
        min_value=0,
        max_value=100,
        step=1)

    if st.button("Update Student"):

        if manager.update_student(
            roll,
            python,
            sql,
            maths):

            manager.save_data()

            st.success("Student updated successfully! ✅")

        else:
            st.error("Student not found!")

# DELETE STUDENT

elif choice == "DELETE":

    st.header("🗑️ Delete Student")

    roll = st.number_input(
        "Enter Roll Number",
        min_value=1,
        step=1)

    if st.button("Delete Student"):

        student = manager.search_student(roll)

        if student:

            manager.delete_student(roll)

            manager.save_data()

            st.success( "Student deleted successfully!")

        else:
            st.error("Student not found!")

# STUDENT RESULT

elif choice == "RESULT":

    st.header("📊 Student Result")

    roll = st.number_input(
        "Enter Roll Number",
        min_value=1,
        step=1)

    if st.button("View Result"):

        student = manager.search_student(roll)

        if student:

            st.subheader(
                f"🎓 {student.name}")

            st.write(
                f"**Roll Number:** {student.roll}")

            st.write(
                f"**Total:** "
                f"{student.calculate_total()}" )

            st.write(
                f"**Average:** "
                f"{student.calculate_average():.2f}" )

            st.write(
                f"**Grade:** "
                f"{student.calculate_grade()}")

            if student.get_status() == "PASS":
                st.success("PASS ✅")

            else:
                st.error("FAIL ❌")

        else:
            st.error("Student not found!" )


# TOPPER

elif choice == "TOPPER":

    st.header("🏆 Top Rank Student")

    topper = manager.find_topper()

    if topper:

        st.success(
            f"🏆 Topper: {topper.name}")

        st.write(
            f"**Roll:** {topper.roll}")

        st.write(
            f"**Total Marks:** "
            f"{topper.calculate_total()}")

        st.write(
            f"**Average:** "
            f"{topper.calculate_average():.2f}")

        st.write(f"**Grade:** "
            f"{topper.calculate_grade()}" )

    else:
        st.info("No students found!")


# ==========================================
# SAVE
# ==========================================

elif choice == "SAVE":

    st.header("💾 Save Data")

    if st.button("Save Student Data"):

        manager.save_data()

        st.success(
            "Student data saved successfully! 💾")