# Generated by Django 4.2 on 2023-04-26 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0011_simplefile_alter_linkedfile_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.company'),
        ),
    ]
