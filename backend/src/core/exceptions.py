from typing import Optional, Any

class AppException(Exception):
    """Базовое исключение приложения"""
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: Optional[dict] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class FileNotFoundError(AppException):
    """Файл не найден"""
    def __init__(self, file_id: str):
        super().__init__(
            message=f"File with id {file_id} not found",
            status_code=404,
            details={"file_id": file_id}
        )

class FileValidationError(AppException):
    """Ошибка валидации файла"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=400,
            details=details
        )

class FileStorageError(AppException):
    """Ошибка хранилища файлов"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=500,
            details=details
        )

class AlertCreationError(AppException):
    """Ошибка создания алерта"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=500,
            details=details
        )

class TaskQueueError(AppException):
    """Ошибка очереди задач"""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            status_code=500,
            details=details
        )

class UnauthorizedError(AppException):
    """Ошибка авторизации"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            status_code=401
        )

class ForbiddenError(AppException):
    """Доступ запрещен"""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            status_code=403
        )