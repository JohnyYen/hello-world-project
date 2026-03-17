"""
Tests for shared application providers.

These tests verify that the provider functions correctly instantiate
services with injected repositories following the dependency injection pattern.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession


class TestUserProviders:
    """Tests for user domain providers."""

    @pytest.mark.asyncio
    async def test_get_user_repository_returns_repository_instance(self):
        """Test that get_user_repository returns a UserRepository instance."""
        from src.shared.application.providers.users_providers import (
            get_user_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.users_providers.UserRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_user_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_student_service_returns_service_with_injected_repository(self):
        """Test that get_student_service returns StudentService with injected repository."""
        from src.shared.application.providers.users_providers import (
            get_student_service,
        )

        mock_repository = MagicMock()

        with patch(
            "src.shared.application.providers.users_providers.StudentService"
        ) as mock_service_class:
            mock_service_instance = MagicMock()
            mock_service_class.return_value = mock_service_instance

            with patch(
                "src.shared.application.providers.users_providers.Student"
            ) as mock_student_model:
                result = get_student_service(student_repository=mock_repository)

                mock_service_class.assert_called_once_with(
                    repository=mock_repository, model=mock_student_model
                )
                assert result == mock_service_instance


class TestStudentProviders:
    """Tests for student domain providers."""

    @pytest.mark.asyncio
    async def test_get_student_repository_returns_repository_instance(self):
        """Test that get_student_repository returns a StudentRepository instance."""
        from src.shared.application.providers.users_providers import (
            get_student_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.users_providers.StudentRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_student_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_student_service_returns_service_with_injected_repository(self):
        """Test that get_student_service returns StudentService with injected repository."""
        from src.shared.application.providers.users_providers import (
            get_student_service,
        )

        mock_repository = MagicMock()

        with patch(
            "src.shared.application.providers.users_providers.StudentService"
        ) as mock_service_class:
            mock_service_instance = MagicMock()
            mock_service_class.return_value = mock_service_instance

            with patch(
                "src.shared.application.providers.users_providers.Student"
            ) as mock_model:
                result = get_student_service(student_repository=mock_repository)

                mock_service_class.assert_called_once_with(
                    repository=mock_repository, model=mock_model
                )
                assert result == mock_service_instance


class TestProfessorProviders:
    """Tests for professor domain providers."""

    @pytest.mark.asyncio
    async def test_get_professor_repository_returns_repository_instance(self):
        """Test that get_professor_repository returns a ProfessorRepository instance."""
        from src.shared.application.providers.users_providers import (
            get_professor_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.users_providers.ProfessorRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_professor_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_professor_service_returns_service_with_injected_repository(self):
        """Test that get_professor_service returns ProfessorService with injected repository."""
        from src.shared.application.providers.users_providers import (
            get_professor_service,
        )

        mock_repository = MagicMock()

        with patch(
            "src.shared.application.providers.users_providers.ProfessorService"
        ) as mock_service_class:
            mock_service_instance = MagicMock()
            mock_service_class.return_value = mock_service_instance

            with patch("src.shared.application.providers.users_providers.Professor"):
                result = get_professor_service(professor_repository=mock_repository)

                mock_service_class.assert_called_once_with(repository=mock_repository)
                assert result == mock_service_instance


class TestTeacherSettingsProviders:
    """Tests for teacher settings domain providers."""

    @pytest.mark.asyncio
    async def test_get_teacher_settings_repository_returns_repository_instance(self):
        """Test that get_teacher_settings_repository returns a TeacherSettingsRepository instance."""
        from src.shared.application.providers.users_providers import (
            get_teacher_settings_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.users_providers.TeacherSettingsRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_teacher_settings_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_teacher_settings_service_returns_service_with_injected_repository(
        self,
    ):
        """Test that get_teacher_settings_service returns TeacherSettingsService with injected repository."""
        from src.shared.application.providers.users_providers import (
            get_teacher_settings_service,
        )

        mock_repository = MagicMock()

        with patch(
            "src.shared.application.providers.users_providers.TeacherSettingsService"
        ) as mock_service_class:
            mock_service_instance = MagicMock()
            mock_service_class.return_value = mock_service_instance

            with patch(
                "src.shared.application.providers.users_providers.TeacherSettings"
            ):
                result = get_teacher_settings_service(
                    teacher_settings_repository=mock_repository
                )

                mock_service_class.assert_called_once_with(repository=mock_repository)
                assert result == mock_service_instance


class TestLMSCredentialProviders:
    """Tests for LMS credential domain providers."""

    @pytest.mark.asyncio
    async def test_get_lms_credential_repository_returns_repository_instance(self):
        """Test that get_lms_credential_repository returns a LMSCredentialRepository instance."""
        from src.shared.application.providers.users_providers import (
            get_lms_credential_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.users_providers.LMSCredentialRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_lms_credential_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_lms_credential_service_returns_service_with_injected_repository(
        self,
    ):
        """Test that get_lms_credential_service returns LMSCredentialService with injected repository."""
        from src.shared.application.providers.users_providers import (
            get_lms_credential_service,
        )

        mock_repository = MagicMock()

        with patch(
            "src.shared.application.providers.users_providers.LMSCredentialService"
        ) as mock_service_class:
            mock_service_instance = MagicMock()
            mock_service_class.return_value = mock_service_instance

            with patch(
                "src.shared.application.providers.users_providers.LMSCredential"
            ):
                result = get_lms_credential_service(
                    lms_credential_repository=mock_repository
                )

                mock_service_class.assert_called_once_with(repository=mock_repository)
                assert result == mock_service_instance


class TestStatisticProviders:
    """Tests for statistic domain providers."""

    @pytest.mark.asyncio
    async def test_get_xapi_statement_repository_returns_repository_instance(self):
        """Test that get_xapi_statement_repository returns a XAPIStatementRepository instance."""
        from src.shared.application.providers.statistic_providers import (
            get_xapi_statement_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.statistic_providers.XAPIStatementRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_xapi_statement_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_feedback_repository_returns_repository_instance(self):
        """Test that get_feedback_repository returns a FeedbackRepository instance."""
        from src.shared.application.providers.statistic_providers import (
            get_feedback_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.statistic_providers.FeedbackRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_feedback_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_progress_repository_returns_repository_instance(self):
        """Test that get_progress_repository returns a ProgressRepository instance."""
        from src.shared.application.providers.statistic_providers import (
            get_progress_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.statistic_providers.ProgressRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_progress_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_metric_type_repository_returns_repository_instance(self):
        """Test that get_metric_type_repository returns a MetricTypeRepository instance."""
        from src.shared.application.providers.statistic_providers import (
            get_metric_type_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.statistic_providers.MetricTypeRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_metric_type_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance


class TestGameProviders:
    """Tests for game domain providers."""

    @pytest.mark.asyncio
    async def test_get_game_repository_returns_repository_instance(self):
        """Test that get_game_repository returns a GameRepository instance."""
        from src.shared.application.providers.game_providers import (
            get_game_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.game_providers.GameRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_game_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_level_repository_returns_repository_instance(self):
        """Test that get_level_repository returns a LevelRepository instance."""
        from src.shared.application.providers.game_providers import (
            get_level_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.game_providers.LevelRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_level_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_game_instance_repository_returns_repository_instance(self):
        """Test that get_game_instance_repository returns a GameInstanceRepository instance."""
        from src.shared.application.providers.game_providers import (
            get_game_instance_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.game_providers.GameInstanceRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_game_instance_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance

    @pytest.mark.asyncio
    async def test_get_segment_level_repository_returns_repository_instance(self):
        """Test that get_segment_level_repository returns a SegmentLevelRepository instance."""
        from src.shared.application.providers.game_providers import (
            get_segment_level_repository,
        )

        mock_db = MagicMock(spec=AsyncSession)

        with patch(
            "src.shared.application.providers.game_providers.SegmentLevelRepository"
        ) as mock_repo_class:
            mock_repo_instance = MagicMock()
            mock_repo_class.return_value = mock_repo_instance

            result = get_segment_level_repository(db=mock_db)

            mock_repo_class.assert_called_once_with(mock_db)
            assert result == mock_repo_instance


class TestProviderExports:
    """Tests that all providers are properly exported from __init__.py."""

    def test_users_providers_exported(self):
        """Test that all user domain providers are exported."""
        from src.shared.application.providers import (
            get_user_repository,
            get_user_service,
            get_student_repository,
            get_student_service,
            get_professor_repository,
            get_professor_service,
            get_teacher_settings_repository,
            get_teacher_settings_service,
            get_lms_credential_repository,
            get_lms_credential_service,
        )

        assert callable(get_user_repository)
        assert callable(get_user_service)
        assert callable(get_student_repository)
        assert callable(get_student_service)
        assert callable(get_professor_repository)
        assert callable(get_professor_service)
        assert callable(get_teacher_settings_repository)
        assert callable(get_teacher_settings_service)
        assert callable(get_lms_credential_repository)
        assert callable(get_lms_credential_service)

    def test_statistic_providers_exported(self):
        """Test that all statistic domain providers are exported."""
        from src.shared.application.providers import (
            get_xapi_statement_repository,
            get_xapi_statement_service,
            get_feedback_repository,
            get_feedback_service,
            get_progress_repository,
            get_progress_service,
            get_metric_type_repository,
            get_metric_type_service,
        )

        assert callable(get_xapi_statement_repository)
        assert callable(get_xapi_statement_service)
        assert callable(get_feedback_repository)
        assert callable(get_feedback_service)
        assert callable(get_progress_repository)
        assert callable(get_progress_service)
        assert callable(get_metric_type_repository)
        assert callable(get_metric_type_service)

    def test_game_providers_exported(self):
        """Test that all game domain providers are exported."""
        from src.shared.application.providers import (
            get_game_repository,
            get_game_service,
            get_level_repository,
            get_level_service,
            get_game_instance_repository,
            get_game_instance_service,
            get_segment_level_repository,
            get_segment_level_service,
        )

        assert callable(get_game_repository)
        assert callable(get_game_service)
        assert callable(get_level_repository)
        assert callable(get_level_service)
        assert callable(get_game_instance_repository)
        assert callable(get_game_instance_service)
        assert callable(get_segment_level_repository)
        assert callable(get_segment_level_service)
