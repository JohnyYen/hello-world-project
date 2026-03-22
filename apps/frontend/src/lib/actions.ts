"use server";

import { z } from "zod";
import { revalidatePath, revalidateTag } from "next/cache";
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

    // Obtener usuario desde el servidor
    const { getServerUser } = await import("@/lib/auth-server");
    const { user } = await getServerUser();
    
    if (!user || !user.id) {
      return {
        success: false,
        message: "No se pudo obtener la información del usuario",
      };
    }

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
      email: email,
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
      // Invalidate student-related caches after login
      revalidateTag('students-list');
      revalidateTag('all-students');
      revalidateTag('student-detail');
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
    // Enhanced error logging for debugging 403 issue
    console.error("Error creating student:", error);
    
    // Extract ResponseError details if available
    let errorDetail = "Error al guardar en base de datos";
    let errorStatus: number | null = null;
    let errorBody: unknown = null;
    
    if (error && typeof error === 'object') {
      const err = error as Record<string, unknown>;
      
      // Check for ResponseError from api-client-ts
      if (err.response && typeof err.response === 'object') {
        const response = err.response as Record<string, unknown>;
        errorStatus = response.status as number | null;
        errorBody = response.body;
        
        // Try to parse body if it's a string
        if (typeof response.body === 'string') {
          try {
            errorBody = JSON.parse(response.body);
          } catch {
            // Keep as string if not JSON
          }
        }
        
        console.error(`Backend response: ${response.status} ${response.statusText}`, errorBody);
      }
      
      // Check for detail property (common in FastAPI errors)
      if (err.detail && typeof err.detail === 'string') {
        errorDetail = err.detail;
      }
    }
    
    const message = error instanceof Error ? error.message : "Error al crear estudiante";
    
    // Include status in error detail for debugging
    const statusInfo = errorStatus ? ` [HTTP ${errorStatus}]` : '';
    
    return {
      success: false,
      message,
      errors: { _form: [errorDetail + statusInfo] },
    };
  }
}

// 👤 Schema de validación para actualización de perfil
const profileUpdateSchema = z.object({
  name: z.string().min(2, "El nombre debe tener al menos 2 caracteres").max(100, "El nombre no puede exceder 100 caracteres").optional(),
  lastname: z.string().max(100, "El apellido no puede exceder 100 caracteres").optional(),
  email: z.string().email("Email inválido").optional().or(z.literal("")),
  department: z.string().max(100, "El departamento no puede exceder 100 caracteres").optional().or(z.literal("")),
  contactPhone: z.string().max(20, "El teléfono no puede exceder 20 caracteres").regex(/^[\d\s\-\+\(\)]*$/, "Formato de teléfono inválido").optional().or(z.literal("")),
});

// 👤 Server action para actualizar perfil
export async function updateProfileAction(
  prevState: ActionState | null,
  formData: FormData
): Promise<ActionState> {
  try {
    const validatedFields = profileUpdateSchema.safeParse({
      name: formData.get("name"),
      lastname: formData.get("lastname"),
      email: formData.get("email"),
      department: formData.get("department"),
      contactPhone: formData.get("contactPhone"),
    });

    if (!validatedFields.success) {
      return {
        success: false,
        message: "Errores de validación",
        errors: validatedFields.error.flatten().fieldErrors,
      };
    }

    const cookieStore = await cookies();
    const token = cookieStore.get("auth_token")?.value;
    if (!token) {
      return { success: false, message: "No autenticado" };
    }

    const { getServerUser } = await import("@/lib/auth-server");
    const { user } = await getServerUser();
    if (!user || !user.id) {
      return { success: false, message: "No se pudo obtener la información del usuario" };
    }

    const { name, lastname, email, department, contactPhone } = validatedFields.data;
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    // Direct fetch call instead of API client (API client has header bug)
    const response = await fetch(`${API_URL}/api/v1/users/professors/me`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: name || undefined,
        lastname: lastname || undefined,
        email: email || undefined,
        department: department || undefined,
        contact_phone: contactPhone || undefined,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Error ${response.status}`);
    }

    revalidatePath("/dashboard/account");

    return { success: true, message: "Perfil actualizado exitosamente" };

  } catch (error: unknown) {
    console.error("Error updating profile:", error);
    const message = error instanceof Error ? error.message : "Error al actualizar el perfil";
    
    return {
      success: false,
      message,
      errors: { _form: [message] },
    };
  }
}
