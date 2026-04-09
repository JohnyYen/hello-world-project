"use client";

import { useActionState, useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Eye, EyeOff, CheckCircle, XCircle } from "lucide-react";
import { signupAction, ActionState } from "@/lib/actions";
import { toast } from "sonner";

interface PasswordRequirements {
  minLength: boolean;
  hasUppercase: boolean;
  hasLowercase: boolean;
  hasNumber: boolean;
}

function getPasswordRequirements(password: string): PasswordRequirements {
  return {
    minLength: password.length >= 8,
    hasUppercase: /[A-Z]/.test(password),
    hasLowercase: /[a-z]/.test(password),
    hasNumber: /\d/.test(password),
  };
}

export function SignupForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  const [state, action, isPending] = useActionState<ActionState | null, FormData>(
    signupAction,
    null
  );
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordValue, setPasswordValue] = useState("");
  const [showRequirements, setShowRequirements] = useState(false);

  const requirements = getPasswordRequirements(passwordValue);

  useEffect(() => {
    if (state?.success) {
      toast.success(state.message);
    } else if (state?.success === false) {
      toast.error(state.message);
    }
  }, [state]);

  return (
    <form action={action} className={cn("flex flex-col gap-6", className)} {...props}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Crea tu cuenta</h1>
          <p className="text-muted-foreground text-sm text-balance">
            Completa el siguiente formulario para crear tu cuenta de profesor
          </p>
        </div>

        {state?.errors?._form && (
          <div className="bg-destructive/15 text-destructive text-sm p-3 rounded-md" role="alert" aria-live="polite">
            {state.errors._form[0]}
          </div>
        )}

        <Field>
          <FieldLabel htmlFor="name">Nombre Completo</FieldLabel>
          <Input
            id="name"
            name="name"
            type="text"
            placeholder="Juan Pérez"
            required
            aria-invalid={!!state?.errors?.name}
            aria-describedby={state?.errors?.name ? "name-error" : undefined}
          />
          {state?.errors?.name && (
            <p id="name-error" className="text-destructive text-xs mt-1" role="alert">{state.errors.name[0]}</p>
          )}
        </Field>

        <Field>
          <FieldLabel htmlFor="username">Nombre de Usuario</FieldLabel>
          <Input
            id="username"
            name="username"
            type="text"
            placeholder="juanperez"
            required
            aria-invalid={!!state?.errors?.username}
            aria-describedby={state?.errors?.username ? "username-error" : undefined}
          />
          {state?.errors?.username && (
            <p id="username-error" className="text-destructive text-xs mt-1" role="alert">{state.errors.username[0]}</p>
          )}
        </Field>

        <Field>
          <FieldLabel htmlFor="email">Correo Electrónico</FieldLabel>
          <Input
            id="email"
            name="email"
            type="email"
            placeholder="tu@email.com"
            required
            aria-invalid={!!state?.errors?.email}
            aria-describedby={state?.errors?.email ? "email-error" : undefined}
          />
          {state?.errors?.email && (
            <p id="email-error" className="text-destructive text-xs mt-1" role="alert">{state.errors.email[0]}</p>
          )}
          <FieldDescription>
            Usaremos esto para contactarte. No compartiremos tu correo con nadie.
          </FieldDescription>
        </Field>

        <Field>
          <FieldLabel htmlFor="password">Contraseña</FieldLabel>
          <div className="relative">
            <Input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
              required
              aria-invalid={!!state?.errors?.password}
              aria-describedby={state?.errors?.password ? "password-error" : "password-hint"}
              onFocus={() => setShowRequirements(true)}
              onBlur={(e) => {
                if (!e.currentTarget.value) setShowRequirements(false);
              }}
              onChange={(e) => setPasswordValue(e.target.value)}
            />
            <button
              type="button"
              className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-primary"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
              aria-pressed={showPassword}
            >
              {showPassword ? (
                <EyeOff className="h-4 w-4" />
              ) : (
                <Eye className="h-4 w-4" />
              )}
            </button>
          </div>
          {state?.errors?.password && (
            <p id="password-error" className="text-destructive text-xs mt-1" role="alert">{state.errors.password[0]}</p>
          )}
          {showRequirements && (
            <div className="mt-2 space-y-1" aria-live="polite">
              <p className="text-xs font-medium text-muted-foreground mb-1">La contraseña debe cumplir:</p>
              <ul className="space-y-1 text-xs">
                <li className={cn("flex items-center gap-2", requirements.minLength && "text-success")}>
                  {requirements.minLength ? (
                    <CheckCircle className="h-3 w-3 text-success" />
                  ) : (
                    <XCircle className="h-3 w-3 text-destructive" />
                  )}
                  Al menos 8 caracteres
                </li>
                <li className={cn("flex items-center gap-2", requirements.hasUppercase && "text-success")}>
                  {requirements.hasUppercase ? (
                    <CheckCircle className="h-3 w-3 text-success" />
                  ) : (
                    <XCircle className="h-3 w-3 text-destructive" />
                  )}
                  Al menos una mayúscula
                </li>
                <li className={cn("flex items-center gap-2", requirements.hasLowercase && "text-success")}>
                  {requirements.hasLowercase ? (
                    <CheckCircle className="h-3 w-3 text-success" />
                  ) : (
                    <XCircle className="h-3 w-3 text-destructive" />
                  )}
                  Al menos una minúscula
                </li>
                <li className={cn("flex items-center gap-2", requirements.hasNumber && "text-success")}>
                  {requirements.hasNumber ? (
                    <CheckCircle className="h-3 w-3 text-success" />
                  ) : (
                    <XCircle className="h-3 w-3 text-destructive" />
                  )}
                  Al menos un número
                </li>
              </ul>
            </div>
          )}
          {!state?.errors?.password && !showRequirements && (
            <FieldDescription id="password-hint">
              Debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número.
            </FieldDescription>
          )}
        </Field>

        <Field>
          <FieldLabel htmlFor="confirm-password">Confirmar Contraseña</FieldLabel>
          <div className="relative">
            <Input
              id="confirm-password"
              name="confirmPassword"
              type={showConfirmPassword ? "text" : "password"}
              required
              aria-invalid={!!state?.errors?.confirmPassword}
              aria-describedby={state?.errors?.confirmPassword ? "confirm-password-error" : undefined}
            />
            <button
              type="button"
              className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-primary"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              aria-label={showConfirmPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
              aria-pressed={showConfirmPassword}
            >
              {showConfirmPassword ? (
                <EyeOff className="h-4 w-4" />
              ) : (
                <Eye className="h-4 w-4" />
              )}
            </button>
          </div>
          {state?.errors?.confirmPassword && (
            <p id="confirm-password-error" className="text-destructive text-xs mt-1" role="alert">{state.errors.confirmPassword[0]}</p>
          )}
          <FieldDescription>Por favor, confirma tu contraseña.</FieldDescription>
        </Field>

        <Field>
          <Button type="submit" disabled={isPending} aria-live="polite">
            {isPending ? "Creando cuenta..." : "Crear Cuenta"}
          </Button>
        </Field>

        <FieldSeparator>O continúa con</FieldSeparator>

        <Field>
          <Button variant="outline" type="button" disabled={isPending} aria-label="Registrarse con GitHub">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className="h-4 w-4">
              <path
                d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"
                fill="currentColor"
              />
            </svg>
            Registrarse con GitHub
          </Button>
          <FieldDescription className="px-6 text-center">
            ¿Ya tienes cuenta? <a href="/login" className="underline underline-offset-4">Inicia sesión</a>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  );
}

