from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CourseCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    school_year: str = Field(..., alias="schoolYear")
    period_label: str = Field(..., alias="periodLabel")
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")
    student_ids: list[UUID] = Field(default=[], alias="studentIds")
    professor_ids: list[UUID] = Field(default=[], alias="professorIds")

    model_config = {"populate_by_name": True}

    @field_validator("end_date")
    @classmethod
    def end_date_must_be_after_start(cls, v, info):
        if "start_date" in info.data and v <= info.data["start_date"]:
            raise ValueError("end_date debe ser posterior a start_date")
        return v


class CourseUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    school_year: Optional[str] = Field(None, alias="schoolYear")
    period_label: Optional[str] = Field(None, alias="periodLabel")
    start_date: Optional[date] = Field(None, alias="startDate")
    end_date: Optional[date] = Field(None, alias="endDate")
    student_ids: Optional[list[UUID]] = Field(None, alias="studentIds")
    professor_ids: Optional[list[UUID]] = Field(None, alias="professorIds")
    is_active: Optional[bool] = Field(None, alias="isActive")

    model_config = {"populate_by_name": True}


class EnrollmentRequest(BaseModel):
    student_ids: list[UUID] = Field(..., alias="studentIds")

    model_config = {"populate_by_name": True}


class StudentEnrollmentResponse(BaseModel):
    student_id: UUID = Field(alias="studentId")
    name: str
    email: str
    enrolled_at: str = Field(alias="enrolledAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


class ProfessorAssignmentResponse(BaseModel):
    professor_id: UUID = Field(alias="professorId")
    name: str
    email: str

    model_config = {"from_attributes": True, "populate_by_name": True}


class CourseResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    school_year: str = Field(alias="schoolYear")
    period_label: str = Field(alias="periodLabel")
    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    is_active: bool = Field(alias="isActive")
    student_count: int = 0
    professor_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True, "populate_by_name": True}


class CourseDetailResponse(CourseResponse):
    students: list[StudentEnrollmentResponse] = []
    professors: list[ProfessorAssignmentResponse] = []


class PaginatedCourseListResponse(BaseModel):
    items: list[CourseResponse]
    total: int
    skip: int
    limit: int
