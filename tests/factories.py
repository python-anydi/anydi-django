"""Helpers for testing ContainerConfig's CONTAINER_FACTORY handling."""

from __future__ import annotations

import anydi

# A container instance that can be referenced directly.
CONTAINER_INSTANCE = anydi.Container()


def container_factory() -> anydi.Container:
    """Return a reusable container instance."""
    return CALLABLE_CONTAINER


CALLABLE_CONTAINER = anydi.Container()


def bad_container_factory() -> object:
    """Return the wrong type intentionally for tests."""
    return object()


# Alias used by tests via import_string.
container_instance = CONTAINER_INSTANCE
