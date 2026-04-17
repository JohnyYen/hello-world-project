'use client';

import { useState, useEffect } from 'react';
import type { Course } from '@/types/course-report.interface';
import { getCourses } from '@/components/reports/course-report-data';
import { CourseMultiSelector } from '@/components/reports/course-multi-selector';

export default function CourseMultiSelectorClient() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadCourses() {
      const data = await getCourses();
      setCourses(data);
      if (data.length >= 2) {
        setSelectedCourses([String(data[0].id), String(data[1].id)]);
      }
      setLoading(false);
    }
    loadCourses();
  }, []);

  if (loading) {
    return <div className="h-12 bg-slate-200 animate-pulse rounded-lg" />;
  }

  return (
    <CourseMultiSelector
      courses={courses}
      selectedCourses={selectedCourses}
      onSelectionChange={setSelectedCourses}
      maxSelection={4}
    />
  );
}
