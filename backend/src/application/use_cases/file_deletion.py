from uuid import UUID
from ..ports.file_repository import FileRepository
from ..ports.file_storage import FileStorage
from ...core.exceptions import FileNotFoundError

class FileDeletionUseCase:
    """Use case для удаления файла"""

    def __init__(
        self,
        file_repository: FileRepository,
        file_storage: FileStorage
    ):
        self.file_repository = file_repository
        self.file_storage = file_storage

    async def execute(self, file_id: UUID) -> None:
        """Удаление файла"""

        # Получение файла
        file = await self.file_repository.get_by_id(file_id)
        if not file:
            raise FileNotFoundError(str(file_id))

        # Удаление из хранилища
        await self.file_storage.delete(file.id, file.stored_name)

        # Удаление из БД
        await self.file_repository.delete(file_id)