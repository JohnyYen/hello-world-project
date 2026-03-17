/**
 * Tipos TypeScript para el editor de niveles
 * Basados en standard_config.json
 */

// Estado inicial del nivel (key-value pairs dinámicos)
export interface InitialState {
  [key: string]: string | number | boolean | null | InitialState | InitialState[];
}

// Criterio de validación
export interface ValidationCriterion {
  condition: string;
  description: string;
}

// Mensajes de feedback
export interface FeedbackMessages {
  success: string;
  failure: string;
  hints: string[];
}

// Configuración de UI
export interface CodeEditorConfig {
  syntax_highlighting: boolean;
  line_numbers: boolean;
}

export interface VisualizationConfig {
  show_state: boolean;
  animation_speed: number; // 0.1 a 5.0
}

export interface UiConfig {
  code_editor: CodeEditorConfig;
  visualization: VisualizationConfig;
}

// Acciones definidas
export interface DefinedAction {
  name: string;
  value: string;
}

// Configuración completa del nivel
export interface LevelConfig {
  title: string;
  description?: string;
  segment_id: number;
  version: number;
  initial_state: InitialState;
  expected_outputs: string[];
  available_blocks: string[];
  learning_objective: string;
  environment_data: { [key: string]: unknown };
  execution_rules: { [key: string]: unknown };
  validation_criteria: ValidationCriterion[];
  feedback_messages: FeedbackMessages;
  ui_config: UiConfig;
  defined_actions: DefinedAction[];
}

// Estado del editor
export interface EditorState {
  config: LevelConfig;
  saved: boolean;
  lastSaved: Date | null;
  currentId: string | null; // Para edición
}

// Acciones del store
export interface EditorActions {
  updateField: <K extends keyof LevelConfig>(field: K, value: LevelConfig[K]) => void;
  updateInitialField: (key: string, value: unknown) => void;
  removeInitialField: (key: string) => void;
  addAvailableBlock: (block: string) => void;
  removeAvailableBlock: (index: number) => void;
  updateValidationCriterion: (index: number, criterion: ValidationCriterion) => void;
  addValidationCriterion: () => void;
  removeValidationCriterion: (index: number) => void;
  updateFeedbackMessage: (type: 'success' | 'failure' | 'hints', value: unknown) => void;
  updateUiConfig: (config: Partial<UiConfig>) => void;
  addAction: () => void;
  updateAction: (index: number, action: DefinedAction) => void;
  removeAction: (index: number) => void;
  loadFromJson: (json: string) => void;
  exportToJson: () => string;
  saveToLocalStorage: () => void;
  loadFromLocalStorage: (id: string) => boolean;
  reset: () => void;
  generateNewSegmentId: () => number;
}
