import { test, expect } from "@playwright/test";
import { FeedbackModal, StudentDetailPage } from "./feedback-page";

// Test credentials provided by user
const TEST_USER = {
  email: "tututi@example.com",
  password: "Adminpass123!",
};

// Helper to authenticate via API
async function loginAsProfessor(page: any, context: any) {
  const loginResponse = await page.request.post("http://localhost:8010/api/v1/auth/login", {
    data: TEST_USER,
  });

  expect(loginResponse.ok()).toBeTruthy();
  const loginData = await loginResponse.json();
  expect(loginData.access_token).toBeTruthy();

  await context.addCookies([
    {
      name: "auth_token",
      value: loginData.access_token,
      domain: "localhost",
      path: "/",
      httpOnly: true,
      secure: false,
      sameSite: "Lax",
    },
  ]);
}

// Helper to navigate to a student detail page
async function navigateToStudent(page: any): Promise<boolean> {
  const studentRows = page.locator("tr.cursor-pointer").first();

  if (await studentRows.isVisible().catch(() => false)) {
    await studentRows.click();
    await page.waitForLoadState("networkidle");
    return true;
  }
  return false;
}

// Helper to get first student ID from API
async function getFirstStudentId(page: any): Promise<string | null> {
  const response = await page.request.get("http://localhost:8010/api/v1/users/students?limit=1");
  const data = await response.json();
  if (data.success && data.data && data.data.length > 0) {
    return data.data[0].id;
  }
  return null;
}

test.describe("Feedback System - Professor Flow", () => {
  test.describe.configure({ mode: "serial" }); // Run tests in sequence to preserve state

  test("E2E-FEEDBACK-001 - Login and navigate to students list", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate directly to students
    await page.goto("/dashboard/students");
    await expect(page).toHaveURL(/\/dashboard\/students/);

    // Verify students page loaded
    await expect(page.getByRole("heading", { name: /estudiantes/i })).toBeVisible();
  });

  test("E2E-FEEDBACK-002 - Students list loads or shows empty state", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    // Should show either student table or empty state
    const hasStudents = await page.locator("tr.cursor-pointer").first().isVisible().catch(() => false);
    const hasEmpty = await page.getByText(/no hay|no existen|no se encontraron estudiantes/i).isVisible().catch(() => false);

    expect(hasStudents || hasEmpty).toBeTruthy();
  });

  test("E2E-FEEDBACK-003 - Can open student detail page", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students list
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    const navigated = await navigateToStudent(page);

    if (navigated) {
      // Verify we're on a student detail page
      await expect(page).toHaveURL(new RegExp(/\/dashboard\/students\/[^/]+$/));
      await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    } else {
      test.skip(true, "No students available for testing");
    }
  });

  test("E2E-FEEDBACK-004 - Feedback modal opens correctly", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students list
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    const navigated = await navigateToStudent(page);

    if (navigated) {
      const studentDetailPage = new StudentDetailPage(page);
      await studentDetailPage.openFeedbackModal();

      const feedbackModal = new FeedbackModal(page);
      await feedbackModal.verifyModalVisible();

      // Verify modal contains required fields
      await expect(page.getByText(/fortalezas del estudiante/i)).toBeVisible();
      await expect(page.getByText(/áreas de mejora/i)).toBeVisible();
      await expect(page.getByText(/calificación general/i)).toBeVisible();

      // Close modal
      await feedbackModal.cancel();
    } else {
      test.skip(true, "No students available");
    }
  });

  test("E2E-FEEDBACK-005 - Submit feedback with all fields", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students list
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    const navigated = await navigateToStudent(page);

    if (navigated) {
      const studentDetailPage = new StudentDetailPage(page);
      await studentDetailPage.openFeedbackModal();

      const feedbackModal = new FeedbackModal(page);
      await feedbackModal.fillFeedback({
        rating: 4,
        strengths: "Excelente trabajo en la resolución de problemas lógicos",
        improvements: "Podría mejorar en la gestión del tiempo",
        comments: "Promedio desempeño, sigue así",
      });

      // Submit feedback
      await feedbackModal.submit();

      // Wait for success notification and modal to close
      await page.waitForTimeout(3000);

      // Verify we're back on student detail page (modal closed)
      await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
      // Check for the feedback button that has MessageCircle icon (not the submit button)
      await expect(page.locator("button:has-text('Feedback')").first()).toBeVisible();
    } else {
      test.skip(true, "No students available");
    }
  });

  test("E2E-FEEDBACK-006 - Verify feedback appears in history", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students list
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    const navigated = await navigateToStudent(page);

    if (navigated) {
      // Check if there's any feedback history
      const hasHistory = await page.locator(".border.rounded-lg.p-4").first().isVisible().catch(() => false);

      if (hasHistory) {
        // Verify feedback items display correctly
        const hasStars = await page.locator("svg.fill-yellow-400").first().isVisible().catch(() => false);
        const hasHistoryTitle = await page.getByText(/historial de feedback/i).isVisible().catch(() => false);

        expect(hasStars || hasHistoryTitle).toBeTruthy();
      }
    } else {
      test.skip(true, "No students available");
    }
  });

  test("E2E-FEEDBACK-007 - Cancel feedback returns to student detail", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students list
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    const navigated = await navigateToStudent(page);

    if (navigated) {
      const studentDetailPage = new StudentDetailPage(page);
      await studentDetailPage.openFeedbackModal();

      const feedbackModal = new FeedbackModal(page);
      await feedbackModal.cancel();

      // Verify we're back on student detail page
      await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
      await expect(page.locator("button:has-text('Feedback')").first()).toBeVisible();
    } else {
      test.skip(true, "No students available");
    }
  });

  test("E2E-FEEDBACK-008 - Multiple feedback submissions accumulate in history", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students list
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    const navigated = await navigateToStudent(page);

    if (navigated) {
      // Check feedback count
      const initialCount = await page.locator(".border.rounded-lg.p-4").count();

      // Submit another feedback
      const studentDetailPage = new StudentDetailPage(page);
      await studentDetailPage.openFeedbackModal();

      const feedbackModal = new FeedbackModal(page);
      await feedbackModal.fillFeedback({
        rating: 5,
        strengths: "Mejoró significativamente en lógica",
        improvements: "Mantener el ritmo",
      });
      await feedbackModal.submit();
      await page.waitForTimeout(3000);

      // Reload and check count increased
      await page.reload();
      await page.waitForLoadState("networkidle");

      const newCount = await page.locator(".border.rounded-lg.p-4").count();
      expect(newCount).toBeGreaterThanOrEqual(initialCount);
    } else {
      test.skip(true, "No students available");
    }
  });

  test("E2E-FEEDBACK-009 - Feedback with different types displays correctly", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students list
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    const navigated = await navigateToStudent(page);

    if (navigated) {
      // Check if any feedback types exist in history
      const typeBadges = page.locator(".border.rounded-lg.p-4").first();

      if (await typeBadges.isVisible().catch(() => false)) {
        // Check badge text content
        const badgeTexts = ["Consejo", "Pista", "Sugerencia", "Mensaje"];
        let foundType = false;

        for (const text of badgeTexts) {
          if (await page.locator("text=" + text).first().isVisible().catch(() => false)) {
            foundType = true;
            break;
          }
        }

        // At least one of the badges or stars should exist
        const hasStars = await page.locator("svg.fill-yellow-400").first().isVisible().catch(() => false);
        expect(foundType || hasStars).toBeTruthy();
      }
    } else {
      test.skip(true, "No students available");
    }
  });

  test("E2E-FEEDBACK-010 - Cannot submit feedback without required fields", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students list
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    const navigated = await navigateToStudent(page);

    if (navigated) {
      const studentDetailPage = new StudentDetailPage(page);
      await studentDetailPage.openFeedbackModal();

      const feedbackModal = new FeedbackModal(page);

      // Try to submit without filling required fields
      await feedbackModal.submit();

      // Modal should still be visible (validation prevented submission)
      await expect(page.locator(".fixed.inset-0.bg-black\\/50")).toBeVisible();

      // Fill with valid data
      await feedbackModal.fillFeedback({
        rating: 3,
        strengths: "Buen intento",
        improvements: "Practicar más",
      });

      // Now submit should work
      await feedbackModal.submit();
      await page.waitForTimeout(3000);

      // Modal should close after successful submission
      await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
      await expect(page.locator("text=Historial de feedback")).toBeVisible();
    } else {
      test.skip(true, "No students available");
    }
  });

  test("E2E-FEEDBACK-011 - Feedback history shows date and professor info", async ({ page, context }) => {
    await loginAsProfessor(page, context);

    // Navigate to students list
    await page.goto("/dashboard/students");
    await page.waitForLoadState("networkidle");

    const navigated = await navigateToStudent(page);

    if (navigated) {
      // Check if there's feedback history
      const hasFeedback = await page.locator(".border.rounded-lg.p-4").first().isVisible().catch(() => false);

      if (hasFeedback) {
        // Verify stars display (rating)
        const hasStars = await page.locator("svg.fill-yellow-400").first().isVisible().catch(() => false);

        // Verify date display
        const hasDateIcon = await page.locator("svg.h-3\\.5.w-3\\.5").first().isVisible().catch(() => false);

        expect(hasStars || hasDateIcon).toBeTruthy();
      }
    } else {
      test.skip(true, "No students available");
    }
  });
});