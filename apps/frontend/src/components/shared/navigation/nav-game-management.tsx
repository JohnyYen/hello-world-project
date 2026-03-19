"use client"

import { type Icon } from "@tabler/icons-react"
import Link from "next/link"

import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

export function NavGameManagement({
  items,
}: {
  items: {
    title: string
    url: string
    icon: Icon
  }[]
}) {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>Gestión de Juegos y Niveles</SidebarGroupLabel>
      <SidebarMenu>
        {items.map((item) => (
          <SidebarMenuItem key={item.title}>
            <SidebarMenuButton asChild>
              <Link href={item.url}>
                <item.icon />
                <span>{item.title}</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        ))}
      </SidebarMenu>
    </SidebarGroup>
  )
}