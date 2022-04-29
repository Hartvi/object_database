# Generated by Django 3.2.12 on 2022-03-04 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoricalProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('repository', models.URLField()),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('png', models.ImageField(upload_to='uploads/measurements/')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='ObjectInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_instance', models.BooleanField(default=True)),
                ('instance_id', models.IntegerField()),
                ('dataset', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('entry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='property', to='database.entry')),
            ],
        ),
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vector3D',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SizeProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='size', to='database.property')),
            ],
        ),
        migrations.CreateModel(
            name='SetupElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('output_quantities', models.JSONField()),
                ('parameters', models.JSONField()),
                ('setup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='setup_elements', to='database.setup')),
            ],
        ),
        migrations.CreateModel(
            name='SensorOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_output', models.JSONField()),
                ('measurement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_outputs', to='database.measurement')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor_outputs', to='database.setupelement')),
            ],
        ),
        migrations.CreateModel(
            name='OtherProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('other', models.JSONField()),
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='other', to='database.property')),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='object_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='database.objectinstance'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='measurements', related_query_name='measurement', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='measurement',
            name='setup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', related_query_name='measurement', to='database.setup'),
        ),
        migrations.CreateModel(
            name='Grasp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grasped', models.BooleanField()),
                ('measurement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='grasp', to='database.measurement')),
                ('rotation', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='rotation', to='database.vector3d')),
                ('translation', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='translation', to='database.vector3d')),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='measurement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', related_query_name='entry', to='database.measurement'),
        ),
        migrations.AddField(
            model_name='entry',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entries', related_query_name='entry', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ContinuousProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(choices=[('MASS', 'mass'), ('VOLUME', 'volume'), ('DENSITY', 'density'), ('STIFFNESS', 'stiffness'), ('YOUNGS_MODULUS', 'youngs_modulus'), ('XDIM', 'xdim'), ('YDIM', 'ydim'), ('ZDIM', 'zdim'), ('TABLEFRICTION', 'tablefriction'), ('MATERIAL', 'material'), ('MODEL', 'model')], max_length=100)),
                ('value', models.FloatField()),
                ('std', models.FloatField()),
                ('units', models.CharField(choices=[('G', 'g'), ('KG', 'kg'), ('M3', 'm^3'), ('DM3', 'dm^3'), ('CM3', 'cm^3'), ('MM3', 'mm^3'), ('GCM_3', 'g cm^-3'), ('KGM_3', 'kg m^-3'), ('M', 'm'), ('DM', 'dm'), ('CM', 'cm'), ('MM', 'mm')], max_length=100)),
                ('other', models.JSONField(null=True)),
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='continuous', to='database.property')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('probability', models.FloatField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='database.categoricalproperty')),
            ],
        ),
        migrations.AddField(
            model_name='categoricalproperty',
            name='property',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='categorical', to='database.property'),
        ),
    ]