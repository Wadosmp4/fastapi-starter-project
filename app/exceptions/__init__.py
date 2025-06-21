from fastapi import HTTPException, status


class BaseAppException(Exception):
    """Base exception for the application"""

    pass


class NotFoundException(BaseAppException):
    """Exception raised when a resource is not found"""

    def __init__(self, message: str = 'Resource not found'):
        self.message = message
        super().__init__(self.message)


class ValidationException(BaseAppException):
    """Exception raised when validation fails"""

    def __init__(self, message: str = 'Validation failed'):
        self.message = message
        super().__init__(self.message)


class DatabaseException(BaseAppException):
    """Exception raised when database operations fail"""

    def __init__(self, message: str = 'Database operation failed'):
        self.message = message
        super().__init__(self.message)


class UnauthorizedException(BaseAppException):
    """Exception raised when user is not authorized"""

    def __init__(self, message: str = 'Unauthorized'):
        self.message = message
        super().__init__(self.message)


class ConflictException(BaseAppException):
    """Exception raised when there's a conflict (e.g., duplicate resource)"""

    def __init__(self, message: str = 'Resource conflict'):
        self.message = message
        super().__init__(self.message)


# FastAPI HTTP exceptions for easy conversion
def to_http_exception(exception: BaseAppException | Exception) -> HTTPException:
    """Convert custom exceptions to FastAPI HTTP exceptions"""
    if isinstance(exception, NotFoundException):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exception.message)
    elif isinstance(exception, ValidationException):
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exception.message)
    elif isinstance(exception, DatabaseException):
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exception.message)
    elif isinstance(exception, UnauthorizedException):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exception.message)
    elif isinstance(exception, ConflictException):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exception.message)
    else:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
