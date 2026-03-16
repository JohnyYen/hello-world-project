"use client";

import { Separator } from "@/components/ui/separator";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { NavUser } from "@/components/shared/navigation/nav-user";
import { useAuth } from "@/context/auth-context";

// Demo user for development/preview
const DEMO_USER = {
  name: "Profesor Demo",
  email: "demo@plataforma.com",
  avatar: "",
  role: "Profesor",
  status: "online" as const,
};

export function SiteHeader() {
  const { user, isAuthenticated, isLoading } = useAuth();

  // If still loading, show skeleton or wait
  if (isLoading) {
    return (
      <header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b border-border/50 bg-background/50 backdrop-blur-sm transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
        <div className="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
          <SidebarTrigger className="-ml-1 hover:bg-primary/10 hover:text-primary transition-colors" />
          <Separator orientation="vertical" className="mx-2 data-[orientation=vertical]:h-4" />
          <div className="ml-auto flex items-center gap-2">
            <div className="h-9 w-32 animate-pulse rounded-lg bg-muted" />
          </div>
        </div>
      </header>
    );
  }

  // Use real user if authenticated, otherwise use demo for preview
  const navUser = isAuthenticated && user
    ? {
        name: user.lastname ? `${user.name} ${user.lastname}` : user.name,
        email: user.email,
        avatar: `/avatars/${user.username}.jpg`,
        role: user.role?.roleName || "Usuario",
        status: user.isActive ? "online" as const : "offline" as const,
      }
    : DEMO_USER;

  return (
    <header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b border-border/50 bg-background/50 backdrop-blur-sm transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
      <div className="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
        <SidebarTrigger className="-ml-1 hover:bg-primary/10 hover:text-primary transition-colors" />
        <Separator orientation="vertical" className="mx-2 data-[orientation=vertical]:h-4" />
        <div className="ml-auto flex items-center gap-2">
          <NavUser user={navUser} />
        </div>
      </div>
    </header>
  );
}
