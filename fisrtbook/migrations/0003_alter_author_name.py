# Generated by Django 5.0.6 on 2024-05-23 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fisrtbook', '0002_author_alter_book_title_book_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=220, null=True),
        ),
    ]
