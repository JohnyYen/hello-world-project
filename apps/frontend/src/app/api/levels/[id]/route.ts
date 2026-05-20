import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function GET(_request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const token = (await _request.cookies).get("auth_token")?.value;
  if (!token) {
    return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
  }

  const { id } = await params;

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/levels/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json({ detail: error.detail || "Error" }, { status: response.status });
    }
    return NextResponse.json(await response.json());
  } catch {
    return NextResponse.json({ detail: "Error de servidor" }, { status: 500 });
  }
}

export async function PUT(request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const token = (await request.cookies).get("auth_token")?.value;
  if (!token) {
    return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
  }

  const { id } = await params;
  const body = await request.json();

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/levels/${id}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json({ detail: error.detail || "Error" }, { status: response.status });
    }
    return NextResponse.json(await response.json());
  } catch {
    return NextResponse.json({ detail: "Error de servidor" }, { status: 500 });
  }
}

export async function DELETE(_request: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const token = (await _request.cookies).get("auth_token")?.value;
  if (!token) {
    return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
  }

  const { id } = await params;

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/levels/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json({ detail: error.detail || "Error" }, { status: response.status });
    }
    return NextResponse.json({ success: true });
  } catch {
    return NextResponse.json({ detail: "Error de servidor" }, { status: 500 });
  }
}
