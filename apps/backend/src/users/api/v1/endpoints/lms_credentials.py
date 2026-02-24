from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.session import get_db
from src.users.infrastructure.lms_credential_repository import LMSCredentialRepository
from src.users.api.v1.schemas.lms_credential import (
    LMSCredentialCreate,
    LMSCredentialResponse,
)
from src.shared.domain.exceptions import NotFoundException, DuplicateEntryException


router = APIRouter(prefix="/lms/credentials", tags=["LMS Credentials"])


@router.post(
    "", response_model=LMSCredentialResponse, status_code=status.HTTP_201_CREATED
)
async def register_lms_credentials(
    credentials: LMSCredentialCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Registrar credenciales LMS para un usuario.

    - **user_id**: ID del usuario que registra las credenciales
    - **lms_url**: URL del LMS (ej: https://moodle.university.edu)
    - **lms_email**: Email de la cuenta en el LMS
    - **lms_password**: Contraseña de la cuenta LMS
    - **lms_provider**: Proveedor LMS (moodle, canvas, etc.)
    """
    repo = LMSCredentialRepository(db)

    # Verificar si ya existen credenciales para este email
    existing = await repo.get_by_lms_email(credentials.lms_email)
    if existing:
        raise DuplicateEntryException("Ya existen credenciales LMS para este email")

    # Crear la credencial (simplificado, implementar lógica completa según necesidad)
    credential_data = credentials.model_dump()
    credential_data["hashed_password"] = credential_data.pop("lms_password")

    new_credential = await repo.create(credential_data)
    return new_credential


@router.get("/user/{user_id}", response_model=LMSCredentialResponse)
async def get_user_lms_credentials(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtener las credenciales LMS de un usuario.

    Retorna las credenciales con la contraseña oculta.
    """
    repo = LMSCredentialRepository(db)
    credential = await repo.get_by_user_id(user_id)

    if not credential:
        raise NotFoundException(
            f"No se encontraron credenciales LMS para el usuario {user_id}"
        )

    return credential


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_lms_credentials(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Eliminar las credenciales LMS de un usuario.

    Realiza un soft delete de las credenciales.
    """
    repo = LMSCredentialRepository(db)
    credential = await repo.get_by_user_id(user_id)

    if not credential:
        raise NotFoundException(
            f"No se encontraron credenciales LMS para el usuario {user_id}"
        )

    await repo.soft_delete(credential.id)
