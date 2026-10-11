from pathlib import Path
import csv

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_PATH = Path(__file__).resolve().parent.parent / "q-fastapi.csv"


def load_students():
    students = []

    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            students.append({
                "studentId": int(row["studentId"]),
                "class": row["class"],
            })

    return students


@app.get("/")
async def get_students(
    class_: list[str] | None = Query(default=None, alias="class")
):
    students = load_students()

    if class_:
        students = [
            student
            for student in students
            if student["class"] in class_
        ]

    return {
        "students": students
    }
