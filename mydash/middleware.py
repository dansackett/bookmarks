from django.conf import settings
from django.http import HttpResponseRedirect


class require_login(object):
    """
    Middleware that will check the request URL and detirmine if a user should
    be served that URL or if they will have to login first.

    """
    def process_request(self, request):
        if request.user.is_anonymous():
            if settings.DEBUG and self.is_media_url(request):
                return
            elif not self.is_public_url(request.path):
                return HttpResponseRedirect('/login/')
        else:
            if self.is_public_url(request.path):
                return HttpResponseRedirect('/account/')

    def is_public_url(self, url):
        public_urls = [
            '/',
            '/login/',
            '/register/',
        ]
        return url in public_urls

    def is_media_url(self, request):
        return request.path.startswith('/media/')
