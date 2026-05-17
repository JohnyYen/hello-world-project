"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Student } from "@/types";

type StudentFormProps = {
  student: Partial<Student> & { maxLevel: number };
  onChange: (student: Partial<Student> & { maxLevel: number }) => void;
  onSubmit: (e: React.FormEvent) => void;
  onCancel: () => void;
};

export default function StudentForm({ student, onChange, onSubmit, onCancel }: StudentFormProps) {
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    onChange({
      ...student,
      [name]: name === "maxLevel" ? parseInt(value) : value
    });
  };

  // Generate possible course options (from 2020 to 2030)
  const generateCourseOptions = () => {
    const options = [];
    for (let startYear = 2020; startYear <= 2030; startYear++) {
      const endYear = startYear + 3; // Assuming a 3-year course
      options.push(`${startYear}-${endYear}`);
    }
    return options;
  };

  const courseOptions = generateCourseOptions();

  return (
    <form onSubmit={onSubmit}>
      <div className="grid gap-4 py-4">
        <div className="grid grid-cols-4 items-center gap-4">
          <Label htmlFor="name" className="text-right">
            Nombre
          </Label>
          <Input
            id="name"
            name="name"
            value={student.name || ""}
            onChange={handleInputChange}
            className="col-span-3"
            required
            placeholder="Ingrese el nombre completo del estudiante"
            minLength={2}
            aria-describedby="name-error"
          />
          {student.name && student.name.length < 2 && (
            <p id="name-error" className="text-sm text-red-500 col-span-4">
              El nombre debe tener al menos 2 caracteres
            </p>
          )}
        </div>
        <div className="grid grid-cols-4 items-center gap-4">
          <Label htmlFor="email" className="text-right">
            Email
          </Label>
          <Input
            id="email"
            name="email"
            type="email"
            value={student.email || ""}
            onChange={handleInputChange}
            className="col-span-3"
            required
            placeholder="ejemplo@correo.com"
            aria-describedby="email-error"
          />
          {student.email && !student.email.includes('@') && (
            <p id="email-error" className="text-sm text-red-500 col-span-4">
              Ingrese un email válido
            </p>
          )}
        </div>
        <div className="grid grid-cols-4 items-center gap-4">
          <Label htmlFor="maxLevel" className="text-right">
            Nivel Máximo
          </Label>
          <Input
            id="maxLevel"
            name="maxLevel"
            type="number"
            min="1"
            max="20"
            value={student.maxLevel}
            onChange={handleInputChange}
            className="col-span-3"
            required
          />
        </div>
        <div className="grid grid-cols-4 items-center gap-4">
          <Label htmlFor="status" className="text-right">
            Estado
          </Label>
          <Select 
            value={student.status || "active"} 
            onValueChange={(value: "active" | "inactive" | "unregistered") => 
              onChange({...student, status: value})
            }
          >
            <SelectTrigger className="col-span-3">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="active">Activo</SelectItem>
              <SelectItem value="inactive">Inactivo</SelectItem>
              <SelectItem value="unregistered">Pendiente</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="grid grid-cols-4 items-center gap-4">
          <Label htmlFor="course" className="text-right">
            Curso
          </Label>
          <Select 
            value={student.course || "2024-2027"} 
            onValueChange={(value: string) => 
              onChange({...student, course: value})
            }
          >
            <SelectTrigger className="col-span-3">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {courseOptions.map((course) => (
                <SelectItem key={course} value={course}>
                  {course}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
      <div className="flex justify-end space-x-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancelar
        </Button>
        <Button type="submit">Guardar</Button>
      </div>
    </form>
  );
}