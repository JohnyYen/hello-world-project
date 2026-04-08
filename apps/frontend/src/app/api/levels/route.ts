import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8010";

export async function GET(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;
  if (!token) {
    return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const skip = searchParams.get("skip") || "0";
  const limit = searchParams.get("limit") || "100";

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/levels?skip=${skip}&limit=${limit}`, {
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

export async function POST(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;
  if (!token) {
    return NextResponse.json({ detail: "No autorizado" }, { status: 401 });
  }

  const body = await request.json();

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/levels`, {
      method: "POST",
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
