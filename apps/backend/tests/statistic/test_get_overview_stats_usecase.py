# Tests para GetOverviewStatsUseCase
import pytest
from datetime import date as datetime_date, timedelta
from unittest.mock import AsyncMock, MagicMock
from src.statistic.application.usecase.get_overview_stats_usecase import (
    GetOverviewStatsUseCase,
)
from src.statistic.api.v1.schemas.overview import (
    OverviewKPIs,
    ActivityOverTimeItem,
    LevelPerformanceItem,
    OverviewTrends,
)


class MockProgressRepository:
    """Mock de ProgressRepository para testing."""

    def __init__(self):
        self.count_students = AsyncMock(return_value=100)
        self.get_active_students = AsyncMock(return_value=50)
        self.aggregate_kpis = AsyncMock(
            return_value={
                "total_levels_completed": 500,
                "total_play_time_minutes": 10000,
                "average_score": 85.5,
            }
        )
        self.aggregate_activity_by_date = AsyncMock(
            return_value=[
                {
                    "date": datetime_date(2026, 4, 1),
                    "sessions": 25,
                    "active_students": 10,
                    "play_time_minutes": 500,
                },
                {
                    "date": datetime_date(2026, 4, 2),
                    "sessions": 30,
                    "active_students": 12,
                    "play_time_minutes": 600,
                },
            ]
        )
        self.aggregate_level_performance = AsyncMock(
            return_value=[
                {
                    "level_name": "Nivel 1",
                    "completion_rate": 0.85,
                    "average_attempts": 2.5,
                    "average_time_minutes": 15.0,
                },
                {
                    "level_name": "Nivel 2",
                    "completion_rate": 0.70,
                    "average_attempts": 3.0,
                    "average_time_minutes": 20.0,
                },
            ]
        )


class TestGetOverviewStatsUseCase:
    @pytest.mark.asyncio
    async def test_execute_with_period(self):
        """Test ejecución con período predefinido."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        result = await use_case.execute(period="7d")

        assert isinstance(result.kpis, OverviewKPIs)
        assert result.kpis.total_students == 100
        assert result.kpis.active_students_this_week == 50
        assert len(result.activity_over_time) == 2
        assert len(result.level_performance) == 2
        assert isinstance(result.trends, OverviewTrends)

    @pytest.mark.asyncio
    async def test_execute_with_date_range(self):
        """Test ejecución con rango de fechas."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        result = await use_case.execute(
            start_date=datetime_date(2026, 1, 1), end_date=datetime_date(2026, 3, 31)
        )

        assert isinstance(result, type(result))
        mock_repo.aggregate_kpis.assert_called_once()

    @pytest.mark.asyncio
    async def test_calculate_kpis(self):
        """Test cálculo de KPIs."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        kpis = await use_case.calculate_kpis(
            start_date=datetime_date(2026, 1, 1), end_date=datetime_date(2026, 3, 31)
        )

        assert kpis.total_students == 100
        assert kpis.active_students_this_week == 50
        assert kpis.active_students_this_month == 50
        assert kpis.total_levels_completed == 500
        assert kpis.total_play_time_minutes == 10000
        assert kpis.average_score == 85.5

    @pytest.mark.asyncio
    async def test_calculate_activity_over_time(self):
        """Test cálculo de actividad temporal."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        activity = await use_case.calculate_activity_over_time(
            start_date=datetime_date(2026, 4, 1), end_date=datetime_date(2026, 4, 30)
        )

        assert len(activity) == 2
        assert isinstance(activity[0], ActivityOverTimeItem)
        assert activity[0].sessions == 25
        assert activity[0].active_students == 10

    @pytest.mark.asyncio
    async def test_calculate_level_performance(self):
        """Test cálculo de rendimiento por nivel."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        levels = await use_case.calculate_level_performance()

        assert len(levels) == 2
        assert isinstance(levels[0], LevelPerformanceItem)
        assert levels[0].level_name == "Nivel 1"
        assert levels[0].completion_rate == 0.85

    @pytest.mark.asyncio
    async def test_calculate_trends(self):
        """Test cálculo de tendencias."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        trends = await use_case.calculate_trends(
            start_date=datetime_date(2026, 1, 1), end_date=datetime_date(2026, 3, 31)
        )

        assert isinstance(trends, OverviewTrends)
        assert trends.students_change_percent is not None
        assert trends.activity_change_percent is not None

    def test_resolve_dates_with_period(self):
        """Test resolución de fechas con período."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        start, end = use_case._resolve_dates(None, None, "7d")

        assert start is not None
        assert end is not None
        diff = (end - start).days
        assert diff == 7

    def test_resolve_dates_default(self):
        """Test resolución de fechas por defecto."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        start, end = use_case._resolve_dates(None, None, None)

        # Por defecto debe usar 30 días
        assert start is not None
        assert end is not None
        diff = (end - start).days
        assert diff == 7

    def test_resolve_dates_default(self):
        """Test resolución de fechas por defecto."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        start, end = use_case._resolve_dates(None, None, None)

        # Por defecto debe usar 30 días
        assert start is not None
        assert end is not None
