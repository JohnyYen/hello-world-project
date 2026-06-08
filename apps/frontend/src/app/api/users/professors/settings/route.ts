import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function GET(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;

  if (!token) {
    return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/users/professors/settings`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json(
        { detail: error.detail || "Error al obtener configuración" },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data.data || data);
  } catch {
    return NextResponse.json(
      { detail: "Error de servidor" },
      { status: 500 }
    );
  }
}

export async function PUT(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;

  if (!token) {
    return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
  }

  try {
    const body = await request.json();

    const response = await fetch(`${API_BASE_URL}/api/v1/users/professors/settings`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json(
        { detail: error.detail || "Error al actualizar configuración" },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data.data || data);
  } catch {
    return NextResponse.json(
      { detail: "Error de servidor" },
      { status: 500 }
    );
  }
}
