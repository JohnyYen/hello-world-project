# Frontend — Course Management Specification

## Purpose

This specification defines the UI for course management in the professor dashboard: a sidebar navigation item, a course list page with CRUD actions, a course detail page with student management, and a create/edit form with multi-select assignment. All UI text MUST be in Spanish.

## Requirements

### Requirement: Sidebar — Navigation Item "Cursos"

The dashboard sidebar MUST include a new navigation item labeled "Cursos" with a `BookOpen` icon from `@tabler/icons-react`.

The item MUST navigate to `/dashboard/cursos` when clicked.

The item SHOULD be placed below "Estudiantes" and above "Métricas" in the `navMain` section.

#### Scenario: Sidebar displays "Cursos" item

- GIVEN the user is on any dashboard page
- WHEN the sidebar is rendered
- THEN a "Cursos" navigation item is visible
- AND the item displays a `BookOpen` icon
- AND clicking the item navigates to `/dashboard/cursos`

#### Scenario: "Cursos" is active on course pages

- GIVEN the user navigates to `/dashboard/cursos` or `/dashboard/cursos/{id}`
- WHEN the sidebar is rendered
- THEN the "Cursos" item is highlighted as the active page

---

### Requirement: Course List Page — `/dashboard/cursos`

The system MUST provide a page at `/dashboard/cursos` that displays a table of all courses.

The page MUST be a Server Component that fetches course data server-side.

The table MUST display columns: `Nombre`, `Año Escolar`, `Período`, `Estudiantes`, `Profesores`, `Acciones`.

The `Acciones` column MUST include buttons for: `Ver detalle` (link to detail page), `Editar` (opens edit modal/form), `Eliminar` (with confirmation dialog).

The page MUST include a `Crear Curso` button that navigates to or opens the create form.

The page SHOULD display a loading skeleton while the initial data is being fetched.

#### Scenario: Display course list

- GIVEN there are 3 courses in the database
- WHEN the user visits `/dashboard/cursos`
- THEN a table is rendered with 3 rows
- AND each row displays the course name, school year, period label, student count, and professor count
- AND each row has "Ver detalle", "Editar", and "Eliminar" action buttons

#### Scenario: Empty state

- GIVEN there are no courses in the database
- WHEN the user visits `/dashboard/cursos`
- THEN a message "No hay cursos registrados" is displayed
- AND a "Crear Curso" button is prominently shown

#### Scenario: Delete course with confirmation

- GIVEN a course exists in the list
- WHEN the user clicks "Eliminar"
- THEN a confirmation dialog appears with "¿Estás seguro de eliminar este curso?"
- AND the dialog has "Cancelar" and "Eliminar" buttons
- WHEN the user confirms
- THEN the course is soft-deleted
- AND the course row is removed from the table
- AND a success toast "Curso eliminado correctamente" is shown

#### Scenario: Delete course failure

- GIVEN a course exists in the list
- WHEN the user confirms deletion
- AND the API returns an error
- THEN an error toast "Error al eliminar el curso" is shown
- AND the course row remains in the table

---

### Requirement: Course Detail Page — `/dashboard/cursos/[id]`

The system MUST provide a page at `/dashboard/cursos/{id}` that displays full course detail and a table of enrolled students.

The page MUST be a Server Component that fetches course detail server-side.

The header MUST display: course name, school year, period, start/end dates, and description.

The student table MUST display columns: `Nombre`, `Email`, `Fecha de inscripción`, `Acciones`.

The `Acciones` column MUST include an `Desasignar` button per student row.

The page MUST include an `Asignar Estudiantes` button that opens a multi-select dialog to add students.

The page MUST include a `Volver` link to navigate back to `/dashboard/cursos`.

#### Scenario: Display course detail with students

- GIVEN a course with 2 enrolled students
- WHEN the user visits `/dashboard/cursos/{id}`
- THEN the course header shows name, school year, period, dates, and description
- AND a table lists the 2 enrolled students with `Nombre`, `Email`, `Fecha de inscripción`, and `Desasignar` button per row

#### Scenario: Course not found

- GIVEN a course ID that does not exist
- WHEN the user visits `/dashboard/cursos/{non-existent-id}`
- THEN a "Curso no encontrado" message is displayed
- AND a "Volver a cursos" link is provided

#### Scenario: Unassign student with confirmation

- GIVEN a student is enrolled in the course
- WHEN the user clicks "Desasignar"
- THEN a confirmation dialog appears with "¿Estás seguro de desasignar a {student name}?"
- WHEN the user confirms
- THEN the student is unenrolled
- AND the student row is removed from the table
- AND a success toast "Estudiante desasignado correctamente" is shown

#### Scenario: Assign students dialog

- GIVEN a course with available (unenrolled) students
- WHEN the user clicks "Asignar Estudiantes"
- THEN a dialog opens with a multi-select list of available students
- AND each student shows name and email
- AND there is a search input to filter students
- AND a "Asignar" button to confirm the selection
- WHEN the user selects students and clicks "Asignar"
- THEN the selected students appear in the enrolled table
- AND a success toast "Estudiantes asignados correctamente" is shown

#### Scenario: Assign already enrolled student is prevented

- GIVEN a student is already enrolled in the course
- WHEN the "Asignar Estudiantes" dialog is opened
- THEN the already-enrolled student is NOT shown in the available list
- OR is shown but disabled with "Ya inscrito" label

---

### Requirement: Create/Edit Course Form

The system MUST provide a form for creating and editing courses.

The form MUST be a Client Component with the following fields:
- `Nombre del curso` (text, required, max 100 chars)
- `Descripción` (textarea, optional)
- `Año Escolar` (text, required, pattern "YYYY-YYYY", e.g. "2025-2026")
- `Período` (select, required: "Semestre 1", "Semestre 2", "Anual", "Trimestre 1", "Trimestre 2", "Trimestre 3")
- `Fecha de inicio` (date picker, required)
- `Fecha de fin` (date picker, required)
- `Estudiantes` (multi-select with search, optional)
- `Profesores` (multi-select with search, optional)

The form MUST validate all fields with Zod before submission.

The `Año Escolar` field MUST validate the "YYYY-YYYY" format.

The `Fecha de fin` MUST be after `Fecha de inicio`.

When editing, the form MUST pre-populate with existing course data and current assignments.

The form MUST display field-level validation errors in Spanish.

#### Scenario: Create course successfully

- GIVEN the user fills all required fields and selects 2 students and 1 professor
- WHEN the user clicks "Crear Curso"
- THEN a POST request is sent with the form data
- AND on success, the user is redirected to `/dashboard/cursos`
- AND a success toast "Curso creado correctamente" is shown

#### Scenario: Edit course with pre-populated data

- GIVEN the user navigates to edit an existing course with 2 students and 1 professor
- WHEN the edit form loads
- THEN the form fields are pre-filled with existing course data
- AND the student multi-select shows the 2 existing students as selected
- AND the professor multi-select shows the 1 existing professor as selected

#### Scenario: Validation error — end date before start date

- GIVEN the user sets `Fecha de inicio` to 2025-03-01 and `Fecha de fin` to 2025-02-01
- WHEN the user clicks "Crear Curso"
- THEN a validation error "La fecha de fin debe ser posterior a la fecha de inicio" is displayed
- AND the form is NOT submitted

#### Scenario: Validation error — invalid school year format

- GIVEN the user enters "2025" in the `Año Escolar` field
- WHEN the form is validated
- THEN an error "Formato inválido. Use YYYY-YYYY" is displayed

#### Scenario: Server validation error display

- GIVEN the user submits a course with a duplicate `schoolYear` + `periodLabel`
- WHEN the server returns a 409 error
- THEN the error message "Ya existe un curso para este año y período" is displayed in the form
- AND the form data is preserved

#### Scenario: Multi-select search filters students

- GIVEN there are 50 students in the database
- WHEN the user types "Maria" in the multi-select search input
- THEN the list is filtered to show only students matching "Maria"
- AND the search is debounced (300ms minimum)

---

### Requirement: Server Actions for Mutations

All mutations (create, update, delete, assign, unassign) MUST use Server Actions.

Each Server Action MUST validate input using a Zod schema.

Errors MUST be returned as structured objects, not thrown.

#### Scenario: Delete uses Server Action

- GIVEN the user confirms deletion of a course
- WHEN the delete button is clicked
- THEN the form uses a Server Action (`deleteCourseAction`) via `useActionState`
- AND on success, the page revalidates the course list

#### Scenario: Server Action returns validation errors

- GIVEN the user submits invalid form data
- WHEN the Server Action processes it
- THEN it returns `{ errors: { fieldName: "Error message" } }`
- AND the form displays field-level errors

---

### Requirement: Spanish UI Text

All UI text on course management pages MUST be in Spanish.

#### Scenario: All pages use Spanish text

- GIVEN the user navigates to any course management page
- THEN all labels, buttons, placeholders, toasts, errors, and headers are in Spanish
- AND no English UI text is present in the course management feature

---

## Acceptance Criteria

- [ ] Sidebar shows "Cursos" with `BookOpen` icon, navigates to `/dashboard/cursos`
- [ ] `/dashboard/cursos` table displays all courses with student/professor counts
- [ ] Empty state shows "No hay cursos registrados"
- [ ] "Crear Curso" button opens create form
- [ ] Create form validates: required fields, year format, date ordering
- [ ] Create form has multi-select for students and professors with search
- [ ] On successful create, redirect to `/dashboard/cursos` with success toast
- [ ] Edit form pre-populates existing data and assignments
- [ ] Delete shows confirmation dialog, removes course, shows success toast
- [ ] `/dashboard/cursos/{id}` shows course detail and enrolled student table
- [ ] "Desasignar" removes student with confirmation
- [ ] "Asignar Estudiantes" opens multi-select dialog, filters available students
- [ ] All mutations use Server Actions with Zod validation
- [ ] All UI text is in Spanish
- [ ] 404 state for non-existent course detail page
