# Hello World Frontend - AI Agent Ruleset

> **Skills Reference**: For detailed patterns, use these skills:
> - [`nextjs-15`](#) - App Router, Server Actions, streaming
> - [`react-19`](#) - React Compiler, no useMemo/useCallback
> - [`tailwind-4`](#) - cn() utility, modern CSS-first config
> - [`typescript`](#) - Explicit typing, strict mode
> - [`tdd`](#) - Test-Driven Development workflow

### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| App Router / Server Actions | `nextjs-15` |
| Committing changes | `prowler-commit` |
| Creating Zod schemas | `zod-4` |
| Creating/modifying React components | `react-19` |
| Fixing bug | `tdd` |
| Implementing feature | `tdd` |
| Refactoring code | `tdd` |
| Working on task | `tdd` |
| Working with Tailwind classes | `tailwind-4` |
| Writing TypeScript types/interfaces | `typescript` |

---

## CRITICAL RULES - NON-NEGOTIABLE

### Components & Rendering
- ALWAYS: Use Server Components by default. Use `"use client"` only for interactivity.
- ALWAYS: Use `cn()` utility for conditional classes.
- NEVER: Use `useMemo` or `useCallback` (rely on React Compiler).

### Data & Mutations
- ALWAYS: Use Server Actions for all mutations.
- ALWAYS: Validate data with Zod schemas.
- ALWAYS: UI text MUST be in Spanish.

### TypeScript
- ALWAYS: Explicit return types on all functions and components.
- ALWAYS: Prefer `interface` over `type` for object definitions.
- NEVER: Use `any`; use `unknown` or generics if the type is truly dynamic.

### API Client
- ALWAYS: When the communicate with de api, use the api client package `workspace/api-client-ts`
---

## TECH STACK

Next.js 15 | React 19 | Tailwind 4 | shadcn/ui | Zod | TypeScript 5

---

## PROJECT STRUCTURE

```
apps/frontend/src/
├── app/                 # App Router (pages & layouts)
├── components/
│   ├── ui/              # shadcn/ui components
│   └── {feature}/       # Domain-specific components
├── hooks/               # Custom React hooks
├── lib/                 # Utilities and shared logic
├── services/            # API interaction layers
└── types/               # Global TypeScript definitions
```

---

## COMMANDS

```bash
# Development
pnpm run dev

# Build & Lint
pnpm run build
pnpm run lint
```

---

## QA CHECKLIST

- [ ] UI text is in Spanish
- [ ] Zod validation applied to forms/actions
- [ ] Server Actions used for mutations
- [ ] `cn()` utility used for Tailwind classes
- [ ] No `any` types in new code
