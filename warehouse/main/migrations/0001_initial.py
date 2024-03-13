# Generated by Django 5.0.2 on 2024-03-13 15:28

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=20)),
                ('brand_pic', models.ImageField(upload_to='media/')),
                ('add_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('surname', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('company', models.CharField(max_length=15)),
                ('add_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=20)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment', models.CharField(max_length=255)),
                ('amount', models.FloatField(max_length=200)),
                ('add_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('date', models.DateTimeField(auto_now=True)),
                ('dropzone', models.IntegerField()),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_photo', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('supplier_name', models.CharField(max_length=15)),
                ('supplier_surname', models.CharField(max_length=15)),
                ('supplier_email', models.EmailField(max_length=20)),
                ('supplier_phone', models.CharField(max_length=15)),
                ('supplier_address', models.CharField(max_length=50)),
                ('supplier_add_d', models.DateField(auto_now=True)),
                ('supplier_company_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UplodedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('upload_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='myUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('comp_name', models.CharField(max_length=20)),
                ('birth_date', models.DateField()),
                ('phone', models.CharField(max_length=15)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positions', models.CharField(max_length=20)),
                ('date', models.DateField(auto_now=True)),
                ('dep_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.departments')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=15)),
                ('buy', models.FloatField(max_length=100)),
                ('sell', models.FloatField(max_length=100)),
                ('quantity', models.IntegerField(verbose_name=100)),
                ('add_date', models.DateField(auto_now=True)),
                ('dropzone', models.IntegerField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.brand')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name=100)),
                ('add_date', models.DateField(auto_now_add=True)),
                ('tesdiq', models.IntegerField(default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.clients')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('surname', models.CharField(max_length=15)),
                ('birth_date', models.DateField()),
                ('photo', models.ImageField(upload_to='media/')),
                ('email', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('sallary', models.FloatField(max_length=20)),
                ('j_start_d', models.DateField()),
                ('pos_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.positions')),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('doc_num', models.IntegerField()),
                ('about', models.TextField()),
                ('dropzone', models.IntegerField()),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_name', models.CharField(max_length=50)),
                ('issue_date', models.DateTimeField(auto_now=True)),
                ('deadline', models.DateTimeField()),
                ('approve', models.IntegerField(default=0)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.staff')),
            ],
        ),
    ]
