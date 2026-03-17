/**
 * Zustand store para el editor de niveles
 * Gestiona el estado global del formulario
 */

import { create } from 'zustand';
import type { EditorState, EditorActions, LevelConfig } from '@/types/editor';
import { saveToLocalStorage, loadFromLocalStorage, generateUniqueId, generateSegmentId, configToJson, jsonToConfig, deepClone } from '@/lib/editor-helpers';

// Configuración inicial por defecto
const createDefaultConfig = (): LevelConfig => ({
  title: '',
  description: '',
  segment_id: 1,
  version: 1.0,
  initial_state: {},
  expected_outputs: [],
  available_blocks: [],
  learning_objective: '',
  environment_data: {},
  execution_rules: {},
  validation_criteria: [],
  feedback_messages: {
    success: '',
    failure: '',
    hints: []
  },
  ui_config: {
    code_editor: {
      syntax_highlighting: true,
      line_numbers: true
    },
    visualization: {
      show_state: true,
      animation_speed: 1.0
    }
  },
  defined_actions: []
});

interface EditorStoreState extends EditorState {
  actions: EditorActions;
}

// Definir el tipo para el set y get del store
type SetFn = (partial: Partial<EditorStoreState> | ((state: EditorStoreState) => Partial<EditorStoreState>)) => void;
type GetFn = () => EditorStoreState;

export const useEditorStore = create<EditorStoreState>((set: SetFn, get: GetFn) => ({
  config: createDefaultConfig(),
  saved: false,
  lastSaved: null,
  currentId: null,
  
  actions: {
    // Actualizar campo simple del config
    updateField: <K extends keyof LevelConfig>(field: K, value: LevelConfig[K]): void => {
      set((state: EditorStoreState) => ({
        config: { ...state.config, [field]: value },
        saved: false
      }));
    },

    // Actualizar campo en initial_state
    updateInitialField: (key: string, value: unknown): void => {
      set((state: EditorStoreState) => ({
        config: {
          ...state.config,
          initial_state: {
            ...state.config.initial_state,
            [key]: value
          }
        },
        saved: false
      }));
    },

    // Eliminar campo de initial_state
    removeInitialField: (key: string): void => {
      set((state: EditorStoreState) => {
        const newState = { ...state.config.initial_state };
        delete newState[key];
        return {
          config: {
            ...state.config,
            initial_state: newState
          },
          saved: false
        };
      });
    },

    // Añadir bloque disponible
    addAvailableBlock: (block: string): void => {
      set((state: EditorStoreState) => ({
        config: {
          ...state.config,
          available_blocks: [...state.config.available_blocks, block]
        },
        saved: false
      }));
    },

    // Eliminar bloque disponible
    removeAvailableBlock: (index: number): void => {
      set((state: EditorStoreState) => ({
        config: {
          ...state.config,
          available_blocks: state.config.available_blocks.filter((_: string, i: number) => i !== index)
        },
        saved: false
      }));
    },

    // Actualizar criterio de validación
    updateValidationCriterion: (index: number, criterion: { condition: string; description: string }): void => {
      set((state: EditorStoreState) => {
        const criteria = [...state.config.validation_criteria];
        criteria[index] = criterion;
        return {
          config: {
            ...state.config,
            validation_criteria: criteria
          },
          saved: false
        };
      });
    },

    // Añadir criterio de validación
    addValidationCriterion: (): void => {
      set((state: EditorStoreState) => ({
        config: {
          ...state.config,
          validation_criteria: [
            ...state.config.validation_criteria,
            { condition: '', description: '' }
          ]
        },
        saved: false
      }));
    },

    // Eliminar criterio de validación
    removeValidationCriterion: (index: number): void => {
      set((state: EditorStoreState) => ({
        config: {
          ...state.config,
          validation_criteria: state.config.validation_criteria.filter((_, i: number) => i !== index)
        },
        saved: false
      }));
    },

    // Actualizar mensaje de feedback
    updateFeedbackMessage: (type: 'success' | 'failure' | 'hints', value: unknown): void => {
      set((state: EditorStoreState) => {
        const feedback = { ...state.config.feedback_messages };
        
        if (type === 'success' || type === 'failure') {
          feedback[type] = value as string;
        } else if (type === 'hints') {
          feedback.hints = value as string[];
        }

        return {
          config: {
            ...state.config,
            feedback_messages: feedback
          },
          saved: false
        };
      });
    },

    // Actualizar configuración de UI
    updateUiConfig: (partialConfig: Partial<typeof import('@/types/editor').UiConfig>): void => {
      set((state: EditorStoreState) => ({
        config: {
          ...state.config,
          ui_config: {
            ...state.config.ui_config,
            ...partialConfig
          }
        },
        saved: false
      }));
    },

    // Añadir acción definida
    addAction: (): void => {
      set((state: EditorStoreState) => ({
        config: {
          ...state.config,
          defined_actions: [
            ...state.config.defined_actions,
            { name: '', value: '' }
          ]
        },
        saved: false
      }));
    },

    // Actualizar acción definida
    updateAction: (index: number, action: { name: string; value: string }): void => {
      set((state: EditorStoreState) => {
        const actions = [...state.config.defined_actions];
        actions[index] = action;
        return {
          config: {
            ...state.config,
            defined_actions: actions
          },
          saved: false
        };
      });
    },

    // Eliminar acción definida
    removeAction: (index: number): void => {
      set((state: EditorStoreState) => ({
        config: {
          ...state.config,
          defined_actions: state.config.defined_actions.filter((_, i: number) => i !== index)
        },
        saved: false
      }));
    },

    // Cargar configuración desde JSON
    loadFromJson: (json: string): boolean => {
      const result = jsonToConfig(json);
      if (result.success && result.config) {
        set({
          config: result.config,
          saved: false,
          lastSaved: null,
          currentId: null
        });
        return true;
      }
      return false;
    },

    // Exportar a JSON
    exportToJson: (): string => {
      const { config } = get();
      return configToJson(config);
    },

    // Guardar en localStorage
    saveToLocalStorage: (): string => {
      const { config, currentId } = get();
      const id = currentId || generateUniqueId();
      saveToLocalStorage(id, config);
      set({
        saved: true,
        lastSaved: new Date(),
        currentId: id
      });
      return id;
    },

    // Cargar desde localStorage
    loadFromLocalStorage: (id: string): boolean => {
      const data = loadFromLocalStorage(id);
      if (data) {
        set({
          config: data.config,
          saved: true,
          lastSaved: new Date(data.savedAt),
          currentId: id
        });
        return true;
      }
      return false;
    },

    // Resetear a configuración por defecto
    reset: (): void => {
      set({
        config: createDefaultConfig(),
        saved: false,
        lastSaved: null,
        currentId: null
      });
    },

    // Generar nuevo ID de segmento
    generateNewSegmentId: (): number => {
      const id = generateSegmentId();
      set((state: EditorStoreState) => ({
        config: {
          ...state.config,
          segment_id: id
        }
      }));
      return id;
    }
  }
}));

// Hook para usar el store fácilmente
export const useEditor = () => {
  const { config, saved, lastSaved, currentId, actions } = useEditorStore();
  return {
    config,
    saved,
    lastSaved,
    currentId,
    ...actions
  };
};

export default useEditorStore;
