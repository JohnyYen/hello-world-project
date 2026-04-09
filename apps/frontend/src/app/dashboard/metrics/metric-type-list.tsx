"use client";

import { useState } from "react";
import type { MetricType } from "@/services/statistics";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Plus, Trash2, Code, FileText } from "lucide-react";
import { createMetricType, deleteMetricType } from "./metric-types-actions";

interface MetricTypeListProps {
  initialMetricTypes: Array<MetricType>;
}

const metricTypeSchema = {
  name: "",
  code: "",
  description: "",
};

export function MetricTypeList({ initialMetricTypes }: MetricTypeListProps) {
  const [metricTypes, setMetricTypes] = useState<Array<MetricType>>(initialMetricTypes);
  const [isCreating, setIsCreating] = useState(false);
  const [formData, setFormData] = useState(metricTypeSchema);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError("");

    try {
      const result = await createMetricType(formData);
      setMetricTypes([...metricTypes, result]);
      setFormData(metricTypeSchema);
      setIsCreating(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al crear la métrica");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("¿Estás seguro de que deseas eliminar esta métrica?")) {
      return;
    }

    try {
      await deleteMetricType(id);
      setMetricTypes(metricTypes.filter((m) => m.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al eliminar la métrica");
    }
  };

  return (
    <div className="space-y-4">
      {/* Formulario de creación */}
      {isCreating ? (
        <Card className="border-primary/50 bg-primary/5">
          <CardContent className="pt-4">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Nombre</Label>
                  <Input
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="Tiempo de completado"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="code">Código</Label>
                  <Input
                    id="code"
                    value={formData.code}
                    onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                    placeholder="completion_time"
                    required
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="description">Descripción</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Tiempo total que tarda el estudiante en completar la actividad"
                />
              </div>
              {error && (
                <p className="text-sm text-red-500">{error}</p>
              )}
              <div className="flex gap-2">
                <Button type="submit" disabled={isSubmitting}>
                  {isSubmitting ? "Creando..." : "Crear métrica"}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    setIsCreating(false);
                    setFormData(metricTypeSchema);
                    setError("");
                  }}
                >
                  Cancelar
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      ) : (
        <Button onClick={() => setIsCreating(true)} className="gap-2">
          <Plus className="h-4 w-4" />
          Nueva métrica
        </Button>
      )}

      {/* Lista de métricas */}
      {metricTypes.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>No hay métricas definidas</p>
          <p className="text-sm">Crea tu primera métrica para comenzar</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {metricTypes.map((metricType) => (
            <Card key={metricType.id} className="group">
              <CardContent className="pt-4">
                <div className="flex items-start justify-between">
                  <div className="space-y-1 flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold">{metricType.name}</h3>
                    </div>
                    <div className="flex items-center gap-1 text-sm text-muted-foreground">
                      <Code className="h-3 w-3" />
                      <span className="font-mono text-xs">{metricType.code}</span>
                    </div>
                    {metricType.description && (
                      <p className="text-sm text-muted-foreground line-clamp-2">
                        {metricType.description}
                      </p>
                    )}
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="opacity-0 group-hover:opacity-100 transition-opacity"
                    onClick={() => handleDelete(metricType.id)}
                  >
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
