from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=10)),
                ('captured_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_records', to='products.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_records', to='stores.store')),
            ],
            options={
                'ordering': ['-captured_at'],
                'unique_together': {('product', 'store', 'captured_at')},
            },
        ),
    ]
