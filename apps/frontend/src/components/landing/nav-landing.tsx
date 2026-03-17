import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu, Globe } from "lucide-react";
import Link from "next/link";
import { ThemeToggle } from "@/components/theme/theme-toggle";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function NavLanding() {
  return (
    <nav className="sticky top-0 z-50 flex items-center justify-between p-4 border-b border-border/40 bg-background/95 backdrop-blur-sm supports-[backdrop-filter]:bg-background/60">
      <div className="flex items-center space-x-2">
        <Link href="/" className="text-xl font-bold font-mono">
          AprendeProgramación
        </Link>
      </div>

      {/* Desktop Navigation */}
      <div className="hidden md:flex items-center space-x-6 font-mono text-sm">
        <Link
          href="/"
          className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
        >
          Inicio
        </Link>
          <Link
          href="/docs"
          className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
        >
          Docs
        </Link>
        <Link
          href="/#description"
          className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
        >
          Descripción
        </Link>
        <Link
          href="/#features"
          className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
        >
          Características
        </Link>
        <Link
          href="/signup"
          className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
        >
          Regístrate
        </Link>
        <Link
          href="/login"
          className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
        >
          Iniciar Sesión
        </Link>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="default" size="icon">
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
            <Button variant="default" size="icon">
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
            <Button variant="default" size="icon">
              <Menu className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="bg-background border-4 border-foreground shadow-none flat-shadow [&>button]:hidden border-l-4">
            <div className="flex flex-col space-y-4 mt-6 font-mono text-sm">
              <Link
                href="/"
                className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
              >
                Inicio
              </Link>
              <Link
                href="/#description"
                className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
              >
                Descripción
              </Link>
              <Link
                href="/#features"
                className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
              >
                Características
              </Link>
              <Link
                href="/signup"
                className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
              >
                Regístrate
              </Link>
              <Link
                href="/login"
                className="hover:bg-foreground hover:text-background px-2 py-1 transition-colors"
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
