from django.contrib import admin
from app import models

class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'property_type', 'creation_date')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')

class LeaseContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'owner', 'tenant')
    list_display_links = ('id',)
    search_fields = ('property',)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_real_estate', 'order')
    list_display_links = ('id',)
    search_fields = ('id',)

class MaillingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email')
    list_display_links = ('id',)
    search_fields = ('user', 'email')

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property')
    list_display_links = ('id',)
    search_fields = ('user', 'property')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'content')
    list_display_links = ('id',)
    search_fields = ('user', 'email')

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'comment')
    list_display_links = ('id',)
    search_fields = ('user',)

admin.site.register(models.RealEstate, RealEstateAdmin)
admin.site.register(models.LeaseContract, LeaseContractAdmin)
admin.site.register(models.Photo, PhotoAdmin)
admin.site.register(models.Notifications)
admin.site.register(models.Mailling, MaillingAdmin)
admin.site.register(models.Favorites, FavoritesAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Reviews,  ReviewsAdmin)
