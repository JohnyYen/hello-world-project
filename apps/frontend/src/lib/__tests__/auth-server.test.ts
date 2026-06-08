import { describe, it, expect, vi, beforeEach } from "vitest";
import { getServerUser } from "../auth-server";

function base64url(str: string): string {
  return btoa(str).replace(/=/g, "").replace(/\+/g, "-").replace(/\//g, "_");
}

function createToken(payload: Record<string, unknown>): string {
  const header = base64url(JSON.stringify({ alg: "HS256", typ: "JWT" }));
  const body = base64url(JSON.stringify(payload));
  const sig = base64url("fake-signature");
  return `${header}.${body}.${sig}`;
}

const mockCookieGet = vi.fn();
vi.mock("next/headers", () => ({
  cookies: vi.fn(() => ({
    get: mockCookieGet,
  })),
}));

beforeEach(() => {
  vi.clearAllMocks();
});

describe("getServerUser", () => {
  it("returns null when no cookie is present", async () => {
    mockCookieGet.mockReturnValue(undefined);

    const result = await getServerUser();

    expect(result.user).toBeNull();
    expect(result.token).toBeNull();
  });

  it("returns null when the token is expired", async () => {
    const expiredToken = createToken({
      sub: "johny yen",
      exp: Math.floor(Date.now() / 1000) - 3600,
    });

    mockCookieGet.mockReturnValue({ value: expiredToken });
    // No fetch calls should be made — decodeJWT should reject before that

    const result = await getServerUser();

    expect(result.user).toBeNull();
    expect(result.token).toBeNull();
  });

  it("returns user data when backend accepts the token", async () => {
    const validToken = createToken({
      sub: "johny yen",
      exp: Math.floor(Date.now() / 1000) + 3600,
    });

    mockCookieGet.mockReturnValue({ value: validToken });

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

    const result = await getServerUser();

    expect(result.user).not.toBeNull();
    expect(result.user?.username).toBe("johny yen");
    expect(result.token).toBe(validToken);
  });

  it("returns null when backend rejects the token (no fake user)", async () => {
    const validToken = createToken({
      sub: "johny yen",
      exp: Math.floor(Date.now() / 1000) + 3600,
    });

    mockCookieGet.mockReturnValue({ value: validToken });

    // Both API calls fail
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(null, { status: 401 })
    );

    const result = await getServerUser();

    // Should NOT create a fake user from JWT data
    expect(result.user).toBeNull();
    expect(result.token).toBeNull();
  });
});
