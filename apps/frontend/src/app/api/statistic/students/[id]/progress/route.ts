import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.API_URL || "http://hwp-backend:8000";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const studentId = params.id;
    const token = request.cookies.get("auth_token")?.value;

    if (!token) {
      return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
    }

    const response = await fetch(
      `${API_BASE_URL}/api/v1/statistic/students/${studentId}/progress`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json(
        { detail: error.detail || "Error al obtener progreso" },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Route error:", error);
    return NextResponse.json(
      { detail: "Error: " + String(error) },
      { status: 500 }
    );
  }
}