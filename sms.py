import json
import os

DATA_FILE = "data.json"


class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Address: {self.address}")


class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def display_student_info(self):
        self.display_person_info()
        print(f"Student ID: {self.student_id}")
        print(f"Enrolled Courses: {', '.join(self.courses)}")
        print(f"Grades: {self.grades}")


class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def display_course_info(self):
        print(f"Course Name: {self.course_name}, Code: {self.course_code}, Instructor: {self.instructor}")
        print("Enrolled Students:", ", ".join(student.name for student in self.students))


def save_data(students, courses):
    try:
        data = {
            "students": [
                {
                    "name": student.name,
                    "age": student.age,
                    "address": student.address,
                    "student_id": student.student_id,
                    "grades": student.grades,
                    "courses": student.courses
                }
                for student in students.values()
            ],
            "courses": [
                {
                    "course_name": course.course_name,
                    "course_code": course.course_code,
                    "instructor": course.instructor,
                    "students": [student.student_id for student in course.students]
                }
                for course in courses.values()
            ]
        }
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print("All student and course data saved successfully.")
    except IOError as e:
        print(f"Error saving data: {e}")


def load_data():
    if not os.path.exists(DATA_FILE):
        print("No saved data found. Starting with an empty dataset.")
        return {}, {}

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        students = {
            item["student_id"]: Student(item["name"], item["age"], item["address"], item["student_id"])
            for item in data["students"]
        }
        for student_data in data["students"]:
            student = students[student_data["student_id"]]
            student.grades = student_data["grades"]
            student.courses = student_data["courses"]

        courses = {
            item["course_code"]: Course(item["course_name"], item["course_code"], item["instructor"])
            for item in data["courses"]
        }
        for course_data in data["courses"]:
            course = courses[course_data["course_code"]]
            for student_id in course_data["students"]:
                student = students.get(student_id)
                if student:
                    course.add_student(student)

        print("Data loaded successfully.")
        return students, courses
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading data: {e}")
        return {}, {}


def main():
    students, courses = load_data()
    while True:
        print("\n==== Student Management System ====")
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")

        choice = input("Select Option: ")

        if choice == "1":
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            address = input("Enter Address: ")
            student_id = input("Enter Student ID: ")
            students[student_id] = Student(name, age, address, student_id)
            print(f"Student {name} (ID: {student_id}) added successfully.")
            save_data(students, courses)

        elif choice == "2":
            course_name = input("Enter Course Name: ")
            course_code = input("Enter Course Code: ")
            instructor = input("Enter Instructor Name: ")
            courses[course_code] = Course(course_name, course_code, instructor)
            print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")
            save_data(students, courses)

        elif choice == "3":
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            student = students.get(student_id)
            course = courses.get(course_code)
            if student and course:
                student.enroll_course(course.course_name)
                course.add_student(student)
                print(
                    f"Student {student.name} (ID: {student_id}) enrolled in {course.course_name} (Code: {course_code}).")
                save_data(students, courses)
            else:
                print("Invalid Student ID or Course Code.")

        elif choice == "4":
            student_id = input("Enter Student ID: ")
            course_code = input("Enter Course Code: ")
            grade = input("Enter Grade: ")
            student = students.get(student_id)
            course = courses.get(course_code)
            if student and course and course.course_name in student.courses:
                student.add_grade(course.course_name, grade)
                print(f"Grade {grade} added for {student.name} in {course.course_name}.")
                save_data(students, courses)
            else:
                print("Invalid Student ID or Course Code, or the student is not enrolled in this course.")

        elif choice == "5":
            student_id = input("Enter Student ID: ")
            student = students.get(student_id)
            if student:
                print("Student Information:")
                student.display_student_info()
            else:
                print("Student not found.")

        elif choice == "6":
            course_code = input("Enter Course Code: ")
            course = courses.get(course_code)
            if course:
                print("Course Information:")
                course.display_course_info()
            else:
                print("Course not found.")

        elif choice == "7":
            save_data(students, courses)

        elif choice == "8":
            students, courses = load_data()

        elif choice == "0":
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
