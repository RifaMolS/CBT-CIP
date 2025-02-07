from django.contrib import admin
from .models import registration

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'address', 'bio')  # You can customize the fields shown in the list
    search_fields = ('username', 'email')  # Allows you to search by these fields
    list_filter = ('phone_number',)  # Allows you to filter by phone number

admin.site.register(registration, RegistrationAdmin)



