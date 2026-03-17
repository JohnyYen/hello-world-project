"use client";

import {
  IconCreditCard,
  IconLogout,
  IconNotification,
  IconSettings,
  IconUserCircle,
} from "@tabler/icons-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";
import Link from "next/link";
import { cn } from "@/lib/utils";

interface NavUserProps {
  user: {
    name: string;
    email: string;
    avatar: string;
    role?: string;
    status?: "online" | "away" | "busy" | "offline";
  };
}

const statusColors = {
  online: "bg-emerald-500 shadow-glow-primary",
  away: "bg-amber-500",
  busy: "bg-red-500",
  offline: "bg-slate-400",
};

const statusLabels = {
  online: "En línea",
  away: "Ausente",
  busy: "Ocupado",
  offline: "Desconectado",
};

export function NavUser({ user }: NavUserProps) {
  const { isMobile } = useSidebar();
  const status = user.status || "online";
  const role = user.role || "Usuario";

  const initials = user.name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className={cn(
                "group relative overflow-hidden rounded-xl border-0",
                "bg-transparent transition-all duration-300 ease-out",
                "hover:bg-gradient-to-r hover:from-primary/10 hover:to-accent/10",
                "data-[state=open]:bg-gradient-to-r data-[state=open]:from-primary/15 data-[state=open]:to-accent/15",
                "data-[state=open]:shadow-glow-primary/30"
              )}
            >
              {/* Animated gradient background */}
              <div className="absolute inset-0 -z-10 opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                <div className="absolute inset-0 bg-gradient-to-r from-primary/20 via-accent/10 to-primary/20" />
              </div>

              <div className="relative flex items-center gap-3">
                {/* Avatar with glow effect */}
                <div className="relative">
                  <Avatar className="h-9 w-9 rounded-lg ring-2 ring-primary/20 transition-all duration-300 group-hover:ring-primary/40 group-hover:shadow-glow-primary/50">
                    <AvatarImage src={user.avatar} alt={user.name} />
                    <AvatarFallback className="rounded-lg bg-gradient-to-br from-primary to-accent text-white font-semibold text-sm">
                      {initials}
                    </AvatarFallback>
                  </Avatar>
                  {/* Status indicator */}
                  <span
                    className={cn(
                      "absolute -bottom-0.5 -right-0.5 h-3 w-3 rounded-full border-2 border-background",
                      statusColors[status],
                      "transition-all duration-300 group-hover:scale-110"
                    )}
                  />
                </div>

                {/* User info - hidden on small screens */}
                <div className="grid flex-1 text-left text-sm leading-tight max-lg:hidden">
                  <span className="truncate font-semibold text-foreground">
                    {user.name}
                  </span>
                  <span className="truncate text-xs text-muted-foreground">
                    {role}
                  </span>
                </div>
              </div>
            </SidebarMenuButton>
          </DropdownMenuTrigger>

          <DropdownMenuContent
            className="w-72 rounded-xl border border-border/50 bg-popover/95 backdrop-blur-xl p-1.5 shadow-xl"
            side={"bottom"}
            align="end"
            sideOffset={8}
          >
            {/* User header in dropdown */}
            <DropdownMenuLabel className="p-0">
              <div className="relative overflow-hidden rounded-t-lg bg-gradient-to-r from-primary/10 via-accent/5 to-primary/10 p-4">
                <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-accent/5" />
                <div className="relative flex items-center gap-3">
                  <div className="relative">
                    <Avatar className="h-12 w-12 rounded-xl ring-2 ring-primary/20">
                      <AvatarImage src={user.avatar} alt={user.name} />
                      <AvatarFallback className="rounded-xl bg-gradient-to-br from-primary to-accent text-white font-bold">
                        {initials}
                      </AvatarFallback>
                    </Avatar>
                    <span
                      className={cn(
                        "absolute -bottom-0.5 -right-0.5 h-3.5 w-3.5 rounded-full border-2 border-popover",
                        statusColors[status]
                      )}
                    />
                  </div>
                  <div className="grid flex-1 text-left">
                    <span className="font-semibold text-foreground">
                      {user.name}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {user.email}
                    </span>
                    <span className="mt-1 inline-flex items-center gap-1 text-xs font-medium text-primary">
                      <span
                        className={cn(
                          "h-1.5 w-1.5 rounded-full",
                          statusColors[status]
                        )}
                      />
                      {statusLabels[status]}
                    </span>
                  </div>
                </div>
              </div>
            </DropdownMenuLabel>

            <DropdownMenuSeparator className="my-1" />

            {/* Menu items */}
            <DropdownMenuGroup>
              <DropdownMenuItem className="rounded-lg cursor-pointer group/item" asChild>
                <Link href="/dashboard/account">
                  <IconUserCircle className="mr-2 h-4 w-4 text-primary transition-transform duration-200 group-hover/item:scale-110" />
                  <span>Mi Perfil</span>
                  <span className="ml-auto text-xs text-muted-foreground group-hover/item:text-primary">
                    →
                  </span>
                </Link>
              </DropdownMenuItem>

              <DropdownMenuItem className="rounded-lg cursor-pointer group/item" asChild>
                <Link href="/dashboard/settings">
                  <IconSettings className="mr-2 h-4 w-4 text-accent transition-transform duration-200 group-hover/item:scale-110" />
                  <span>Configuración</span>
                  <span className="ml-auto text-xs text-muted-foreground group-hover/item:text-accent">
                    →
                  </span>
                </Link>
              </DropdownMenuItem>

              <DropdownMenuItem className="rounded-lg cursor-pointer group/item" asChild>
                <Link href="/dashboard/notifications">
                  <IconNotification className="mr-2 h-4 w-4 text-amber-500 transition-transform duration-200 group-hover/item:scale-110" />
                  <span>Notificaciones</span>
                  <span className="ml-auto flex h-5 min-w-5 items-center justify-center rounded-full bg-primary/10 px-1.5 text-xs font-medium text-primary">
                    3
                  </span>
                </Link>
              </DropdownMenuItem>
            </DropdownMenuGroup>

            <DropdownMenuSeparator className="my-2" />

            {/* Logout */}
            <DropdownMenuItem className="rounded-lg cursor-pointer text-destructive/80 hover:bg-destructive/10 hover:text-destructive group/logout">
              <IconLogout className="mr-2 h-4 w-4 transition-transform duration-200 group-hover/logout:translate-x-1" />
              <span className="font-medium">Cerrar Sesión</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
