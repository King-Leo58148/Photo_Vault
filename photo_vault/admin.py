from django.contrib import admin
from .models import Photo,Album,CustomUser

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title','user','album','private')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(private=False)
    
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('album_name',)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display= ('username','email','is_staff','is_superuser')