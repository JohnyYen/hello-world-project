"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { Configuration, UsersApi } from "@workspace/api-client-ts";
import { login as authLogin, register as authRegister, getMe as authGetMe, changePassword as authChangePassword } from "@/services/auth";

// 📝 Type para las acciones
export type ActionState = {
  message?: string;
  errors?: Record<string, string[]>;
  success?: boolean;
};

// 🔐 Helper para obtener instancia de Users API configurada
async function getUsersApi(): Promise<UsersApi> {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;
  
  const config = new Configuration({
    basePath: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    accessToken: token,
  });
  
  return new UsersApi(config);
}

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

// 🔐 Schema de validación para cambio de contraseña
const changePasswordSchema = z.object({
  currentPassword: z.string().min(1, "La contraseña actual es requerida"),
  newPassword: passwordSchema,
  confirmPassword: z.string(),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: "Las contraseñas no coinciden",
  path: ["confirmPassword"],
});

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

// 🔑 Change Password Action
export async function changePasswordAction(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const validatedFields = changePasswordSchema.safeParse({
      currentPassword: formData.get("currentPassword"),
      newPassword: formData.get("newPassword"),
      confirmPassword: formData.get("confirmPassword"),
    });

    if (!validatedFields.success) {
      return {
        success: false,
        message: "Errores de validación",
        errors: validatedFields.error.flatten().fieldErrors,
      };
    }

    const { currentPassword, newPassword } = validatedFields.data;
    
    const cookieStore = await cookies();
    const token = cookieStore.get("auth_token")?.value;
    if (!token) {
      return {
        success: false,
        message: "No autenticado",
      };
    }

    const user = await authGetMe(token);
    await authChangePassword(user.id, currentPassword, newPassword, token);

    return {
      success: true,
      message: "Contraseña actualizada exitosamente",
    };
    
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Error de red o del servidor";
    console.error("Error changing password:", error);
    return {
      success: false,
      message,
      errors: { _form: [message] },
    };
  }
}

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
    
    const result = await authLogin({
      username: email,
      password: password,
    });

    if (result.accessToken) {
      const cookieStore = await cookies();
      cookieStore.set("auth_token", result.accessToken, {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        path: "/",
      });
    }
    
  } catch (error: unknown) {
    if (error instanceof Error && error.message.includes("NEXT_REDIRECT")) {
      throw error;
    }
    const detail = (error as { detail?: string }).detail;
    return {
      success: false,
      message: detail || "Error al iniciar sesión",
      errors: { _form: [detail || "Credenciales inválidas"] },
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
    
    await authRegister({
      name,
      username,
      email,
      password,
    });
    
  } catch (error: unknown) {
    if (error instanceof Error && error.message.includes("NEXT_REDIRECT")) {
      throw error;
    }
    const detail = (error as { detail?: string }).detail;
    return {
      success: false,
      message: detail || "Error al crear cuenta",
      errors: { _form: [detail || "Email o usuario ya existe"] },
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
      username: z.string().min(3, "Mínimo 3 caracteres"),
      email: z.string().email("Email inválido"),
      name: z.string().min(2, "Mínimo 2 caracteres"),
      lastname: z.string().min(2, "Mínimo 2 caracteres"),
      password: passwordSchema,
    });

    const validatedFields = studentSchema.safeParse({
      username: formData.get("username"),
      email: formData.get("email"),
      name: formData.get("name"),
      lastname: formData.get("lastname"),
      password: formData.get("password"),
    });

    if (!validatedFields.success) {
      return {
        success: false,
        message: "Errores de validación",
        errors: validatedFields.error.flatten().fieldErrors,
      };
    }

    const usersApi = await getUsersApi();
    await usersApi.createStudentApiV1UsersStudentsPost({
      studentCreate: {
        ...validatedFields.data,
        isActive: true,
      }
    });
    
    // Revalidar caché
    revalidatePath("/dashboard/students");
    
    return { 
      success: true,
      message: "Estudiante creado exitosamente" 
    };
    
  } catch (error: unknown) {
    console.error("Error creating student:", error);
    const detail = (error as { detail?: string }).detail;
    const message = error instanceof Error ? error.message : "Error al crear estudiante";
    return {
      success: false,
      message,
      errors: { _form: [detail || "Error al guardar en base de datos"] },
    };
  }
}
