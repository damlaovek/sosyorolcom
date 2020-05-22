# Generated by Django 3.0.6 on 2020-05-20 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sosyorol', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('user_name', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='WordsAndPhrases',
        ),
    ]
