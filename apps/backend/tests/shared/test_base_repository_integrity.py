"""
Unit tests for BaseRepository IntegrityError classification.

These tests pin down the mapping from PostgreSQL SQLSTATE codes
(observed via SQLAlchemy IntegrityError.orig.pgcode) to the right
domain exception. Misclassification here is what produced the
"duplicate entry" 500 for feedback creation in production.
"""
import pytest
from sqlalchemy.exc import IntegrityError

from src.shared.domain.exceptions import (
    DuplicateEntryException,
    ForeignKeyViolationException,
    DatabaseException,
)
from src.shared.infrastructure.repositories.base_repository import (
    _integrity_error_to_domain,
)


class FakeOrig:
    def __init__(self, pgcode: str | None) -> None:
        self.pgcode = pgcode


def make_integrity_error(pgcode: str | None) -> IntegrityError:
    return IntegrityError("INSERT ...", {}, FakeOrig(pgcode))


class TestIntegrityErrorClassification:
    def test_unique_violation_maps_to_duplicate_entry(self):
        err = make_integrity_error("23505")
        mapped = _integrity_error_to_domain(err, "create Feedback")
        assert isinstance(mapped, DuplicateEntryException)
        assert mapped.status_code == 400

    def test_foreign_key_violation_maps_to_fk_exception(self):
        err = make_integrity_error("23503")
        mapped = _integrity_error_to_domain(err, "create Feedback")
        assert isinstance(mapped, ForeignKeyViolationException)
        assert mapped.status_code == 400

    def test_not_null_violation_maps_to_database_exception(self):
        err = make_integrity_error("23502")
        mapped = _integrity_error_to_domain(err, "create Feedback")
        assert isinstance(mapped, DatabaseException)
        assert mapped.status_code == 500

    def test_check_violation_maps_to_database_exception(self):
        err = make_integrity_error("23514")
        mapped = _integrity_error_to_domain(err, "create Feedback")
        assert isinstance(mapped, DatabaseException)
        assert mapped.status_code == 500

    def test_unknown_pgcode_falls_back_to_database_exception(self):
        err = make_integrity_error("99999")
        mapped = _integrity_error_to_domain(err, "create Feedback")
        assert isinstance(mapped, DatabaseException)

    def test_missing_pgcode_falls_back_to_database_exception(self):
        err = make_integrity_error(None)
        mapped = _integrity_error_to_domain(err, "create Feedback")
        assert isinstance(mapped, DatabaseException)
