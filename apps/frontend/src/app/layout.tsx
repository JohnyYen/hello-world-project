import type { Metadata } from "next";
import { Share_Tech_Mono } from 'next/font/google';
import "@/app/globals.css";
import { ThemeProvider } from "@/components/theme/ThemeProvider";

const shareTechMono = Share_Tech_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  weight: '400'
});

// Fuente de respaldo si Google Fonts falla
const fallbackFont = {
  style: {
    fontFamily: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  variable: '--font-sans',
};

export const metadata: Metadata = {
  title: "Plataforma Educativa",
  description: "Sistema de gestión educativa para programación",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" suppressHydrationWarning className={`${shareTechMono.variable} ${fallbackFont.variable}`}>
      <body className="font-sans antialiased">
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
