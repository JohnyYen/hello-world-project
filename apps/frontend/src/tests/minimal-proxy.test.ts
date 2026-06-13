import { describe, it, expect } from "vitest";

describe("process.env proxy check", () => {
  it("has a normal process.env", () => {
    console.log("process.env.NODE_ENV:", process.env.NODE_ENV);
    console.log("process.env constructor:", Object.getPrototypeOf(process.env)?.constructor?.name);
    console.log("isProxy:", Object.prototype.toString.call(process.env));
    const desc = Object.getOwnPropertyDescriptor(process.env, 'NODE_ENV');
    console.log("descriptor:", desc);
    expect(true).toBe(true);
  });
});
