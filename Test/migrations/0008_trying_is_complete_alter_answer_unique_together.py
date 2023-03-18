# Generated by Django 4.1.6 on 2023-03-17 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0007_trying_mark_percents_alter_answer_is_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='trying',
            name='is_complete',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('trying', 'question')},
        ),
    ]
