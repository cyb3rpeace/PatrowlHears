# Generated by Django 3.0.6 on 2020-05-12 14:31

import cves.models
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bulletin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publicid', models.CharField(default='', max_length=250, null=True)),
                ('vendor', models.CharField(default='', max_length=250, null=True)),
                ('title', models.CharField(default='', max_length=250, null=True)),
                ('severity', models.CharField(default='', max_length=250, null=True)),
                ('impact', models.CharField(default='', max_length=250, null=True)),
                ('published', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('monitored', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'kb_bulletin',
            },
        ),
        migrations.CreateModel(
            name='CPE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('vector', models.CharField(default='', max_length=250, null=True)),
                ('vulnerable_products', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250), null=True, size=None)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'kb_cpe',
            },
        ),
        migrations.CreateModel(
            name='CVE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cve_id', models.CharField(max_length=20, null=True, unique=True)),
                ('summary', models.TextField(default='')),
                ('published', models.DateTimeField(null=True)),
                ('modified', models.DateTimeField(null=True)),
                ('assigner', models.CharField(max_length=50, null=True)),
                ('cvss', models.FloatField(default=0.0, null=True)),
                ('cvss_time', models.DateTimeField(null=True)),
                ('cvss_vector', models.CharField(max_length=250, null=True)),
                ('access', django.contrib.postgres.fields.jsonb.JSONField(default=cves.models.access_default_dict)),
                ('impact', django.contrib.postgres.fields.jsonb.JSONField(default=cves.models.impact_default_dict)),
                ('vulnerable_products', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250), null=True, size=None)),
                ('references', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('monitored', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'kb_cve',
            },
        ),
        migrations.CreateModel(
            name='CWE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cwe_id', models.CharField(max_length=20, null=True, unique=True)),
                ('name', models.CharField(max_length=250, null=True)),
                ('description', models.TextField(default='')),
            ],
            options={
                'db_table': 'kb_cwe',
            },
        ),
        migrations.CreateModel(
            name='HistoricalBulletin',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('publicid', models.CharField(default='', max_length=250, null=True)),
                ('vendor', models.CharField(default='', max_length=250, null=True)),
                ('title', models.CharField(default='', max_length=250, null=True)),
                ('severity', models.CharField(default='', max_length=250, null=True)),
                ('impact', models.CharField(default='', max_length=250, null=True)),
                ('published', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('monitored', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical bulletin',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCPE',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('vector', models.CharField(default='', max_length=250, null=True)),
                ('vulnerable_products', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250), null=True, size=None)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical cpe',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.TextField(default='-', max_length=250)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical product',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProductVersion',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('version', models.TextField(default='*', max_length=250)),
                ('vector', models.CharField(default='', max_length=250, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical product version',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalVendor',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.TextField(db_index=True, default='-', max_length=250)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical vendor',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='-', max_length=250)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'kb_product',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='-', max_length=250, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'kb_vendor',
            },
        ),
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.TextField(default='*', max_length=250)),
                ('vector', models.CharField(default='', max_length=250, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cves.Product')),
            ],
            options={
                'db_table': 'kb_product_version',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cves.Vendor'),
        ),
    ]
