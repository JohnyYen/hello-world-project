"use client";

import { useActionState } from "react";
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
import { loginAction } from "@/lib/actions"

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const [state, action, isPending] = useActionState(loginAction, null);

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
                  aria-describedby="email-error"
                />
                {(state?.errors?.email || state?.errors?._form) && (
                  <FieldDescription id="email-error" className="text-red-500">
                    {state.errors?.email?.[0] || state.errors?._form?.[0]}
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
                {state?.errors?.password && (
                  <FieldDescription id="password-error" className="text-red-500">
                    {state.errors.password[0]}
                  </FieldDescription>
                )}
              </Field>
              <Field>
                <Button type="submit" disabled={isPending} variant="default" className="w-full">
                  {isPending ? "Iniciando sesión..." : "Iniciar Sesión"}
                </Button>
                {state?.message && (
                  <FieldDescription className={state.success ? "text-green-500" : "text-red-500"}>
                    {state.message}
                  </FieldDescription>
                )}
                {state?.errors?._form && (
                  <FieldDescription className="text-red-500">
                    {state.errors._form[0]}
                  </FieldDescription>
                )}
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
