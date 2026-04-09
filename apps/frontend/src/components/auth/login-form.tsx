"use client";

import { useActionState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { loginAction, type ActionState } from "@/lib/actions";

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const [state, action, isPending] = useActionState<ActionState | null, FormData>(
    loginAction,
    null
  );

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
          <form action={action}>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="email">Email</FieldLabel>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="m@example.com"
                  required
                  aria-invalid={!!state?.errors?.email}
                  aria-describedby={state?.errors?.email ? "email-error" : undefined}
                />
                {state?.errors?.email && (
                  <FieldDescription id="email-error" className="text-destructive">
                    {state.errors.email[0]}
                  </FieldDescription>
                )}
              </Field>
              <Field>
                <div className="flex items-center">
                  <FieldLabel htmlFor="password">Contraseña</FieldLabel>
                  <a
                    href="#"
                    className="ml-auto text-sm underline-offset-4 hover:underline"
                  >
                    ¿Olvidaste tu contraseña?
                  </a>
                </div>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  required
                  aria-invalid={!!state?.errors?.password}
                  aria-describedby={state?.errors?.password ? "password-error" : undefined}
                />
                {state?.errors?.password && (
                  <FieldDescription id="password-error" className="text-destructive">
                    {state.errors.password[0]}
                  </FieldDescription>
                )}
              </Field>
              <Field>
                {state?.errors?._form && (
                  <div className="bg-destructive/15 text-destructive text-sm p-3 rounded-md mb-2">
                    {state.errors._form[0]}
                  </div>
                )}
                <Button type="submit" disabled={isPending} variant="default" className="w-full">
                  {isPending ? "Iniciando sesión..." : "Iniciar Sesión"}
                </Button>
                <FieldDescription className="text-center">
                  ¿No tienes cuenta? <a href="/signup" className="underline underline-offset-4">Regístrate</a>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

