"use client";

import { Separator } from "@/components/ui/separator";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { NavUser } from "@/components/shared/navigation/nav-user";
import { useAuth } from "@/context/auth-context";

export function SiteHeader() {
  const { user, isAuthenticated } = useAuth();

  // Transform user data for NavUser component
  const navUser = isAuthenticated && user
    ? {
        name: user.lastname ? `${user.name} ${user.lastname}` : user.name,
        email: user.email,
        avatar: `/avatars/${user.username}.jpg`, // Fallback to generated path
        role: user.role?.roleName || "Usuario",
        status: user.isActive ? "online" as const : "offline" as const,
      }
    : null;

  return (
    <header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b border-border/50 bg-background/50 backdrop-blur-sm transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
      <div className="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
        <SidebarTrigger className="-ml-1 hover:bg-primary/10 hover:text-primary transition-colors" />
        <Separator
          orientation="vertical"
          className="mx-2 data-[orientation=vertical]:h-4"
        />
        <div className="ml-auto flex items-center gap-2">
          {navUser ? (
            <NavUser user={navUser} />
          ) : (
            // Fallback placeholder when not authenticated
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>Cargando...</span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
