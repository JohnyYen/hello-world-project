import { describe, it, expect, vi, beforeEach } from "vitest";
import { GET } from "../route";

// Mock NextResponse only (NextRequest is just an interface, we can build the object manually)
vi.mock("next/server", () => ({
  NextResponse: {
    json: vi.fn((body: unknown, init?: { status?: number }) => {
      const status = init?.status || 200;
      return {
        status,
        json: async () => body,
        ...(body as Record<string, unknown>),
      };
    }),
  },
}));

function base64url(str: string): string {
  return btoa(str).replace(/=/g, "").replace(/\+/g, "-").replace(/\//g, "_");
}

function createToken(payload: Record<string, unknown>): string {
  const header = base64url(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body = base64url(JSON.stringify(payload));
  const sig = base64url("fake-signature");
  return `${header}.${body}.${sig}`;
}

function createMockRequest(token?: string) {
  return {
    cookies: {
      get: vi.fn((name: string) => {
        if (name === "auth_token" && token) {
          return { value: token };
        }
        return undefined;
      }),
    },
  };
}

beforeEach(() => {
  vi.clearAllMocks();
});

describe("GET /api/auth/me", () => {
  it("returns 401 when no token is present", async () => {
    const request = createMockRequest();
    const response = await GET(request as never);

    expect(response.status).toBe(401);
    const body = await response.json();
    expect(body.authenticated).toBe(false);
  });

  it("returns 401 when the backend rejects the token (expired/invalid)", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce(
      new Response(null, { status: 401 })
    );

    const expiredToken = createToken({
      sub: "johny yen",
      exp: Math.floor(Date.now() / 1000) - 3600,
      email: "johny@test.com",
    });

    const request = createMockRequest(expiredToken);
    const response = await GET(request as never);

    expect(response.status).toBe(401);
    const body = await response.json();
    expect(body.authenticated).toBe(false);
  });

  it("returns user data when backend accepts the token", async () => {
    const backendUser = {
      id: 1,
      username: "johny yen",
      email: "johny@test.com",
      name: "Johny",
      lastname: "Yen",
      is_active: true,
      role: { id: 2, role_name: "professor" },
    };

    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce(
      new Response(JSON.stringify({ data: backendUser }), { status: 200 })
    );

    const validToken = createToken({
      sub: "johny yen",
      exp: Math.floor(Date.now() / 1000) + 3600,
    });

    const request = createMockRequest(validToken);
    const response = await GET(request as never);

    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.authenticated).toBe(true);
    expect(body.user.username).toBe("johny yen");
  });
});
