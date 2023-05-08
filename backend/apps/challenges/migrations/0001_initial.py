# Generated by Django 4.1.9 on 2023-05-08 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.challenge')),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.challenge')),
            ],
        ),
    ]
