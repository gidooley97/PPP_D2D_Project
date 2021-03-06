# Generated by Django 3.0.2 on 2020-02-11 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20200204_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, default='2.00', max_digits=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='book_formats',
            field=models.CharField(max_length=60),
        ),
    ]
