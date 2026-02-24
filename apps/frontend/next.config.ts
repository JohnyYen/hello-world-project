import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    // ✅ Activado: detectar errores de ESLint en build
    ignoreDuringBuilds: false,
  },
  typescript: {
    // ✅ Activado: detectar errores de TypeScript en build
    ignoreBuildErrors: false,
  },
  // ⚡ Optimización de rendimiento
  experimental: {
    optimizePackageImports: ['lucide-react', '@tanstack/react-query']
  },
  // 📦 Bundle analyzer para desarrollo
  webpack: (config, { dev }) => {
    if (dev) {
      config.devtool = 'eval-source-map';
    }
    return config;
  },
};

export default nextConfig;
