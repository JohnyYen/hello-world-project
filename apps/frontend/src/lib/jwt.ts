/**
 * Decodifica un JWT y valida que no haya expirado.
 * No verifica la firma (solo para extraer datos del payload).
 *
 * @returns `{ sub, exp }` si el token es válido y no ha expirado, `null` en caso contrario.
 */
export function decodeJWT(token: string): { sub: string; exp: number } | null {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;

    const payload = parts[1];
    const decoded = JSON.parse(
      atob(payload.replace(/-/g, "+").replace(/_/g, "/"))
    );

    // Validar expiración
    if (decoded.exp && decoded.exp * 1000 < Date.now()) {
      return null;
    }

    return { sub: decoded.sub, exp: decoded.exp };
  } catch {
    return null;
  }
}
