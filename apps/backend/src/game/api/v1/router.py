from fastapi import APIRouter

from src.game.api.v1.endpoints.get_games import router as get_games_router
from src.game.api.v1.endpoints.create_game import router as create_game_router
from src.game.api.v1.endpoints.get_game import router as get_game_router
from src.game.api.v1.endpoints.update_game import router as update_game_router
from src.game.api.v1.endpoints.delete_game import router as delete_game_router
from src.game.api.v1.endpoints.create_game_instance import router as create_game_instance_router
from src.game.api.v1.endpoints.list_game_instances import router as list_game_instances_router
from src.game.api.v1.endpoints.get_instance import router as get_instance_router
from src.game.api.v1.endpoints.end_instance import router as end_instance_router
from src.game.api.v1.endpoints.get_level import router as get_level_router
from src.game.api.v1.endpoints.update_level import router as update_level_router
from src.game.api.v1.endpoints.delete_level import router as delete_level_router
from src.game.api.v1.endpoints.get_game_levels import router as get_game_levels_router
from src.game.api.v1.endpoints.create_game_level import router as create_game_level_router
from src.game.api.v1.endpoints.get_level_segments import router as get_level_segments_router
from src.game.api.v1.endpoints.create_level_segment import router as create_level_segment_router
from src.game.api.v1.endpoints.update_segment import router as update_segment_router
from src.game.api.v1.endpoints.delete_segment import router as delete_segment_router


router = APIRouter(prefix="", tags=["Games"])

# Incluir todos los routers de endpoints
router.include_router(get_games_router)
router.include_router(create_game_router)
router.include_router(get_game_router)
router.include_router(update_game_router)
router.include_router(delete_game_router)
router.include_router(create_game_instance_router)
router.include_router(list_game_instances_router)
router.include_router(get_instance_router)
router.include_router(end_instance_router)
router.include_router(get_level_router)
router.include_router(update_level_router)
router.include_router(delete_level_router)
router.include_router(get_game_levels_router)
router.include_router(create_game_level_router)
router.include_router(get_level_segments_router)
router.include_router(create_level_segment_router)
router.include_router(update_segment_router)
router.include_router(delete_segment_router)
