from django.contrib import admin

from .models import User, Car, CarBrand, Company,  CarType, MultiImagesCar, Yacht

class MultiImagesAdmin(admin.StackedInline):
    model = MultiImagesCar

class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',  'brand', 'company', 'type', 'count_images')
    inlines = [MultiImagesAdmin]
    class Meta:
        model = Car

class YachtAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'capacity', 'feet', 'price_per_hour')
    class Meta:
        model = Yacht

class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'phone')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' )

admin.site.register(Car, CarAdmin)
admin.site.register(Yacht, YachtAdmin)
admin.site.register(MultiImagesCar)
admin.site.register(Company, CompanyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(CarBrand, CarBrandAdmin)
admin.site.register(CarType, CarTypeAdmin)