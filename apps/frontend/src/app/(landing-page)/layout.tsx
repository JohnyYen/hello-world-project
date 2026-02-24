import { NavLanding } from "@/components/landing";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div>
      <NavLanding />
      {children}
    </div>
  );
}
