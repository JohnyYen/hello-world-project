# 📊 Scripts de Rendimiento

## 1. Análisis de Bundle

```bash
# Instalar analyzer
pnpm add -D @next/bundle-analyzer

# Build con análisis
pnpm run build:analyze

# Ver resultados en http://localhost:8888
```

## 2. Lighthouse CI

```bash
# Instalar
pnpm add -D @lhci/cli

# Medir rendimiento
pnpm lhci autorun
```

## 3. Perfetto Trace

```bash
# Habilitar trazas
export NEXT_PRIVATE_BUILD_WORKER=true

# Build con trazas
next build --profile
```

## 4. Medición Manual

Usar DevTools Performance panel para:
- **First Contentful Paint**: < 1.8s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Total Blocking Time**: < 200ms
- **Cumulative Layout Shift**: < 0.1
