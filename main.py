from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base, Student
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# ------------------ Pydantic Model ------------------

class StudentCreate(BaseModel):
    student_id: int
    name: str
    age: int
    course: str
    marks: int

# ------------------ API Routes ------------------

@app.post("/students/")
def create_student(student: StudentCreate):
    db: Session = SessionLocal()

    new_student = Student(**student.dict())

    db.add(new_student)
    db.commit()
    db.close()

    return {"message": "Student created successfully"}


@app.get("/students/")
def get_students():
    db = SessionLocal()
    students = db.query(Student).all()
    db.close()
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):
    db = SessionLocal()
    student = db.query(Student).filter(Student.student_id == student_id).first()
    db.close()
    return student


@app.put("/students/{student_id}")
def update_student(student_id: int, marks: int):
    db = SessionLocal()
    student = db.query(Student).filter(Student.student_id == student_id).first()

    if student:
        student.marks = marks
        db.commit()
        db.close()
        return {"message": "Updated successfully"}

    db.close()
    return {"error": "Student not found"}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()
    student = db.query(Student).filter(Student.student_id == student_id).first()

    if student:
        db.delete(student)
        db.commit()
        db.close()
        return {"message": "Deleted successfully"}

    db.close()
    return {"error": "Student not found"}


# ------------------ Mount Static (IMPORTANT: AT BOTTOM) ------------------

app.mount("/", StaticFiles(directory="static", html=True), name="static")