'use client';

import { useState, useEffect, useCallback } from 'react';
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { 
  Bell, 
  BellRing, 
  MessageSquare, 
  Mail, 
  Calendar,
  CheckCircle2,
  Trash2,
  Loader2
} from 'lucide-react';
import type { NotificationItem } from '@/api/types';
import { getNotifications, markAsRead as apiMarkAsRead, markAllAsRead as apiMarkAllAsRead, deleteNotification as apiDeleteNotification } from '@/services/notifications';

export default function NotificationPage() {
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [filter, setFilter] = useState<'all' | 'unread'>('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchNotifications = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      // Always fetch all, filter locally for responsiveness
      const response = await getNotifications(0, 50, false);
      if (response.success && Array.isArray(response.data)) {
        setNotifications(response.data);
        setUnreadCount(response.unread_count ?? 0);
      } else {
        setNotifications([]);
        setUnreadCount(0);
      }
    } catch (err) {
      console.error("Error fetching notifications:", err);
      setError("Error al cargar notificaciones");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  const handleMarkAsRead = async (id: string) => {
    try {
      await apiMarkAsRead(id);
      // Optimistic update
      setNotifications(prev => prev.map(n => 
        n.id === id ? { ...n, read: true } : n
      ));
      setUnreadCount(prev => Math.max(0, prev - 1));
    } catch (err) {
      console.error("Error marking as read:", err);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await apiMarkAllAsRead();
      setNotifications(prev => prev.map(n => ({ ...n, read: true })));
      setUnreadCount(0);
    } catch (err) {
      console.error("Error marking all as read:", err);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await apiDeleteNotification(id);
      setNotifications(prev => prev.filter(n => n.id !== id));
      // Recalculate unread count
      const wasUnread = notifications.find(n => n.id === id)?.read === false;
      if (wasUnread) {
        setUnreadCount(prev => Math.max(0, prev - 1));
      }
    } catch (err) {
      console.error("Error deleting notification:", err);
    }
  };

  const filteredNotifications = filter === 'unread' 
    ? notifications.filter(n => !n.read) 
    : notifications;

  const displayUnreadCount = filter === 'unread' ? filteredNotifications.length : unreadCount;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950/20">
      {/* Background pattern */}
      <div className="fixed inset-0 opacity-[0.03] pointer-events-none">
        <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <div className="container mx-auto py-12 px-6 relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400">
                <Bell className="h-6 w-6" />
              </div>
              <span className="text-sm font-medium text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">
                Notificaciones
              </span>
            </div>
            <h1 className="text-4xl font-bold tracking-tight mb-2 bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400 bg-clip-text text-transparent">
              Centro de Notificaciones
            </h1>
            <p className="text-muted-foreground text-lg">
              Gestiona tus notificaciones y preferencias
            </p>
          </div>
          
          {unreadCount > 0 && (
            <Button 
              onClick={handleMarkAllAsRead}
              variant="outline"
              className="hover:bg-indigo-50 dark:hover:bg-indigo-950/30 hover:border-indigo-400"
            >
              <CheckCircle2 className="h-4 w-4 mr-2" />
              Marcar todo como leído
            </Button>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main notifications list */}
          <div className="lg:col-span-2 space-y-4">
            {/* Filter tabs */}
            <div className="flex gap-2 mb-4">
              <Button
                onClick={() => setFilter('all')}
                variant={filter === 'all' ? 'default' : 'outline'}
                className={filter === 'all' ? 'bg-indigo-600 hover:bg-indigo-700' : ''}
              >
                <Bell className="h-4 w-4 mr-2" />
                Todas ({notifications.length})
              </Button>
              <Button
                onClick={() => setFilter('unread')}
                variant={filter === 'unread' ? 'default' : 'outline'}
                className={filter === 'unread' ? 'bg-indigo-600 hover:bg-indigo-700' : ''}
              >
                <BellRing className="h-4 w-4 mr-2" />
                No leídas ({unreadCount})
              </Button>
            </div>

            {/* Notifications */}
            <div className="space-y-3">
              {loading ? (
                <div className="flex items-center justify-center py-16">
                  <Loader2 className="h-8 w-8 animate-spin text-indigo-500" />
                </div>
              ) : error ? (
                <div className="text-center py-12">
                  <Bell className="h-12 w-12 text-muted-foreground/50 mx-auto mb-4" />
                  <p className="text-muted-foreground">{error}</p>
                  <Button variant="outline" className="mt-4" onClick={fetchNotifications}>
                    Reintentar
                  </Button>
                </div>
              ) : filteredNotifications.length === 0 ? (
                <div className="text-center py-12">
                  <Bell className="h-12 w-12 text-muted-foreground/50 mx-auto mb-4" />
                  <p className="text-muted-foreground">No hay notificaciones</p>
                </div>
              ) : (
                filteredNotifications.map((notification) => (
                  <div 
                    key={notification.id}
                    className={`rounded-xl border transition-all ${
                      notification.read 
                        ? 'border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50' 
                        : 'border-indigo-200 dark:border-indigo-800 bg-indigo-50/50 dark:bg-indigo-950/20'
                    }`}
                  >
                    <div className="p-4 flex items-start gap-4">
                      <div className={`p-2 rounded-lg ${
                        notification.type === 'success' ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/50 dark:text-emerald-400' :
                        notification.type === 'warning' ? 'bg-amber-100 text-amber-600 dark:bg-amber-900/50 dark:text-amber-400' :
                        notification.type === 'error' ? 'bg-red-100 text-red-600 dark:bg-red-900/50 dark:text-red-400' :
                        'bg-indigo-100 text-indigo-600 dark:bg-indigo-900/50 dark:text-indigo-400'
                      }`}>
                        {notification.type === 'success' && <CheckCircle2 className="h-5 w-5" />}
                        {notification.type === 'warning' && <Bell className="h-5 w-5" />}
                        {notification.type === 'error' && <Mail className="h-5 w-5" />}
                        {notification.type === 'info' && <MessageSquare className="h-5 w-5" />}
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className={`font-semibold ${!notification.read ? 'text-indigo-700 dark:text-indigo-300' : ''}`}>
                            {notification.title}
                          </h3>
                          {!notification.read && (
                            <span className="w-2 h-2 rounded-full bg-indigo-500" />
                          )}
                        </div>
                        <p className="text-sm text-muted-foreground">{notification.message}</p>
                        <p className="text-xs text-muted-foreground mt-2 flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          {notification.date}
                        </p>
                      </div>

                      <div className="flex items-center gap-2">
                        {!notification.read && (
                          <Button 
                            size="sm" 
                            variant="ghost"
                            onClick={() => handleMarkAsRead(notification.id)}
                            className="hover:bg-indigo-100 dark:hover:bg-indigo-900/50"
                          >
                            <CheckCircle2 className="h-4 w-4" />
                          </Button>
                        )}
                        <Button 
                          size="sm" 
                          variant="ghost"
                          onClick={() => handleDelete(notification.id)}
                          className="hover:bg-red-100 dark:hover:bg-red-900/50 hover:text-red-600"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Sidebar - Settings */}
          <div className="space-y-6">
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
              <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                <h2 className="text-lg font-semibold">Preferencias</h2>
                <p className="text-sm text-muted-foreground">Configura cómo recibes notificaciones</p>
              </div>
              <div className="p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Notificaciones push</p>
                    <p className="text-sm text-muted-foreground">En el navegador</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <Separator />
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Correo electrónico</p>
                    <p className="text-sm text-muted-foreground">Resumen diario</p>
                  </div>
                  <Switch defaultChecked />
                </div>
                <Separator />
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Notificaciones de estudiantes</p>
                    <p className="text-sm text-muted-foreground">Actividad en cursos</p>
                  </div>
                  <Switch defaultChecked />
                </div>
              </div>
            </div>

            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm shadow-xl shadow-indigo-500/5 overflow-hidden">
              <div className="p-6 border-b border-slate-100 dark:border-slate-800">
                <h2 className="text-lg font-semibold">Estadísticas</h2>
              </div>
              <div className="p-6 grid grid-cols-2 gap-4">
                <div className="text-center p-3 bg-indigo-50 dark:bg-indigo-950/30 rounded-lg border border-indigo-100 dark:border-indigo-800">
                  <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">{notifications.length}</p>
                  <p className="text-xs text-muted-foreground">Total</p>
                </div>
                <div className="text-center p-3 bg-amber-50 dark:bg-amber-950/30 rounded-lg border border-amber-100 dark:border-amber-800">
                  <p className="text-2xl font-bold text-amber-600 dark:text-amber-400">{unreadCount}</p>
                  <p className="text-xs text-muted-foreground">Sin leer</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
