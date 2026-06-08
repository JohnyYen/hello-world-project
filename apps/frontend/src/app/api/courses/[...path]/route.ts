import { NextRequest, NextResponse } from "next/server";

function getBackendUrl(): string {
  // Server-side: check if running in Docker
  if (process.env.API_URL) {
    return process.env.API_URL;
  }
  // Fallback: use NEXT_PUBLIC_API_URL or default
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
}

export async function GET(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;

  if (!token) {
    return NextResponse.json({ detail: "Unauthorized" }, { status: 401 });
  }

  const { pathname, search } = new URL(request.url);
  // Transform /api/courses/... to /api/v1/courses/...
  const backendPath = pathname.replace("/api/courses", "/api/v1/courses");
  const queryString = search ? `?${search.slice(1)}` : "";
  const backendUrl = `${getBackendUrl()}${backendPath}${queryString}`;

  try {
    const response = await fetch(backendUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      return NextResponse.json(
        { detail: error.detail || `Error ${response.status}: ${response.statusText}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json(
      { detail: "Server error" },
      { status: 500 }
    );
  }
}
