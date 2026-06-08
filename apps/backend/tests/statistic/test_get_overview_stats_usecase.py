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
        self.get_active_students_in_range = AsyncMock(return_value=50)
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
        mock_repo.aggregate_kpis.assert_called()

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
        """Test cálculo de tendencias con datos reales."""
        mock_repo = MockProgressRepository()

        # Configurar datos diferentes para período actual vs anterior
        mock_repo.aggregate_kpis = AsyncMock(
            side_effect=[
                # Llamada 1: período actual
                {
                    "total_levels_completed": 600,
                    "total_play_time_minutes": 12000,
                    "average_score": 88.0,
                },
                # Llamada 2: período anterior
                {
                    "total_levels_completed": 400,
                    "total_play_time_minutes": 8000,
                    "average_score": 82.0,
                },
            ]
        )
        mock_repo.get_active_students_in_range = AsyncMock(
            side_effect=[80, 60]  # 80 current, 60 previous
        )

        use_case = GetOverviewStatsUseCase(mock_repo)

        trends = await use_case.calculate_trends(
            start_date=datetime_date(2026, 1, 1), end_date=datetime_date(2026, 3, 31)
        )

        assert isinstance(trends, OverviewTrends)

        # 80 - 60 / 60 * 100 = 33.3%
        assert trends.students_change_percent == 33.3

        # 600 - 400 / 400 * 100 = 50.0%
        assert trends.activity_change_percent == 50.0

        # 88 - 82 / 82 * 100 = 7.3%
        assert trends.score_change_percent == 7.3

        # Verificar que se llamó con los rangos correctos
        assert mock_repo.get_active_students_in_range.call_count == 2

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
        """Test resolución de fechas por defecto (30 días)."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        start, end = use_case._resolve_dates(None, None, None)

        # Por defecto debe usar 30 días
        assert start is not None
        assert end is not None
        diff = (end - start).days
        assert diff == 30

    def test_resolve_dates_with_start_only(self):
        """Test resolución con solo start_date."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        start_date = datetime_date(2026, 1, 1)
        start, end = use_case._resolve_dates(start_date, None, None)

        assert start == datetime_date(2026, 1, 1)
        assert end == datetime_date(2026, 1, 31)
        diff = (end - start).days
        assert diff == 30

    def test_resolve_dates_with_end_only(self):
        """Test resolución con solo end_date."""
        mock_repo = MockProgressRepository()
        use_case = GetOverviewStatsUseCase(mock_repo)

        end_date = datetime_date(2026, 3, 31)
        start, end = use_case._resolve_dates(None, end_date, None)

        assert end == datetime_date(2026, 3, 31)
        assert start == datetime_date(2026, 3, 1)
        diff = (end - start).days
        assert diff == 30
