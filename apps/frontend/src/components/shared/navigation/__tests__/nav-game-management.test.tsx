import { render, screen } from "@testing-library/react"
import { NavGameManagement } from "../nav-game-management"
import { SidebarProvider } from "@/components/ui/sidebar"
import { IconListDetails, IconPlus } from "@tabler/icons-react"
import { describe, it, expect } from "vitest"

const items = [
  { title: "Niveles", url: "/dashboard/levels", icon: IconListDetails },
  { title: "Crear Nivel", url: "/dashboard/levels/create", icon: IconPlus },
]

describe("NavGameManagement", () => {
  it("renders label 'Gestión de Juegos y Niveles'", () => {
    render(
      <SidebarProvider>
        <NavGameManagement items={items} />
      </SidebarProvider>
    )
    expect(screen.getByText("Gestión de Juegos y Niveles")).toBeInTheDocument()
  })

  it("renders all menu items with correct titles and links", () => {
    render(
      <SidebarProvider>
        <NavGameManagement items={items} />
      </SidebarProvider>
    )
    items.forEach((item) => {
      expect(screen.getByText(item.title)).toBeInTheDocument()
      const link = screen.getByRole("link", { name: item.title })
      expect(link).toHaveAttribute("href", item.url)
    })
  })
})