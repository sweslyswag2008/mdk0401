import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        ('readers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_type', models.CharField(choices=[('home', 'На дом'), ('hall', 'В читальный зал'), ('reserve', 'Бронь')], max_length=20, verbose_name='Вид выдачи')),
                ('status', models.CharField(choices=[('new', 'Оформлена'), ('issued', 'Книга выдана'), ('returned', 'Возвращена'), ('cancelled', 'Отменена')], default='new', max_length=20, verbose_name='Статус')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Вернуть до')),
                ('fine', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Штраф, руб.')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Оформлена')),
                ('issued_at', models.DateTimeField(blank=True, null=True, verbose_name='Выдана')),
                ('returned_at', models.DateTimeField(blank=True, null=True, verbose_name='Возвращена')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loans', to='catalog.book', verbose_name='Книга')),
                ('librarian', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loans', to=settings.AUTH_USER_MODEL, verbose_name='Библиотекарь')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='readers.reader', verbose_name='Читатель')),
            ],
            options={
                'verbose_name': 'Выдача',
                'verbose_name_plural': 'Выдачи',
                'ordering': ['-created_at'],
            },
        ),
    ]
