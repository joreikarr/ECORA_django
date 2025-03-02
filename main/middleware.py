from django.utils.translation import activate

class ForceAdminLanguageMiddleware:
    """ Принудительно устанавливает украинский язык в админке Django """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            activate('uk')
        return self.get_response(request)


class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]  # удаляем порт, если он есть
        parts = host.split('.')
        # Если домен вида subdomain.domain.tld (как минимум 3 части)
        if len(parts) > 2:
            request.subdomain = parts[0]
        else:
            request.subdomain = None
        return self.get_response(request)
