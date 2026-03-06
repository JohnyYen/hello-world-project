"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { authService } from "@/lib/api-client";

// 📝 Type para las acciones
export type ActionState = {
  message?: string;
  errors?: Record<string, string[]>;
  success?: boolean;
};

// 🔐 Schema de validación para login
const loginSchema = z.object({
  email: z.string().email("Email inválido"),
  password: z.string().min(6, "Mínimo 6 caracteres"),
});

const passwordSchema = z.string()
  .min(8, "La contraseña debe tener al menos 8 caracteres")
  .regex(/[A-Z]/, "Debe contener al menos una mayúscula")
  .regex(/[a-z]/, "Debe contener al menos una minúscula")
  .regex(/\d/, "Debe contener al menos un número");

// 🔐 Schema de validación para signup
const signupSchema = z.object({
  name: z.string().min(2, "Mínimo 2 caracteres"),
  username: z.string().min(3, "Mínimo 3 caracteres"),
  email: z.string().email("Email inválido"),
  password: passwordSchema,
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Las contraseñas no coinciden",
  path: ["confirmPassword"],
});

// 🔑 Login Action
export async function loginAction(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const validatedFields = loginSchema.safeParse({
      email: formData.get("email"),
      password: formData.get("password"),
    });

    if (!validatedFields.success) {
      return {
        success: false,
        message: "Errores de validación",
        errors: validatedFields.error.flatten().fieldErrors,
      };
    }

    const { email, password } = validatedFields.data;
    
    const result = await authService.login({
      username: email, // Backend accepts email in username field or has email field
      password: password,
    });

    if (result.access_token) {
      const cookieStore = await cookies();
      cookieStore.set("auth_token", result.access_token, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        path: "/",
      });
    }
    
  } catch (error: any) {
    if (error?.message?.includes("NEXT_REDIRECT")) {
      throw error;
    }
    return {
      success: false,
      message: error.detail || error.message || "Error al iniciar sesión",
      errors: { _form: [error.detail || "Credenciales inválidas"] },
    };
  }
  
  // Revalidar caché y redirigir
  revalidatePath("/dashboard");
  redirect("/dashboard");
}

// 📝 Signup Action
export async function signupAction(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const validatedFields = signupSchema.safeParse({
      name: formData.get("name"),
      username: formData.get("username"),
      email: formData.get("email"),
      password: formData.get("password"),
      confirmPassword: formData.get("confirmPassword"),
    });

    if (!validatedFields.success) {
      return {
        success: false,
        message: "Errores de validación",
        errors: validatedFields.error.flatten().fieldErrors,
      };
    }

    const { name, username, email, password } = validatedFields.data;
    
    await authService.signup({
      name,
      username,
      email,
      password,
    });
    
  } catch (error: any) {
    if (error?.message?.includes("NEXT_REDIRECT")) {
      throw error;
    }
    
    return {
      success: false,
      message: error.detail || error.message || "Error al crear cuenta",
      errors: { _form: [error.detail || "Email o usuario ya existe"] },
    };
  }

  revalidatePath("/login");
  redirect("/login");
}

// 🎓 Student Creation Action
export async function createStudentAction(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const studentSchema = z.object({
      name: z.string().min(2, "Mínimo 2 caracteres"),
      email: z.string().email("Email inválido"),
      course: z.string().min(1, "Selecciona un curso"),
    });

    const validatedFields = studentSchema.safeParse({
      name: formData.get("name"),
      email: formData.get("email"),
      course: formData.get("course"),
    });

    if (!validatedFields.success) {
      return {
        success: false,
        message: "Errores de validación",
        errors: validatedFields.error.flatten().fieldErrors,
      };
    }

    // TODO: Implementar creación real en base de datos
    // await db.students.create(validatedFields.data);
    
    // Simulación
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Revalidar caché
    revalidatePath("/dashboard/students");
    
    return { 
      success: true,
      message: "Estudiante creado exitosamente" 
    };
    
  } catch (_error) {
    return {
      success: false,
      message: "Error al crear estudiante",
      errors: { _form: ["Error al guardar en base de datos"] },
    };
  }
}
