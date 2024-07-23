from django.contrib import admin
from banking import models
# Register your models here.
admin.site.register(models.UserProfiles)
admin.site.register(models.Account)
admin.site.register(models.Transactions)
