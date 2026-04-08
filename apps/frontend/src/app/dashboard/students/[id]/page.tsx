import { getStudentById } from "@/components/student/student-data-provider";
import StudentDetail from "@/components/student/student-detail";
import StudentNotFound from "@/components/student/student-not-found";

export default async function StudentPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const student = await getStudentById(id);

  if (!student) {
    return <StudentNotFound />;
  }

  return <StudentDetail student={student} studentId={id} />;
}