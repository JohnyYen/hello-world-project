"use server";

import { cookies } from "next/headers";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface SimpleUser {
  id: number;
  username: string;
  email: string;
  name: string;
  lastname: string | null;
  is_active: boolean;
  role: {
    id: number;
    role_name: string;
  } | null;
}

/**
 * Decodifica un JWT sin verificar la firma (solo para extraer datos)
 */
function decodeJWT(token: string): { sub: string; exp: number } | null {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;
    
    const payload = parts[1];
    const decoded = Buffer.from(payload, "base64url").toString("utf-8");
    return JSON.parse(decoded);
  } catch {
    return null;
  }
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
      const user = await response.json();
      return { user, token };
    }

    // Si falla (usuario sin perfil de profesor), decodificamos el JWT
    // y devolvemos los datos básicos del usuario
    const basicUser: SimpleUser = {
      id: 0, // No tenemos el ID del JWT
      username: decoded.sub,
      email: "", // No disponible en el JWT
      name: decoded.sub, // Usar username como name temporal
      lastname: null,
      is_active: true,
      role: {
        id: 2,
        role_name: "professor",
      },
    };
    
    return { user: basicUser, token };
  } catch {
    return { user: null, token: null };
  }
}
