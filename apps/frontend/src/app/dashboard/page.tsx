import { ChartAreaInteractive, SectionCards, DataTable } from "@/components/dashboard";

import data from "./data.json";

export default function Page() {
  return (
    <div className="space-y-6">
      <SectionCards />
      <div className="px-4 lg:px-6">
        <ChartAreaInteractive />
      </div>
      <DataTable data={data} />
    </div>
  );
}
