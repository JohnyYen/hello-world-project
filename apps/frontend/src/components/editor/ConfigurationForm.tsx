/**
 * Componente principal del formulario del editor de niveles
 * Ensambla todas las secciones del formulario
 */

'use client';

import BasicInfoForm from './BasicInfoForm';
import InitialStateForm from './InitialStateForm';
import AvailableBlocksForm from './AvailableBlocksForm';
import ExecutionRulesForm from './ExecutionRulesForm';
import ValidationCriteriaForm from './ValidationCriteriaForm';
import FeedbackMessagesForm from './FeedbackMessagesForm';
import UIConfigForm from './UIConfigForm';
import DefinedActionsForm from './DefinedActionsForm';

export function ConfigurationForm() {
  return (
    <div className="space-y-6">
      <BasicInfoForm />
      <InitialStateForm />
      <AvailableBlocksForm />
      <ExecutionRulesForm />
      <ValidationCriteriaForm />
      <FeedbackMessagesForm />
      <UIConfigForm />
      <DefinedActionsForm />
    </div>
  );
}

export default ConfigurationForm;
