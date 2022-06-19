# Generated by Django 3.2.13 on 2022-06-14 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('awardsapp', '0002_projects'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'ordering': ['-pub_date']},
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('usability', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('content', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('design_average', models.FloatField(default=0)),
                ('usability_average', models.FloatField(default=0)),
                ('content_average', models.FloatField(default=0)),
                ('average_rating', models.FloatField(default=0)),
                ('projects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='awardsapp.projects')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='awardsapp.profile')),
            ],
        ),
    ]
