#mixin login required limita l'accesso ai soli utenti utenticati (non serve qui)
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from users.forms import LoginForm

class IndexTemplateView(TemplateView):

    def get_template_names(self):
        template_name = "index.html"
        return template_name




