import { describe, it, expect } from "vitest";

function flattenKeys(obj: Record<string, unknown>, prefix = ""): string[] {
  const keys: string[] = [];
  for (const [key, value] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}.${key}` : key;
    if (value && typeof value === "object" && !Array.isArray(value)) {
      keys.push(...flattenKeys(value as Record<string, unknown>, fullKey));
    } else {
      keys.push(fullKey);
    }
  }
  return keys.sort();
}

describe("Translation keys parity", () => {
  it("en.json and es.json should have identical keys", async () => {
    const enMessages = await import("../../../messages/en.json");
    const esMessages = await import("../../../messages/es.json");

    const en = enMessages.default ?? enMessages;
    const es = esMessages.default ?? esMessages;

    const enKeys = flattenKeys(en);
    const esKeys = flattenKeys(es);

    const enOnly = enKeys.filter((k) => !esKeys.includes(k));
    const esOnly = esKeys.filter((k) => !enKeys.includes(k));

    if (enOnly.length > 0 || esOnly.length > 0) {
      const diff: string[] = [];
      if (enOnly.length > 0) {
        diff.push(`Keys missing in es.json (${enOnly.length}):`);
        diff.push(enOnly.map((k) => `  - ${k}`).join("\n"));
      }
      if (esOnly.length > 0) {
        diff.push(`Keys missing in en.json (${esOnly.length}):`);
        diff.push(esOnly.map((k) => `  - ${k}`).join("\n"));
      }
      throw new Error(diff.join("\n"));
    }

    expect(enKeys).toEqual(esKeys);
  });

  it("should have the same number of top-level sections", async () => {
    const enMessages = await import("../../../messages/en.json");
    const esMessages = await import("../../../messages/es.json");

    const en = enMessages.default ?? enMessages;
    const es = esMessages.default ?? esMessages;

    const enSections = Object.keys(en).sort();
    const esSections = Object.keys(es).sort();

    expect(enSections).toEqual(esSections);
  });
});
