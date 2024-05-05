# Generated by Django 4.2 on 2024-05-04 16:47

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('payment_method', models.CharField(choices=[('CREDIT_CARD', 'Credit Card'), ('PAYPAL', 'PayPal'), ('BANK_TRANSFER', 'Bank Transfer'), ('CASH_ON_DELIVERY', 'Cash on Delivery')], max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('payment_getway', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_status', models.CharField(choices=[('AUTHORIZED', 'Authorized'), ('CAPTURED', 'Captured'), ('FAILED', 'Failed'), ('REFUNDED', 'Refunded'), ('CANCELED', 'Canceled')], default='AUTHORIZED', max_length=20)),
                ('payment_amount', models.DecimalField(decimal_places=3, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('getway_response_raw', models.JSONField(blank=True, null=True)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='order.order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
