# Generated by Django 4.0.5 on 2022-06-23 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='활성화 여부'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0, verbose_name='가격'),
        ),
        migrations.AddField(
            model_name='product',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='수정일자'),
        ),
    ]
