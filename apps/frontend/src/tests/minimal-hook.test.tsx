import { describe, it, expect } from "vitest";
import { renderHook, render, screen } from "@testing-library/react";
import { useState } from "react";

function useSimple() {
  const [val] = useState("hello");
  return val;
}

function SimpleComponent() {
  const [val] = useState("hello");
  return <div>{val}</div>;
}

describe("Minimal test", () => {
  it("useState works in render", () => {
    render(<SimpleComponent />);
    expect(screen.getByText("hello")).toBeDefined();
  });

  it("useState works in renderHook", () => {
    const { result } = renderHook(() => useSimple());
    expect(result.current).toBe("hello");
  });
});
