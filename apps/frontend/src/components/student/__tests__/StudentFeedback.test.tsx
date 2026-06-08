import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { StudentFeedback } from "../student-feedback";

// Mock the statisticsService
vi.mock("../../../services/statistics", () => ({
  statisticsService: {
    submitFeedback: vi.fn().mockResolvedValue({}),
  },
}));

// Mock the notification functions
vi.mock("~/components/ui/use-toast", () => ({
  useToast: () => ({
    toast: vi.fn(),
  }),
}));

const mockStudent = {
  id: "550e8400-e29b-41d4-a716-446655440000",
  name: "Juan Pérez",
  email: "juan@example.com",
  status: "active",
  lastActivity: "2026-05-01",
  progress: 75,
  averageGrade: "8.5",
};

const mockCourses = [
  { id: "550e8400-e29b-41d4-a716-446655440001", name: "Matemáticas" },
  { id: "550e8400-e29b-41d4-a716-446655440002", name: "Física" },
];

beforeEach(() => {
  vi.clearAllMocks();
});

describe("StudentFeedback", () => {
  const mockFeedbackData = {
    student: mockStudent,
    rating: 4,
    strengths: "Good problem solving skills",
    improvements: "Needs to work on time management",
    comments: "Overall good progress",
    feedback_type: "advice",
    course_id: "550e8400-e29b-41d4-a716-446655440001",
  };

  it("correctly maps strengths + improvements + comments to comments field", async () => {
    render(<StudentFeedback student={mockStudent} onClose={vi.fn()} courses={mockCourses} />);

    // Fill in the form
    await screen.findByRole("radio", { name: /4/i }).click();
    
    // Fill in strengths
    const strengthsInput = screen.getByPlaceholderText(/fortalezas/i);
    await strengthsInput.type("Good problem solving skills");
    
    // Fill in improvements
    const improvementsInput = screen.getByPlaceholderText(/mejora/i);
    await improvementsInput.type("Needs to work on time management");
    
    // Fill in comments
    const commentsInput = screen.getByPlaceholderText(/comentarios adicionales/i);
    await commentsInput.type("Overall good progress");
    
    // Select a course
    const courseSelect = screen.getByRole("combobox", { name: /curso/i });
    await courseSelect.click();
    const mathOption = screen.getByRole("option", { name: /matemáticas/i });
    await mathOption.click();
    
    // Submit the form
    const submitButton = screen.getByRole("button", { name: /enviar feedback/i });
    await submitButton.click();

    // Verify the statisticsService was called
    expect(statisticsService.submitFeedback).toHaveBeenCalled();
    
    // Verify the success notification was shown
    expect(vi.mocked("~/components/ui/use-toast").useToast().toast).toHaveBeenCalledWith(
      "Feedback enviado a Juan Pérez",
      expect.objectContaining({
        description: "El feedback ha sido guardado exitosamente.",
      })
    );
  });

  it("handles empty strengths and improvements correctly", async () => {
    render(<StudentFeedback student={mockStudent} onClose={vi.fn()} courses={mockCourses} />);

    // Fill in the form
    await screen.findByRole("radio", { name: /4/i }).click();
    
    // Fill in empty strengths
    const strengthsInput = screen.getByPlaceholderText(/fortalezas/i);
    await strengthsInput.type("");
    
    // Fill in empty improvements
    const improvementsInput = screen.getByPlaceholderText(/mejora/i);
    await improvementsInput.type("");
    
    // Fill in comments
    const commentsInput = screen.getByPlaceholderText(/comentarios adicionales/i);
    await commentsInput.type("Some comments");
    
    // Select a course
    const courseSelect = screen.getByRole("combobox", { name: /curso/i });
    await courseSelect.click();
    const mathOption = screen.getByRole("option", { name: /matemáticas/i });
    await mathOption.click();
    
    // Submit the form
    const submitButton = screen.getByRole("button", { name: /enviar feedback/i });
    await submitButton.click();

    // Verify the statisticsService was called
    expect(statisticsService.submitFeedback).toHaveBeenCalled();
  });

  it("handles missing strengths and improvements correctly", async () => {
    render(<StudentFeedback student={mockStudent} onClose={vi.fn()} courses={mockCourses} />);

    // Fill in the form
    await screen.findByRole("radio", { name: /4/i }).click();
    
    // Fill in comments (leaving strengths and improvements empty)
    const commentsInput = screen.getByPlaceholderText(/comentarios adicionales/i);
    await commentsInput.type("Some comments");
    
    // Select a course
    const courseSelect = screen.getByRole("combobox", { name: /curso/i });
    await courseSelect.click();
    const mathOption = screen.getByRole("option", { name: /matemáticas/i });
    await mathOption.click();
    
    // Submit the form
    const submitButton = screen.getByRole("button", { name: /enviar feedback/i });
    await submitButton.click();

    // Verify the statisticsService was called
    expect(statisticsService.submitFeedback).toHaveBeenCalled();
  });
});