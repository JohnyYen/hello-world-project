import { getStudent } from "@/components/student/student-data-provider";
import StudentDetail from "@/components/student/student-detail";
import StudentNotFound from "@/components/student/student-not-found";

export default async function StudentPage({ params }: { params: { id: string } }) {
  const student = await getStudent(params.id);

  if (!student) {
    return <StudentNotFound studentId={params.id} />;
  }

  return <StudentDetail student={student} studentId={params.id} />;
}