import { statisticsService, type MetricType } from "@/services/statistics";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { MetricTypeList } from "./metric-type-list";

export async function MetricTypesServer() {
  const metricTypes = await statisticsService.getMetricTypes();

  return (
    <Card className="col-span-full">
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-lg">Tipos de Métricas</CardTitle>
          <p className="text-sm text-muted-foreground">
            Catálogo de métricas disponibles en el sistema
          </p>
        </div>
        <Badge variant="secondary">{metricTypes.length} métricas</Badge>
      </CardHeader>
      <CardContent>
        <MetricTypeList initialMetricTypes={metricTypes} />
      </CardContent>
    </Card>
  );
}
