"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(formData: FormData) {
    setError(null);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    startTransition(async () => {
      try {
        // Use internal API that sets the cookie server-side
        const response = await fetch("/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
          throw new Error(data.message || "Credenciales incorrectas");
        }

        // Token is stored in HTTP-only cookie server-side, no client-side storage needed

        // Redirect to dashboard
        router.push("/dashboard");
        router.refresh();
      } catch (err: unknown) {
        const message = err instanceof Error
          ? err.message
          : "Credenciales incorrectas";
        // Extract detail from ApiError if available
        if (err && typeof err === "object" && "detail" in err) {
          setError((err as { detail?: string }).detail ?? "Credenciales incorrectas");
        } else {
          setError(message.includes("NEXT_REDIRECT") ? null : message);
        }
      }
    });
  }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="text-xl">Bienvenido de vuelta</CardTitle>
          <CardDescription>
            Inicia sesión con tus credenciales
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form action={handleSubmit}>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="m@example.com"
                  required
                  aria-describedby="email-error"
                />
                {error && (
                  <FieldDescription id="email-error" className="text-red-500">
                    {error}
                  </FieldDescription>
                )}
              </Field>
              <Field>
                <div className="flex items-center">
                  <FieldLabel htmlFor="password">Password</FieldLabel>
                  <a
                    href="#"
                    className="ml-auto text-sm underline-offset-4 hover:underline"
                  >
                    Forgot your password?
                  </a>
                </div>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  required
                  aria-describedby="password-error"
                />
              </Field>
              <Field>
                <Button type="submit" disabled={isPending} variant="default" className="w-full">
                  {isPending ? "Iniciando sesión..." : "Iniciar Sesión"}
                </Button>
                <FieldDescription className="text-center">
                  Don&apos;t have an account? <a href="/signup">Sign up</a>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
