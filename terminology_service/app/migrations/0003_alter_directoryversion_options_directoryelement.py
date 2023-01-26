# Generated by Django 4.1.5 on 2023-01-26 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_directoryversion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='directoryversion',
            options={'ordering': ['directory__name', 'version'], 'verbose_name': 'Версия справочника', 'verbose_name_plural': 'Версии справочников'},
        ),
        migrations.CreateModel(
            name='DirectoryElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=300)),
                ('directory_version', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.directoryversion', verbose_name='Версия справочника')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочников',
                'ordering': ['directory_version__directory__name', 'directory_version__version', 'value'],
                'unique_together': {('directory_version', 'code')},
            },
        ),
    ]
