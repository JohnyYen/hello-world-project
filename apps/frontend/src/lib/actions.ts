"use server";

import { z } from "zod";
import { revalidatePath, revalidateTag } from "next/cache";
import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { ApiError } from "@/api/client";
import { login as authLogin, register as authRegister, getMe as authGetMe, changePassword as authChangePassword } from "@/services/auth";
import { usersApi } from "@/api/client";

// 📝 Type para las acciones
export type ActionState = {
  message?: string;
  errors?: Record<string, string[]>;
  success?: boolean;
};

// 🔐 Helper para obtener token de auth
async function getAuthToken(): Promise<string | undefined> {
  const cookieStore = await cookies();
  return cookieStore.get("auth_token")?.value;
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

    await authChangePassword(String(user.id), currentPassword, newPassword, token);

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

    if (result.access_token) {
      const cookieStore = await cookies();
      cookieStore.set("auth_token", result.access_token, {
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

    // Enhanced error handling - extract backend error message properly
    let errorMessage = "Error al iniciar sesión";
    let errorFormMessage = "Credenciales inválidas";

    // Check if it's a ResponseError from the API client
    if (error && typeof error === 'object' && 'response' in error) {
      const responseError = error as { response?: Response; message?: string };
      
      if (responseError.response) {
        try {
          const response = responseError.response;
          const body = await response.json().catch(() => ({}));
          
          if (body && typeof body === 'object') {
            const detail = (body as { detail?: string }).detail;
            
            if (detail) {
              errorMessage = detail;
              errorFormMessage = detail;
            }
          }
        } catch {
          // Failed to parse response body, use default
        }
      } else if (responseError.message) {
        errorMessage = responseError.message;
        errorFormMessage = responseError.message;
      }
    } else if (error instanceof Error) {
      errorMessage = error.message;
      errorFormMessage = error.message;
    }

    return {
      success: false,
      message: errorMessage,
      errors: { _form: [errorFormMessage] },
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

    // Enhanced error handling - extract backend error message properly
    let errorMessage = "Error al crear cuenta";
    let errorFormMessage = "Email o usuario ya existe";

    // Check if it's a ResponseError from the API client
    if (error && typeof error === 'object' && 'response' in error) {
      const responseError = error as { response?: Response; message?: string };
      
      if (responseError.response) {
        try {
          const response = responseError.response;
          const body = await response.json().catch(() => ({}));
          
          // Backend returns { detail: string } for validation errors
          // or { detail: string, error: string } for AppException
          if (body && typeof body === 'object') {
            const detail = (body as { detail?: string }).detail;
            
            if (detail) {
              errorMessage = detail;
              
              // Map specific backend errors to user-friendly messages
              if (detail.toLowerCase().includes('email')) {
                errorFormMessage = "El email ya está registrado";
              } else if (detail.toLowerCase().includes('username')) {
                errorFormMessage = "El nombre de usuario ya está en uso";
              } else {
                errorFormMessage = detail;
              }
            }
          }
        } catch {
          // Failed to parse response body, use default
        }
      } else if (responseError.message) {
        // Fallback: use message property if available
        errorMessage = responseError.message;
        errorFormMessage = responseError.message;
      }
    } else if (error instanceof Error) {
      // Generic error handling
      errorMessage = error.message;
      errorFormMessage = error.message;
    }

    return {
      success: false,
      message: errorMessage,
      errors: { _form: [errorFormMessage] },
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

    const token = await getAuthToken();
    if (!token) {
      return { success: false, message: "No autenticado" };
    }

    await usersApi.createStudent(
      { ...validatedFields.data, is_active: true },
      token
    );

    // Revalidar caché
    revalidatePath("/dashboard/students");

    return {
      success: true,
      message: "Estudiante creado exitosamente"
    };

  } catch (error: unknown) {
    console.error("Error creating student:", error);

    let errorDetail = "Error al guardar en base de datos";

    if (error instanceof ApiError) {
      errorDetail = error.detail;
      console.error(`Backend response: ${error.status} ${error.message}`);
    } else if (error instanceof Error) {
      errorDetail = error.message;
    }

    return {
      success: false,
      message: errorDetail,
      errors: { _form: [errorDetail] },
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

    await usersApi.updateTeacherProfile(token, {
      name: name || undefined,
      lastname: lastname || undefined,
      email: email || undefined,
      department: department || undefined,
      contact_phone: contactPhone || undefined,
    });

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

// 🔓 Logout Action - clears auth cookie
export async function logoutAction(): Promise<void> {
  const cookieStore = await cookies();
  cookieStore.delete("auth_token");
  revalidatePath("/");
}
