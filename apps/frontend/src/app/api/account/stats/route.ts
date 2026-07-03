import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface CourseItem {
  studentCount?: number;
  isActive?: boolean;
}

export async function GET(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;

  if (!token) {
    return NextResponse.json({ detail: "No autenticado" }, { status: 401 });
  }

  try {
    // Fetch teacher's courses to derive stats
    const response = await fetch(`${API_BASE_URL}/api/v1/courses/management?skip=0&limit=1000`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    if (!response.ok) {
      // If the courses endpoint isn't available, return empty data
      return NextResponse.json({ activeCourses: 0, totalStudents: 0 });
    }

    const data = await response.json();
    const courses: CourseItem[] = data?.items ?? data?.data ?? [];

    const activeCourses = courses.filter(
      (c: CourseItem) => c.isActive !== false
    ).length;

    const totalStudents = courses.reduce(
      (sum: number, c: CourseItem) => sum + (c.studentCount ?? 0),
      0
    );

    return NextResponse.json({
      activeCourses,
      totalStudents,
    });
  } catch {
    // Silently fail — stats are not critical for the page
    return NextResponse.json({ activeCourses: 0, totalStudents: 0 });
  }
}
