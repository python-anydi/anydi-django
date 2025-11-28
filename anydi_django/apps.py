from __future__ import annotations

import types

import anydi
from anydi._container import import_container
from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from ._settings import get_settings
from ._utils import inject_urlpatterns, register_components, register_settings


class ContainerConfig(AppConfig):
    name = "anydi_django"
    label = "anydi_django"

    def __init__(self, app_name: str, app_module: types.ModuleType | None) -> None:
        super().__init__(app_name, app_module)
        self.settings = get_settings()
        self.container = self._make_container()

    def _make_container(self) -> anydi.Container:
        """Create the AnyDI container configured for this app."""
        container_path = self.settings["CONTAINER_FACTORY"]
        if not container_path:
            return anydi.Container()

        try:
            return import_container(container_path)
        except ImportError as exc:
            raise ImproperlyConfigured(
                f"Cannot import container factory '{container_path}'."
            ) from exc

    def ready(self) -> None:  # noqa: C901
        # Register Django settings
        if self.settings["REGISTER_SETTINGS"]:
            register_settings(
                self.container,
                prefix=getattr(
                    settings,
                    "ANYDI_SETTINGS_PREFIX",
                    "django.conf.settings.",
                ),
            )

        # Register Django components
        if self.settings["REGISTER_COMPONENTS"]:
            register_components(self.container)

        # Register modules
        for module_path in self.settings["MODULES"]:
            try:
                module_cls = import_string(module_path)
            except ImportError as exc:
                raise ImproperlyConfigured(
                    f"Cannot import module '{module_path}'."
                ) from exc
            self.container.register_module(module_cls)

        # Patching the django-ninja framework if it installed
        if self.settings["PATCH_NINJA"]:
            from .ninja import patch_ninja

            patch_ninja()

        # Auto-injecting the container into views
        if urlconf := self.settings["INJECT_URLCONF"]:
            if isinstance(urlconf, str):
                urlconf = [urlconf]
            for u in urlconf:
                inject_urlpatterns(self.container, urlconf=u)

        # Scan packages
        for scan_package in self.settings["SCAN_PACKAGES"]:
            self.container.scan(scan_package)
