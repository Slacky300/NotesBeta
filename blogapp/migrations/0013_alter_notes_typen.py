# Generated by Django 4.1.7 on 2023-03-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0012_alter_notes_typen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='typeN',
            field=models.CharField(blank=True, choices=[('Assignment', 'Assignment'), ('Experiment', 'Experiment'), ('Notes', 'Notes'), ('ReferenceBook', 'Reference Book'), ('LectureSlides', 'Lecture Slides'), ('PYQ', 'PYQ'), ('Numericals', 'Numericals')], max_length=50, null=True),
        ),
    ]