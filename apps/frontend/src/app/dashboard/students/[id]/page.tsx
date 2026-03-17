import { getStudent } from "@/components/student/student-data-provider";
import StudentDetail from "@/components/student/student-detail";
import StudentNotFound from "@/components/student/student-not-found";

export default async function StudentPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const student = await getStudent(id);

  if (!student) {
    return <StudentNotFound studentId={id} />;
  }

  return <StudentDetail student={student} studentId={id} />;
}