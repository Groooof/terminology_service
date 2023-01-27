import typing as tp
import datetime as dt

from django.db import models

from .models import (
    Directory,
    DirectoryVersion,
    DirectoryElement
)


def get_latest_directory_version(directory_id: Directory) -> DirectoryVersion:
    current_date = dt.datetime.now()
    return DirectoryVersion.objects.filter(
        models.Q(directory_id=directory_id)
        &
        models.Q(start_date__lte=current_date)
        ).latest('start_date')
    

def get_all_refbooks() -> tp.List[Directory]:
    return Directory.objects.all()


def get_refbooks_actual_by_date(date: str) -> tp.List[Directory]:
    return Directory.objects.filter(
        pk__in=DirectoryVersion.objects.filter(
            start_date__lte=date
        ).values_list('directory_id', flat=True)
        )


def get_refbook_elements_for_version(refbook_id: int, version: str) -> tp.List[DirectoryElement]:
    return DirectoryElement.objects.filter(
        models.Q(directory_version__version=version)
        &
        models.Q(directory_version__directory_id=refbook_id)
    )


def check_refbook_element_exists(code: str, value: str, version: str) -> bool:
    return DirectoryElement.objects.filter(
        models.Q(code=code)
        &
        models.Q(value=value)
        &
        models.Q(directory_version__version=version)
    ).exists()
