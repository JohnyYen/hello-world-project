/**
 * Validación Zod para el editor de niveles
 * Basado en standard_config.json
 */

import { z } from 'zod';

// Validación para estado inicial
export const initialStateSchema = z.record(
  z.union([
    z.string(),
    z.number(),
    z.boolean(),
    z.null(),
    z.lazy(() => initialStateSchema),
    z.array(z.lazy(() => initialStateSchema))
  ])
);

// Validación para criterios de validación
export const validationCriterionSchema = z.object({
  condition: z.string().min(1, "La condición no puede estar vacía"),
  description: z.string().min(1, "La descripción no puede estar vacía")
});

export const validationCriteriaSchema = z.array(validationCriterionSchema);

// Validación para mensajes de feedback
export const feedbackMessagesSchema = z.object({
  success: z.string().min(1, "El mensaje de éxito no puede estar vacío"),
  failure: z.string().min(1, "El mensaje de fallo no puede estar vacío"),
  hints: z.array(z.string().min(1, "Cada hint no puede estar vacío"))
});

// Validación para configuración de UI
export const codeEditorConfigSchema = z.object({
  syntax_highlighting: z.boolean(),
  line_numbers: z.boolean()
});

export const visualizationConfigSchema = z.object({
  show_state: z.boolean(),
  animation_speed: z.number().min(0.1).max(5.0)
});

export const uiConfigSchema = z.object({
  code_editor: codeEditorConfigSchema,
  visualization: visualizationConfigSchema
});

// Validación para acciones definidas
export const definedActionSchema = z.object({
  name: z.string().min(1, "El nombre de la acción no puede estar vacío"),
  value: z.string().min(1, "El valor de la acción no puede estar vacío")
});

export const definedActionsSchema = z.array(definedActionSchema);

// Validación para configuración completa del nivel
export const levelConfigSchema = z.object({
  title: z.string().min(1, "El título es obligatorio").max(200, "El título no puede tener más de 200 caracteres"),
  description: z.string().optional(),
  segment_id: z.number().int().positive("El ID del segmento debe ser un número positivo"),
  version: z.number().int().positive("La versión debe ser un número positivo"),
  initial_state: initialStateSchema,
  expected_outputs: z.array(z.string()),
  available_blocks: z.array(z.string()),
  learning_objective: z.string().min(1, "El objetivo educacional es obligatorio"),
  environment_data: z.record(z.unknown()),
  execution_rules: z.record(z.unknown()),
  validation_criteria: validationCriteriaSchema,
  feedback_messages: feedbackMessagesSchema,
  ui_config: uiConfigSchema,
  defined_actions: definedActionsSchema
});

// Inferir tipos de los schemas
export type LevelConfigSchema = z.infer<typeof levelConfigSchema>;
export type InitialStateSchema = z.infer<typeof initialStateSchema>;
export type ValidationCriterionSchema = z.infer<typeof validationCriterionSchema>;
export type FeedbackMessagesSchema = z.infer<typeof feedbackMessagesSchema>;
export type UiConfigSchema = z.infer<typeof uiConfigSchema>;
export type DefinedActionSchema = z.infer<typeof definedActionSchema>;

// Función de validación con manejo de errores
export function validateLevelConfig(data: unknown): { success: boolean; data?: LevelConfigSchema; errors?: z.ZodError } {
  try {
    const result = levelConfigSchema.parse(data);
    return { success: true, data: result };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error };
    }
    throw error;
  }
}

// Validación parcial (útil para formulario en progreso)
export function partialLevelConfigSchema() {
  return levelConfigSchema.partial();
}
