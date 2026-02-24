import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { Camera, User, Mail, Lock, Save, Settings } from "lucide-react";

// Mock user data - in a real app, this would come from an API
const mockUser = {
  id: "1",
  name: "Dr. María Rodríguez",
  email: "maria.rodriguez@educacion.com",
  role: "teacher",
  avatar: "/placeholder-avatar.jpg", // This would be a real image URL
  username: "mrodriguez"
};

export default function AccountPage() {
  return (
    <div className="container mx-auto py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Settings className="h-8 w-8 text-blue-600" />
          Mi Cuenta
        </h1>
        <p className="text-muted-foreground mt-2">
          Gestiona tu perfil y preferencias de cuenta
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Card */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader className="items-center">
              <Avatar className="h-32 w-32">
                <AvatarImage src={mockUser.avatar} alt={mockUser.name} />
                <AvatarFallback>
                  {mockUser.name
                    .split(" ")
                    .map((n) => n[0])
                    .join("")}
                </AvatarFallback>
              </Avatar>
              <div className="text-center mt-4">
                <h2 className="text-2xl font-bold flex items-center gap-2">
                  {mockUser.name}
                  <Badge variant="secondary" className="text-xs">
                    {mockUser.role === "teacher" ? "Docente" : "Estudiante"}
                  </Badge>
                </h2>
                <p className="text-muted-foreground mt-1">{mockUser.email}</p>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-2">
                <Button variant="outline" className="flex items-center gap-2">
                  <Camera className="h-4 w-4" />
                  Cambiar Avatar
                </Button>
                <Button variant="outline" className="flex items-center gap-2">
                  <Save className="h-4 w-4" />
                  Guardar Cambios
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Account Details */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Información del Perfil</CardTitle>
              <CardDescription>
                Actualiza tu información personal y preferencias
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="name">Nombre Completo</Label>
                  <div className="flex items-center gap-2">
                    <Input id="name" defaultValue={mockUser.name} />
                    <Button size="icon" variant="outline">
                      <User className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Correo Electrónico</Label>
                  <div className="flex items-center gap-2">
                    <Input id="email" type="email" defaultValue={mockUser.email} />
                    <Button size="icon" variant="outline">
                      <Mail className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="username">Nombre de Usuario</Label>
                  <div className="flex items-center gap-2">
                    <Input id="username" defaultValue={mockUser.username} />
                    <Button size="icon" variant="outline">
                      <User className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="role">Rol</Label>
                  <div className="flex items-center gap-2">
                    <Input id="role" value={mockUser.role === "teacher" ? "Docente" : "Estudiante"} readOnly />
                    <Button size="icon" variant="outline" disabled>
                      <User className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Seguridad de la Cuenta</CardTitle>
              <CardDescription>
                Cambia tu contraseña y configura la seguridad de tu cuenta
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="current-password">Contraseña Actual</Label>
                  <div className="flex items-center gap-2">
                    <Input id="current-password" type="password" placeholder="Ingresa tu contraseña actual" />
                    <Button size="icon" variant="outline">
                      <Lock className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <Separator />
                <div className="space-y-2">
                  <Label htmlFor="new-password">Nueva Contraseña</Label>
                  <div className="flex items-center gap-2">
                    <Input id="new-password" type="password" placeholder="Ingresa una nueva contraseña" />
                    <Button size="icon" variant="outline">
                      <Lock className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="confirm-password">Confirmar Nueva Contraseña</Label>
                  <div className="flex items-center gap-2">
                    <Input id="confirm-password" type="password" placeholder="Confirma la nueva contraseña" />
                    <Button size="icon" variant="outline">
                      <Lock className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <div className="pt-4">
                  <Button className="flex items-center gap-2">
                    <Lock className="h-4 w-4" />
                    Actualizar Contraseña
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Conexiones Externas</CardTitle>
              <CardDescription>
                Conecta tu cuenta con otros servicios y plataformas
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-red-100 p-2 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-mail text-red-600">
                      <path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold">Google</h3>
                    <p className="text-sm text-muted-foreground">Cuenta de Google conectada</p>
                  </div>
                </div>
                <Button variant="outline">Desconectar</Button>
              </div>
              
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-gray-800 p-2 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-apple text-white">
                      <path d="M12 2c2 0 4 1 5 3 1 2 1 4 0 6-1 2-3 3-5 3s-4-1-5-3c-1-2-1-4 0-6 1-2 3-3 5-3z"></path>
                      <path d="M12 13c1 0 2 1 2 2v3c0 1-1 2-2 2s-2-1-2-2v-3c0-1 1-2 2-2z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold">Apple</h3>
                    <p className="text-sm text-muted-foreground">Conecta tu cuenta de Apple</p>
                  </div>
                </div>
                <Button variant="outline">Conectar</Button>
              </div>
              
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-blue-500 p-2 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-school text-white">
                      <path d="M14 22v-4a2 2 0 1 0-4 0v4"></path>
                      <path d="M18 8h-6"></path>
                      <path d="M10 8H4"></path>
                      <path d="M18 12H4"></path>
                      <path d="m8 16-3 3 3 3"></path>
                      <path d="m16 19-3-3 3-3"></path>
                      <path d="M16 16c-2 0-3 1-3 3 0 1 1 3 3 3 2 0 3-1 3-3 0-2-1-3-3-3Z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold">Google Classroom</h3>
                    <p className="text-sm text-muted-foreground">Integrado con Google Classroom</p>
                  </div>
                </div>
                <Button variant="outline">Configurar</Button>
              </div>
              
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="bg-green-600 p-2 rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-languages text-white">
                      <path d="m5 8 6 6"></path>
                      <path d="m4 14 6-6 2-3"></path>
                      <path d="M2 5h12"></path>
                      <path d="M7 2h1"></path>
                      <path d="m22 22-5-10-5 10"></path>
                      <path d="M14 18h6"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold">Moodle</h3>
                    <p className="text-sm text-muted-foreground">Cuenta de Moodle conectada</p>
                  </div>
                </div>
                <Button variant="outline">Configurar</Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Preferencias</CardTitle>
              <CardDescription>
                Configura tus preferencias de cuenta
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label>Notificaciones por Email</Label>
                  <p className="text-sm text-muted-foreground">Recibir actualizaciones sobre tu cuenta</p>
                </div>
                <Button variant="outline">Activar</Button>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <Label>Modo Oscuro</Label>
                  <p className="text-sm text-muted-foreground">Cambiar entre temas claros y oscuros</p>
                </div>
                <Button variant="outline">Configurar</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}