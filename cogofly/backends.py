# coding=UTF-8
"""
Création de mon propre modèle d'authentification
https://docs.djangoproject.com/fr/1.8/topics/auth/customizing/
"""

from django.contrib.auth.models import User


class ModelBackendOnlyEmail(object):
    """
    Authentification uniquement par un e-mail.

    Utilise l'idée qu'on est bien authentifié par google ou facebook, donc
    seul l'email suffit pour être authentifié. Par contre, par mesure de
    sécurité, il faut passer, codé en dur, le mot de passe u'_.|._', exemple :

    email = 'cogofly@gmail.com'
    secure = u'_.|._'
    """
    def authenticate(self, username=None, email=None, secure=None):
        if username:
            return User.objects.get(username=username)
        return User.objects.get(email=email)

    # La classe qui teste si l'utilisateur est connecté envoie l'id du user.
    def get_user(self, key=None):
        try:
            return User.objects.get(id=key)
        except User.DoesNotExist:
            return None


