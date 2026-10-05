from typing import Annotated, Optional

from fastapi import FastAPI, Header, HTTPException, status, Cookie
from pydantic import BaseModel, Field


app = FastAPI(title="Student Attendance System")



class AttendanceHeaders(BaseModel):
    x_school_key: str
    x_app_version: str = "1.0"


class StudentCreate(BaseModel):
    matric_number: str
    full_name: Optional[str] = None
    level: int = Field(..., ge=100, le=600)
    department: str

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "matric_number": "AE-FUNAI-CS-001",
                    "full_name": "Victor Igbodo",
                    "level": 400,
                    "department": "Computer Science"
                }
            ]
        }
    }


class StudentResponse(BaseModel):
    matric_number: str
    full_name: Optional[str] = None
    level: int
    department: str



@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_student(
    headers: Annotated[AttendanceHeaders, Header()],
    student: StudentCreate,
) -> StudentResponse:

    if headers.x_school_key != "SCHOOL-2026":
        raise HTTPException(
            status_code=401,
            detail="Invalid school access key."
        )

    return student



class StudentCookies(BaseModel):
    session_id: str
    language: str = "en"


class GreetingResponse(BaseModel):
    message: str
    session_id: str


GREETINGS = {
    "en": "Welcome back, student!",
    "pidgin": "How far, student! You don come again!",
}



@app.get("/student/greeting", response_model=GreetingResponse)
async def greet_student(
    cookies: Annotated[StudentCookies, Cookie()],
) -> GreetingResponse:

    message = GREETINGS.get(
        cookies.language,
        "Welcome, student!"
    )

    return GreetingResponse(
        message=message,
        session_id=cookies.session_id
    )