# Generated by Django 5.1.1 on 2025-01-30 19:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('goal', models.CharField(max_length=255)),
                ('experience_level', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diary_workout_plans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(max_length=255)),
                ('sets', models.IntegerField(default=3)),
                ('reps', models.IntegerField(default=10)),
                ('rest_time', models.IntegerField(default=90)),
                ('workout_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='diary.workoutplan')),
            ],
        ),
        migrations.CreateModel(
            name='DiaryEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('completed_exercises', models.JSONField(default=list)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workout_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary.workoutplan')),
            ],
        ),
    ]
