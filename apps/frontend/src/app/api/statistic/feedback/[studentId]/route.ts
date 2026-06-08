import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL =
  process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ studentId: string }> }
): Promise<NextResponse> {
  const token = request.cookies.get("auth_token")?.value;

  if (!token) {
    return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
  }

  try {
    const { studentId } = await params;
    const { searchParams } = new URL(request.url);
    const skip = searchParams.get("skip") ?? "0";
    const limit = searchParams.get("limit") ?? "10";

    const response = await fetch(
      `${API_BASE_URL}/api/v1/statistic/feedback/${studentId}?skip=${skip}&limit=${limit}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        cache: "no-store",
      }
    );

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json(
        { detail: error.detail || "Error al obtener historial de feedback" },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Feedback GET route error:", error);
    return NextResponse.json(
      { detail: "Error de servidor" },
      { status: 500 }
    );
  }
}
