# Generated by Django 5.0 on 2024-03-24 09:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('books', 'Books'), ('kitchen_appliances', 'Kitchen Appliances'), ('electronics', 'Electronics'), ('clothing', 'Clothing'), ('home_decor', 'Home Decor'), ('toys', 'Toys'), ('sports_equipment', 'Sports Equipment'), ('beauty_products', 'Beauty Products'), ('health_products', 'Health Products'), ('pet_supplies', 'Pet Supplies')], max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField()),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('discount', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expire_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('promo_code', models.CharField(blank=True, max_length=20, unique=True)),
                ('products', models.ManyToManyField(related_name='offers', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='product_images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
        ),
    ]
