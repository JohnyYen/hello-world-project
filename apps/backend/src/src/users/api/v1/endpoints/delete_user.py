from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from src.users.application.usecase.delete_user_usecase import DeleteUserUseCase


router = APIRouter()


@router.delete(
    "/{user_id}",
    summary="Eliminar un usuario (soft delete)",
    status_code=status.HTTP_200_OK,
)
async def delete_user(user_id: UUID, delete_user_uc: DeleteUserUseCase = Depends()):
    """
    Realiza un soft delete de un usuario por su ID.
    """
    try:
        result = await delete_user_uc.execute(user_id=user_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        return {"message": "Usuario eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
