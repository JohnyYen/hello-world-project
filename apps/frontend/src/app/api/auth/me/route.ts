import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function GET(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;

  if (!token) {
    return NextResponse.json({ authenticated: false }, { status: 401 });
  }

  try {
    // Try to get professor profile
    const response = await fetch(`${API_BASE_URL}/api/v1/users/professors/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    if (response.ok) {
      const data = await response.json();
      return NextResponse.json({
        authenticated: true,
        user: data.data || data,
      });
    }

    // Fallback: decode JWT to get basic user info
    const parts = token.split(".");
    if (parts.length === 3) {
      const payload = JSON.parse(
        atob(parts[1].replace(/-/g, "+").replace(/_/g, "/"))
      );
      return NextResponse.json({
        authenticated: true,
        user: {
          id: payload.sub || "",
          username: payload.sub || "",
          email: payload.email || "",
          name: payload.sub || "",
          lastname: null,
          is_active: true,
        },
      });
    }

    return NextResponse.json({ authenticated: false }, { status: 401 });
  } catch {
    return NextResponse.json({ authenticated: false }, { status: 500 });
  }
}
