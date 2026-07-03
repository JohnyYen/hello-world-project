import { NextRequest, NextResponse } from "next/server";
import { writeFile, mkdir } from "fs/promises";
import path from "path";
import { randomUUID } from "crypto";

const API_BASE_URL = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const UPLOAD_DIR = path.join(process.cwd(), "public", "uploads", "avatars");

export async function POST(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;

  if (!token) {
    return NextResponse.json({ detail: "No autenticado" }, { status: 401 });
  }

  try {
    const formData = await request.formData();
    const file = formData.get("avatar") as File | null;

    if (!file) {
      return NextResponse.json({ detail: "No se recibió ninguna imagen" }, { status: 400 });
    }

    // Validate file type
    if (!file.type.startsWith("image/")) {
      return NextResponse.json({ detail: "Solo se permiten imágenes" }, { status: 400 });
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      return NextResponse.json({ detail: "La imagen no puede superar los 5MB" }, { status: 400 });
    }

    // Save file to public directory
    const ext = file.name.split(".").pop() || "jpg";
    const filename = `avatar-${randomUUID()}.${ext}`;
    
    await mkdir(UPLOAD_DIR, { recursive: true });

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    await writeFile(path.join(UPLOAD_DIR, filename), buffer);

    // Public URL for the avatar
    const avatarUrl = `/uploads/avatars/${filename}`;

    // Update user profile via backend API
    const updateResponse = await fetch(`${API_BASE_URL}/api/v1/users/professors/me`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ avatar_url: avatarUrl }),
      cache: "no-store",
    });

    if (!updateResponse.ok) {
      const errorData = await updateResponse.json().catch(() => ({}));
      return NextResponse.json(
        { detail: errorData.detail || "Error al actualizar el perfil" },
        { status: updateResponse.status }
      );
    }

    return NextResponse.json({
      success: true,
      avatarUrl,
      message: "Foto de perfil actualizada",
    });
  } catch (error) {
    console.error("Error uploading avatar:", error);
    return NextResponse.json(
      { detail: "Error interno al subir la imagen" },
      { status: 500 }
    );
  }
}
