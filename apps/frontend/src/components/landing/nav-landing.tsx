import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu, Globe } from "lucide-react";
import Link from "next/link";
import { ThemeToggle } from "@/components/dashboard";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function NavLanding() {
  return (
    <nav className="flex items-center justify-between p-4 border-b">
      <div className="flex items-center space-x-2">
        <Link href="/" className="text-xl font-bold">
          AprendeProgramación
        </Link>
      </div>

      {/* Desktop Navigation */}
      <div className="hidden md:flex items-center space-x-6">
        <Link
          href="/"
          className="text-sm font-medium hover:underline underline-offset-4"
        >
          Inicio
        </Link>
          <Link
          href="/docs"
          className="text-sm font-medium hover:underline underline-offset-4"
        >
          Docs
        </Link>
        <Link
          href="/#description"
          className="text-sm font-medium hover:underline underline-offset-4"
        >
          Descripción
        </Link>
        <Link
          href="/#features"
          className="text-sm font-medium hover:underline underline-offset-4"
        >
          Características
        </Link>
        <Link
          href="/signup"
          className="text-sm font-medium hover:underline underline-offset-4"
        >
          Regístrate
        </Link>
        <Link
          href="/login"
          className="text-sm font-medium hover:underline underline-offset-4"
        >
          Iniciar Sesión
        </Link>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" size="icon">
              <Globe className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <span>English</span>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <span>Español</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <ThemeToggle />
      </div>

      {/* Mobile Navigation */}
      <div className="flex items-center space-x-4 md:hidden">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" size="icon">
              <Globe className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <span>English</span>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <span>Español</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <ThemeToggle />
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" size="icon">
              <Menu className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="right">
            <div className="flex flex-col space-y-4 mt-6">
              <Link
                href="/"
                className="text-sm font-medium hover:underline underline-offset-4"
              >
                Inicio
              </Link>
              <Link
                href="/#description"
                className="text-sm font-medium hover:underline underline-offset-4"
              >
                Descripción
              </Link>
              <Link
                href="/#features"
                className="text-sm font-medium hover:underline underline-offset-4"
              >
                Características
              </Link>
              <Link
                href="/signup"
                className="text-sm font-medium hover:underline underline-offset-4"
              >
                Regístrate
              </Link>
              <Link
                href="/login"
                className="text-sm font-medium hover:underline underline-offset-4"
              >
                Iniciar Sesión
              </Link>
            </div>
          </SheetContent>
        </Sheet>
      </div>
    </nav>
  );
}
