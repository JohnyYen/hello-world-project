'use client';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { getAllCourses, getMostRecentCourse } from "./reports-data-provider";
import { useEffect, useState, useRef } from "react";

type CourseSelectorProps = {
  onCourseChange: (course: string) => void;
  initialCourse?: string;
};

export default function CourseSelector({ onCourseChange, initialCourse }: CourseSelectorProps) {
  const [courses, setCourses] = useState<string[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<string>(initialCourse || "");
  const hasInitialized = useRef(false);

  useEffect(() => {
    // Prevent re-running if already initialized
    if (hasInitialized.current) return;
    hasInitialized.current = true;
    
    const loadCourses = async () => {
      const courseList = await getAllCourses();
      setCourses(courseList);
      
      // Set default to the most recent course if no initial course is provided
      if (!initialCourse) {
        const mostRecent = await getMostRecentCourse();
        setSelectedCourse(mostRecent);
        onCourseChange(mostRecent);
      } else {
        setSelectedCourse(initialCourse);
      }
    };

    loadCourses();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Only run once on mount

  const handleCourseChange = (value: string) => {
    setSelectedCourse(value);
    onCourseChange(value);
  };

  return (
    <div className="mb-6">
      <div className="flex items-center space-x-4">
        <label htmlFor="course-select" className="text-sm font-medium">
          Seleccionar Curso:
        </label>
        <Select value={selectedCourse} onValueChange={handleCourseChange}>
          <SelectTrigger id="course-select" className="w-[200px]">
            <SelectValue placeholder="Seleccionar curso" />
          </SelectTrigger>
          <SelectContent>
            {courses.map((course) => (
              <SelectItem key={course} value={course}>
                {course}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}