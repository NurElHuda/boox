# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import User, Book


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'date_joined',
        'created_at',
        'updated_at',
        'deleted_at',
        'name',
        'email',
        'facebook',
        'whatsapp',
        'messenger',
        'wilaya',
        'is_admin',
        'is_seller',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'created_at',
        'updated_at',
        'deleted_at',
        'is_admin',
        'is_seller',
    )
    raw_id_fields = ('groups', 'user_permissions')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'deleted_at',
        'seller',
        'title',
        'cover',
        'author_name',
        'wilaya',
        'price',
        'goodreads',
        'messenger',
        'whatsup',
    )
    list_filter = ('created_at', 'updated_at', 'deleted_at', 'seller')
    date_hierarchy = 'created_at'
