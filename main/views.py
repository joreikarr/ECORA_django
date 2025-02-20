from django.shortcuts import render, redirect, get_object_or_404
from .models import Initiative, Article, Language


def home(request):
    lang_code = request.session.get('language', 'uk')
    initiatives = Initiative.objects.all()
    translated_initiatives = [
        {"id": i.id, "name": i.name, "logo": i.logo, "translated": i.get_translation(lang_code)} for i in initiatives
    ]
    return render(request, 'home.html', {'initiatives': translated_initiatives})


def initiatives(request):
    lang_code = request.session.get('language', 'uk')
    initiatives = Initiative.objects.all()
    translated_initiatives = [
        {"id": i.id, "name": i.name, "logo": i.logo, "translated": i.get_translation(lang_code)} for i in initiatives
    ]
    return render(request, 'initiatives.html', {'initiatives': translated_initiatives})


def initiative_detail(request, initiative_id):
    lang_code = request.session.get('language', 'uk')
    initiative = get_object_or_404(Initiative, id=initiative_id)
    translated_data = \
        {"id": initiative.id, "background": initiative.background, "name": initiative.name, "logo": initiative.logo,
         "translated": initiative.get_translation(lang_code)}
    related_initiatives = Initiative.objects.exclude(id=initiative_id)[:3]
    translated_related = [
        {"id": i.id, "name": i.name, "logo": i.logo, "translated": i.get_translation(lang_code)} for i in
        related_initiatives
    ]

    context = {
        'initiative': translated_data,
        'related_initiatives': translated_related,
    }
    return render(request, 'initiative_detail.html', context)


def articles(request):
    lang_code = request.session.get('language', 'uk')
    articles = Article.objects.all()
    translated_articles = [
        {"name": a.title, "image": a.image, "source_link": a.source_link,
         "translated": a.get_translation(lang_code)} for a in articles
    ]
    return render(request, 'articles.html', {'articles': translated_articles})


def change_language(request):
    if request.method == "POST":
        lang_code = request.POST.get('language', 'uk')
        if Language.objects.filter(code=lang_code).exists():
            request.session['language'] = lang_code
    return redirect(request.META.get('HTTP_REFERER', '/'))


def contact(request):
    return render(request, 'contact.html', )
