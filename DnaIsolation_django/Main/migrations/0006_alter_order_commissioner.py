# Generated by Django 4.2 on 2023-04-25 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_alter_company_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='commissioner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.company'),
        ),
    ]
