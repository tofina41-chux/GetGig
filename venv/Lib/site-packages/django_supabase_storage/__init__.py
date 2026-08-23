"""
Django Supabase Storage

A Django storage backend for Supabase buckets.
"""

__version__ = "1.0.1"
__author__ = "Madhav Sharma"
__license__ = "MIT"

try:
    from .storage_backends import (
        SupabaseStorage,
        SupabaseMediaStorage,
        SupabaseStaticStorage,
    )

    __all__ = [
        "SupabaseStorage",
        "SupabaseMediaStorage",
        "SupabaseStaticStorage",
    ]
except ImportError as e:
    # Allow the package to be imported even if dependencies are missing
    # The error will be raised when trying to actually use the storage backend
    import warnings
    warnings.warn(
        f"django-supabase-storage could not be fully imported: {str(e)}. "
        "Make sure all dependencies are installed (especially 'supabase').",
        ImportWarning
    )
    __all__ = []
