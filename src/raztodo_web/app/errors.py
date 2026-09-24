from __future__ import annotations

from dataclasses import dataclass

from fastapi import HTTPException
from raztodo.domain.exceptions import (
    DatabaseConnectionError,
    DatabaseError,
    DuplicateTaskError,
    FileOperationError,
    FilePermissionError,
    InvalidFileFormatError,
    RazTodoException,
    TaskFileNotFoundError,
    TaskNotFoundError,
    TaskValidationError,
)


@dataclass(frozen=True)
class APIErrorDefinition:
    status_code: int
    code: str
    message: str


_ERROR_DEFINITIONS: dict[type[RazTodoException], APIErrorDefinition] = {
    TaskNotFoundError: APIErrorDefinition(
        status_code=404,
        code="TASK_NOT_FOUND",
        message="Task not found",
    ),
    TaskValidationError: APIErrorDefinition(
        status_code=400,
        code="TASK_VALIDATION_ERROR",
        message="Task validation failed",
    ),
    DuplicateTaskError: APIErrorDefinition(
        status_code=409,
        code="DUPLICATE_TASK",
        message="Task already exists",
    ),
    TaskFileNotFoundError: APIErrorDefinition(
        status_code=404,
        code="FILE_NOT_FOUND",
        message="File not found",
    ),
    FilePermissionError: APIErrorDefinition(
        status_code=403,
        code="PERMISSION_DENIED",
        message="Permission denied",
    ),
    InvalidFileFormatError: APIErrorDefinition(
        status_code=400,
        code="INVALID_FILE_FORMAT",
        message="Invalid file format",
    ),
    FileOperationError: APIErrorDefinition(
        status_code=400,
        code="FILE_OPERATION_ERROR",
        message="File operation failed",
    ),
    DatabaseConnectionError: APIErrorDefinition(
        status_code=503,
        code="DATABASE_CONNECTION_ERROR",
        message="Database connection failed",
    ),
    DatabaseError: APIErrorDefinition(
        status_code=500,
        code="DATABASE_ERROR",
        message="Database operation failed",
    ),
}


def api_error_response(definition: APIErrorDefinition) -> dict[str, dict[str, str]]:
    return {
        "error": {
            "code": definition.code,
            "message": definition.message,
        }
    }


def _definition_for_error(error: RazTodoException) -> APIErrorDefinition:
    definition = _ERROR_DEFINITIONS.get(type(error))

    if definition is not None:
        return definition

    error_message = str(error)

    if error_message.startswith("DuplicateTaskError:"):
        return _ERROR_DEFINITIONS[DuplicateTaskError]

    if error_message.startswith("TaskValidationError:"):
        return _ERROR_DEFINITIONS[TaskValidationError]

    if error_message.startswith("No task found with id "):
        return _ERROR_DEFINITIONS[TaskNotFoundError]

    if error_message.startswith("DatabaseConnectionError:"):
        return _ERROR_DEFINITIONS[DatabaseConnectionError]

    if error_message.startswith("DatabaseError:"):
        return _ERROR_DEFINITIONS[DatabaseError]

    if error_message.startswith("FilePermissionError:"):
        return _ERROR_DEFINITIONS[FilePermissionError]

    if error_message.startswith("InvalidFileFormatError:"):
        return _ERROR_DEFINITIONS[InvalidFileFormatError]

    if error_message.startswith("TaskFileNotFoundError:"):
        return _ERROR_DEFINITIONS[TaskFileNotFoundError]

    if error_message.startswith("FileOperationError:"):
        return _ERROR_DEFINITIONS[FileOperationError]

    return APIErrorDefinition(
        status_code=400,
        code="DOMAIN_ERROR",
        message="The request could not be completed",
    )


def domain_error_response(
    error: RazTodoException,
) -> tuple[int, dict[str, dict[str, str]]]:
    definition = _definition_for_error(error)
    return definition.status_code, api_error_response(definition)


def domain_error(error: RazTodoException) -> HTTPException:
    status_code, detail = domain_error_response(error)
    return HTTPException(status_code=status_code, detail=detail["error"])


def llm_error_response() -> dict[str, dict[str, str]]:
    return api_error_response(
        APIErrorDefinition(
            status_code=500,
            code="LLM_ERROR",
            message="Unable to generate explanation",
        )
    )
