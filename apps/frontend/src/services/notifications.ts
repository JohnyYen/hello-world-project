/**
 * Notification service - handles fetching and mutating notifications.
 * Uses Next.js API routes as proxy (reads HttpOnly cookie server-side).
 */

import type { NotificationListResponse, NotificationActionResponse } from "@/api/types";

export async function getNotifications(
  skip = 0,
  limit = 50,
  unreadOnly = false
): Promise<NotificationListResponse> {
  let url = `/api/notifications?skip=${skip}&limit=${limit}`;
  if (unreadOnly) {
    url += "&unread_only=true";
  }
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Error al cargar notificaciones" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

export async function markAsRead(
  notificationId: string
): Promise<NotificationActionResponse> {
  const response = await fetch(`/api/notifications/${notificationId}/read`, {
    method: "PATCH",
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Error al marcar como leída" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

export async function markAllAsRead(): Promise<NotificationActionResponse> {
  const response = await fetch("/api/notifications/read-all", {
    method: "PATCH",
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Error al marcar todas como leídas" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

export async function deleteNotification(
  notificationId: string
): Promise<NotificationActionResponse> {
  const response = await fetch(`/api/notifications/${notificationId}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Error al eliminar notificación" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}
