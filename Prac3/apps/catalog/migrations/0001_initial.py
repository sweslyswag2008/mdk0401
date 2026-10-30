import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Раздел')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Место хранения')),
            ],
            options={
                'verbose_name': 'Место хранения',
                'verbose_name_plural': 'Места хранения',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Издательство')),
            ],
            options={
                'verbose_name': 'Издательство',
                'verbose_name_plural': 'Издательства',
            },
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Издание')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.category', verbose_name='Раздел')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.publisher', verbose_name='Издательство')),
            ],
            options={
                'verbose_name': 'Издание',
                'verbose_name_plural': 'Издания',
            },
        ),
    ]
