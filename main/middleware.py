from django.utils.translation import activate

class ForceAdminLanguageMiddleware:
    """ Принудительно устанавливает украинский язык в админке Django """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            activate('uk')
        return self.get_response(request)



