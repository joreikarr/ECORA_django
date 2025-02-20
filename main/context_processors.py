from .models import Language

def available_languages(request):
    return {'available_languages': Language.objects.all()}
