from django.contrib import admin

from django.contrib.auth import get_user_model

from .models import Asset, AssetOwnerHistory, AssetType

admin.site.register(get_user_model())
admin.site.register(Asset)
admin.site.register(AssetType)
admin.site.register(AssetOwnerHistory)
