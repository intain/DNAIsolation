# Generated by Django 4.2 on 2023-04-25 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_alter_order_commissioner'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='files',
            field=models.FileField(null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='contractor',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=16),
        ),
        migrations.CreateModel(
            name='LinkedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.order')),
            ],
        ),
    ]
