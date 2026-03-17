/**
 * Página de creación de nuevos niveles
 */

'use client';

import { LevelEditor } from '@/components/editor/LevelEditor';
import { PageHeader, PageHeaderDescription, PageHeaderTitle } from '@/components/ui/page-header';

export default function CreateLevelPage() {
  return (
    <div className="flex flex-col h-full">
      <PageHeader>
        <PageHeaderTitle>Nuevo Nivel</PageHeaderTitle>
        <PageHeaderDescription>
          Crea un nuevo nivel educativo configurando sus parámetros.
        </PageHeaderDescription>
      </PageHeader>

      <div className="flex-1 min-h-0">
        <LevelEditor />
      </div>
    </div>
  );
}
