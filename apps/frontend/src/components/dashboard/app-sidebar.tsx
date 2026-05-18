"use client"

import * as React from "react"
import Link from "next/link"
import {
  IconBook2,
  IconCamera,
  IconChartBar,
  IconDashboard,
  IconFileAi,
  IconFileDescription,
  IconFolder,
  IconHelp,
  IconInnerShadowTop,
  IconListDetails,
  IconPlus,
  IconSettings,
} from "@tabler/icons-react"

import { NavGameManagement, NavMain, NavSecondary } from "@/components/shared/navigation"
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  navMain: [
    {
      title: "Overview",
      url: "/dashboard",
      icon: IconDashboard,
    },
    {
      title: "Estudiantes",
      url: "/dashboard/students",
      icon: IconListDetails,
    },
    {
      title: "Cursos",
      url: "/dashboard/cursos",
      icon: IconBook2,
    },
    {
      title: "Métricas",
      url: "/dashboard/metrics",
      icon: IconChartBar,
    },
    {
      title: "Reportes",
      url: "/dashboard/reports",
      icon: IconFolder,
    }
  ],
  navGameManagement: [
    {
      title: "Niveles",
      url: "/dashboard/levels",
      icon: IconListDetails,
    },
    {
      title: "Crear Nivel",
      url: "/dashboard/levels/create",
      icon: IconPlus,
    },
  ],
  navClouds: [
    {
      title: "Proyectos Activos",
      icon: IconCamera,
      isActive: true,
      url: "/dashboard/projects",
      items: [
        {
          title: "Propuestas Activas",
          url: "/dashboard/projects/proposals",
        },
        {
          title: "Archivados",
          url: "/dashboard/projects/archived",
        },
      ],
    },
    {
      title: "Documentos",
      icon: IconFileDescription,
      url: "/dashboard/documents",
      items: [
        {
          title: "Propuestas Activas",
          url: "/dashboard/documents/proposals",
        },
        {
          title: "Archivados",
          url: "/dashboard/documents/archived",
        },
      ],
    },
    {
      title: "Recursos",
      icon: IconFileAi,
      url: "/dashboard/resources",
      items: [
        {
          title: "Propuestas Activas",
          url: "/dashboard/resources/proposals",
        },
        {
          title: "Archivados",
          url: "/dashboard/resources/archived",
        },
      ],
    },
  ],
  navSecondary: [
    {
      title: "Settings",
      url: "/dashboard/settings",
      icon: IconSettings,
    },
    {
      title: "Ayuda",
      url: "/dashboard/help",
      icon: IconHelp,
    }
  ],

}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <Link href="/dashboard">
                <IconInnerShadowTop className="!size-5" />
                <span className="text-base font-semibold">Mi Plataforma</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} label="Estadísticas" />
        <NavGameManagement items={data.navGameManagement} />
        <NavSecondary items={data.navSecondary} className="mt-auto" />
      </SidebarContent>
    </Sidebar>
  )
}
