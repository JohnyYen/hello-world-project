import { render, screen } from "@testing-library/react"
import { NavMain } from "../nav-main"
import { SidebarProvider } from "@/components/ui/sidebar"
import { describe, it, expect } from "vitest"

const items = [
  { title: "Dashboard", url: "/dashboard", icon: undefined },
]

describe("NavMain", () => {
  it("renders without label when label prop is omitted", () => {
    render(
      <SidebarProvider>
        <NavMain items={items} />
      </SidebarProvider>
    )
    expect(screen.queryByText("Estadísticas")).not.toBeInTheDocument()
  })

  it("renders label when label prop is provided", () => {
    render(
      <SidebarProvider>
        <NavMain items={items} label="Estadísticas" />
      </SidebarProvider>
    )
    expect(screen.getByText("Estadísticas")).toBeInTheDocument()
  })
})