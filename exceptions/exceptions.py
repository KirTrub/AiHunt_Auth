from fastapi import status

class AppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Внутренняя ошибка сервера"

    def __init__(self, detail: str = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)

class NotFoundException(AppException):
    """404: Ресурс не найден"""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Ресурс не найден"

class UnauthorizedException(AppException):
    """401: Ошибка аутентификации (неверный пароль или токен)"""
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный email или пароль"

class ForbiddenException(AppException):
    """403: Ошибка авторизации (нет прав доступа)"""
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав для выполнения операции"

class ConflictException(AppException):
    """409: Конфликт данных"""
    status_code = status.HTTP_409_CONFLICT
    detail = "Ресурс уже существует"

class BadRequestException(AppException):
    """400: Некорректный запрос"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка в данных запроса"

class EmailAlreadyExistsException(ConflictException):
    detail = "Пользователь с таким email уже существует"

class DifferingPasswordsException(BadRequestException):
    detail = "Пароли не совпадают"