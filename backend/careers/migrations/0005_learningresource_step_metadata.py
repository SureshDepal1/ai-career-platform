from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careers', '0005_career_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningresource',
            name='expected_outcome',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='learningresource',
            name='learning_objectives',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='learningresource',
            name='phase',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='learningresource',
            name='practice_project',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
