"use client";

import { useActionState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { createStudentAction } from "@/lib/actions";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";

interface CreateStudentFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

export default function CreateStudentForm({ onSuccess, onCancel }: CreateStudentFormProps) {
  const [state, action, isPending] = useActionState(createStudentAction, null);

  useEffect(() => {
    if (state?.success) {
      toast.success(state.message);
      onSuccess();
    } else if (state?.success === false) {
      toast.error(state.message);
    }
  }, [state, onSuccess]);

  return (
    <form action={action} className="space-y-4 py-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="name">Nombre</Label>
          <Input
            id="name"
            name="name"
            placeholder="Juan"
            required
            disabled={isPending}
          />
          {state?.errors?.name && (
            <p className="text-xs text-destructive">{state.errors.name[0]}</p>
          )}
        </div>
        <div className="space-y-2">
          <Label htmlFor="lastname">Apellidos</Label>
          <Input
            id="lastname"
            name="lastname"
            placeholder="Pérez"
            required
            disabled={isPending}
          />
          {state?.errors?.lastname && (
            <p className="text-xs text-destructive">{state.errors.lastname[0]}</p>
          )}
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="username">Nombre de usuario</Label>
        <Input
          id="username"
          name="username"
          placeholder="juanperez"
          required
          disabled={isPending}
        />
        {state?.errors?.username && (
          <p className="text-xs text-destructive">{state.errors.username[0]}</p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="email">Correo electrónico</Label>
        <Input
          id="email"
          name="email"
          type="email"
          placeholder="juan.perez@ejemplo.com"
          required
          disabled={isPending}
        />
        {state?.errors?.email && (
          <p className="text-xs text-destructive">{state.errors.email[0]}</p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="password">Contraseña inicial</Label>
        <Input
          id="password"
          name="password"
          type="password"
          required
          disabled={isPending}
        />
        {state?.errors?.password && (
          <p className="text-xs text-destructive">{state.errors.password[0]}</p>
        )}
      </div>

      {state?.errors?._form && (
        <p className="text-sm text-destructive font-medium text-center">
          {state.errors._form[0]}
        </p>
      )}

      <div className="flex justify-end space-x-2 pt-4">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isPending}
        >
          Cancelar
        </Button>
        <Button type="submit" disabled={isPending}>
          {isPending ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Creando...
            </>
          ) : (
            "Crear Estudiante"
          )}
        </Button>
      </div>
    </form>
  );
}
