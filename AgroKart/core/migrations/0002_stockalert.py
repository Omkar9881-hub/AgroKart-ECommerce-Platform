# Generated manually for StockAlert model

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_type', models.CharField(choices=[('low_stock', 'Low Stock'), ('out_of_stock', 'Out of Stock'), ('critical_stock', 'Critical Stock')], default='low_stock', max_length=20)),
                ('message', models.TextField()),
                ('stock_quantity', models.IntegerField()),
                ('is_read', models.BooleanField(default=False)),
                ('is_resolved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_alerts', to='core.product')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='is_low_stock',
            field=models.BooleanField(default=False),
        ),
    ] 