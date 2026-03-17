/**
 * Página de edición de niveles existentes
 */

'use client';

import { useEffect } from 'react';
import { useParams } from 'next/navigation';
import { LevelEditor } from '@/components/editor/LevelEditor';
import { PageHeader, PageHeaderDescription, PageHeaderTitle } from '@/components/ui/page-header';
import { useEditor } from '@/lib/editor-store';

export default function EditLevelPage() {
  const params = useParams();
  const levelId = params.id as string;
  const { loadFromLocalStorage, config } = useEditor();

  useEffect(() => {
    if (levelId) {
      loadFromLocalStorage(levelId);
    }
  }, [levelId, loadFromLocalStorage]);

  return (
    <div className="flex flex-col h-full">
      <PageHeader>
        <PageHeaderTitle>Editar Nivel</PageHeaderTitle>
        <PageHeaderDescription>
          {config.title ? `Editando: ${config.title}` : 'Cargando nivel...'}
        </PageHeaderDescription>
      </PageHeader>

      <div className="flex-1 min-h-0">
        <LevelEditor />
      </div>
    </div>
  );
}
