import CourseTable from "@/components/courses/course-table";
import { coursesApi } from "@/api/client";
import { cookies } from "next/headers";

export const dynamic = "force-dynamic";

export default async function CursosPage() {
  const token = (await cookies()).get("auth_token")?.value;
  if (!token) return <div className="p-6 text-center text-muted-foreground">No autenticado</div>;

  const [courses, students, professors, games] = await Promise.all([
    coursesApi.list(token),
    coursesApi.listByRole("student", token),
    coursesApi.listByRole("professor", token),
    coursesApi.listGames(token),
  ]);

  // Build gamesMap: id → title
  const gamesMap: Record<string, string> = {};
  games.forEach((g) => {
    gamesMap[g.id] = g.title;
  });

  return (
    <CourseTable
      initialCourses={courses.items}
      total={courses.total}
      students={students}
      professors={professors}
      games={games}
      gamesMap={gamesMap}
    />
  );
}
