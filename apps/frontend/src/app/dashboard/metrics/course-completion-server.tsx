import { unstable_cache } from 'next/cache';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

async function getCourseCompletion() {
  return unstable_cache(
    async () => {
      await new Promise(resolve => setTimeout(resolve, 80));
      return [
        { courseId: "c1", courseName: "Introducción a la Programación", completionRate: 85, enrolled: 120, completed: 102 },
        { courseId: "c2", courseName: "Fundamentos de JavaScript", completionRate: 78, enrolled: 95, completed: 74 },
        { courseId: "c3", courseName: "Estructuras de Datos", completionRate: 65, enrolled: 80, completed: 52 },
        { courseId: "c4", courseName: "Algoritmos", completionRate: 58, enrolled: 75, completed: 44 },
        { courseId: "c5", courseName: "Programación Orientada a Objetos", completionRate: 72, enrolled: 88, completed: 63 },
      ];
    },
    ['course-completion'],
    { revalidate: 300, tags: ['metrics'] }
  )();
}

export async function CourseCompletionServer() {
  const courses = await getCourseCompletion();

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold">Completado de Cursos</CardTitle>
        <CardDescription>Porcentaje de estudiantes por curso</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {courses.map((course) => (
            <div key={course.courseId} className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-900 truncate flex-1 mr-2">
                  {course.courseName}
                </span>
                <span className="text-sm text-slate-500 whitespace-nowrap">
                  {course.completed}/{course.enrolled}
                </span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2">
                <div 
                  className="bg-gradient-to-r from-emerald-500 to-emerald-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${course.completionRate}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
