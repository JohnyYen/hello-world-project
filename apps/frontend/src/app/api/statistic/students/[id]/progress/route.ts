import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8010";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id: studentId } = await params;
  const token = request.cookies.get("auth_token")?.value;

  if (!token) {
    return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/statistic/students/${studentId}/progress`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        cache: "no-store",
      }
    );

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json(
        { detail: error.detail || "Error al obtener progreso del estudiante" },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json(
      { detail: "Error de servidor" },
      { status: 500 }
    );
  }
}
