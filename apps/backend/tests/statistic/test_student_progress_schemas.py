"""
Tests de validación para schemas Pydantic del módulo Student Progress.

Este test suite verifica:
- Serialización y deserialización de schemas
- Validación de campos requeridos
- Validación de tipos de datos
- Valores por defecto
"""

import pytest
from datetime import datetime, timezone
from uuid import UUID

from src.statistic.api.v1.schemas.student_progress import (
    StudentReportKPIs,
    ProgressOverTimeItem,
    LevelPerformanceItem,
    ActivityDistributionItem,
    StudentProgressResponse,
)


class TestStudentReportKPIs:
    """Test suite para el schema StudentReportKPIs."""

    def test_create_kpis_with_all_fields(self):
        """Test que se puede crear KPIs con todos los campos."""
        kpis = StudentReportKPIs(
            total_levels_completed=5,
            total_games_played=3,
            total_play_time=120,
            average_score=85.5,
            current_streak=7,
            last_activity=datetime(2026, 3, 20, 10, 30, tzinfo=timezone.utc),
        )

        assert kpis.total_levels_completed == 5
        assert kpis.total_games_played == 3
        assert kpis.total_play_time == 120
        assert kpis.average_score == 85.5
        assert kpis.current_streak == 7

    def test_create_kpis_with_optional_last_activity_none(self):
        """Test que last_activity puede ser None."""
        kpis = StudentReportKPIs(
            total_levels_completed=0,
            total_games_played=0,
            total_play_time=0,
            average_score=0.0,
            current_streak=0,
            last_activity=None,
        )

        assert kpis.last_activity is None

    def test_kpis_serialization_to_dict(self):
        """Test que el schema serializa correctamente a dict."""
        kpis = StudentReportKPIs(
            total_levels_completed=3,
            total_games_played=2,
            total_play_time=60,
            average_score=75.0,
            current_streak=5,
            last_activity=None,
        )

        result = kpis.model_dump()

        assert result["total_levels_completed"] == 3
        assert result["total_games_played"] == 2

    def test_kpis_model_validate(self):
        """Test que model_validate funciona correctamente."""
        data = {
            "total_levels_completed": 10,
            "total_games_played": 4,
            "total_play_time": 200,
            "average_score": 88.5,
            "current_streak": 12,
            "last_activity": "2026-03-20T10:30:00+00:00",
        }

        kpis = StudentReportKPIs(**data)

        assert kpis.total_levels_completed == 10
        assert kpis.average_score == 88.5


class TestProgressOverTimeItem:
    """Test suite para el schema ProgressOverTimeItem."""

    def test_create_progress_item(self):
        """Test que se puede crear un item de progreso."""
        item = ProgressOverTimeItem(
            date="Mar 15",
            level=3,
            score=85,
            time_spent=15,
        )

        assert item.date == "Mar 15"
        assert item.level == 3
        assert item.score == 85
        assert item.time_spent == 15

    def test_progress_item_serialization(self):
        """Test que serializa correctamente."""
        item = ProgressOverTimeItem(
            date="Mar 10",
            level=2,
            score=70,
            time_spent=10,
        )

        result = item.model_dump()

        assert result["date"] == "Mar 10"
        assert result["level"] == 2


class TestLevelPerformanceItem:
    """Test suite para el schema LevelPerformanceItem."""

    def test_create_level_performance(self):
        """Test que se puede crear un item de rendimiento por nivel."""
        item = LevelPerformanceItem(
            level_name="Nivel 1",
            score=90,
            attempts=2,
            time_spent=30,
            completed=True,
        )

        assert item.level_name == "Nivel 1"
        assert item.score == 90
        assert item.attempts == 2
        assert item.time_spent == 30
        assert item.completed is True

    def test_level_performance_incomplete(self):
        """Test que completed puede ser False."""
        item = LevelPerformanceItem(
            level_name="Nivel 2",
            score=50,
            attempts=5,
            time_spent=45,
            completed=False,
        )

        assert item.completed is False


class TestActivityDistributionItem:
    """Test suite para el schema ActivityDistributionItem."""

    def test_create_activity_distribution(self):
        """Test que se puede crear un item de distribución."""
        item = ActivityDistributionItem(
            game_name="Juego 12345678",
            time_spent=120,
            sessions=8,
        )

        assert item.game_name == "Juego 12345678"
        assert item.time_spent == 120
        assert item.sessions == 8


class TestStudentProgressResponse:
    """Test suite para el schema StudentProgressResponse completo."""

    def test_create_full_response(self):
        """Test que se puede crear la respuesta completa."""
        kpis = StudentReportKPIs(
            total_levels_completed=5,
            total_games_played=3,
            total_play_time=120,
            average_score=85.5,
            current_streak=7,
            last_activity=None,
        )

        progress_over_time = [
            ProgressOverTimeItem(date="Mar 15", level=3, score=85, time_spent=15),
            ProgressOverTimeItem(date="Mar 14", level=2, score=80, time_spent=20),
        ]

        level_performance = [
            LevelPerformanceItem(
                level_name="Nivel 1",
                score=90,
                attempts=1,
                time_spent=30,
                completed=True,
            ),
        ]

        activity_distribution = [
            ActivityDistributionItem(
                game_name="Juego 12345678",
                time_spent=60,
                sessions=4,
            ),
        ]

        response = StudentProgressResponse(
            student_id="550e8400-e29b-41d4-a716-446655440000",
            kpis=kpis,
            progress_over_time=progress_over_time,
            level_performance=level_performance,
            activity_distribution=activity_distribution,
        )

        assert response.student_id == "550e8400-e29b-41d4-a716-446655440000"
        assert len(response.progress_over_time) == 2
        assert len(response.level_performance) == 1
        assert len(response.activity_distribution) == 1

    def test_response_with_default_empty_lists(self):
        """Test que las listas pueden estar vacías por defecto."""
        kpis = StudentReportKPIs(
            total_levels_completed=0,
            total_games_played=0,
            total_play_time=0,
            average_score=0.0,
            current_streak=0,
            last_activity=None,
        )

        response = StudentProgressResponse(
            student_id="550e8400-e29b-41d4-a716-446655440000",
            kpis=kpis,
        )

        assert response.progress_over_time == []
        assert response.level_performance == []
        assert response.activity_distribution == []

    def test_response_serialization(self):
        """Test que serializa correctamente a JSON."""
        kpis = StudentReportKPIs(
            total_levels_completed=1,
            total_games_played=1,
            total_play_time=30,
            average_score=75.0,
            current_streak=1,
            last_activity=None,
        )

        response = StudentProgressResponse(
            student_id="550e8400-e29b-41d4-a716-446655440000",
            kpis=kpis,
        )

        json_data = response.model_dump_json()

        assert "550e8400-e29b-41d4-a716-446655440000" in json_data
        assert "total_levels_completed" in json_data
