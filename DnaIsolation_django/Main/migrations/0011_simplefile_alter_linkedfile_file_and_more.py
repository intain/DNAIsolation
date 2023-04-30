# Generated by Django 4.2 on 2023-04-26 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_order_contractor'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
            ],
        ),
        migrations.AlterField(
            model_name='linkedfile',
            name='file',
            field=models.FileField(upload_to='attachments/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='material',
            name='action',
            field=models.CharField(choices=[('Dodanie', 'Dodanie'), ('Usunięcie', 'Usunięcie')], max_length=16),
        ),
        migrations.AlterField(
            model_name='material',
            name='unit',
            field=models.CharField(choices=[('Liczba reakcji', 'Liczba reakcji'), ('Zestaw', 'Zestaw')], max_length=16),
        ),
        migrations.AlterField(
            model_name='order',
            name='contractor',
            field=models.CharField(choices=[('Genomed', 'Genomed'), ('A&A', 'A&A')], max_length=16),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Oczekuje', 'Oczekuje'), ('Otrzymano', 'Otrzymano'), ('W realizacji', 'W realizacji'), ('Wysłano', 'Wysłano'), ('Zakończono', 'Zakończono'), ('Anulowano', 'Anulowano')], max_length=16),
        ),
    ]