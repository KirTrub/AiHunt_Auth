class AppException(Exception):
    pass

class NotFoundException(AppException):
    """Ресурс не найден"""
    def __init__(self, message: str = "Resource not found"):
        self.message = message

class NotAuthenticatedException(AppException):
    """Ошибка аутентификации"""
    def __init__(self, message: str = "Not authenticated"):
        self.message = message
    pass

class ForbiddenException(AppException):
    """Ошибка авторизации"""
    def __init__(self, message: str = "Forbidden resource"):
        self.message = message
    pass

class EmailAlreadyExistsException(AppException):
    """Email уже есть в базе"""
    def __init__(self, message: str = "Email already exists"):
        self.message = message
    pass

class DifferingPasswordsException(AppException):
    """При регистрации не совпали пароли"""
    def __init__(self, message: str = "Differing passwords"):
        self.message = message
    pass