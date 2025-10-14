SECRET_KEY = "secret"
DEBUG = True

INSTALLED_APPS = ("anydi_django",)

ROOT_URLCONF = "tests.urls"

MIDDLEWARE = ("anydi_django.middleware.request_scoped_middleware",)

# AnyDI settings
ANYDI = {
    "STRICT_MODE": False,
    "REGISTER_SETTINGS": True,
    "REGISTER_COMPONENTS": True,
    "MODULES": ["tests.container.configure"],
    "PATCH_NINJA": True,
    "INJECT_URLCONF": ROOT_URLCONF,
    "SCAN_PACKAGES": ["tests.scan"],
}

# Custom settings
HELLO_MESSAGE = "Hello, World!"
