import { AuthProvider } from "@/context/auth-context";
import { AuthGuard } from "@/components/auth/auth-guard";
import { AppSidebar, SiteHeader } from "@/components/dashboard";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { getServerUser } from "@/lib/auth-server";

export default async function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Obtener el usuario desde la cookie del servidor
  const { user, token } = await getServerUser();

  return (
    <AuthProvider initialUser={user} initialToken={token}>
      <AuthGuard>
        <div>
          <SidebarProvider
            style={
              {
                "--sidebar-width": "calc(var(--spacing) * 72)",
                "--header-height": "calc(var(--spacing) * 12)",
              } as React.CSSProperties
            }
          >
            <AppSidebar variant="inset" />
            <SidebarInset>
              <SiteHeader />
              <div className="flex flex-1 flex-col">
                <div className="@container/main flex flex-1 flex-col gap-2">
                  <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
                    {children}
                  </div>
                </div>
              </div>
            </SidebarInset>
          </SidebarProvider>
        </div>
      </AuthGuard>
    </AuthProvider>
  );
}
