'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
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
  Filter
} from 'lucide-react';

interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  read: boolean;
  date: string;
}

export default function NotificationPage() {
  const [notifications, setNotifications] = useState<Notification[]>([
    { id: '1', title: 'Nuevo estudiante registrado', message: 'Juan Pérez se ha registrado en el curso de Matemáticas I', type: 'info', read: false, date: '2024-03-15' },
    { id: '2', title: 'Nivel completado', message: 'María García ha completado el nivel 5 de Física', type: 'success', read: false, date: '2024-03-14' },
    { id: '3', title: 'Alerta de progreso', message: '3 estudiantes no han accedido en los últimos 7 días', type: 'warning', read: true, date: '2024-03-13' },
    { id: '4', title: 'Reporte de error', message: 'Se reportó un problema con el nivel 3 de Química', type: 'error', read: true, date: '2024-03-12' },
  ]);

  const [filter, setFilter] = useState<'all' | 'unread'>('all');

  const filteredNotifications = filter === 'unread' 
    ? notifications.filter(n => !n.read) 
    : notifications;

  const markAsRead = (id: string) => {
    setNotifications(prev => prev.map(n => 
      n.id === id ? { ...n, read: true } : n
    ));
  };

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  };

  const deleteNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const unreadCount = notifications.filter(n => !n.read).length;

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
              onClick={markAllAsRead}
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
              {filteredNotifications.map((notification) => (
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
                          onClick={() => markAsRead(notification.id)}
                          className="hover:bg-indigo-100 dark:hover:bg-indigo-900/50"
                        >
                          <CheckCircle2 className="h-4 w-4" />
                        </Button>
                      )}
                      <Button 
                        size="sm" 
                        variant="ghost"
                        onClick={() => deleteNotification(notification.id)}
                        className="hover:bg-red-100 dark:hover:bg-red-900/50 hover:text-red-600"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}

              {filteredNotifications.length === 0 && (
                <div className="text-center py-12">
                  <Bell className="h-12 w-12 text-muted-foreground/50 mx-auto mb-4" />
                  <p className="text-muted-foreground">No hay notificaciones</p>
                </div>
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
