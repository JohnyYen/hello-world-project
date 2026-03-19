import { render, screen } from "@testing-library/react"
import { AppSidebar } from "../app-sidebar"
import { SidebarProvider } from "@/components/ui/sidebar"
import { describe, it, expect } from "vitest"

describe("AppSidebar", () => {
  it("renders Estadísticas label for NavMain section", () => {
    render(
      <SidebarProvider>
        <AppSidebar />
      </SidebarProvider>
    )
    expect(screen.getByText("Estadísticas")).toBeInTheDocument()
  })

  it("renders Gestión de Juegos y Niveles label for game management section", () => {
    render(
      <SidebarProvider>
        <AppSidebar />
      </SidebarProvider>
    )
    expect(screen.getByText("Gestión de Juegos y Niveles")).toBeInTheDocument()
  })

  it("renders navigation items for levels and create level", () => {
    render(
      <SidebarProvider>
        <AppSidebar />
      </SidebarProvider>
    )
    const nivelesLink = screen.getByRole("link", { name: /Niveles/i })
    expect(nivelesLink).toHaveAttribute("href", "/dashboard/levels")
    const crearNivelLink = screen.getByRole("link", { name: /Crear Nivel/i })
    expect(crearNivelLink).toHaveAttribute("href", "/dashboard/levels/create")
  })
})