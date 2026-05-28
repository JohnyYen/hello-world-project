import { describe, it, expect } from "vitest";
import { decodeJWT } from "../jwt";

// Helper to create test JWTs (base64url encoded)
function createToken(payload: Record<string, unknown>): string {
  const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }))
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
  const body = btoa(JSON.stringify(payload))
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
  const signature = btoa("fake-signature")
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
  return `${header}.${body}.${signature}`;
}

describe("decodeJWT", () => {
  it("decodes a valid token and returns sub and exp", () => {
    const futureExp = Math.floor(Date.now() / 1000) + 3600; // 1 hour from now
    const token = createToken({ sub: "johny yen", exp: futureExp });

    const result = decodeJWT(token);

    expect(result).not.toBeNull();
    expect(result?.sub).toBe("johny yen");
    expect(result?.exp).toBe(futureExp);
  });

  it("returns null for an expired token", () => {
    const pastExp = Math.floor(Date.now() / 1000) - 3600; // 1 hour ago
    const token = createToken({ sub: "johny yen", exp: pastExp });

    const result = decodeJWT(token);

    expect(result).toBeNull();
  });

  it("returns null for a token without 3 parts", () => {
    expect(decodeJWT("only.two")).toBeNull();
    expect(decodeJWT("one")).toBeNull();
    expect(decodeJWT("")).toBeNull();
  });

  it("returns null for a token with malformed JSON payload", () => {
    const token = "header.😎.signature";
    expect(decodeJWT(token)).toBeNull();
  });

  it("returns null for null or undefined", () => {
    expect(decodeJWT(null as unknown as string)).toBeNull();
    expect(decodeJWT(undefined as unknown as string)).toBeNull();
  });
});
