import typing as tp
import datetime as dt

from django.db import models

from .models import (
    Refbook,
    RefbookElement,
    RefbookVersion
)


def check_any_refbook_version_exists(refbook_id: int) -> bool:
    return RefbookVersion.objects.filter(refbook_id=refbook_id).exists()


def get_current_refbook_version(refbook_id: int) -> RefbookVersion:
    current_date = dt.datetime.now()
    return RefbookVersion.objects.filter(
        models.Q(refbook_id=refbook_id)
        &
        models.Q(start_date__lte=current_date)
        ).latest('start_date')
    

def get_all_refbooks() -> tp.List[Refbook]:
    return Refbook.objects.all()


def get_refbooks_actual_by_date(date: str) -> tp.List[Refbook]:
    return Refbook.objects.filter(
        pk__in=RefbookVersion.objects.filter(
            start_date__lte=date
        ).values_list('refbook_id', flat=True)
        )


def get_refbook_elements_for_version(refbook_id: int, version: str) -> tp.List[RefbookElement]:
    return RefbookElement.objects.filter(
        models.Q(refbook_version__version=version)
        &
        models.Q(refbook_version__refbook_id=refbook_id)
    )


def check_refbook_element_exists(code: str, value: str, version: str) -> bool:
    return RefbookElement.objects.filter(
        models.Q(code=code)
        &
        models.Q(value=value)
        &
        models.Q(refbook_version__version=version)
    ).exists()
