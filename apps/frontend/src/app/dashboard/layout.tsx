import { AuthProvider } from "@/context/auth-context";
import { AuthGuard } from "@/components/auth/auth-guard";
import { AppSidebar, SiteHeader } from "@/components/dashboard";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";

export default async function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Don't pass server auth data - let the client handle auth via localStorage.
  // The Server Action login path sets httpOnly cookies, but the client-side
  // login path uses localStorage. To support both, we let the client manage auth.
  return (
    <AuthProvider>
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
