from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from uuid import UUID
from ....schemas.responses.alert_response import AlertResponse
from .....application.use_cases.alert_retrieval import AlertRetrievalUseCase
from .....application.ports.alert_repository import AlertRepository
from .....core.dependencies import get_alert_repository

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=List[AlertResponse])
async def list_alerts(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    alert_repository: AlertRepository = Depends(get_alert_repository),
):
    """Получение списка алертов"""
    use_case = AlertRetrievalUseCase(alert_repository)
    alerts = await use_case.get_all(limit, offset)
    return [AlertResponse.from_domain(alert) for alert in alerts]

@router.get("/file/{file_id}", response_model=List[AlertResponse])
async def get_alerts_by_file(
    file_id: UUID,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    alert_repository: AlertRepository = Depends(get_alert_repository),
):
    """Получение алертов по файлу"""
    use_case = AlertRetrievalUseCase(alert_repository)
    alerts = await use_case.get_by_file(file_id, limit, offset)
    return [AlertResponse.from_domain(alert) for alert in alerts]