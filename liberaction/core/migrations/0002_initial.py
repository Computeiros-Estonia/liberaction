# Generated by Django 4.0 on 2022-01-19 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user', verbose_name='usuário'),
        ),
        migrations.AddField(
            model_name='product',
            name='base',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.baseproduct'),
        ),
        migrations.AddField(
            model_name='picture',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.album'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='fornecedor'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='tags',
            field=models.ManyToManyField(to='core.Tag'),
        ),
        migrations.AddField(
            model_name='album',
            name='base_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.baseproduct', verbose_name='produto'),
        ),
    ]
