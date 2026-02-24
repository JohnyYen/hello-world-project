# AGENTS.md - Coding Guidelines for AI Agents

## Build/Lint Commands

```bash
# Development
npm run dev              # Start dev server with Turbopack

# Build
npm run build            # Production build with Turbopack
npm start                # Start production server

# Linting
npm run lint             # Run ESLint
```

> **Note:** No test framework is configured yet. To add tests, install Jest/Vitest/Playwright first.

## Tech Stack

- **Framework:** Next.js 15.5.4 with App Router
- **Language:** TypeScript 5 (strict mode enabled)
- **Styling:** Tailwind CSS v4 with CSS-first config
- **UI Components:** shadcn/ui + Radix UI primitives
- **State:** React hooks, Server Actions for mutations
- **Validation:** Zod v4
- **Charts:** Recharts
- **Icons:** Lucide React + Tabler Icons

## Code Style Guidelines

### Imports (Priority Order)

1. React/Next imports
2. Third-party libraries
3. `@/components/ui/*` (shadcn components)
4. `@/components/*` (custom components)
5. `@/hooks/*`, `@/lib/*`, `@/types/*`
6. Relative imports ( `./` last)

```tsx
import { useState } from "react";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { StudentTable } from "@/components/student";
import { useNotifications } from "@/hooks/use-notifications";
import { cn } from "@/lib/utils";
import StudentForm from "./student-form";
```

### Formatting

- Use **semicolons** always
- **Double quotes** for strings
- **2 spaces** indentation
- **Trailing commas** in multi-line objects/arrays
- Max line length: 100 characters

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `StudentTable`, `LoginForm` |
| Hooks | camelCase with `use` prefix | `useNotifications`, `useStudentData` |
| Types/Interfaces | PascalCase | `Student`, `ApiResponse<T>` |
| Constants | UPPER_SNAKE_CASE | `CHART_COLORS`, `API_BASE_URL` |
| Functions | camelCase | `handleSubmit`, `loadStudentData` |
| Server Actions | camelCase with `Action` suffix | `loginAction`, `createStudentAction` |
| Files (components) | kebab-case | `student-table.tsx`, `login-form.tsx` |
| Files (utils) | camelCase | `utils.ts`, `colors.ts` |

### TypeScript Rules

- **Always** use explicit return types on functions
- Prefer `interface` over `type` for object shapes
- Use `type` for unions, tuples, and mapped types
- Avoid `any` - use `unknown` or proper generics
- Enable strict mode (already configured)

```tsx
// ✅ Good
interface StudentProps {
  id: string;
  name: string;
}

function processStudent(student: StudentProps): string {
  return student.name;
}

// ❌ Bad
function processStudent(student: any) {
  return student.name;
}
```

### Component Structure

```tsx
"use client"; // If needed (forms, interactivity)

import { useState } from "react";
import { Button } from "@/components/ui/button";

// Types first
interface MyComponentProps {
  title: string;
  onAction: () => void;
}

// Component function
export function MyComponent({ title, onAction }: MyComponentProps) {
  const [state, setState] = useState("");
  
  return (
    <div>
      <h1>{title}</h1>
      <Button onClick={onAction}>Action</Button>
    </div>
  );
}
```

### Server Actions Pattern

```tsx
"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";

const schema = z.object({
  email: z.string().email(),
});

export type ActionState = {
  message?: string;
  errors?: Record<string, string[]>;
  success?: boolean;
};

export async function myAction(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const validated = schema.safeParse({
      email: formData.get("email"),
    });
    
    if (!validated.success) {
      return {
        success: false,
        message: "Validation failed",
        errors: validated.error.flatten().fieldErrors,
      };
    }
    
    // Business logic here
    revalidatePath("/path");
    return { success: true, message: "Success!" };
    
  } catch (_error) {
    return {
      success: false,
      message: "Something went wrong",
    };
  }
}
```

### Error Handling

- Use `try/catch` in async functions
- Prefix unused catch variables with `_` (e.g., `_error`)
- Return error states, don't throw in Server Actions
- Use Sonner toast for user-facing errors

```tsx
try {
  await riskyOperation();
} catch (_error) {
  toast.error("Operation failed");
}
```

### Styling with Tailwind

- Use `cn()` utility from `@/lib/utils` for conditional classes
- Prefer semantic color tokens: `bg-primary`, `text-muted-foreground`
- Use color system from `src/lib/colors.ts` for charts

```tsx
import { cn } from "@/lib/utils";
import { COLORS } from "@/lib/colors";

// Conditional classes
<div className={cn("base-class", isActive && "active-class")}>

// Chart colors
<Bar fill={COLORS.primary} />
```

### File Organization

```
src/
├── app/                 # Next.js App Router
│   ├── (auth)/          # Route groups
│   ├── dashboard/
│   └── layout.tsx       # Root layout
├── components/
│   ├── ui/              # shadcn components
│   ├── student/         # Feature components
│   └── shared/          # Shared components
├── hooks/               # Custom React hooks
├── lib/                 # Utilities, colors, actions
├── types/               # TypeScript types
└── services/            # API services
```

### Key Principles

1. **Use Server Components by default** - Only add `"use client"` when needed
2. **Validate all inputs** with Zod schemas
3. **Use barrel exports** - Create `index.ts` in component folders
4. **Keep components focused** - One component, one responsibility
5. **Accessibility first** - Use Radix UI primitives, add aria labels
6. **Spanish UI** - All user-facing text should be in Spanish
