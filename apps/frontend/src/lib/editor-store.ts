/**
 * Zustand store para el editor de niveles
 * Gestiona el estado global del formulario
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { EditorState, EditorActions, LevelConfig, InitialState, ValidationCriterion, FeedbackMessages, UiConfig, DefinedAction } from '@/types/editor';
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

export const useEditorStore = create<EditorStoreState>((set, get) => ({
  config: createDefaultConfig(),
  saved: false,
  lastSaved: null,
  currentId: null,
  
  actions: {
    // Actualizar campo simple del config
    updateField: <K extends keyof LevelConfig>(field: K, value: LevelConfig[K]) => {
      set(state => ({
        config: { ...state.config, [field]: value },
        saved: false
      }));
    },

    // Actualizar campo en initial_state
    updateInitialField: (key: string, value: unknown) => {
      set(state => ({
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
    removeInitialField: (key: string) => {
      set(state => {
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
    addAvailableBlock: (block: string) => {
      set(state => ({
        config: {
          ...state.config,
          available_blocks: [...state.config.available_blocks, block]
        },
        saved: false
      }));
    },

    // Eliminar bloque disponible
    removeAvailableBlock: (index: number) => {
      set(state => ({
        config: {
          ...state.config,
          available_blocks: state.config.available_blocks.filter((_, i) => i !== index)
        },
        saved: false
      }));
    },

    // Actualizar criterio de validación
    updateValidationCriterion: (index: number, criterion: ValidationCriterion) => {
      set(state => {
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
    addValidationCriterion: () => {
      set(state => ({
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
    removeValidationCriterion: (index: number) => {
      set(state => ({
        config: {
          ...state.config,
          validation_criteria: state.config.validation_criteria.filter((_, i) => i !== index)
        },
        saved: false
      }));
    },

    // Actualizar mensaje de feedback
    updateFeedbackMessage: (type: 'success' | 'failure' | 'hints', value: unknown) => {
      set(state => {
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
    updateUiConfig: (partialConfig: Partial<UiConfig>) => {
      set(state => ({
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
    addAction: () => {
      set(state => ({
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
    updateAction: (index: number, action: DefinedAction) => {
      set(state => {
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
    removeAction: (index: number) => {
      set(state => ({
        config: {
          ...state.config,
          defined_actions: state.config.defined_actions.filter((_, i) => i !== index)
        },
        saved: false
      }));
    },

    // Cargar configuración desde JSON
    loadFromJson: (json: string) => {
      const result = jsonToConfig(json);
      if (result.success && result.config) {
        set({
          config: result.config,
          saved: false,
          lastSaved: null,
          currentId: null
        });
      }
      return result.success;
    },

    // Exportar a JSON
    exportToJson: () => {
      const { config } = get();
      return configToJson(config);
    },

    // Guardar en localStorage
    saveToLocalStorage: () => {
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
    loadFromLocalStorage: (id: string) => {
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
    reset: () => {
      set({
        config: createDefaultConfig(),
        saved: false,
        lastSaved: null,
        currentId: null
      });
    },

    // Generar nuevo ID de segmento
    generateNewSegmentId: () => {
      const id = generateSegmentId();
      set(state => ({
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
