import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import type { ReactNode } from "react";

vi.mock("@/hooks/use-student-reports", () => ({
  useStudentReports: vi.fn(),
}));

vi.mock("@/components/student/student-feedback", () => ({
  StudentFeedback: () => null,
}));

vi.mock("@/components/student/student-feedback-history", () => ({
  StudentFeedbackHistory: () => null,
}));

vi.mock("next/link", () => ({
  default: ({
    children,
    href,
    ...props
  }: {
    children: ReactNode;
    href: string;
  }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

import { useStudentReports } from "@/hooks/use-student-reports";
import type { GameProgressItem } from "@/api/types";
import StudentDetail from "../student-detail";

const mockUseStudentReports = vi.mocked(useStudentReports);

const mockStudent = {
  id: "550e8400-e29b-41d4-a716-446655440000",
  name: "Juan Pérez",
  email: "juan@example.com",
  maxLevel: 5,
  status: "active" as const,
  registrationDate: "2025-01-15T00:00:00Z",
  lastActivity: "2026-06-01T00:00:00Z",
  completedLessons: 12,
  totalLessons: 20,
  progress: 60,
  achievements: ["Primer juego completado"],
};

const baseHookReturn = {
  kpis: null,
  progressOverTime: [],
  levelPerformance: [],
  activityDistribution: [],
  isLoading: false,
  error: null,
};

describe("StudentDetail", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders student information and empty progress state", () => {
    mockUseStudentReports.mockReturnValue({
      ...baseHookReturn,
      gamesProgress: [],
    });

    render(<StudentDetail student={mockStudent} studentId="test-id" />);

    expect(screen.getByText("Juan Pérez")).toBeDefined();
    expect(screen.getByText("juan@example.com")).toBeDefined();
    expect(screen.getByText("Sin progreso registrado")).toBeDefined();
  });

  it("renders game progress cards when gamesProgress has items", () => {
    const gamesProgress: GameProgressItem[] = [
      {
        gameTitle: "Matemáticas Básicas",
        completedSegments: 3,
        totalSegments: 5,
        completionPercentage: 60,
      },
      {
        gameTitle: "Física Divertida",
        completedSegments: 2,
        totalSegments: 4,
        completionPercentage: 50,
      },
    ];

    mockUseStudentReports.mockReturnValue({
      ...baseHookReturn,
      gamesProgress,
    });

    render(<StudentDetail student={mockStudent} studentId="test-id" />);

    expect(screen.getByText("Matemáticas Básicas")).toBeDefined();
    expect(screen.getByText("Física Divertida")).toBeDefined();
    expect(screen.getByText("3 de 5 segmentos completados")).toBeDefined();
    expect(screen.getByText("2 de 4 segmentos completados")).toBeDefined();
    expect(screen.getByText("60%")).toBeDefined();
    expect(screen.getByText("50%")).toBeDefined();
  });

  it("does not show empty message when gamesProgress has items", () => {
    const gamesProgress: GameProgressItem[] = [
      {
        gameTitle: "Matemáticas Básicas",
        completedSegments: 3,
        totalSegments: 5,
        completionPercentage: 60,
      },
    ];

    mockUseStudentReports.mockReturnValue({
      ...baseHookReturn,
      gamesProgress,
    });

    render(<StudentDetail student={mockStudent} studentId="test-id" />);

    expect(screen.queryByText("Sin progreso registrado")).toBeNull();
  });
});
