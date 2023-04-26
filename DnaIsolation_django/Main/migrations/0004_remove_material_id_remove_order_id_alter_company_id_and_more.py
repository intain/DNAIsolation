# Generated by Django 4.2 on 2023-04-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_alter_company_email_alter_company_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AlterField(
            model_name='company',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='material',
            name='number',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
