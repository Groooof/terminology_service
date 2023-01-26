from django.db import models

# Create your models here.


class Directory(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField('Код', max_length=100, blank=False, unique=True)
    name = models.CharField('Наименование', max_length=300, blank=False)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name}'
