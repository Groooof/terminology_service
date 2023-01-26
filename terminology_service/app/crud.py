from django.db import models

from .models import (
    Directory,
    DirectoryVersion
)


def get_latest_directory_version(directory: Directory) -> DirectoryVersion:
    return DirectoryVersion.objects.filter(directory=directory).latest('start_date')
