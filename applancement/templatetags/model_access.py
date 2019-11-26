# coding=UTF-8
"""
Plusieurs fonctions pour accéder aux modèles. Ce n'est pas très "propre",
mais c'est pratique, ça fonctionne bien et ça reste tout à fait maintenable.
"""


from django import template

from app.forms.personne_invitation_accept import PersonneInvitationAcceptForm
from app.forms.personne_invitation_refuse import PersonneInvitationRefuseForm

register = template.Library()


@register.filter(name='type_of_relation_with')
def type_of_relation_with(arg1, arg2):
    """
    chercher si arg1 est lié à arg2 via PersonneRelation
    Args:
        arg2: une entité de type Personne
        arg1: une entité de type Personne
    """
    return arg1.type_of_relation_with(arg2)


@register.filter(name='type_of_relation_you')
def type_of_relation_you(arg1, arg2):
    """
    Si arg1 est lié à arg2 via PersonneRelation, et renvoie une description
    du type "Vous êtes ami avec YY" au lieu de "XX est ami avec YY"
    Args:
        arg2: une entité de type Personne
        arg1: une entité de type Personne
    """
    return arg1.type_of_relation_you(arg2)


@register.filter(name='type_of_relation_you_short')
def type_of_relation_you_short(arg1, arg2):
    """
    Si arg1 est lié à arg2 via PersonneRelation, et renvoie une description
    du type "Vous êtes ami avec YY" au lieu de "XX est ami avec YY"
    Args:
        arg2: une entité de type Personne
        arg1: une entité de type Personne
    """
    return arg1.type_of_relation_you_short(arg2)


@register.filter(name='can_remove_relation')
def can_remove_relation(arg1, arg2):
    """
    Si arg1 est lié à arg2 via PersonneRelation renvoie si on peut supprimer
    cette relation (True) ou si cette relation n'est pas changeable
    (en cours d'attente acceptation/refus, ou déjà refusée)
    Args:
        arg2: une entité de type Personne
        arg1: une entité de type Personne
    """
    return arg1.can_remove_relation(arg2)


@register.filter(name='make_form_invitation_refuse')
def make_form_invitation_refuse(arg):
    return PersonneInvitationRefuseForm(obj_bd=arg, champ='id_personne_refused')


@register.filter(name='make_form_invitation_accept')
def make_form_invitation_accept(arg):
    return PersonneInvitationAcceptForm(obj_bd=arg, champ='id_personne_accept')


@register.filter(name='first_person_who_is_not')
def first_person_who_is_not(arg1, arg2):
    """
      J'avais un problème avec l'affichage d'une conversation basique :
      - il fallait que j'aille rechercher la fiche de l'AUTRE personne, et
        que je l'affiche
      - *pendant* que je l'affiche = DANS le template, il fallait que je
        ressorte :
        - les messages non lus
        - l'historique au complet, avec les messages non lus
      J'ai donc crée quelques fonctions utilitaires qui ne concernent que les
      conversations.
    Args:
        arg1: objet de type Conversation
        arg2: objet de type Personne

    Returns:
        Objet de type Personne
    """
    return arg1.first_person_who_is_not(arg2)


@register.filter(name='messages_unread_written_by')
def messages_unread_written_by(arg1, arg2):
    """
    Voir très long commentaire sur les fonctions utilitaires pour afficher
    les conversations, au dessus.
    Args:
        arg1: objet de type Conversation
        arg2: objet de type Personne

    Returns:
        Tableau de messages de type Message
    """
    return arg1.messages_unread_written_by(arg2)


@register.filter(name='persons_who_shared_this_to')
def persons_who_shared_this_to(arg1, arg2):
    """
    Voir si l'activité est partagée à une personne (-> sur le mur, on affiche
    si l'activité a été partagée par un de nos amis)
    Args:
        arg1: objet de type Activite
        arg2: objet de type Personne

    Returns:
        Boolean
    """
    return arg1.persons_who_shared_this_to(arg2)


@register.filter(name='person_who_shared_this_is')
def person_who_shared_this_is(arg1, arg2):
    """
    Voir si l'activité est partagé par une personne (-> sur le mur, on affiche
    si l'activité a été partagée par un de nos amis ou vice-versa)
    Args:
        arg1: objet de type Activite
        arg2: objet de type Personne

    Returns:
        Boolean
    """
    return arg1.person_who_shared_this_is(arg2)


@register.filter(name='description_with_tag')
def description_with_tag(arg1, arg2):
    """
    Avant, les like étaient affichés genre :
    Il y a un jour, Xxx a aimé "28 février 2016, blabla"
    Mais Franck a voulu mettre en gras la personne concernée, du genre :
    Il y a un jour, <strong>Xxx</strong> a aimé "28 février 2016, blabla"
    J'ai dû créer ce tag dans le template pour faire passer le tag qui se
    met autour de personne
    Args:
        arg1: objet de type PersonneLike ou PersonneRelation (ils implémentent
              tous les deux "description()" de la même manière)
        arg2: objet de type String = tag

    Returns:
        Description de la personne
    """
    return arg1.description(arg2)


@register.filter(name='can_see_informations_of')
def can_see_informations_of(arg1, arg2):
    """
    Voir si les informations qu'une personne essaie de voir sont autorisées par
    l'autre. Rappel : visibilité = tout le monde, mes amis ou moi uniquement
    Args:
        arg1: objet de type Personne
        arg2: objet de type Personne

    Returns:
        Boolean
    """
    return arg1.can_see_informations_of(arg2)

