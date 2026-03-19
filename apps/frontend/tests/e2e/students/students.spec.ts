import { test, expect } from "@playwright/test";
import { StudentsPage } from "./students-page";

test.describe("Students Page", () => {
  test("E2E-STUDENTS-001 - Students page loads correctly", async ({ page }) => {
    const studentsPage = new StudentsPage(page);
    await studentsPage.goto();
    
    await studentsPage.verifyStudentsPage();
  });

  test("E2E-STUDENTS-002 - Students list loads or shows empty state", async ({ page }) => {
    const studentsPage = new StudentsPage(page);
    await studentsPage.goto();
    
    await studentsPage.verifyStudentListOrEmpty();
  });
});
