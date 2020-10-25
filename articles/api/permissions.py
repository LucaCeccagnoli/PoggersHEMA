from rest_framework import permissions

# restituisce true se l'utente è amministratore o sta solo effettuando una richiesta get (metodo safe)
class IsAdminUserOrReadonly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin