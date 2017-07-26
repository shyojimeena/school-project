
from django.views.generic import TemplateView, ListView
from braces.views import SetHeadlineMixin



class HomeView(SetHeadlineMixin, TemplateView):
    template_name = 'index.html'
    headline = 'Welcome'


   