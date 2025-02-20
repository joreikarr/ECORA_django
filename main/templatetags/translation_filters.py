import json
from django import template
from django.conf import settings
from main.models import StaticTranslationFile

register = template.Library()

# Кеш для загрузки файлов переводов
_translation_cache = {}

def load_translations(lang_code):
    """ Загружает переводы статического контента из модели, а не из файловой системы """
    try:
        static_translation = StaticTranslationFile.objects.get(language__code=lang_code)
        file_path = static_translation.file.path

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f).get(lang_code, {})

    except (StaticTranslationFile.DoesNotExist, FileNotFoundError, json.JSONDecodeError):
        return {}

@register.simple_tag(takes_context=True)
def translate(context, text):
    """ Переводит статический текст, загружая переводы из модели """
    lang_code = context.request.session.get('language', 'uk')

    if lang_code not in _translation_cache:
        _translation_cache[lang_code] = load_translations(lang_code)

    translations = _translation_cache.get(lang_code, {})
    return translations.get(text, text)  # Если перевода нет, вернуть оригинальный текст
