from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, Form, HTTPException
from typing import List
from uuid import UUID
from ....schemas.requests.file_request import FileCreateRequest
from ....schemas.responses.file_response import FileResponse
from .....application.use_cases.file_upload import FileUploadUseCase
from .....application.use_cases.file_retrieval import FileRetrievalUseCase
from .....application.use_cases.file_update import FileUpdateUseCase
from .....application.use_cases.file_deletion import FileDeletionUseCase
from .....application.ports.file_repository import FileRepository
from .....application.ports.file_storage import FileStorage
from .....application.ports.task_queue import TaskQueue
from .....core.dependencies import get_file_repository, get_file_storage, get_task_queue

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/", response_model=FileResponse, status_code=201)
async def upload_file(
    title: str = Form(...),
    file: UploadFile = FastAPIFile(...),
    file_repository: FileRepository = Depends(get_file_repository),
    file_storage: FileStorage = Depends(get_file_storage),
    task_queue: TaskQueue = Depends(get_task_queue),
):
    """Загрузка нового файла"""
    use_case = FileUploadUseCase(file_repository, file_storage, task_queue)

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")

    result = await use_case.execute(
        title=title,
        original_name=file.filename or "unknown",
        content=content,
        mime_type=file.content_type or "application/octet-stream"
    )
    return FileResponse.from_domain(result)

@router.get("/", response_model=List[FileResponse])
async def list_files(
    limit: int = 100,
    offset: int = 0,
    file_repository: FileRepository = Depends(get_file_repository),
):
    """Получение списка файлов"""
    use_case = FileRetrievalUseCase(file_repository)
    files = await use_case.get_all(limit, offset)
    return [FileResponse.from_domain(file) for file in files]

@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: UUID,
    file_repository: FileRepository = Depends(get_file_repository),
):
    """Получение информации о файле"""
    use_case = FileRetrievalUseCase(file_repository)
    file = await use_case.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse.from_domain(file)

@router.patch("/{file_id}", response_model=FileResponse)
async def update_file(
    file_id: UUID,
    request: FileCreateRequest,
    file_repository: FileRepository = Depends(get_file_repository),
):
    """Обновление информации о файле"""
    use_case = FileUpdateUseCase(file_repository)
    file = await use_case.execute(file_id, request.title)
    return FileResponse.from_domain(file)

@router.delete("/{file_id}", status_code=204)
async def delete_file(
    file_id: UUID,
    file_repository: FileRepository = Depends(get_file_repository),
    file_storage: FileStorage = Depends(get_file_storage),
):
    """Удаление файла"""
    use_case = FileDeletionUseCase(file_repository, file_storage)
    await use_case.execute(file_id)

@router.get("/{file_id}/download")
async def download_file(
    file_id: UUID,
    file_repository: FileRepository = Depends(get_file_repository),
    file_storage: FileStorage = Depends(get_file_storage),
):
    """Скачивание файла"""
    use_case = FileRetrievalUseCase(file_repository)
    file = await use_case.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    content = await file_storage.get_content(file.id, file.stored_name)
    if not content:
        raise HTTPException(status_code=404, detail="File content not found")

    from fastapi.responses import Response
    return Response(
        content=content,
        media_type=file.mime_type,
        headers={
            "Content-Disposition": f'attachment; filename="{file.original_name}"'
        }
    )