# Generated by Django 5.0.6 on 2024-05-24 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fisrtbook', '0003_alter_author_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default=1234, upload_to='bookmedia'),
            preserve_default=False,
        ),
    ]
