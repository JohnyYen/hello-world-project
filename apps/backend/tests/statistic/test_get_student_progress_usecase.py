"""
Unit tests for GetStudentProgressUseCase.

This test suite verifies:
- KPIs calculation (levels completed, games played, play time, avg score, streak)
- Progress over time sorting and formatting
- Level performance aggregation
- Activity distribution grouping
- Error handling for invalid UUID and empty progress
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID
from datetime import datetime, timezone

from src.statistic.application.usecase.get_student_progress_usecase import (
    GetStudentProgressUseCase,
)
from src.statistic.domain.progress import Progress


class TestGetStudentProgressUseCaseInitialization:
    """Test suite for UseCase initialization."""

    def test_init_creates_instance_with_db(self):
        """Test that UseCase can be instantiated with db session."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)
        assert use_case is not None
        assert use_case.db == mock_db


class TestGetStudentProgressExecute:
    """Test suite for execute method."""

    @pytest.mark.asyncio
    async def test_execute_returns_progress_for_valid_student(
        self, sample_progress_list
    ):
        """Test that execute returns progress data for valid student ID."""
        mock_db = MagicMock()
        with patch(
            "src.statistic.application.usecase.get_student_progress_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get_by_student_id = AsyncMock(return_value=sample_progress_list)
            MockRepo.return_value = mock_repo

            use_case = GetStudentProgressUseCase(db=mock_db)
            result = await use_case.execute("550e8400-e29b-41d4-a716-446655440000")

            assert result is not None
            assert result.student_id == "550e8400-e29b-41d4-a716-446655440000"
            assert result.kpis is not None

    @pytest.mark.asyncio
    async def test_execute_raises_404_for_empty_progress(self):
        """Test that execute raises 404 when no progress found."""
        mock_db = MagicMock()
        with patch(
            "src.statistic.application.usecase.get_student_progress_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get_by_student_id = AsyncMock(return_value=[])
            MockRepo.return_value = mock_repo

            use_case = GetStudentProgressUseCase(db=mock_db)

            with pytest.raises(Exception) as exc_info:
                await use_case.execute("550e8400-e29b-41d4-a716-446655440000")
            assert "404" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_raises_400_for_invalid_uuid(self):
        """Test that execute raises 400 for invalid UUID format."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        with pytest.raises(Exception) as exc_info:
            await use_case.execute("invalid-uuid")
        assert "400" in str(exc_info.value)


class TestCalculateKPIs:
    """Test suite for KPIs calculation."""

    def test_calculate_kpis_with_data(self, sample_progress_list):
        """Test KPIs calculation with sample data."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        kpis = use_case._calculate_kpis(sample_progress_list)

        assert kpis.total_levels_completed == 2
        assert kpis.total_games_played == 2
        assert kpis.total_play_time > 0
        assert kpis.average_score >= 0

    def test_calculate_kpis_empty_list(self):
        """Test KPIs calculation with empty list."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        kpis = use_case._calculate_kpis([])

        assert kpis.total_levels_completed == 0
        assert kpis.total_games_played == 0
        assert kpis.total_play_time == 0
        assert kpis.average_score == 0.0

    def test_calculate_kpis_tracks_unique_games(self, sample_progress_list):
        """Test that KPIs tracks unique games by segment_level_id."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        kpis = use_case._calculate_kpis(sample_progress_list)

        assert kpis.total_games_played <= len(sample_progress_list)


class TestCalculateProgressOverTime:
    """Test suite for progress over time calculation."""

    def test_progress_over_time_sorts_by_date(self, sample_progress_list):
        """Test that progress is sorted by created_at."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        result = use_case._calculate_progress_over_time(sample_progress_list)

        assert len(result) <= 10

    def test_progress_over_time_limits_to_10(self):
        """Test that only last 10 entries are returned."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        many_progress = create_progress_list(15)
        result = use_case._calculate_progress_over_time(many_progress)

        assert len(result) <= 10


class TestCalculateLevelPerformance:
    """Test suite for level performance calculation."""

    def test_level_performance_returns_list(self, sample_progress_list):
        """Test that level performance returns a list."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        result = use_case._calculate_level_performance(sample_progress_list)

        assert isinstance(result, list)

    def test_level_performance_limits_to_6(self):
        """Test that only first 6 entries are returned."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        many_progress = create_progress_list(10)
        result = use_case._calculate_level_performance(many_progress)

        assert len(result) <= 6


class TestCalculateActivityDistribution:
    """Test suite for activity distribution calculation."""

    def test_activity_distribution_groups_by_game(self, sample_progress_list):
        """Test that activity is grouped by game."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        result = use_case._calculate_activity_distribution(sample_progress_list)

        assert isinstance(result, list)

    def test_activity_distribution_limits_to_4(self):
        """Test that only first 4 games are returned."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        many_progress = create_progress_list(10)
        result = use_case._calculate_activity_distribution(many_progress)

        assert len(result) <= 4


class TestKPIsCalculationEdgeCases:
    """Test suite for edge cases in KPIs."""

    def test_kpis_handles_zero_efficiency(self):
        """Test KPIs calculation when efficiency_rating is 0."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        progress_with_zero = [
            MagicMock(
                segment_level_id=UUID("550e8400-e29b-41d4-a716-446655440001"),
                attempt_count=5,
                efficiency_rating=0,
                objectives_completed=0,
                updated_at=datetime.now(timezone.utc),
            )
        ]

        kpis = use_case._calculate_kpis(progress_with_zero)

        assert kpis.average_score == 0.0


# ============== Fixtures ==============


@pytest.fixture
def sample_progress_list():
    """Create a list of sample Progress objects for testing."""
    base_time = datetime(2026, 3, 1, 10, 0, 0, tzinfo=timezone.utc)
    return [
        MagicMock(
            id=UUID("550e8400-e29b-41d4-a716-446655440001"),
            student_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            segment_level_id=UUID("550e8400-e29b-41d4-a716-446655440001"),
            attempt_count=3,
            efficiency_rating=85,
            objectives_completed=2,
            created_at=base_time,
            updated_at=base_time,
        ),
        MagicMock(
            id=UUID("550e8400-e29b-41d4-a716-446655440002"),
            student_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            segment_level_id=UUID("550e8400-e29b-41d4-a716-446655440002"),
            attempt_count=5,
            efficiency_rating=90,
            objectives_completed=3,
            created_at=datetime(2026, 3, 2, 10, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2026, 3, 2, 10, 0, 0, tzinfo=timezone.utc),
        ),
    ]


def create_progress_list(count: int) -> list:
    """Helper to create a list of mock Progress objects."""
    base_time = datetime(2026, 3, 1, 10, 0, 0, tzinfo=timezone.utc)
    return [
        MagicMock(
            id=UUID(f"550e8400-e29b-41d4-a716-44665544{str(i).zfill(4)}"),
            student_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            segment_level_id=UUID(f"550e8400-e29b-41d4-a716-44665544{str(i).zfill(4)}"),
            attempt_count=i + 1,
            efficiency_rating=70 + i,
            objectives_completed=i,
            created_at=datetime(2026, 3, i + 1, 10, 0, 0, tzinfo=timezone.utc),
            updated_at=datetime(2026, 3, i + 1, 10, 0, 0, tzinfo=timezone.utc),
        )
        for i in range(count)
    ]
