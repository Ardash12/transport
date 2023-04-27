from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

#Note: We are renaming the original Admin and Form as we import them!
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from django import forms

from . import models


class FlatpageForm(FlatpageFormOld):
#   content = forms.CharField(widget=CKEditorWidget())
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = FlatPage
        fields = '__all__'
    
class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(models.Order)
admin.site.register(models.City)
admin.site.register(models.Client)
admin.site.register(models.Banner)
admin.site.register(models.ShippingRates)
admin.site.register(models.Insurance)
admin.site.register(models.CityDeliveryRates)
admin.site.register(models.DeliveryTime)
admin.site.register(models.News)
admin.site.register(models.Advantages)
admin.site.register(models.TextIndex)
