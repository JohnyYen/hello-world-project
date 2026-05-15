'use client';

import { useState, useMemo } from 'react';
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
  const [expandedYears, setExpandedYears] = useState<Record<string, boolean>>({});

  // Group courses by school year
  const coursesByYear = useMemo(() => {
    return courses.reduce<Record<string, Course[]>>((acc, course) => {
      const year = course.schoolYear;
      if (!acc[year]) acc[year] = [];
      acc[year].push(course);
      return acc;
    }, {});
  }, [courses]);

  const schoolYears = Object.keys(coursesByYear).sort().reverse();

  // Toggle year expansion
  const toggleYearExpansion = (year: string) => {
    setExpandedYears(prev => ({
      ...prev,
      [year]: !prev[year]
    }));
  };

  const toggleCourse = (courseId: string) => {
    if (selectedCourses.includes(courseId)) {
      onSelectionChange(selectedCourses.filter(id => id !== courseId));
    } else if (maxSelection === undefined || selectedCourses.length < maxSelection) {
      onSelectionChange([...selectedCourses, courseId]);
    }
  };

  // Toggle all courses in a year
  const toggleYear = (year: string) => {
    const yearCourses = coursesByYear[year].map(c => String(c.id));
    const allSelected = yearCourses.every(courseId => selectedCourses.includes(courseId));
    
    if (allSelected) {
      // Deselect all courses in this year
      const newSelection = selectedCourses.filter(id => !yearCourses.includes(id));
      onSelectionChange(newSelection);
    } else {
      // Select all courses in this year and deselect any that were not in this year
      onSelectionChange(yearCourses);
    }
  };

  // Generate display names for selected courses (grouped by year if all courses in year are selected)
  const selectedCourseNames = useMemo(() => {
    const result: string[] = [];
    
    for (const year of schoolYears) {
      const yearCourses = coursesByYear[year];
      const yearCourseIds = yearCourses.map(c => String(c.id));
      const selectedInYear = yearCourseIds.filter(id => selectedCourses.includes(id));
      
      if (selectedInYear.length === yearCourseIds.length) {
        // All courses in this year are selected
        result.push(`${year} (Todos)`);
      } else if (selectedInYear.length > 0) {
        // Some courses in this year are selected
        result.push(...selectedInYear.map(courseId => {
          const course = courses.find(c => c.id === courseId || String(c.id) === courseId);
          return course ? `${course.period} - ${course.schoolYear}` : '';
        }).filter(name => name !== ''));
      }
    }
    
    return result;
  }, [selectedCourses, courses, coursesByYear, schoolYears]);

  // Check if a year is fully selected
  const isYearFullySelected = (year: string) => {
    const yearCourses = coursesByYear[year].map(c => String(c.id));
    return yearCourses.every(courseId => selectedCourses.includes(courseId));
  };

  // Check if a year has partial selection
  const isYearPartiallySelected = (year: string) => {
    const yearCourses = coursesByYear[year].map(c => String(c.id));
    const selectedInYear = yearCourses.filter(id => selectedCourses.includes(id));
    return selectedInYear.length > 0 && selectedInYear.length < yearCourses.length;
  };

  return (
    <Card className="border-0 shadow-lg bg-white/80 dark:bg-slate-900/30 border border-slate-200 dark:border-slate-700/50">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5 text-indigo-400" />
            <CardTitle className="text-lg font-semibold text-slate-600 dark:text-slate-200">Comparar Cursos</CardTitle>
          </div>
          <span className="text-sm text-slate-500 dark:text-slate-400">
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
                ? "border-slate-300 dark:border-slate-600 bg-slate-100 dark:bg-slate-800/50" 
                : "border-slate-300 dark:border-slate-700 hover:border-slate-400 dark:hover:border-slate-600 bg-slate-50 dark:bg-slate-900"
            )}
          >
            <span className={cn(
              "text-sm",
              selectedCourseNames.length > 0 ? "text-slate-900 dark:text-slate-100 font-medium" : "text-slate-500 dark:text-slate-400"
            )}>
              {selectedCourseNames.length > 0 
                ? selectedCourseNames.join(', ')
                : 'Seleccionar cursos para comparar'}
            </span>
            <ChevronDown className={cn(
              "h-4 w-4 text-slate-500 dark:text-slate-400 transition-transform duration-200",
              isOpen && "rotate-180"
            )} />
          </button>

          {/* Dropdown menu */}
          {isOpen && (
            <div className="absolute z-50 w-full mt-2 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 shadow-xl max-h-64 overflow-y-auto">
              {schoolYears.map((year) => {
                const yearCourses = coursesByYear[year];
                const isFullySelected = isYearFullySelected(year);
                const isPartiallySelected = isYearPartiallySelected(year);
                const isExpanded = expandedYears[year] ?? false;
                
                return (
                  <div key={year} className="border-b border-slate-200 dark:border-slate-700 last:border-b-0">
                    {/* Year header */}
                    <div className="flex">
                      <button
                        onClick={() => toggleYearExpansion(year)}
                        className="w-10 flex items-center justify-center transition-colors hover:bg-slate-200 dark:hover:bg-slate-700/30 border-r border-slate-200 dark:border-slate-700"
                      >
                        <ChevronDown className={cn(
                          "h-4 w-4 text-slate-500 dark:text-slate-400 transition-transform duration-200",
                          isExpanded && "rotate-180"
                        )} />
                      </button>
                      <button
                        onClick={() => toggleYear(year)}
                        className="flex-1 flex items-center gap-3 px-4 py-3 text-left transition-colors hover:bg-slate-100 dark:hover:bg-slate-700/50"
                      >
                        <div className={cn(
                          "w-5 h-5 rounded border-2 flex items-center justify-center transition-all",
                          isFullySelected 
                            ? "bg-indigo-500 border-indigo-500" 
                            : isPartiallySelected
                            ? "bg-indigo-500/50 border-indigo-500"
                            : "border-slate-400 dark:border-slate-500"
                        )}>
                          {isFullySelected && <Check className="h-3 w-3 text-white" />}
                          {isPartiallySelected && <div className="w-2 h-2 rounded-full bg-white" />}
                        </div>
                        <div className="flex-1">
                          <p className="text-sm font-medium text-slate-700 dark:text-slate-100">{year} (Todos)</p>
                          <p className="text-xs text-slate-500 dark:text-slate-400">{yearCourses.length} períodos, {yearCourses.reduce((sum, c) => sum + c.totalStudents, 0)} estudiantes</p>
                        </div>
                      </button>
                    </div>
                    
                    {/* Individual periods within the year (only if expanded) */}
                    {isExpanded && (
                      <div className="bg-slate-50 dark:bg-slate-900/30">
                        {yearCourses.map((course) => {
                          const isSelected = selectedCourses.includes(String(course.id));
                          
                          return (
                            <button
                              key={course.id}
                              onClick={() => toggleCourse(String(course.id))}
                              className={cn(
                                "w-full flex items-center gap-3 px-4 py-2 text-left transition-colors hover:bg-slate-100 dark:hover:bg-slate-700/50",
                                isSelected && "bg-indigo-50 dark:bg-slate-700/70"
                              )}
                            >
                              <div className="w-4" /> {/* Spacer for alignment */}
                              <div className={cn(
                                "w-4 h-4 rounded border flex items-center justify-center transition-all",
                                isSelected 
                                  ? "bg-indigo-500 border-indigo-500" 
                                  : "border-slate-400 dark:border-slate-500"
                              )}>
                                {isSelected && <Check className="h-2.5 w-2.5 text-white" />}
                              </div>
                              <div className="flex-1">
                                <p className="text-sm font-medium text-slate-700 dark:text-slate-200">{course.period}</p>
                                <p className="text-xs text-slate-500 dark:text-slate-400">{course.name} - {course.totalStudents} estudiantes</p>
                              </div>
                            </button>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Selected pills */}
        {selectedCourses.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-3">
            {schoolYears.map((year) => {
              const yearCourses = coursesByYear[year];
              const yearCourseIds = yearCourses.map(c => String(c.id));
              const selectedInYear = yearCourseIds.filter(id => selectedCourses.includes(id));
              
              if (selectedInYear.length === yearCourseIds.length) {
                // Show single pill for the whole year
                return (
                  <span
                    key={year}
                    className="inline-flex items-center gap-1 px-3 py-1 bg-indigo-100 dark:bg-indigo-500/20 text-indigo-700 dark:text-indigo-200 text-sm rounded-full border border-indigo-300 dark:border-indigo-500/30"
                  >
                    {year} (Todos)
                    <button
                      onClick={() => toggleYear(year)}
                      className="hover:bg-indigo-200 dark:hover:bg-indigo-600/50 rounded-full p-0.5 ml-1"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                );
              } else if (selectedInYear.length > 0) {
                // Show individual pills for selected courses in the year
                return selectedInYear.map(courseId => {
                  const course = courses.find(c => String(c.id) === courseId);
                  if (!course) return null;
                  
                  return (
                    <span
                      key={courseId}
                      className="inline-flex items-center gap-1 px-3 py-1 bg-indigo-100 dark:bg-indigo-500/20 text-indigo-700 dark:text-indigo-200 text-sm rounded-full border border-indigo-300 dark:border-indigo-500/30"
                    >
                      {course.period} - {course.schoolYear}
                      <button
                        onClick={() => toggleCourse(courseId)}
                        className="hover:bg-indigo-200 dark:hover:bg-indigo-600/50 rounded-full p-0.5 ml-1"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </span>
                  );
                });
              }
              return null;
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
