# Generated by Django 5.0.6 on 2024-05-31 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fisrtbook', '0006_delete_logintable_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(default=1234),
            preserve_default=False,
        ),
    ]