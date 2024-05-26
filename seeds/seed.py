import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from app.db import session
from app.models import Student, Group, Teacher, Subject, Grade


fake = Faker('uk-UA')


def seed():
    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)

    teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
    session.add_all(teachers)

    subjects = [Subject(name=fake.word(), teacher=random.choice(teachers)) for _ in range(8)]
    session.add_all(subjects)

    students = []
    for _ in range(50):
        student = Student(fullname=fake.name(), group=random.choice(groups))
        students.append(student)
        session.add(student)

    for student in students:
        for subject in subjects:
            grade = Grade(
                grade=random.randint(1, 100),
                grade_date=fake.date_between(start_date='-1y', end_date='today'),
                student=student,
                subject=subject
            )
            session.add(grade)

if __name__ == '__main__':
    try:
        seed()
        session.commit()

    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
