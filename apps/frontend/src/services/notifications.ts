/**
 * Notification service - handles fetching and mutating notifications.
 */

import { notificationsApi } from "@/api/client";
import type { NotificationListResponse, NotificationActionResponse } from "@/api/types";

export async function getNotifications(
  token: string,
  skip = 0,
  limit = 50,
  unreadOnly = false
): Promise<NotificationListResponse> {
  return notificationsApi.list(token, skip, limit, unreadOnly);
}

export async function markAsRead(
  notificationId: string,
  token: string
): Promise<NotificationActionResponse> {
  return notificationsApi.markAsRead(notificationId, token);
}

export async function markAllAsRead(
  token: string
): Promise<NotificationActionResponse> {
  return notificationsApi.markAllAsRead(token);
}

export async function deleteNotification(
  notificationId: string,
  token: string
): Promise<NotificationActionResponse> {
  return notificationsApi.delete(notificationId, token);
}
