import { toast } from "sonner";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";

interface NotificationOptions {
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export class NotificationService {
  constructor(private router?: AppRouterInstance) {}

  success(message: string, options?: NotificationOptions) {
    return toast.success(message, {
      description: options?.description,
      action: options?.action ? {
        label: options.action.label,
        onClick: options.action.onClick,
      } : undefined,
    });
  }

  error(message: string, options?: NotificationOptions) {
    return toast.error(message, {
      description: options?.description,
      action: options?.action ? {
        label: options.action.label,
        onClick: options.action.onClick,
      } : undefined,
    });
  }

  info(message: string, options?: NotificationOptions) {
    return toast.info(message, {
      description: options?.description,
      action: options?.action ? {
        label: options.action.label,
        onClick: options.action.onClick,
      } : undefined,
    });
  }

  warning(message: string, options?: NotificationOptions) {
    return toast.warning(message, {
      description: options?.description,
      action: options?.action ? {
        label: options.action.label,
        onClick: options.action.onClick,
      } : undefined,
    });
  }

  loading(message: string) {
    return toast.loading(message);
  }

  dismiss(id?: string | number) {
    toast.dismiss(id);
  }

  // Navigation helper
  successWithNavigation(message: string, href: string, options?: Omit<NotificationOptions, 'action'>) {
    return this.success(message, {
      description: options?.description,
      action: {
        label: "Ver",
        onClick: () => this.router?.push(href),
      },
    });
  }

  // Form feedback
  formError(field: string, message: string) {
    return this.error(`${field}: ${message}`);
  }

  formSuccess(message: string, description?: string) {
    return this.success(message, {
      description: description || "Los cambios han sido guardados exitosamente.",
    });
  }

  // CRUD operations
  created(entity: string, name?: string) {
    const entityName = name || `${entity} creado exitosamente`;
    return this.success(entityName, {
      description: `El ${entity.toLowerCase()} ha sido agregado al sistema.`,
    });
  }

  updated(entity: string, name?: string) {
    const entityName = name || `${entity} actualizado exitosamente`;
    return this.success(entityName, {
      description: `Los cambios en el ${entity.toLowerCase()} han sido guardados.`,
    });
  }

  deleted(entity: string, name?: string) {
    const entityName = name || `${entity} eliminado exitosamente`;
    return this.success(entityName, {
      description: `El ${entity.toLowerCase()} ha sido eliminado del sistema.`,
    });
  }

  // Error handling
  apiError(error: any, fallbackMessage = "Error de conexión") {
    const message = error?.message || error?.data?.message || fallbackMessage;
    return this.error(message, {
      description: "Por favor, intenta nuevamente más tarde.",
    });
  }

  networkError() {
    return this.error("Error de conexión", {
      description: "No se pudo conectar con el servidor. Verifica tu conexión a internet.",
    });
  }

  unauthorized() {
    return this.error("No autorizado", {
      description: "Tu sesión ha expirado. Por favor, inicia sesión nuevamente.",
      action: {
        label: "Iniciar Sesión",
        onClick: () => this.router?.push("/login"),
      },
    });
  }
}

// Singleton instance
export const notifications = new NotificationService();

// Hook for components
export function useNotifications(router?: AppRouterInstance) {
  return new NotificationService(router);
}