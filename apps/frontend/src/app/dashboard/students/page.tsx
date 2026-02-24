import StudentTable from "@/components/student/student-table";
import { getStudents, getUniqueCourses } from "@/components/student/student-data-provider";

export default async function StudentPage() {
  const students = await getStudents();
  const courses = await getUniqueCourses();

  return <StudentTable initialStudents={students} initialCourses={courses} />;
}
