# Generated by Django 3.2.5 on 2021-12-08 20:41

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='product',
            name='body',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]