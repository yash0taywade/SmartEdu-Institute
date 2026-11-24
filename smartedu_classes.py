from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, age, city):
        self.name = name
        self.__age = age
        self.city = city

    @abstractmethod
    def get_summary(self):
        pass


class Student(Person):
    def __init__(self, name, age, city, roll, marks, fees):
        super().__init__(name, age, city)
        self.roll = roll
        self.marks = marks
        self.__fees = fees

    def get_fees(self):
        return self.__fees

    def average(self):
        return sum(self.marks.values()) / len(self.marks)

    def grade(self):
        avg = self.average()
        if avg >= 85: return "A"
        elif avg >= 70: return "B"
        elif avg >= 55: return "C"
        else: return "F"

    def to_dict(self):
        d = {
            'Name': self.name,
            'City': self.city,
            'Roll': self.roll
        }
        d.update(self.marks)
        d['Average'] = round(self.average(), 2)
        d['Grade'] = self.grade()
        d['Fees'] = self.get_fees()
        return d

    def get_summary(self):
        return f"{self.name} | Avg: {self.average():.2f} | Grade: {self.grade()}"


class ScholarshipStudent(Student):
    def __init__(self, name, age, city, roll, marks, fees, scholarship):
        super().__init__(name, age, city, roll, marks, fees)
        self.scholarship = scholarship

    def effective_fees(self):
        return self.get_fees() * (1 - self.scholarship / 100)

    def get_summary(self):
        return super().get_summary() + f" | Scholarship: {self.scholarship}%"


class Batch:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.__students = []

    def add_student(self, student):
        self.__students.append(student)

    def batch_average(self):
        if not self.__students:
            return 0.0
        return sum(s.average() for s in self.__students) / len(self.__students)

    def top_student(self):
        return max(self.__students, key=lambda s: s.average(), default=None)

    def at_risk(self):
        return [s for s in self.__students if s.average() < 55]


class ClassReport:
    def __init__(self, students):
        self.students = students

    def class_average(self):
        if not self.students:
            return 0.0
        return sum(s.average() for s in self.students) / len(self.students)

    def top_student(self):
        return max(self.students, key=lambda s: s.average(), default=None)

    def at_risk_students(self):
        return [s for s in self.students if s.average() < 55]
