"""
Unit tests for GetStudentProgressUseCase.

This test suite verifies:
- KPIs calculation (levels completed, games played, play time, avg score, streak)
- Progress over time sorting and formatting with real level names
- Level performance aggregation with real level names
- Activity distribution grouping with real game names
- Error handling for invalid UUID and empty progress
- Current streak calculation (consecutive days of activity)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID
from datetime import datetime, timezone, date

from src.statistic.application.usecase.get_student_progress_usecase import (
    GetStudentProgressUseCase,
)
from src.statistic.api.v1.schemas.student_progress import (
    StudentReportKPIs,
)


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
        self, sample_enriched_data
    ):
        """Test that execute returns progress data for valid student ID."""
        mock_db = MagicMock()
        with patch(
            "src.statistic.application.usecase.get_student_progress_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get_enriched_by_student_id = AsyncMock(
                return_value=sample_enriched_data
            )
            MockRepo.return_value = mock_repo

            use_case = GetStudentProgressUseCase(db=mock_db)
            result = await use_case.execute("550e8400-e29b-41d4-a716-446655440000")

            assert result is not None
            assert result.student_id == "550e8400-e29b-41d4-a716-446655440000"
            assert result.kpis is not None

    @pytest.mark.asyncio
    async def test_execute_returns_empty_data_for_no_progress(self):
        """Test that execute returns empty KPIs when no progress found (not an error)."""
        mock_db = MagicMock()
        with patch(
            "src.statistic.application.usecase.get_student_progress_usecase.ProgressRepository"
        ) as MockRepo:
            mock_repo = MagicMock()
            mock_repo.get_enriched_by_student_id = AsyncMock(return_value=[])
            MockRepo.return_value = mock_repo

            use_case = GetStudentProgressUseCase(db=mock_db)
            result = await use_case.execute("550e8400-e29b-41d4-a716-446655440000")

            assert result is not None
            assert result.kpis.total_levels_completed == 0
            assert result.kpis.total_games_played == 0
            assert result.kpis.total_play_time == 0
            assert result.progress_over_time == []
            assert result.level_performance == []
            assert result.activity_distribution == []

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

    def test_calculate_kpis_with_data(self, sample_enriched_data):
        """Test KPIs calculation with sample data."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        kpis = use_case._calculate_kpis(sample_enriched_data)

        assert kpis.total_levels_completed == 2
        assert kpis.total_games_played == 2  # "Nivelación" y "Operaciones"
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
        assert kpis.current_streak == 0

    def test_calculate_kpis_tracks_unique_games_by_name(self, sample_enriched_data):
        """Test that KPIs tracks unique games by game title."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        kpis = use_case._calculate_kpis(sample_enriched_data)

        assert kpis.total_games_played == 2  # "Nivelación" y "Operaciones"

    def test_calculate_kpis_no_arbitrary_multiplier(self, sample_enriched_data):
        """Test play_time uses attempt_count directly without x5 multiplier."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        kpis = use_case._calculate_kpis(sample_enriched_data)

        # Total attempt_count = 3 + 5 = 8, without x5 multiplier
        assert kpis.total_play_time == 8


class TestCalculateCurrentStreak:
    """Test suite for current streak calculation."""

    def test_streak_with_consecutive_days(self):
        """Test streak with 3 consecutive days."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        activity_dates = {
            date(2026, 3, 3),
            date(2026, 3, 2),
            date(2026, 3, 1),
        }
        streak = use_case._calculate_current_streak(activity_dates)
        assert streak == 3

    def test_streak_with_gap(self):
        """Test streak breaks when there's a gap."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        activity_dates = {
            date(2026, 3, 5),
            date(2026, 3, 3),
            date(2026, 3, 2),
            date(2026, 3, 1),
        }
        streak = use_case._calculate_current_streak(activity_dates)
        # Último día es 5, no hay día 4, streak = 1
        assert streak == 1

    def test_streak_with_single_day(self):
        """Test streak is 1 for single day activity."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        activity_dates = {date(2026, 3, 1)}
        streak = use_case._calculate_current_streak(activity_dates)
        assert streak == 1

    def test_streak_empty_set(self):
        """Test streak is 0 for no activity."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        streak = use_case._calculate_current_streak(set())
        assert streak == 0

    def test_streak_with_recent_consecutive_and_older_gap(self):
        """Test streak counts from most recent day backwards."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        activity_dates = {
            date(2026, 3, 10),
            date(2026, 3, 9),
            date(2026, 3, 8),
            date(2026, 3, 5),
        }
        streak = use_case._calculate_current_streak(activity_dates)
        # Últimos 3 días consecutivos: 8, 9, 10
        assert streak == 3


class TestCalculateProgressOverTime:
    """Test suite for progress over time calculation."""

    def test_progress_over_time_sorts_by_date(self, sample_enriched_data):
        """Test that progress is sorted by created_at."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        result = use_case._calculate_progress_over_time(sample_enriched_data)

        assert len(result) == 2
        assert result[0].date == "Mar 01"  # First entry
        assert result[1].date == "Mar 02"  # Second entry

    def test_progress_over_time_shows_real_level_number(self, sample_enriched_data):
        """Test level field shows actual level_number, not attempt_count."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        result = use_case._calculate_progress_over_time(sample_enriched_data)

        assert result[0].level == 1  # level_number from enriched data
        assert result[1].level == 2

    def test_progress_over_time_no_hard_limit(self):
        """Test progress over time shows all entries without arbitrary limit."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        many_data = create_enriched_data(15)
        result = use_case._calculate_progress_over_time(many_data)

        assert len(result) == 15  # No hard limit


class TestCalculateLevelPerformance:
    """Test suite for level performance calculation."""

    def test_level_performance_returns_list(self, sample_enriched_data):
        """Test that level performance returns a list."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        result = use_case._calculate_level_performance(sample_enriched_data)

        assert isinstance(result, list)

    def test_level_performance_shows_real_level_name(self, sample_enriched_data):
        """Test level_name shows real title, not 'Nivel {attempt_count}'."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        result = use_case._calculate_level_performance(sample_enriched_data)

        assert result[0].level_name == "Sumas Básicas"
        assert result[1].level_name == "Sumas Avanzadas"

    def test_level_performance_attempts_correct(self, sample_enriched_data):
        """Test attempts shows actual attempt_count, not attempt_count + 1."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        result = use_case._calculate_level_performance(sample_enriched_data)

        assert result[0].attempts == 3  # actual attempt_count, not 4
        assert result[1].attempts == 5  # actual attempt_count, not 6

    def test_level_performance_aggregates_by_level(self):
        """Test level performance groups multiple attempts per level."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        # Two entries for same level
        data = [
            {
                "progress": MagicMock(
                    attempt_count=3, efficiency_rating=80,
                    objectives_completed=1, created_at=datetime(2026, 3, 1, tzinfo=timezone.utc),
                ),
                "level_title": "Sumas Básicas",
                "level_number": 1,
                "game_title": "Nivelación",
            },
            {
                "progress": MagicMock(
                    attempt_count=2, efficiency_rating=90,
                    objectives_completed=0, created_at=datetime(2026, 3, 2, tzinfo=timezone.utc),
                ),
                "level_title": "Sumas Básicas",
                "level_number": 1,
                "game_title": "Nivelación",
            },
        ]

        result = use_case._calculate_level_performance(data)

        assert len(result) == 1  # Aggregated into one level
        assert result[0].attempts == 5  # 3 + 2
        assert result[0].score == 85.0  # avg of 80 and 90
        assert result[0].completed is True  # At least one completion


class TestCalculateActivityDistribution:
    """Test suite for activity distribution calculation."""

    def test_activity_distribution_groups_by_game_name(self, sample_enriched_data):
        """Test that activity is grouped by game title."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        result = use_case._calculate_activity_distribution(sample_enriched_data)

        assert isinstance(result, list)
        assert result[0].game_name == "Nivelación"
        assert result[1].game_name == "Operaciones"

    def test_activity_distribution_uses_real_game_name(self):
        """Test game_name shows actual game title, not 'Juego {hash}'."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        data = [
            {
                "progress": MagicMock(
                    attempt_count=5, efficiency_rating=90,
                    objectives_completed=3, created_at=datetime(2026, 3, 1, tzinfo=timezone.utc),
                ),
                "level_title": "Sumas Avanzadas",
                "level_number": 2,
                "game_title": "Operaciones Matemáticas",
            },
        ]

        result = use_case._calculate_activity_distribution(data)

        assert result[0].game_name == "Operaciones Matemáticas"

    def test_activity_distribution_no_hard_limit(self):
        """Test activity distribution shows all games without arbitrary limit."""
        mock_db = MagicMock()
        use_case = GetStudentProgressUseCase(db=mock_db)

        many_data = create_enriched_data(10)
        result = use_case._calculate_activity_distribution(many_data)

        # 10 entries across 3 unique games (i % 3 + 1), so 3 groups
        assert len(result) == 3  # All unique games returned, no limit of 4


# ============== Fixtures ==============


@pytest.fixture
def sample_enriched_data():
    """Create a list of sample enriched progress data for testing."""
    base_time = datetime(2026, 3, 1, 10, 0, 0, tzinfo=timezone.utc)
    return [
        {
            "progress": MagicMock(
                attempt_count=3,
                efficiency_rating=85,
                objectives_completed=2,
                created_at=base_time,
                updated_at=base_time,
            ),
            "level_title": "Sumas Básicas",
            "level_number": 1,
            "game_title": "Nivelación",
        },
        {
            "progress": MagicMock(
                attempt_count=5,
                efficiency_rating=90,
                objectives_completed=3,
                created_at=datetime(2026, 3, 2, 10, 0, 0, tzinfo=timezone.utc),
                updated_at=datetime(2026, 3, 2, 10, 0, 0, tzinfo=timezone.utc),
            ),
            "level_title": "Sumas Avanzadas",
            "level_number": 2,
            "game_title": "Operaciones",
        },
    ]


def create_enriched_data(count: int) -> list:
    """Helper to create a list of mock enriched data."""
    base_time = datetime(2026, 3, 1, 10, 0, 0, tzinfo=timezone.utc)
    return [
        {
            "progress": MagicMock(
                attempt_count=i + 1,
                efficiency_rating=70 + i,
                objectives_completed=i,
                created_at=datetime(2026, 3, i + 1, 10, 0, 0, tzinfo=timezone.utc),
                updated_at=datetime(2026, 3, i + 1, 10, 0, 0, tzinfo=timezone.utc),
            ),
            "level_title": f"Nivel {i + 1}",
            "level_number": i + 1,
            "game_title": f"Juego {i % 3 + 1}",
        }
        for i in range(count)
    ]
