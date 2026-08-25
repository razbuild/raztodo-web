from __future__ import annotations

from unittest.mock import Mock

import pytest

from raztodo_web.app import dependencies as deps


class FakeStorage:
    """Stand-in for SQLiteTaskRepository; identity is all that matters here."""


@pytest.fixture()
def fake_storage() -> FakeStorage:
    return FakeStorage()


@pytest.fixture()
def fake_container(monkeypatch: pytest.MonkeyPatch, fake_storage: FakeStorage) -> Mock:
    container = Mock()
    container.repo_singleton.return_value = fake_storage
    monkeypatch.setattr(deps, "_container", container)
    return container


class TestGetStorage:
    def test_returns_container_singleton(
        self, fake_container: Mock, fake_storage: FakeStorage
    ) -> None:
        assert deps.get_storage() is fake_storage

    def test_delegates_to_repo_singleton(self, fake_container: Mock) -> None:
        deps.get_storage()
        fake_container.repo_singleton.assert_called_once_with()


class TestGetFactory:
    def test_returns_factory_instance(self) -> None:
        assert isinstance(deps.get_factory(), deps.DefaultUseCaseFactory)

    def test_returns_new_instance_each_call(self) -> None:
        assert deps.get_factory() is not deps.get_factory()


class TestGetUseCase:
    def test_calls_named_factory_method_with_storage(
        self, fake_storage: FakeStorage
    ) -> None:
        factory = Mock()
        dependency = deps.get_use_case("create_list_tasks")

        result = dependency(fake_storage, factory)

        factory.create_list_tasks.assert_called_once_with(fake_storage)
        assert result is factory.create_list_tasks.return_value


class TestUseCaseProviders:
    """Each exported *_uc provider must be wired to the matching factory method."""

    @pytest.mark.parametrize(
        ("provider", "method_name"),
        [
            (deps.get_list_uc, "create_list_tasks"),
            (deps.get_create_uc, "create_create_task"),
            (deps.get_update_uc, "create_update_task"),
            (deps.get_delete_uc, "create_delete_task"),
            (deps.get_clear_uc, "create_clear_tasks"),
            (deps.get_mark_done_uc, "create_mark_done"),
            (deps.get_export_uc, "create_export_tasks"),
            (deps.get_import_uc, "create_import_tasks"),
            (deps.get_explain_uc, "create_explain_task"),
        ],
    )
    def test_provider_calls_expected_factory_method(
        self, provider, method_name: str, fake_storage: FakeStorage
    ) -> None:
        factory = Mock()

        provider(fake_storage, factory)

        getattr(factory, method_name).assert_called_once_with(fake_storage)
