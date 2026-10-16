# Changelog

## [0.1.1] - 2026-10-16

### Added
- Added a **Report a bug** link to the sidebar

### Fixed
- Fixed partial task updates to preserve existing values for fields that are not provided
- Improved export error handling and cleanup after failed exports
- Standardized API error messages for more consistent responses

### Tests
- Added test coverage for partial task updates and export cleanup

## [0.1.0] - 2026-08-26

### Added

- Initial standalone release of RazTodo Web
- FastAPI-based REST API and browser-based Web UI
- Task creation, editing, completion, and deletion
- Task search and status filtering
- Support for priorities, tags, projects, and due dates
- JSON import and export
- Light and dark themes
- Optional Ollama-powered task explanations
- Configurable web host and port
- Swagger UI and ReDoc API documentation
- Local-first architecture built on top of RazTodo