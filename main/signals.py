from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from .models import Language, Initiative, Article, StaticTranslationFile, Video
import os
import json
from django.conf import settings


@receiver(post_migrate)
def create_default_language(sender, **kwargs):
    """ Создаёт украинский язык по умолчанию при первой миграции """
    if sender.name == 'main':  # Проверяем, что миграция относится к нашему приложению
        if not Language.objects.filter(code='uk').exists():
            Language.objects.create(code='uk', name='Українська')



@receiver(post_save, sender=Language)
def create_static_translation_file(sender, instance, created, **kwargs):
    """ Создаёт файл перевода для статического контента при добавлении нового языка """
    if created:  # Только если язык создан впервые
        translations_dir = os.path.join(settings.MEDIA_ROOT, "translations/static")
        os.makedirs(translations_dir, exist_ok=True)

        # Путь к файлу
        translation_file_path = os.path.join(translations_dir, f"static_{instance.code}.json")

        # Пример статического контента на украинском
        ukrainian_texts = {
            "Статті": "",
            "Ініціативи": "",
            "Головна": "",
            "Сайт": "",
            "П.І.Б.": "",
            "напр. Джон Картер": "",
            "Електронна пошта": "",
            "Телефон": "",
            "Компанія": "",
            "напр. Facebook": "",
            "Напишіть своє повідомлення...": "",
            "Повідомлення": "",
            "Надіслати повідомлення": "",
            "Звʼязатись": "",
            "Надішліть листа": "",
            "Слідкуйте за мною у соціальних медіа": "",
            "Посилення інновацій": "",
            "що резонують по світу": "",
            "Видатний розробник та засновник ECORA": "",
            "глобального інноваційного підприємства": "",
            "Моя непохитна прихильність інноваціям": "",
            "перетворює життя та створює нові стандарти": "",
            "для кращого, більш стійкого майбутнього": "",
            "Звʼяжіться": "",
            "Дізнатись більше": "",
            "Пацієнтів досліджено для визначення причин дисфункцій та покращення якості життя": "",
            "Років у бізнесі": "",
            "Публічних виступів як спікера, доповідача, науковця, розробника на інтер-національних заходах": "",
            "Імʼя": "",
            "Напишіть своє імʼя...": "",
            "Зачекайте...": "",
            "Надіслати": "",
            "Дізнайтеся, як спільна робота може створити майбутнє для всіх нас.": "",
            "Надішліть електронний лист": "",
            "Більше ініціатив": "",
            "Більше": "",
            "глобального інноваційного підприємства": "",
            "Розробник і засновник ECORA": "",
            "Дізнатися більше": "",
            "Під моїм керівництвом десять взаємопов&#x27;язаних підприємств працюють як одна згуртована екосистема, стимулюючи трансформаційні рішення, які покращують здоров&#x27;я та якість життя громад у всьому світі.": "",
            "Еко холдинг": "",
            "Відео спікер": "",
            "Знайдіть відео виступів спікера, що підходять для вашого заходу.": "",
            "Ваш браузер не підтримує відео.": "",
            "Ця сторінка поки пуста": ""

        }

        # Структура файла
        translation_content = {
            instance.code: ukrainian_texts
        }

        # Записываем файл
        with open(translation_file_path, 'w', encoding='utf-8') as f:
            json.dump(translation_content, f, ensure_ascii=False, indent=4)

        # Создаём запись в базе данных
        StaticTranslationFile.objects.create(language=instance, file=f"translations/static/static_{instance.code}.json")



@receiver(post_save, sender=Language)
def update_translation_files(sender, instance, **kwargs):
    """ Проверяет и добавляет новый язык в файлы переводов статей и инициатив """

    # Проверяем файлы инициатив
    for initiative in Initiative.objects.all():
        file_path = os.path.join(settings.MEDIA_ROOT, f"translations/initiatives/{initiative.id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = json.load(f)

            # Добавляем язык в список языков, если его нет
            if instance.code not in translations["languages"]:
                translations["languages"].append(instance.code)

            # Добавляем пустой перевод, если его нет
            if instance.code not in translations:
                translations[instance.code] = {
                    "type": "",
                    "short_description": "",
                    "full_description": ""
                }

            # Перезаписываем файл
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=4)

    # Проверяем файлы статей
    for article in Article.objects.all():
        file_path = os.path.join(settings.MEDIA_ROOT, f"translations/articles/{article.id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = json.load(f)

            # Добавляем язык в список языков, если его нет
            if instance.code not in translations["languages"]:
                translations["languages"].append(instance.code)

            # Добавляем пустой перевод, если его нет
            if instance.code not in translations:
                translations[instance.code] = {
                    "title": "",
                    "short_description": "",
                    "full_description": ""
                }

            # Перезаписываем файл
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=4)

    for video in Video.objects.all():
        file_path = os.path.join(settings.MEDIA_ROOT, f"translations/videos/{video.id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = json.load(f)
            if instance.code not in translations["languages"]:
                translations["languages"].append(instance.code)
            if instance.code not in translations:
                translations[instance.code] = {
                    "short_description": "",
                    "price": ""
                }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=4)
