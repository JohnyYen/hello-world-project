# Tests para Overview Schemas
import pytest
from datetime import date as datetime_date
from src.statistic.api.v1.schemas.overview import (
    OverviewKPIs,
    ActivityOverTimeItem,
    LevelPerformanceItem,
    OverviewTrends,
    OverviewResponse,
    OverviewQueryParams,
)


class TestOverviewKPIs:
    def test_valid_kpis(self):
        kpis = OverviewKPIs(
            total_students=100,
            active_students_this_week=50,
            active_students_this_month=80,
            total_levels_completed=500,
            total_play_time_minutes=10000,
            average_score=85.5,
        )
        assert kpis.total_students == 100
        assert kpis.average_score == 85.5

    def test_negative_values_fail(self):
        with pytest.raises(ValueError):
            OverviewKPIs(
                total_students=-1,
                active_students_this_week=50,
                active_students_this_month=80,
                total_levels_completed=500,
                total_play_time_minutes=10000,
                average_score=85.5,
            )

    def test_score_exceeds_100_fail(self):
        with pytest.raises(ValueError):
            OverviewKPIs(
                total_students=100,
                active_students_this_week=50,
                active_students_this_month=80,
                total_levels_completed=500,
                total_play_time_minutes=10000,
                average_score=101.0,
            )


class TestActivityOverTimeItem:
    def test_valid_item(self):
        item = ActivityOverTimeItem(
            date=datetime_date(2026, 4, 1),
            sessions=25,
            active_students=10,
            play_time_minutes=500,
        )
        assert item.sessions == 25

    def test_negative_sessions_fail(self):
        with pytest.raises(ValueError):
            ActivityOverTimeItem(
                date=datetime_date(2026, 4, 1),
                sessions=-1,
                active_students=10,
                play_time_minutes=500,
            )


class TestLevelPerformanceItem:
    def test_valid_item(self):
        item = LevelPerformanceItem(
            level_name="Nivel 1",
            completion_rate=0.85,
            average_attempts=2.5,
            average_time_minutes=15.0,
        )
        assert item.completion_rate == 0.85

    def test_completion_rate_exceeds_1_fail(self):
        with pytest.raises(ValueError):
            LevelPerformanceItem(
                level_name="Nivel 1",
                completion_rate=1.5,
                average_attempts=2.5,
                average_time_minutes=15.0,
            )


class TestOverviewTrends:
    def test_valid_trends(self):
        trends = OverviewTrends(
            students_change_percent=10.5,
            activity_change_percent=-5.0,
            score_change_percent=2.3,
        )
        assert trends.students_change_percent == 10.5

    def test_negative_trends_allowed(self):
        trends = OverviewTrends(
            students_change_percent=-10.0,
            activity_change_percent=-5.0,
            score_change_percent=0.0,
        )
        assert trends.students_change_percent == -10.0


class TestOverviewResponse:
    def test_valid_response(self):
        kpis = OverviewKPIs(
            total_students=100,
            active_students_this_week=50,
            active_students_this_month=80,
            total_levels_completed=500,
            total_play_time_minutes=10000,
            average_score=85.5,
        )
        activity = [
            ActivityOverTimeItem(
                date=datetime_date(2026, 4, 1),
                sessions=25,
                active_students=10,
                play_time_minutes=500,
            )
        ]
        levels = [
            LevelPerformanceItem(
                level_name="Nivel 1",
                completion_rate=0.85,
                average_attempts=2.5,
                average_time_minutes=15.0,
            )
        ]
        trends = OverviewTrends(
            students_change_percent=10.0,
            activity_change_percent=5.0,
            score_change_percent=2.0,
        )

        response = OverviewResponse(
            kpis=kpis,
            activity_over_time=activity,
            level_performance=levels,
            trends=trends,
        )

        assert response.kpis.total_students == 100
        assert len(response.activity_over_time) == 1


class TestOverviewQueryParams:
    def test_valid_empty_params(self):
        params = OverviewQueryParams()
        is_valid, error = params.validate_params()
        assert is_valid is True
        assert error is None

    def test_valid_period(self):
        params = OverviewQueryParams(period="7d")
        is_valid, error = params.validate_params()
        assert is_valid is True

    def test_valid_date_range(self):
        params = OverviewQueryParams(
            start_date=datetime_date(2026, 1, 1), end_date=datetime_date(2026, 3, 31)
        )
        is_valid, error = params.validate_params()
        assert is_valid is True

    def test_start_date_and_period_invalid(self):
        params = OverviewQueryParams(start_date=datetime_date(2026, 1, 1), period="7d")
        is_valid, error = params.validate_params()
        assert is_valid is False
        assert "start_date y period" in error

    def test_end_date_before_start_date_invalid(self):
        params = OverviewQueryParams(
            start_date=datetime_date(2026, 3, 1), end_date=datetime_date(2026, 1, 1)
        )
        is_valid, error = params.validate_params()
        assert is_valid is False
        assert "end_date no puede ser menor" in error

    def test_invalid_period_value(self):
        # Con Literal, Pydantic valida directamente en el schema
        # Por lo tanto, un período inválido genera error de validación antes de validate_params
        # Este test verifica que el endpoint maneja el error correctamente
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            params = OverviewQueryParams(period="invalid")
