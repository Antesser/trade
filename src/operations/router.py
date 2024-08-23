import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/operations", tags=["operation"])

@router.get("/long_operation")
@cache(expire=90)
async def get_long_operation(delay:int):

    asyncio.sleep(delay)
    return {
        "status": "faster than a bullet",
        "data": f"we've not waited for {delay} sec",
        "details": None,
    }

@router.get("/")
async def get_specific_operations(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            "status": "oks",
            "data": result.mappings().all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(
            status_code=400,
            detail={"status": "err", "data": None, "details": "wild exception occured"},
        )


@router.post("/")
async def add_specific_operations(
    new_operation: OperationCreate,
    session: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    statement = insert(operation).values(new_operation.model_dump())
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}
