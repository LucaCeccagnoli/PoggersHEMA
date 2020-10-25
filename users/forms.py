from django_registration.forms import RegistrationForm
from users.models import CustomUser

# estensione del form di registrazione standar per adattarlo a utenti customizzati
class CustomUserForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = CustomUser