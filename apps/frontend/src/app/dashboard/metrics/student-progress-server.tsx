import { unstable_cache } from 'next/cache';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

// Data fetching
async function getStudentProgress() {
  return unstable_cache(
    async () => {
      await new Promise(resolve => setTimeout(resolve, 80));
      return [
        { id: "1", name: "Juan Pérez", progress: 85, score: 88, lastActivity: "2024-10-28" },
        { id: "2", name: "María González", progress: 92, score: 94, lastActivity: "2024-10-30" },
        { id: "3", name: "Carlos Rodríguez", progress: 65, score: 70, lastActivity: "2024-10-25" },
        { id: "4", name: "Ana López", progress: 78, score: 82, lastActivity: "2024-10-29" },
        { id: "5", name: "Luis Fernández", progress: 45, score: 52, lastActivity: "2024-10-20" },
      ];
    },
    ['student-progress'],
    { revalidate: 300, tags: ['metrics'] }
  )();
}

export async function StudentProgressServer() {
  const students = await getStudentProgress();

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold">Progreso de Estudiantes</CardTitle>
        <CardDescription>Top 5 estudiantes por progreso</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {students.map((student) => (
            <div key={student.id} className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-slate-900">{student.name}</span>
                  <span className="text-sm text-slate-500">{student.progress}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-primary to-primary h-2 rounded-full transition-all duration-500"
                    style={{ width: `${student.progress}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
