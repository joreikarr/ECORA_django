from django.contrib import admin
from django.http import HttpResponse
import os
from django.conf import settings
from .models import Initiative, Article, Language, StaticTranslationFile
from django.utils.html import format_html

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code")

@admin.register(StaticTranslationFile)
class StaticTranslationFileAdmin(admin.ModelAdmin):
    list_display = ("language", "file", "download_file")

    def download_file(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}">Завантажити</a>',
                f'/admin/main/statictranslationfile/download/{obj.id}/'
            )
        return "Нет файла"
    download_file.short_description = "Завантажити файл"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('download/<int:file_id>/', self.download_static_file, name="download_static_file"),
        ]
        return custom_urls + urls



    def download_static_file(self, request, file_id):
        obj = StaticTranslationFile.objects.get(id=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, obj.file.name)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response

@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "download_translation")

    def download_translation(self, obj):
        if obj.translation_file:
            return format_html(
                '<a href="{}">Завантажити</a>',
                f'/admin/main/initiative/download/{obj.id}/'
            )
        return "Нет файла"
    download_translation.short_description = "Завантажити файл"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('download/<int:obj_id>/', self.download_translation_file, name="download_initiative_translation"),
        ]
        return custom_urls + urls

    def download_translation_file(self, request, obj_id):
        obj = Initiative.objects.get(id=obj_id)
        file_path = os.path.join(settings.MEDIA_ROOT, obj.translation_file.name)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "download_translation")

    def download_translation(self, obj):
        if obj.translation_file:
            return format_html(
                '<a href="{}">Завантажити</a>',
                f'/admin/main/article/download/{obj.id}/'
            )
        return "Нет файла"
    download_translation.short_description = "Завантажити файл"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('download/<int:obj_id>/', self.download_translation_file, name="download_article_translation"),
        ]
        return custom_urls + urls

    def download_translation_file(self, request, obj_id):
        obj = Article.objects.get(id=obj_id)
        file_path = os.path.join(settings.MEDIA_ROOT, obj.translation_file.name)
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
