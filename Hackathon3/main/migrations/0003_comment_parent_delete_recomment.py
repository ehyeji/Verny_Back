# Generated by Django 4.2 on 2023-08-08 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_comment_author_alter_post_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relply', to='main.comment'),
        ),
        migrations.DeleteModel(
            name='Recomment',
        ),
    ]
