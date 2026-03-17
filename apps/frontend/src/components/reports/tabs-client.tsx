'use client';

import * as React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface TabsClientProps {
  children: React.ReactNode;
  defaultTab?: string;
}

export default function TabsClient({ children, defaultTab = 'overview' }: TabsClientProps) {
  const [activeTab, setActiveTab] = React.useState(defaultTab);
  
  // Parse children to get tabs
  const tabItems = React.Children.toArray(children).filter(
    (child): child is React.ReactElement<{ value: string; children: React.ReactNode }> => {
      if (!React.isValidElement(child)) return false;
      const props = child.props as { value?: string };
      return 'value' in props && typeof props.value === 'string';
    }
  );

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
      <TabsList className="bg-white border border-slate-200 p-1 h-auto">
        <TabsTrigger 
          value="overview" 
          className="flex items-center gap-2 px-4 py-2 data-[state=active]:bg-slate-900 data-[state=active]:text-white"
        >
          <span className="w-4 h-4">📊</span>
          Vista General
        </TabsTrigger>
        <TabsTrigger 
          value="comparison" 
          className="flex items-center gap-2 px-4 py-2 data-[state=active]:bg-slate-900 data-[state=active]:text-white"
        >
          <span className="w-4 h-4">📈</span>
          Comparación
        </TabsTrigger>
      </TabsList>

      {tabItems.map((tab) => (
        <TabsContent key={tab.props.value} value={tab.props.value} className="space-y-6">
          {tab.props.children}
        </TabsContent>
      ))}
    </Tabs>
  );
}
