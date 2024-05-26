from sqlalchemy import func

from app.db import session
from app.models import Student, Grade, Subject, Teacher, Group


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    query = session.query(Student, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
                   .join(Grade).group_by(Student.id) \
                   .order_by(func.avg(Grade.grade).desc()).limit(5)
    result = query.all()
    print("Результат запиту select_1:")
    for student, avg_grade in result:
        print(f"Студент: {student.fullname}, Середній бал: {avg_grade}")

def select_2(subject_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    query = session.query(Student, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
                   .join(Grade).join(Subject) \
                   .filter(Subject.id == subject_id) \
                   .group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()
    result = query
    print("Результат запиту select_2:")
    if result:
        student, avg_grade = result
        print(f"Студент: {student.fullname}, Середній бал: {avg_grade}")
    else:
        print("Студент не знайдений.")

def select_3(subject_id):
    """Знайти середній бал у групах з певного предмета."""
    query = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
                   .select_from(Group) \
                   .join(Student).join(Grade).join(Subject) \
                   .filter(Subject.id == subject_id) \
                   .group_by(Group.name).order_by(func.avg(Grade.grade).desc())
    result = query.all()
    print("Результат запиту select_3:")
    for group_name, avg_grade in result:
        print(f"Група: {group_name}, Середній бал: {avg_grade}")

def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    query = session.query(func.round(func.avg(Grade.grade), 2))
    result = query.scalar()
    print("Результат запиту select_4:")
    print(f"Середній бал на потоці: {result}")

def select_5(teacher_id):
    """Знайти які курси читає певний викладач."""
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    result = teacher.disciplines if teacher else []
    print("Результат запиту select_5:")
    for subject in result:
        print(f"Предмет: {subject.name}")

def select_6(group_id):
    """Знайти список студентів у певній групі."""
    group = session.query(Group).filter(Group.id == group_id).first()
    result = group.students if group else []
    print("Результат запиту select_6:")
    for student in result:
        print(f"Студент: {student.fullname}")

def select_7(group_id, subject_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    query = session.query(Student, Grade) \
                   .join(Grade).join(Subject) \
                   .filter(Student.group_id == group_id, Subject.id == subject_id)
    result = query.all()
    print("Результат запиту select_7:")
    for student, grade in result:
        print(f"Студент: {student.fullname}, Оцінка: {grade.grade}")

def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    query = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
                   .select_from(Subject) \
                   .join(Grade).join(Teacher) \
                   .filter(Teacher.id == teacher_id) \
                   .group_by(Subject.id)
    result = query.all()
    print("Результат запиту select_8:")
    for avg_grade, in result:
        print(f"Середній бал: {avg_grade}")

def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    query = session.query(Subject) \
                   .select_from(Student) \
                   .join(Grade).join(Subject) \
                   .filter(Student.id == student_id)
    result = query.all()
    print("Результат запиту select_9:")
    for subject in result:
        print(f"Предмет: {subject.name}")

def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    query = session.query(Subject) \
                   .join(Grade).join(Student) \
                   .filter(Student.id == student_id, Grade.subject_id == Subject.id, Subject.teacher_id == teacher_id)
    result = query.all()
    print("Результат запиту select_10:")
    for subject in result:
        print(f"Предмет: {subject.name}")

# Виклики функцій для отримання результатів:
select_1()
select_2(subject_id=1)  # Передайте id предмета, наприклад, 1
select_3(subject_id=1)  # Передайте id предмета, наприклад, 1
select_4()
select_5(teacher_id=1)  # Передайте id викладача, наприклад, 1
select_6(group_id=1)    # Передайте id групи, наприклад, 1
select_7(group_id=1, subject_id=1)  # Передайте id групи та id предмета, наприклад, 1 і 1
select_8(teacher_id=1)  # Передайте id викладача, наприклад, 1
select_9(student_id=1)  # Передайте id студента, наприклад, 1
select_10(student_id=1, teacher_id=1)  # Передайте id студента та id викладача, наприклад, 1 і 1
