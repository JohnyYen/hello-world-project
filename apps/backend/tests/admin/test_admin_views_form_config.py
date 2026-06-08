"""
Unit tests for SQLAdmin ModelView form configuration across all admin views.

Verifies that the create/edit form for every admin view excludes the
**inverse side** of its SQLAlchemy relationships.

Background
----------
By default, SQLAdmin auto-renders every SQLAlchemy relationship as a
`<select multiple>` widget in the create/edit form. For inverse relationships
(one-to-many "children" of the model), this is wrong on two axes:

  1. Semantically: a child row does not exist yet when the parent is being
     created, so the select would always be empty in practice (and even if
     it weren't, the user would be assigning children they have no business
     touching from this form).
  2. Performance: SQLAdmin runs a `SELECT *` against the child table on
     every form render to populate the widget, which gets worse as the
     table grows.

The owning side of a relationship (the FK column on this model, a many-to-one
parent pointer) MUST stay in the form — without it, the user cannot create
a child row that references its parent.

For this project we use `form_excluded_columns` (blacklist) consistently,
following the pattern already established by `UserAdminView` (which excludes
`hashed_password`). This is less invasive than `form_columns` (whitelist):
new scalar columns appear in the form automatically, and we only enumerate
the relationships we want hidden.

Why a real class (not MagicMock) for the sqladmin stub
------------------------------------------------------
SQLAdmin's `ModelView` uses a custom metaclass (`ModelViewMeta`) that consumes
the `model=Klass` keyword in the class definition:

    class GameAdminView(BaseAdminModelView, model=Game): ...

A `MagicMock` does not honour normal Python class inheritance (it gets
treated as a metaclass candidate and silently drops class-body attributes).
We use a real class with a permissive `__init_subclass__` so the view's
class body is preserved exactly as defined in `admin.py`.
"""

import sys
from types import ModuleType

# Full sqladmin stub BEFORE any import of the admin module
class _StubModelView:
    """Real class so subclassing preserves class-body attributes."""

    def __init_subclass__(cls, **kwargs):
        # SQLAdmin's metaclass consumes kwargs like `model=...`; we ignore them
        # because the tests only inspect class-body configuration.
        super().__init_subclass__()


sqladmin_stub = ModuleType("sqladmin")
sqladmin_stub.Admin = type("Admin", (), {})
sqladmin_stub.ModelView = _StubModelView
sqladmin_stub.AdminView = type("AdminView", (), {})
sys.modules["sqladmin"] = sqladmin_stub

# Stub the authentication submodule that admin/auth.py imports
class _StubAuthenticationBackend:
    def __init__(self, secret_key=None):
        self.secret_key = secret_key


sqladmin_auth_stub = ModuleType("sqladmin.authentication")
sqladmin_auth_stub.AuthenticationBackend = _StubAuthenticationBackend
sys.modules["sqladmin.authentication"] = sqladmin_auth_stub

import pytest

from src.admin.admin import (
    UserAdminView,
    RoleAdminView,
    ProfessorAdminView,
    StudentAdminView,
    GameAdminView,
    GameInstanceAdminView,
    SegmentLevelAdminView,
    LevelAdminView,
    CourseAdminView,
    SyncSessionAdminView,
)
from src.users.domain import user as user_module
from src.users.domain import role as role_module
from src.users.domain import professor as professor_module
from src.users.domain import student as student_module
from src.game.domain import game as game_module
from src.game.domain import game_instance as game_instance_module
from src.game.domain import segment_level as segment_level_module
from src.game.domain import level as level_module
from src.course.domain import course as course_module
from src.sync.domain import sync_session as sync_session_module


User = user_module.User
Role = role_module.Role
Professor = professor_module.Professor
Student = student_module.Student
Game = game_module.Game
GameInstance = game_instance_module.GameInstance
SegmentLevel = segment_level_module.SegmentLevel
Level = level_module.Level
Course = course_module.Course
SyncSession = sync_session_module.SyncSession


# Each case: (view class, set of InstrumentedAttributes that MUST be in
# form_excluded_columns, human-readable description for failure messages).
#
# The set for each view is exactly the inverse relationships of the model —
# i.e. relationships where the FK lives in the OTHER table. See the
# module docstring for the full reasoning.
ADMIN_VIEW_CASES = [
    pytest.param(
        UserAdminView,
        {
            User.student,
            User.professor,
            User.teacher_settings,
            User.notifications,
            User.activity_logs,
        },
        id="UserAdminView",
    ),
    pytest.param(
        RoleAdminView,
        {Role.users},
        id="RoleAdminView",
    ),
    pytest.param(
        ProfessorAdminView,
        {
            Professor.feedbacks,
            Professor.course_professors,
        },
        id="ProfessorAdminView",
    ),
    pytest.param(
        StudentAdminView,
        {
            Student.game_instances,
            Student.feedbacks,
            Student.progresses,
            Student.xapi_statements,
            Student.course_enrollments,
        },
        id="StudentAdminView",
    ),
    pytest.param(
        GameAdminView,
        {
            Game.levels,
            Game.instances,
            Game.feedbacks,
            Game.courses,
        },
        id="GameAdminView",
    ),
    pytest.param(
        GameInstanceAdminView,
        {GameInstance.sync_sessions},
        id="GameInstanceAdminView",
    ),
    pytest.param(
        SegmentLevelAdminView,
        {SegmentLevel.progresses},
        id="SegmentLevelAdminView",
    ),
    pytest.param(
        LevelAdminView,
        {
            Level.segments,
            Level.feedbacks,
        },
        id="LevelAdminView",
    ),
    pytest.param(
        CourseAdminView,
        {
            Course.enrollments,
            Course.course_professors,
        },
        id="CourseAdminView",
    ),
    pytest.param(
        SyncSessionAdminView,
        {SyncSession.events},
        id="SyncSessionAdminView",
    ),
]


@pytest.mark.parametrize(
    "view_class,expected_excluded",
    ADMIN_VIEW_CASES,
)
def test_view_declares_form_excluded_columns(view_class, expected_excluded):
    """
    Every admin view that has inverse relationships must declare
    `form_excluded_columns` and include them in the set. A view without
    this attribute would let SQLAdmin render those relationships as
    multi-select widgets, triggering the bugs we are guarding against.

    Note: this test only checks that the inverse relationships are
    PRESENT in the excluded list. It does NOT enforce that the list is
    exhaustive (a view may legitimately exclude additional columns, e.g.
    UserAdminView excludes `hashed_password` alongside the inverse
    relationships). The "no owning-side relationships in the excluded
    list" invariant is the *user-facing* contract: if it is broken, the
    form won't let the admin pick a parent, which fails immediately in
    the UI — no extra test needed to catch that.
    """
    assert hasattr(view_class, "form_excluded_columns"), (
        f"{view_class.__name__} must define form_excluded_columns to "
        f"prevent SQLAdmin from auto-rendering inverse relationships as "
        f"multi-select widgets."
    )
    actual = set(view_class.form_excluded_columns)
    missing = expected_excluded - actual
    assert not missing, (
        f"{view_class.__name__}.form_excluded_columns is missing inverse "
        f"relationships that would leak into the form: {missing}."
    )
