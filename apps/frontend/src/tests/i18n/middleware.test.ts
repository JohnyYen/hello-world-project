import { describe, it, expect, vi, beforeEach } from "vitest";
import type { NextRequest } from "next/server";

const { mockIntlFn, mockCreateMiddleware } = vi.hoisted(() => {
  const intlFn = vi.fn();
  return {
    mockIntlFn: intlFn,
    mockCreateMiddleware: vi.fn(() => intlFn),
  };
});

vi.mock("next-intl/middleware", () => ({
  default: mockCreateMiddleware,
}));

vi.mock("@/i18n/routing", () => ({
  routing: {
    defaultLocale: "en",
    locales: ["en", "es"],
    localePrefix: "as-needed",
    localeDetection: false,
  },
}));

import { middleware } from "@/middleware";

function makeRequest(cookies: Record<string, string>): NextRequest {
  return {
    cookies: {
      get: (name: string) => {
        const v = cookies[name];
        return v ? { value: v } : undefined;
      },
    },
  } as unknown as NextRequest;
}

function makeResponse() {
  const h = new Map<string, string>();
  return {
    headers: {
      get: (k: string) => h.get(k),
      set: (k: string, v: string) => { h.set(k, v); },
      forEach: (cb: (v: string, k: string) => void) => h.forEach(cb),
    },
    headerMap: h,
  };
}

describe("i18n middleware", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("forwards request to next-intl middleware", () => {
    const res = makeResponse();
    mockIntlFn.mockReturnValue(res);
    const req = makeRequest({});
    middleware(req);
    expect(mockIntlFn).toHaveBeenCalledWith(req);
  });

  it("sets Authorization header when auth_token cookie exists", () => {
    const res = makeResponse();
    mockIntlFn.mockReturnValue(res);
    const req = makeRequest({ auth_token: "secret123" });
    middleware(req);
    expect(res.headerMap.get("Authorization")).toBe("Bearer secret123");
  });

  it("does not set Authorization when no auth_token cookie", () => {
    const res = makeResponse();
    mockIntlFn.mockReturnValue(res);
    const req = makeRequest({ other: "value" });
    middleware(req);
    expect(res.headerMap.has("Authorization")).toBe(false);
  });

  it("returns the response from intlMiddleware", () => {
    const res = makeResponse();
    mockIntlFn.mockReturnValue(res);
    const req = makeRequest({});
    expect(middleware(req)).toBe(res);
  });
});
