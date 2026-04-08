/**
 * Decodifica un JWT sin verificar la firma (solo para extraer datos)
 */
export function decodeJWT(token: string): { sub: string; exp: number } | null {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;
    
    const payload = parts[1];
    // Use atob for browser compatibility
    const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
    return JSON.parse(decoded);
  } catch {
    return null;
  }
}
