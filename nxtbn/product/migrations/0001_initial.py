# Generated by Django 4.2 on 2024-04-27 09:25

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import nxtbn.core.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filemanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='collection_images/')),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('is_live', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('summary', models.TextField(max_length=500)),
                ('description', models.TextField(max_length=500)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(choices=[('SIMPLE_PRODUCT', 'Simple Product'), ('GROUPED_PRODUCT', 'Services'), ('EXTERNAL_PRODUCT', 'External/Affiliate Product'), ('VARIABLE_PRODUCT', 'Variables Product'), ('SIMPLE_SUBSCRIPTION', 'Simple Subscription'), ('VARIABLE_SUBSCRIPTION', 'Variables Subscription'), ('PRODUCT_BUNDLE', 'Product Bundle')], default='SIMPLE_PRODUCT', max_length=25)),
                ('subscribable', models.BooleanField(default=True, verbose_name='Subscribable')),
                ('currency', models.CharField(default='USD', max_length=10, verbose_name='Currency')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category')),
                ('collections', models.ManyToManyField(blank=True, related_name='products_in_collection', to='product.collection')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, nxtbn.core.models.SEOMixin),
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('compare_at_price', models.DecimalField(decimal_places=3, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('price', models.DecimalField(decimal_places=3, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('cost_per_unit', models.DecimalField(decimal_places=3, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('track_inventory', models.BooleanField(default=True)),
                ('stock', models.IntegerField(default=0, verbose_name='Stock')),
                ('low_stock_threshold', models.IntegerField(default=0, verbose_name='Stock')),
                ('stock_status', models.CharField(choices=[('IN_STOCK', 'In Stock'), ('OUT_OF_STOCK', 'Out of Stock')], default='IN_STOCK', max_length=15)),
                ('sku', models.CharField(max_length=50, unique=True)),
                ('weight_unit', models.CharField(blank=True, choices=[('GRAM', 'Gram'), ('KG', 'Kilogram'), ('LB', 'Pound'), ('OZ', 'Ounce'), ('TON', 'Ton')], max_length=5, null=True)),
                ('weight_value', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='product.product')),
                ('variant_image', models.ManyToManyField(blank=True, to='filemanager.image')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
