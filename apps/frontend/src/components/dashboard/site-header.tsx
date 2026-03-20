"use client";

import { useState } from "react";
import { Separator } from "@/components/ui/separator";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { NavUser } from "@/components/shared/navigation/nav-user";
import { useAuth } from "@/context/auth-context";
import { ThemeToggle } from "@/components/theme/theme-toggle";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { cn } from "@/lib/utils";

// Demo user for development/preview
const DEMO_USER = {
  name: "Profesor Demo",
  email: "demo@plataforma.com",
  avatar: "",
  role: "Profesor",
  status: "online" as const,
};

const languages = [
  { code: "es", label: "Español", flag: "🇪🇸" },
  { code: "en", label: "English", flag: "🇺🇸" },
];

export function SiteHeader() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const [currentLang, setCurrentLang] = useState("es");

  // If still loading, show skeleton
  if (isLoading) {
    return (
      <header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b border-border/50 bg-background/50 backdrop-blur-sm transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
        <div className="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
          <SidebarTrigger className="-ml-1 hover:bg-primary/10 hover:text-primary transition-colors" />
          <Separator orientation="vertical" className="mx-2 data-[orientation=vertical]:h-4" />
          <div className="ml-auto flex items-center gap-3">
            <div className="h-9 w-32 animate-pulse rounded-lg bg-muted" />
            <div className="h-9 w-9 animate-pulse rounded-lg bg-muted" />
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
        role: user.role?.role_name || user.role?.roleName || "Usuario",
        status: user.is_active ? "online" as const : "offline" as const,
      }
    : DEMO_USER;

  const currentLanguage = languages.find((l) => l.code === currentLang) || languages[0];

  return (
    <header className="flex h-(--header-height) shrink-0 items-center gap-2 border-b border-border/50 bg-background/50 backdrop-blur-sm transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
      <div className="flex w-full items-center gap-1 px-4 lg:gap-2 lg:px-6">
        <SidebarTrigger className="-ml-1 hover:bg-primary/10 hover:text-primary transition-colors" />
        <Separator orientation="vertical" className="mx-2 data-[orientation=vertical]:h-4" />
        
        <div className="ml-auto flex items-center gap-2">
          {/* Language Selector */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className={cn(
                  "relative flex items-center gap-2 px-3 h-9",
                  "hover:bg-primary/10 hover:text-primary transition-all duration-200",
                  "rounded-lg border border-transparent hover:border-primary/20"
                )}
              >
                <span className="text-base">{currentLanguage.flag}</span>
                <span className="text-sm font-medium max-lg:hidden">
                  {currentLanguage.code.toUpperCase()}
                </span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              align="end"
              className="rounded-xl border border-border/50 bg-popover/95 backdrop-blur-xl p-1.5 shadow-xl"
              sideOffset={8}
            >
              {languages.map((lang) => (
                <DropdownMenuItem
                  key={lang.code}
                  onClick={() => setCurrentLang(lang.code)}
                  className={cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2 cursor-pointer",
                    "transition-all duration-150",
                    "hover:bg-primary/10 hover:text-primary",
                    currentLang === lang.code && "bg-primary/15 text-primary font-medium"
                  )}
                >
                  <span className="text-base">{lang.flag}</span>
                  <span>{lang.label}</span>
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Theme Toggle */}
          <ThemeToggle />

          {/* User Menu */}
          <NavUser user={navUser} />
        </div>
      </div>
    </header>
  );
}
