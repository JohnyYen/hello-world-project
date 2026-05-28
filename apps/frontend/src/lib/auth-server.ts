"use server";

import { cookies } from "next/headers";
import { decodeJWT } from "@/lib/jwt";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface SimpleUser {
  id: number;
  username: string;
  email: string;
  name: string;
  lastname: string | null;
  is_active: boolean;
  created_at?: string;
  role: {
    id: number;
    role_name: string;
  } | null;
}

/**
 * Obtiene el usuario actual desde la cookie del servidor
 * Esta función solo funciona en Server Components
 */
export async function getServerUser(): Promise<{
  user: SimpleUser | null;
  token: string | null;
}> {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_token")?.value;

  if (!token) {
    return { user: null, token: null };
  }

  // Decodificar el JWT para obtener el username
  const decoded = decodeJWT(token);
  
  if (!decoded?.sub) {
    return { user: null, token: null };
  }

  // Intentar obtener el usuario desde la API
  try {
    // Primero intentamos con el endpoint de professores
    const response = await fetch(`${API_BASE_URL}/api/v1/users/professors/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    if (response.ok) {
      const data = await response.json();
      // El endpoint devuelve { data: {...} }
      const user = data.data || data;
      return { user, token };
    }

    // Si falla (usuario sin perfil de profesor), intentar obtener de la lista de usuarios
    const usersResponse = await fetch(`${API_BASE_URL}/api/v1/users/?limit=1000`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    if (usersResponse.ok) {
      const usersData = await usersResponse.json();
      const users = usersData.data || usersData;
      const foundUser = users.find((u: { username: string }) => u.username === decoded.sub);
      
      if (foundUser) {
        return { 
          user: {
            id: foundUser.id,
            username: foundUser.username,
            email: foundUser.email,
            name: foundUser.name || foundUser.username,
            lastname: foundUser.lastname || null,
            is_active: foundUser.is_active,
            created_at: foundUser.created_at,
            role: foundUser.role || { id: 2, role_name: "professor" },
          }, 
          token 
        };
      }
    }

    // Si el backend respondió pero no encontró el usuario, no inventamos datos
    return { user: null, token: null };
  } catch {
    // Error de red o backend caído — no podemos verificar, mejor sesión nula
    return { user: null, token: null };
  }
}
