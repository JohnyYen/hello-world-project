'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { BarChart3, Check, ChevronDown, X } from 'lucide-react';
import type { Course } from '@/types/course-report.interface';

interface CourseMultiSelectorProps {
  courses: Course[];
  selectedCourses: string[];
  onSelectionChange: (selected: string[]) => void;
  maxSelection?: number | undefined;
}

export function CourseMultiSelector({
  courses,
  selectedCourses,
  onSelectionChange,
  maxSelection = undefined
}: CourseMultiSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  const toggleCourse = (courseId: string) => {
    if (selectedCourses.includes(courseId)) {
      onSelectionChange(selectedCourses.filter(id => id !== courseId));
    } else if (maxSelection === undefined || selectedCourses.length < maxSelection) {
      onSelectionChange([...selectedCourses, courseId]);
    }
  };

  const selectedCourseNames = courses
    .filter(c => selectedCourses.includes(c.id))
    .map(c => `${c.period} - ${c.schoolYear}`);

  return (
    <Card className="border-0 shadow-lg bg-slate-900/30 border border-slate-700/50">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5 text-indigo-400" />
            <CardTitle className="text-lg font-semibold text-slate-200">Comparar Cursos</CardTitle>
          </div>
          <span className="text-sm text-slate-400">
            {maxSelection !== undefined 
              ? `${selectedCourses.length}/${maxSelection} seleccionados`
              : `${selectedCourses.length} seleccionados`}
          </span>
        </div>
      </CardHeader>
      <CardContent>
        {/* Dropdown selector */}
        <div className="relative">
          <button
            onClick={() => setIsOpen(!isOpen)}
            className={cn(
              "w-full flex items-center justify-between px-4 py-3 rounded-lg border transition-all duration-200",
              isOpen 
                ? "border-slate-600 bg-slate-800/50" 
                : "border-slate-700 hover:border-slate-600 bg-slate-900"
            )}
          >
            <span className={cn(
              "text-sm",
              selectedCourseNames.length > 0 ? "text-slate-100 font-medium" : "text-slate-400"
            )}>
              {selectedCourseNames.length > 0 
                ? selectedCourseNames.join(', ')
                : 'Seleccionar cursos para comparar'}
            </span>
            <ChevronDown className={cn(
              "h-4 w-4 text-slate-400 transition-transform duration-200",
              isOpen && "rotate-180"
            )} />
          </button>

          {/* Dropdown menu */}
          {isOpen && (
            <div className="absolute z-50 w-full mt-2 bg-slate-800 rounded-lg border border-slate-700 shadow-xl max-h-64 overflow-y-auto">
              {courses.map((course) => {
                const isSelected = selectedCourses.includes(course.id);
                const isDisabled = !isSelected && maxSelection !== undefined && selectedCourses.length >= maxSelection;
                
                return (
                  <button
                    key={course.id}
                    onClick={() => !isDisabled && toggleCourse(course.id)}
                    disabled={isDisabled}
                    className={cn(
                      "w-full flex items-center gap-3 px-4 py-3 text-left transition-colors",
                      isDisabled && "opacity-50 cursor-not-allowed",
                      !isDisabled && "hover:bg-slate-700/50",
                      isSelected && "bg-slate-700/70"
                    )}
                  >
                    <div className={cn(
                      "w-5 h-5 rounded border-2 flex items-center justify-center transition-all",
                      isSelected 
                        ? "bg-indigo-500 border-indigo-500" 
                        : "border-slate-500"
                    )}>
                      {isSelected && <Check className="h-3 w-3 text-white" />}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-100">{course.period} - {course.schoolYear}</p>
                      <p className="text-xs text-slate-400">{course.name} - {course.totalStudents} estudiantes</p>
                    </div>
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Selected pills */}
        {selectedCourses.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-3">
            {selectedCourses.map((courseId) => {
              const course = courses.find(c => c.id === courseId);
              if (!course) return null;
              
              return (
                <span
                  key={courseId}
                  className="inline-flex items-center gap-1 px-3 py-1 bg-indigo-500/20 text-indigo-200 text-sm rounded-full border border-indigo-500/30"
                >
                  {course.period} - {course.schoolYear}
                  <button
                    onClick={() => toggleCourse(courseId)}
                    className="hover:bg-indigo-600/50 rounded-full p-0.5 ml-1"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </span>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
