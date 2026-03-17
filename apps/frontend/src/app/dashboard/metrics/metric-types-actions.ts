"use server";

import { revalidatePath } from "next/cache";
import { statisticsService, type MetricType } from "@/services/statistics";

export async function createMetricType(data: {
  name: string;
  code: string;
  description?: string;
}): Promise<MetricType> {
  const result = await statisticsService.createMetricType({
    name: data.name,
    code: data.code,
    description: data.description,
  });

  revalidatePath("/dashboard/metrics");

  return result;
}

export async function deleteMetricType(id: number): Promise<void> {
  await statisticsService.deleteMetricType(id);

  revalidatePath("/dashboard/metrics");
}
