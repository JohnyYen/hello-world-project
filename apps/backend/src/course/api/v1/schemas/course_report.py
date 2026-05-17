from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from datetime import date


class CourseResponse(BaseModel):
    id: UUID4
    name: str
    schoolYear: str = Field(alias="school_year")
    periodLabel: Optional[str] = Field(alias="period_label", default=None)
    startDate: date = Field(alias="start_date")
    endDate: date = Field(alias="end_date")
    totalStudents: int = 0

    model_config = {"from_attributes": True, "populate_by_name": True}


class CourseMetricsResponse(BaseModel):
    courseId: str = Field(alias="course_id")
    courseName: str = Field(alias="course_name")
    schoolYear: str = Field(alias="school_year")
    periodLabel: Optional[str] = Field(alias="period_label", default=None)
    totalStudents: int = 0  # ← AGREGADO: Total de estudiantes
    averageProgress: float
    averageGrade: float
    completionRate: float
    studentsCompleted: int
    averageActiveTime: float
    dailyActiveUsers: int = 0
    weeklyActiveUsers: int = 0
    averageSessionsPerStudent: float
    highPerformers: int
    mediumPerformers: int
    lowPerformers: int
    progressTrend: float = 0.0
    gradeTrend: float = 0.0
    engagementTrend: float = 0.0

    model_config = {"from_attributes": False, "populate_by_name": True}


class CourseProgressOverTimeResponse(BaseModel):
    date: str
    averageProgress: float
    averageGrade: float

    model_config = {"populate_by_name": True}


class StudentActivitySummaryResponse(BaseModel):
    date: str
    activeStudents: int
    totalTimeSpent: float
    averageSessionTime: float

    model_config = {"populate_by_name": True}


class CourseReportKPIsResponse(BaseModel):
    totalCourses: int
    totalStudents: int
    overallCompletionRate: float
    overallAverageGrade: float
    topPerformingCourse: Optional[CourseMetricsResponse] = None
    needsAttentionCourse: Optional[CourseMetricsResponse] = None
    yearOverYearProgress: float
    yearOverYearGrade: float

    model_config = {"populate_by_name": True}
