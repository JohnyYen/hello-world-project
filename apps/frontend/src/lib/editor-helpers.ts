/**
 * Helpers para el editor de niveles
 * - localStorage utilities
 * - Conversión JSON
 * - Generación de IDs
 */

import { LevelConfig } from '@/types/editor';
import { levelConfigSchema, validateLevelConfig } from '@/lib/editor-validation';

const STORAGE_KEY_PREFIX = 'level-editor-';

// ==================== LOCALSTORAGE ====================

/**
 * Guarda la configuración en localStorage
 */
export function saveToLocalStorage(id: string, config: LevelConfig): void {
  try {
    const key = `${STORAGE_KEY_PREFIX}${id}`;
    const data = {
      config,
      savedAt: new Date().toISOString()
    };
    localStorage.setItem(key, JSON.stringify(data));
  } catch (error) {
    console.error('Error guardando en localStorage:', error);
  }
}

/**
 * Carga la configuración desde localStorage
 */
export function loadFromLocalStorage(id: string): { config: LevelConfig; savedAt: string } | null {
  try {
    const key = `${STORAGE_KEY_PREFIX}${id}`;
    const data = localStorage.getItem(key);
    
    if (!data) {
      return null;
    }

    const parsed = JSON.parse(data);
    
    // Validar el esquema
    const validation = validateLevelConfig(parsed.config);
    if (!validation.success) {
      console.warn('Configuración inválida en localStorage:', validation.errors);
      return null;
    }

    return {
      config: parsed.config,
      savedAt: parsed.savedAt
    };
  } catch (error) {
    console.error('Error cargando desde localStorage:', error);
    return null;
  }
}

/**
 * Elimina una configuración de localStorage
 */
export function removeFromLocalStorage(id: string): void {
  try {
    const key = `${STORAGE_KEY_PREFIX}${id}`;
    localStorage.removeItem(key);
  } catch (error) {
    console.error('Error eliminando de localStorage:', error);
  }
}

/**
 * Lista todos los niveles guardados en localStorage
 */
export function listSavedLevels(): Array<{ id: string; title: string; savedAt: string }> {
  const levels: Array<{ id: string; title: string; savedAt: string }> = [];
  
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && key.startsWith(STORAGE_KEY_PREFIX)) {
      try {
        const data = localStorage.getItem(key);
        if (data) {
          const parsed = JSON.parse(data);
          const id = key.replace(STORAGE_KEY_PREFIX, '');
          levels.push({
            id,
            title: parsed.config?.title || 'Sin título',
            savedAt: parsed.savedAt || new Date().toISOString()
          });
        }
      } catch (error) {
        console.warn(`Error parseando nivel ${key}:`, error);
      }
    }
  }

  return levels.sort((a, b) => new Date(b.savedAt).getTime() - new Date(a.savedAt).getTime());
}

// ==================== CONVERSIÓN JSON ====================

/**
 * Convierte la configuración a JSON string
 */
export function configToJson(config: LevelConfig): string {
  return JSON.stringify(config, null, 2);
}

/**
 * Convierte JSON string a configuración
 */
export function jsonToConfig(json: string): { success: boolean; config?: LevelConfig; error?: string } {
  try {
    const parsed = JSON.parse(json);
    const validation = validateLevelConfig(parsed);
    
    if (!validation.success) {
      return {
        success: false,
        error: 'JSON inválido: ' + validation.errors?.issues.map(e => e.message).join(', ')
      };
    }

    return {
      success: true,
      config: validation.data
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Error desconocido'
    };
  }
}

// ==================== GENERACIÓN DE IDs ====================

/**
 * Genera un ID único para un nuevo nivel
 */
export function generateUniqueId(): string {
  return `level-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}

/**
 * Genera un ID de segmento secuencial basado en niveles existentes
 */
export function generateSegmentId(): number {
  const levels = listSavedLevels();
  if (levels.length === 0) return 1;
  
  // Extraer el máximo segment_id de los niveles guardados
  let maxId = 0;
  levels.forEach(level => {
    const data = loadFromLocalStorage(level.id);
    if (data?.config.segment_id && data.config.segment_id > maxId) {
      maxId = data.config.segment_id;
    }
  });
  
  return maxId + 1;
}

// ==================== UTILIDADES ====================

/**
 * Clona un objeto profundamente (útil para resetear state)
 */
export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Formatea una fecha para mostrar en la UI
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Decarga JSON como archivo
 */
export function downloadJson(config: LevelConfig, filename?: string): void {
  const json = configToJson(config);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = filename || `${config.title || 'nivel'}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Copia JSON al portapapeles
 */
export async function copyJsonToClipboard(config: LevelConfig): Promise<boolean> {
  try {
    const json = configToJson(config);
    await navigator.clipboard.writeText(json);
    return true;
  } catch (error) {
    console.error('Error copiando al portapapeles:', error);
    return false;
  }
}
