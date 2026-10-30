import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('ticket_number', models.CharField(max_length=20, unique=True, verbose_name='Номер читательского билета')),
                ('phone', models.CharField(max_length=20, unique=True, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('group', models.CharField(blank=True, max_length=20, verbose_name='Группа / класс')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('librarian', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='readers', to=settings.AUTH_USER_MODEL, verbose_name='Записал библиотекарь')),
            ],
            options={
                'verbose_name': 'Читатель',
                'verbose_name_plural': 'Читатели',
                'ordering': ['full_name'],
            },
        ),
    ]
