import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='ФИО автора')),
                ('country', models.CharField(blank=True, max_length=50, verbose_name='Страна')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('year', models.PositiveIntegerField(verbose_name='Год издания')),
                ('publisher', models.CharField(blank=True, max_length=100, verbose_name='Издательство')),
                ('genre', models.CharField(blank=True, choices=[('fiction', 'Художественная'), ('science', 'Научная'), ('textbook', 'Учебная'), ('children', 'Детская'), ('reference', 'Справочная')], max_length=20, verbose_name='Раздел')),
                ('pages', models.PositiveIntegerField(blank=True, null=True, verbose_name='Страниц')),
                ('isbn', models.CharField(blank=True, max_length=20, verbose_name='ISBN')),
                ('inventory_number', models.CharField(max_length=20, unique=True, verbose_name='Инвентарный номер')),
                ('shelf', models.CharField(blank=True, max_length=20, verbose_name='Стеллаж / полка')),
                ('status', models.CharField(choices=[('available', 'В фонде'), ('reserved', 'Забронирована'), ('issued', 'Выдана'), ('written_off', 'Списана')], default='available', max_length=20, verbose_name='Статус')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='catalog.author', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ['-created_at'],
            },
        ),
    ]
