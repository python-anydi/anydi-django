from __future__ import annotations

import importlib

import anydi
import pytest
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from anydi_django.apps import ContainerConfig


def _make_config() -> ContainerConfig:
    """Instantiate a fresh ContainerConfig for testing."""
    module = importlib.import_module("anydi_django")
    return ContainerConfig("anydi_django", module)


def test_container_config_creates_container_without_factory() -> None:
    config = _make_config()
    assert isinstance(config.container, anydi.Container)


def test_container_factory_can_reference_container_instance() -> None:
    from tests import factories

    with override_settings(
        ANYDI={
            **django_settings.ANYDI,
            "CONTAINER_FACTORY": "tests.factories.container_instance",
        }
    ):
        config = _make_config()

    assert config.container is factories.CONTAINER_INSTANCE


def test_container_factory_callable_returns_container() -> None:
    from tests import factories

    with override_settings(
        ANYDI={
            **django_settings.ANYDI,
            "CONTAINER_FACTORY": "tests.factories.container_factory",
        }
    ):
        config = _make_config()

    assert config.container is factories.CALLABLE_CONTAINER


def test_container_factory_callable_must_return_container() -> None:
    with override_settings(
        ANYDI={
            **django_settings.ANYDI,
            "CONTAINER_FACTORY": "tests.factories.bad_container_factory",
        }
    ):
        with pytest.raises(
            ImproperlyConfigured, match="must return an anydi.Container"
        ):
            _make_config()
