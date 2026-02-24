from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from src.statistic.api.v1.schemas.xapi_statement import (
    XAPIStatementCreate,
    XAPIStatementBatchCreate,
    XAPIStatementResponse,
    XAPIStatementListResponse,
)
from src.statistic.application.service.xapi_statement_service import (
    XAPIStatementService,
)
from src.shared.infrastructure.session import get_db
from src.shared.deps import get_current_user
from src.users.domain.user import User


router = APIRouter(prefix="/xapi", tags=["xAPI"])


@router.post(
    "/statements",
    response_model=List[XAPIStatementResponse],
    status_code=status.HTTP_200_OK,
)
async def send_statements(
    batch_data: XAPIStatementBatchCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Receive and store xAPI statements.

    Accepts a batch of xAPI statements (1-1000 per request).
    Supports full xAPI 1.0 specification with game-specific context.

    The game client should send statements with:
    - actor.account.name = student_id
    - verb = standard xAPI verb
    - object.id = activity ID (e.g., hello-world://segment/level_1_seg_3)
    - result = quantitative data (score, success, completion)
    - context = qualitative data (platform, language, extensions)
    - context.extensions = game-specific data (game_id, level_id, segment_id)
    """
    service = XAPIStatementService(db=db)

    try:
        statements = await service.save_batch(batch_data.statements)

        # Convert to response format
        response_statements = []
        for stmt in statements:
            stmt_dict = stmt.statement if isinstance(stmt.statement, dict) else {}
            response_statements.append(
                XAPIStatementResponse(
                    id=stmt.id,
                    actor=stmt_dict.get("actor", {}),
                    verb=stmt_dict.get("verb", {}),
                    object=stmt_dict.get("object", {}),
                    result=stmt_dict.get("result"),
                    context=stmt_dict.get("context"),
                    timestamp=stmt.timestamp,
                    stored=stmt.stored,
                )
            )

        return response_statements

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error storing statements: {str(e)}",
        )


@router.get("/statements", response_model=XAPIStatementListResponse)
async def get_statements(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return"
    ),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    verb_id: Optional[str] = Query(None, description="Filter by verb ID"),
    game_id: Optional[int] = Query(None, description="Filter by game ID"),
    level_id: Optional[int] = Query(None, description="Filter by level ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get xAPI statements with optional filters.

    Returns statements with pagination. Use filters to narrow results.
    """
    service = XAPIStatementService(db=db)

    # Apply filters
    if student_id:
        statements = await service.get_by_student(student_id, skip, limit)
    elif verb_id:
        statements = await service.get_by_verb(verb_id, skip, limit)
    elif game_id:
        statements = await service.get_by_game(game_id, skip, limit)
    elif level_id:
        statements = await service.get_by_level(level_id, skip, limit)
    else:
        statements = await service.get_statements(skip, limit)

    # Convert to response format
    response_statements = []
    for stmt in statements:
        stmt_dict = stmt.statement if isinstance(stmt.statement, dict) else {}
        response_statements.append(
            XAPIStatementResponse(
                id=stmt.id,
                actor=stmt_dict.get("actor", {}),
                verb=stmt_dict.get("verb", {}),
                object=stmt_dict.get("object", {}),
                result=stmt_dict.get("result"),
                context=stmt_dict.get("context"),
                timestamp=stmt.timestamp,
                stored=stmt.stored,
            )
        )

    return XAPIStatementListResponse(
        statements=response_statements,
        total=len(response_statements),
        skip=skip,
        limit=limit,
    )


@router.get("/statements/{statement_id}", response_model=XAPIStatementResponse)
async def get_statement(
    statement_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific xAPI statement by ID.
    """
    service = XAPIStatementService(db=db)

    statement = await service.get_statement(statement_id)
    if not statement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Statement with ID {statement_id} not found",
        )

    stmt_dict = statement.statement if isinstance(statement.statement, dict) else {}
    return XAPIStatementResponse(
        id=statement.id,
        actor=stmt_dict.get("actor", {}),
        verb=stmt_dict.get("verb", {}),
        object=stmt_dict.get("object", {}),
        result=stmt_dict.get("result"),
        context=stmt_dict.get("context"),
        timestamp=statement.timestamp,
        stored=statement.stored,
    )
