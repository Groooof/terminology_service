from django.db import models

# Create your models here.


class Directory(models.Model):
    code = models.CharField('Код', max_length=100, blank=False, unique=True)
    name = models.CharField('Наименование', max_length=300, blank=False)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name}'


class DirectoryVersion(models.Model):
    directory = models.ForeignKey(Directory, models.PROTECT, blank=False, verbose_name='Справочник')
    version = models.CharField('Версия', max_length=50, blank=False)
    start_date = models.DateField('Дата начала действия', blank=True, null=True)

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'
        ordering = ['directory__name', 'version']
        unique_together = (('directory', 'version'), ('directory', 'start_date'))
        
    def __str__(self) -> str:
        return f'{self.directory.name} v{self.version}'


class DirectoryElement(models.Model):
    directory_version = models.ForeignKey(DirectoryVersion, models.PROTECT, blank=False, verbose_name='Версия справочника')
    code = models.CharField(max_length=100, blank=False)
    value = models.CharField(max_length=300, blank=False)
    
    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
        ordering = ['directory_version__directory__name', 'directory_version__version', 'value']
        unique_together = (('directory_version', 'code'),)
        
    def __str__(self) -> str:
        return f'[{self.code}]:[{self.value}] ({self.directory_version.directory.name} v{self.directory_version.version})'
