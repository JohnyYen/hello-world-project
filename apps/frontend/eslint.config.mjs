import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  
  {
    ignores: [".next/**", "next-env.d.ts"],
  },
  
  // ✅ Reglas esenciales para calidad de código
  {
    rules: {
      // Reglas de calidad
      "no-unused-vars": "warn",
      "no-console": "warn", 
      "no-debugger": "error",
      "no-unreachable": "error",
      
      // React best practices
      "react/react-in-jsx-scope": "off", // Next.js no necesita React import
      "react/prop-types": "off", // Usamos TypeScript
      
      // TypeScript rules - keep essential ones
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-unused-vars": "warn",
      
      // Accessibility - keep important ones
      "jsx-a11y/alt-text": "warn",
      "jsx-a11y/anchor-has-content": "warn",
    },
    linterOptions: {
      reportUnusedDisableDirectives: true, // Reportar reglas desactivadas innecesariamente
    },
  },
];

export default eslintConfig;
