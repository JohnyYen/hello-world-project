"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

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

// 🔐 Schema de validación para signup
const signupSchema = z.object({
  name: z.string().min(2, "Mínimo 2 caracteres"),
  email: z.string().email("Email inválido"),
  password: z.string().min(6, "Mínimo 6 caracteres"),
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

    // TODO: Implementar autenticación real aquí
    // const result = await auth.login(validatedFields.data);
    
    // Simulación de login
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Revalidar caché y redirigir
    revalidatePath("/dashboard");
    redirect("/dashboard");
    
  } catch (_error) {
    return {
      success: false,
      message: "Error al iniciar sesión",
      errors: { _form: ["Credenciales inválidas"] },
    };
  }
}

// 📝 Signup Action
export async function signupAction(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const validatedFields = signupSchema.safeParse({
      name: formData.get("name"),
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

    // TODO: Implementar registro real aquí
    // const result = await auth.signup(validatedFields.data);
    
    // Simulación de registro
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Revalidar caché y redirigir
    revalidatePath("/login");
    redirect("/login");
    
  } catch (_error) {
    return {
      success: false,
      message: "Error al crear cuenta",
      errors: { _form: ["Email ya existe o error del sistema"] },
    };
  }
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