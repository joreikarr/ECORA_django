from django.db import models
import json
import os
from django.conf import settings

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Код мови")
    name = models.CharField(max_length=100, verbose_name="Назваяв")


    class Meta:
        verbose_name = "Мова"
        verbose_name_plural = "Мови"

    def __str__(self):
        return self.name


class StaticTranslationFile(models.Model):
    language = models.OneToOneField(Language, on_delete=models.CASCADE, verbose_name="Мова")
    file = models.FileField(upload_to="translations/static/", verbose_name="Файл перекладу")

    class Meta:
        verbose_name = "Статичний файл перекладу"
        verbose_name_plural = "Статичні файли перекладу"


    def __str__(self):
        return f"Переклад для {self.language.name}"




class Initiative(models.Model):
    type = models.CharField(max_length=255, verbose_name="Тип")
    name = models.CharField(max_length=255, verbose_name="Назва")
    logo = models.ImageField(upload_to='initiatives/logos/', verbose_name="Логотип")
    background = models.ImageField(upload_to='initiatives/backgrounds/', verbose_name="Фонове зображення")
    short_description = models.TextField(verbose_name="Короткий опис")
    full_description = models.TextField(verbose_name="Повний опис")
    translation_file = models.FileField(upload_to="translations/initiatives/", blank=True, null=True, verbose_name="Файл перекладу")

    class Meta:
        verbose_name = "Ініціатива"
        verbose_name_plural = "Ініціативи"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_translation_file()

    def get_translation(self, lang_code):
        if not self.translation_file:
            return {
                "type": self.type,
                "short_description": self.short_description,
                "full_description": self.full_description,
            }

        file_path = os.path.join(settings.MEDIA_ROOT, self.translation_file.name)
        with open(file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)

        if lang_code in translations:
            return translations[lang_code]
        return translations["uk"]

    def create_translation_file(self):
        # Проверяем существование директории
        initiatives_dir = os.path.join(settings.MEDIA_ROOT, "translations/initiatives")
        os.makedirs(initiatives_dir, exist_ok=True)

        # Генерируем путь к файлу
        file_path = os.path.join(initiatives_dir, f"{self.id}.json")
        languages = Language.objects.all()

        # Создаём структуру перевода
        translations = {"languages": [lang.code for lang in languages]}
        translations["uk"] = {
            "type": self.type,
            "short_description": self.short_description,
            "full_description": self.full_description
        }

        for lang in languages:
            if lang.code != "uk":
                translations.setdefault(lang.code, {
                    "type": "",
                    "short_description": "",
                    "full_description": ""
                })

        # Сохраняем JSON файл
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=4)

        # Сохраняем путь к файлу в модели
        self.translation_file = f"translations/initiatives/{self.id}.json"
        super().save(update_fields=["translation_file"])

class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    image = models.ImageField(upload_to='articles/images/', verbose_name="Зображення")
    short_description = models.TextField(verbose_name="Короткий опис")
    source_link = models.URLField(verbose_name="Посилання на джерело")
    translation_file = models.FileField(upload_to="translations/articles/", blank=True, null=True, verbose_name="Файл перекладу")

    class Meta:
        verbose_name = "Стаття"
        verbose_name_plural = "Статті"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_translation_file()

    def get_translation(self, lang_code):
        if not self.translation_file:
            return {
                "title": self.title,
                "short_description": self.short_description,
            }

        file_path = os.path.join(settings.MEDIA_ROOT, self.translation_file.name)
        with open(file_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)

        if lang_code in translations:
            return translations[lang_code]
        return translations["uk"]

    def create_translation_file(self):
        # Проверяем существование директории
        articles_dir = os.path.join(settings.MEDIA_ROOT, "translations/articles")
        os.makedirs(articles_dir, exist_ok=True)

        # Генерируем путь к файлу
        file_path = os.path.join(articles_dir, f"{self.id}.json")
        languages = Language.objects.all()

        # Создаём структуру перевода
        translations = {"languages": [lang.code for lang in languages]}
        translations["uk"] = {
            "title": self.title,
            "short_description": self.short_description,
        }

        for lang in languages:
            if lang.code != "uk":
                translations.setdefault(lang.code, {
                    "title": "",
                    "short_description": "",
                })

        # Сохраняем JSON файл
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=4)

        # Сохраняем путь к файлу в модели
        self.translation_file = f"translations/articles/{self.id}.json"
        super().save(update_fields=["translation_file"])
