#!/usr/bin/python3
"""Models package - creates a single FileStorage instance named storage."""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()

