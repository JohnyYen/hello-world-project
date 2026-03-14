# 🚀 Optimización de Rendimiento - Aplicación Educativa

## 📊 Estado Actual del Proyecto

### ✅ Implementado
- Next.js 15 con App Router
- React 19 con Server Components
- Tailwind 4
- Recharts para visualización de datos
- shadcn/ui para componentes UI

### 🚨 Cuellos de Botella Identificados

1. **Página de Reportes**: Todos los gráficos son `"use client"` → hidratación completa en cliente
2. **Datos mock**: Sin caché → cada carga recarga los datos
3. **Providers en layout**: `ThemeProvider` y `AuthProvider` fuerzan hidratación en todas las páginas
4. **Sin imágenes optimizadas**: Uso de `next/font/google` pero sin `next/image`
5. **Sin revalidación configurada**: Las rutas dinámicas no tienen caching estratégico

---

## 🎯 Mejoras Prioritarias

### 1. **Convertir Reportes a Server Components con Streaming**

El problema: La página de reportes usa `"use client"` → todo el JS carga en el cliente.

Solución: Separar en componentes server y client, usar `Suspense` para streaming.

```tsx
// ✅ app/dashboard/reports/page.tsx (Server Component por defecto)
import { Suspense } from 'react';
import { CourseSelectorClient } from '@/components/reports/course-selector-client';
import { CourseReportKPIsServer } from '@/components/reports/course-report-kpis-server';
import { LoadingState } from '@/components/ui/loading-state';

export default async function ReportsPage() {
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-8">Reportes de Curso</h1>
      
      {/* Componente client para interactividad */}
      <CourseSelectorClient />
      
      {/* Server components con streaming */}
      <Suspense fallback={<LoadingState message="Cargando métricas..." />}>
        <CourseReportKPIsServer />
      </Suspense>
      
      <Suspense fallback={<LoadingState message="Cargando gráficos..." />}>
        <CourseComparisonServer />
      </Suspense>
    </div>
  );
}
```

### 2. **Implementar Caching con `unstable_cache`**

Creando un servicio con caché optimizado:

```tsx
// src/components/reports/course-report-data.ts
import { unstable_cache } from 'next/cache';

export const getCourses = unstable_cache(
  async () => {
    const response = await fetch(`${process.env.API_URL}/courses`, {
      next: { revalidate: 3600 } // 1 hora
    });
    return response.json();
  },
  ['courses'], // Cache key
  { revalidate: 3600, tags: ['courses'] }
);

export const getCourseMetrics = unstable_cache(
  async (courseId: string) => {
    const response = await fetch(`${process.env.API_URL}/courses/${courseId}/metrics`, {
      next: { revalidate: 1800 }
    });
    return response.json();
  },
  ['course-metrics'], // Se agrega courseId en la función wrapper
  { revalidate: 1800, tags: ['course-metrics'] }
);
```

### 3. **Optimizar Fonts y Eliminar Hidratación Innecesaria**

El layout actual fuerza hidratación en todas las páginas:

```tsx
// ❌ ANTES (fuerza hidratación total)
import { Inter, JetBrains_Mono } from "next/font/google";
// ... luego usa variables de CSS que requieren JS

// ✅ DESPUÉS (SSG puro para fonts)
// Configurar en next.config.ts
const nextConfig: NextConfig = {
  // Enable font optimization
  optimizeFonts: true,
  
  // External fonts loader (más eficiente que next/font)
  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.googlefonts.com',
      },
    ],
  },
};
```

Para fonts, usar la carga optimizada:

```tsx
// ✅ app/fonts.ts (archivo dedicado)
import { Inter, JetBrains_Mono } from 'next/font/google';

export const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-sans',
});

export const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
});
```

### 4. **Implementar Image Optimization**

```tsx
// ✅ Componente Image optimizado
import Image from 'next/image';

function CourseCard({ course }: { course: Course }) {
  return (
    <div className="relative aspect-video">
      <Image
        src={`/api/og?title=${encodeURIComponent(course.name)}`}
        alt={course.name}
        fill
        priority={false} // Solo primeras 3 cards
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        className="object-cover"
      />
    </div>
  );
}
```

### 5. **Split Providers para Reducir Hidratación**

El problema: `ThemeProvider` y `AuthProvider` en el layout root afectan TODAS las páginas.

Solución: Mover providers a nivel de segmento:

```tsx
// ✅ app/layout.tsx (root layout más ligero)
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}

// ✅ app/dashboard/layout.tsx (providers solo para dashboard)
import { ThemeProvider } from "next-themes";
import { AuthProvider } from "@/context/auth-context";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <AuthProvider>{children}</AuthProvider>
    </ThemeProvider>
  );
}
```

### 6. **Optimizar Recharts (Bundle Size)**

Recharts es pesado (~80KB). Usar importación dinámica:

```tsx
// ✅ Componente de gráfico con import dinámico
import dynamic from 'next/dynamic';

const CourseComparisonChart = dynamic(
  () => import('@/components/reports/course-comparison-chart'),
  { 
    ssr: false, // No renderizar en server
    loading: () => <div className="h-80 animate-pulse bg-slate-100 rounded" />
  }
);
```

### 7. **Next.js 15 Partial Prerendering (PPR)**

Para la página de reportes, usar PPR para prerenderar el shell estático:

```tsx
// ✅ app/dashboard/reports/page.tsx con PPR
export const experimental_ppr = true;

export default async function ReportsPage() {
  // Shell estático prerenderizado
  const staticShell = (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-8">Reportes de Curso</h1>
      {/* Sidebar, filtros - todo estático */}
    </div>
  );

  // Contenido dinámico con streaming
  const dynamicContent = (
    <Suspense fallback={<LoadingState />}>
      <CourseMetricsServer />
    </Suspense>
  );

  return (
    <>
      {staticShell}
      {dynamicContent}
    </>
  );
}
```

---

## 📋 Checklist de Implementación

| Prioridad | Acción | Impacto | Dificultad |
|-----------|--------|---------|------------|
| 🔴 Alta | Eliminar `"use client"` de reportes | Alto | Medio |
| 🔴 Alta | Implementar `unstable_cache` | Alto | Bajo |
| 🟡 Media | Split providers por segmento | Medio | Bajo |
| 🟡 Media | Import dinámico de Recharts | Medio | Bajo |
| 🟢 Baja | Optimizar imágenes | Bajo | Medio |
| 🟢 Baja | Implementar PPR | Alto | Alto |

---

## 🧪 Métricas de Referencia

Antes/después de las optimizaciones:

- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1
- **Bundle Size**: Reducir ~40% en reportes
- **Time to Interactive**: Mejorar ~30%

---

## 📦 Scripts de Build Optimizado

```json
{
  "scripts": {
    "build": "next build",
    "build:analyze": "ANALYZE=true next build",
    "build:profile": "next build --profile",
    "start": "next start",
    "lint": "next lint"
  }
}
```

Para análisis de bundle:

```bash
# Instalar
pnpm add -D @next/bundle-analyzer

# next.config.ts
import withBundleAnalyzer from '@next/bundle-analyzer';

const nextConfig: NextConfig = {
  // ...config
};

export default withBundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})(nextConfig);
```

---

## 🔧 Archivos a Modificar

1. `next.config.ts` - Agregar optimizaciones de bundling
2. `src/app/layout.tsx` - Mover providers a dashboard layout
3. `src/app/dashboard/reports/page.tsx` - Convertir a Server Component
4. `src/components/reports/course-report-data.ts` - Agregar caching
5. `src/components/reports/course-comparison-chart.tsx` - Import dinámico

---

## ✅ Resultados Esperados

1. **Build Time**: Reducción de 15-25%
2. **JS Bundle**: Reducción de 40% en página de reportes
3. **TTFB**: Mejora de 30-50% con caching
4. **SEO**: Mejor con Server Components (SSR)
5. **User Experience**: Streaming con Suspense para carga progresiva
