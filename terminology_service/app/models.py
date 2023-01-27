from django.db import models

# Create your models here.


class Refbook(models.Model):
    code = models.CharField('Код', max_length=100, blank=False, unique=True)
    name = models.CharField('Наименование', max_length=300, blank=False)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name}'


class RefbookVersion(models.Model):
    refbook = models.ForeignKey(Refbook, models.PROTECT, blank=False, verbose_name='Справочник')
    version = models.CharField('Версия', max_length=50, blank=False)
    start_date = models.DateField('Дата начала действия', blank=True, null=True)

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'
        ordering = ['refbook__name', 'version']
        unique_together = (('refbook', 'version'), ('refbook', 'start_date'))
        
    def __str__(self) -> str:
        return f'{self.refbook.name}-v{self.version}'


class RefbookElement(models.Model):
    refbook_version = models.ForeignKey(RefbookVersion, models.PROTECT, blank=False, verbose_name='Версия справочника')
    code = models.CharField('Код', max_length=100, blank=False)
    value = models.CharField('Значение', max_length=300, blank=False)
    
    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
        ordering = ['refbook_version__refbook__name', 'refbook_version__version', 'value']
        unique_together = (('refbook_version', 'code'),)
        
    def __str__(self) -> str:
        return f'{self.code}-{self.value}'
