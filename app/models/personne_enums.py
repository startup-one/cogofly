# coding=UTF-8


from django.utils.translation import ugettext_lazy as _


class PersonneEnums(object):

    VISIBILITE_TOUT_LE_MONDE = 1
    VISIBILITE_MES_AMIS = 2
    VISIBILITE_QUE_MOI = 3
    TAB_VISIBILITE = {
        VISIBILITE_TOUT_LE_MONDE: _("Everyone can see those informations"),
        VISIBILITE_MES_AMIS: _("Only my friends can see those informations"),
        VISIBILITE_QUE_MOI: _("Only me can see those informations"),
    }

    AGE_ENTRE_18_ET_25 = 1
    AGE_ENTRE_26_ET_35 = 2
    AGE_ENTRE_36_ET_45 = 3
    AGE_ENTRE_46_ET_55 = 4
    AGE_ENTRE_56_ET_PLUS = 5
    TAB_AGE = {
        AGE_ENTRE_18_ET_25: _("Between 18 and 25"),
        AGE_ENTRE_26_ET_35: _("Between 26 and 35"),
        AGE_ENTRE_36_ET_45: _("Between 36 and 45"),
        AGE_ENTRE_46_ET_55: _("Between 46 and 55"),
        AGE_ENTRE_56_ET_PLUS: _("56 and more"),
    }
    TAB_AGE_ECART = {
        AGE_ENTRE_18_ET_25:   {'min': 18, 'max': 25},
        AGE_ENTRE_26_ET_35:   {'min': 26, 'max': 35},
        AGE_ENTRE_36_ET_45:   {'min': 36, 'max': 45},
        AGE_ENTRE_46_ET_55:   {'min': 46, 'max': 55},
        AGE_ENTRE_56_ET_PLUS: {'min': 56, 'max': -1},
    }

    INVITATION_REFUS_NON = 1
    INVITATION_REFUS_NON_MERCI = 2
    INVITATION_REFUS_UNE_AUTRE_FOIS = 3
    INVITATION_REFUS_PAS_INTERESSE_JE = 4
    INVITATION_REFUS_PAS_INTERESSE_NOUS = 5
    INVITATION_REFUS_PAS_INTERESSE_MAINTENANT_JE = 6
    INVITATION_REFUS_PAS_INTERESSE_MAINTENANT_NOUS = 7
    INVITATION_REFUS_VOYAGE_PAS_JE = 8
    INVITATION_REFUS_VOYAGE_PAS_NOUS = 9
    INVITATION_REFUS_DEPLACE_PAS_JE = 10
    INVITATION_REFUS_DEPLACE_PAS_NOUS = 11
    INVITATION_REFUS_SOUHAITE_RESTER_SEUL_JE = 12
    INVITATION_REFUS_SOUHAITE_RESTER_SEUL_NOUS = 13
    INVITATION_REFUS_AUCUN_PROJET_VOYAGE_EN_COMMUN_NOUS = 14
    INVITATION_REFUS_AUCUN_PROJET_SORTIE_EN_COMMUN_NOUS = 15
    INVITATION_REFUS_AUCUN_PROJET_ACTIVITE_EN_COMMUN_NOUS = 16
    INVITATION_REFUS_PARLE_PAS_VOTRE_LANGUE_JE = 17
    INVITATION_REFUS_PARLE_PAS_VOTRE_LANGUE_NOUS = 18
    INVITATION_REFUS_PARLE_PAS_ANGLAIS_JE = 19
    INVITATION_REFUS_PARLE_PAS_ANGLAIS_NOUS = 20
    INVITATION_REFUS_UTILISER_MES_CONTACTS_JE = 21
    INVITATION_REFUS_UTILISER_MES_CONTACTS_NOUS = 22
    INVITATION_REFUS_CONTACTER_UNE_AUTRE_PERSONNE_JE = 23
    INVITATION_REFUS_CONTACTER_UNE_AUTRE_PERSONNE_NOUS = 24
    INVITATION_REFUS_CONTACTER_MESSAGE_JE = 25
    INVITATION_REFUS_CONTACTER_MESSAGE_NOUS = 26

    TAB_INVITATION = {
        INVITATION_REFUS_NON:
            _("No"),
        INVITATION_REFUS_NON_MERCI:
            _("No thank you"),
        INVITATION_REFUS_UNE_AUTRE_FOIS:
            _("Maybe another time"),
        INVITATION_REFUS_PAS_INTERESSE_JE:
            _("I am quite simply not interested"),
        INVITATION_REFUS_PAS_INTERESSE_NOUS:
            _("We are quite simply not interested"),
        INVITATION_REFUS_PAS_INTERESSE_MAINTENANT_JE:
            _("I am not interested for now"),
        INVITATION_REFUS_PAS_INTERESSE_MAINTENANT_NOUS:
            _("We are not interested for now"),
        INVITATION_REFUS_VOYAGE_PAS_JE:
            _("I don’t travel"),
        INVITATION_REFUS_VOYAGE_PAS_NOUS:
            _("We don’t travel"),
        INVITATION_REFUS_DEPLACE_PAS_JE:
            _("I don’t travel around"),
        INVITATION_REFUS_DEPLACE_PAS_NOUS:
            _("We don’t travel around"),
        INVITATION_REFUS_SOUHAITE_RESTER_SEUL_JE:
            _("I prefer to remain alone"),
        INVITATION_REFUS_SOUHAITE_RESTER_SEUL_NOUS:
            _("We prefer to remain alone"),
        INVITATION_REFUS_AUCUN_PROJET_VOYAGE_EN_COMMUN_NOUS:
            _("We have no travel plans in common"),
        INVITATION_REFUS_AUCUN_PROJET_SORTIE_EN_COMMUN_NOUS:
            _("We have no ideas in common for trips out"),
        INVITATION_REFUS_AUCUN_PROJET_ACTIVITE_EN_COMMUN_NOUS:
            _("We have nothing in common in terms of activities"),
        INVITATION_REFUS_PARLE_PAS_VOTRE_LANGUE_JE:
            _("I don’t speak your language"),
        INVITATION_REFUS_PARLE_PAS_VOTRE_LANGUE_NOUS:
            _("We don’t speak your language"),
        INVITATION_REFUS_PARLE_PAS_ANGLAIS_JE:
            _("I don’t speak English"),
        INVITATION_REFUS_PARLE_PAS_ANGLAIS_NOUS:
            _("We don’t speak English"),
        INVITATION_REFUS_UTILISER_MES_CONTACTS_JE:
            _("I invite you to use my contacts"),
        INVITATION_REFUS_UTILISER_MES_CONTACTS_NOUS:
            _("We invite you to get in touch with our contacts"),
        INVITATION_REFUS_CONTACTER_UNE_AUTRE_PERSONNE_JE:
            _("I invite you to contact another contact"),
        INVITATION_REFUS_CONTACTER_UNE_AUTRE_PERSONNE_NOUS:
            _("We invite you to contact another person"),
        INVITATION_REFUS_CONTACTER_MESSAGE_JE:
            _("I invite you to contact me by private message"),
        INVITATION_REFUS_CONTACTER_MESSAGE_NOUS:
            _("We invite you to contact us by private message"),
    }

    RELATION_AMI = 0
    RELATION_CONNAISSANCE = 1
    RELATION_INVITATION_EN_COURS = 2
    RELATION_INVITATION_REFUSEE = 3
    RELATION_PARENT_ENFANT = 4
    RELATION_ENFANT_PARENT = 5
    RELATION_MARI_FEMME = 6
    RELATION_FEMME_MARI = 7
    RELATION_PROFESSEUR_ELEVE = 8
    RELATION_ELEVE_PROFESSEUR = 9
    RELATION_RETIREE = 10

    TAB_RELATIONS = {
        RELATION_AMI: _('friend'),
        RELATION_CONNAISSANCE: _('relationship'),
        RELATION_INVITATION_REFUSEE: _("invitation refused"),
        RELATION_INVITATION_EN_COURS: _('sent an invitation'),
        RELATION_PARENT_ENFANT: _('parent / child'),
        RELATION_ENFANT_PARENT: _('child / parent'),
        RELATION_MARI_FEMME: _('husband / wife'),
        RELATION_FEMME_MARI: _('wife / husband'),
        RELATION_PROFESSEUR_ELEVE: _('teacher / student'),
        RELATION_ELEVE_PROFESSEUR: _('student / teacher'),
        RELATION_RETIREE: _('remover / removed'),
    }
    TAB_RELATIONS_REVERSE = {
        RELATION_AMI: _('friend'),
        RELATION_CONNAISSANCE: _('relationship'),
        RELATION_INVITATION_REFUSEE: _("refused invitation"),
        RELATION_INVITATION_EN_COURS: _('received invitation'),
        RELATION_PARENT_ENFANT: _('child / parent'),
        RELATION_ENFANT_PARENT: _('parent / child'),
        RELATION_MARI_FEMME: _('wife / husband'),
        RELATION_FEMME_MARI: _('husband / wife'),
        RELATION_PROFESSEUR_ELEVE: _('student / teacher'),
        RELATION_ELEVE_PROFESSEUR: _('teacher / student'),
        RELATION_RETIREE: _('removed / remover'),
    }

    TAB_RELATIONS_YOU = {
        RELATION_AMI: _('You are friend with {}'),
        RELATION_CONNAISSANCE: _('{} is one of your friend'),
        RELATION_INVITATION_REFUSEE: _("{} declined your invitation"),
        RELATION_INVITATION_EN_COURS: _("Invitation sent to {}"),
        RELATION_PARENT_ENFANT: _('You are the parent of {}'),
        RELATION_ENFANT_PARENT: _('You are the child of {}'),
        RELATION_MARI_FEMME: _('You are the husband of {}'),
        RELATION_FEMME_MARI: _('You are the wife of {}'),
        RELATION_PROFESSEUR_ELEVE: _('You are the teacher of {}'),
        RELATION_ELEVE_PROFESSEUR: _('You are the student of {}'),
        RELATION_RETIREE: _('You have removed this relation'),
    }
    TAB_RELATIONS_REVERSE_YOU = {
        RELATION_AMI: _('You are friend with {}'),
        RELATION_CONNAISSANCE: _('{} is one of your friend'),
        RELATION_INVITATION_REFUSEE: _("You declined {}'s invitation"),
        RELATION_INVITATION_EN_COURS: _('You received an invitation from {}'),
        RELATION_PARENT_ENFANT: _('You are the child of {}'),
        RELATION_ENFANT_PARENT: _('You are the parent of {}'),
        RELATION_MARI_FEMME: _('You are the wife of {}'),
        RELATION_FEMME_MARI: _('You are the husband of {}'),
        RELATION_PROFESSEUR_ELEVE: _('You are the student of {}'),
        RELATION_ELEVE_PROFESSEUR: _('You are the teacher of {}'),
        RELATION_RETIREE: _('{} has removed the relation with you'),
    }

    TAB_RELATIONS_YOU_SHORT = {
        RELATION_AMI: _('You are a friend'),
        RELATION_CONNAISSANCE: _('He/she is one of your friend'),
        RELATION_INVITATION_REFUSEE: _("He/she declined your invitation"),
        RELATION_INVITATION_EN_COURS: _("Invitation sent"),
        RELATION_PARENT_ENFANT: _('You are a parent'),
        RELATION_ENFANT_PARENT: _('You are the child'),
        RELATION_MARI_FEMME: _('You are the husband'),
        RELATION_FEMME_MARI: _('You are the wife'),
        RELATION_PROFESSEUR_ELEVE: _('You are the teacher'),
        RELATION_ELEVE_PROFESSEUR: _('You are the student'),
        RELATION_RETIREE: _('You removed this relation'),
    }
    TAB_RELATIONS_REVERSE_YOU_SHORT = {
        RELATION_AMI: _('You are a friend'),
        RELATION_CONNAISSANCE: _('He/she is one of your friend'),
        RELATION_INVITATION_REFUSEE: _("You declined the invitation"),
        RELATION_INVITATION_EN_COURS: _('You received an invitation'),
        RELATION_PARENT_ENFANT: _('You are the child'),
        RELATION_ENFANT_PARENT: _('You are the parent'),
        RELATION_MARI_FEMME: _('You are the wife'),
        RELATION_FEMME_MARI: _('You are the husband'),
        RELATION_PROFESSEUR_ELEVE: _('You are a student'),
        RELATION_ELEVE_PROFESSEUR: _('You are a teacher'),
        RELATION_RETIREE: _('He/she has removed the relation'),
    }

    NEWSLETTER_CONFIGURATION_EVERY_DAY = 1
    NEWSLETTER_CONFIGURATION_EVERY_WEEK = 2
    NEWSLETTER_CONFIGURATION_EVERY_MONTH = 3
    NEWSLETTER_CONFIGURATION_NEVER = 4

    TAB_NEWSLETTER_CONFIGURATION = {
        NEWSLETTER_CONFIGURATION_EVERY_DAY: _('Every day'),
        NEWSLETTER_CONFIGURATION_EVERY_WEEK: _('Every week'),
        NEWSLETTER_CONFIGURATION_EVERY_MONTH: _('Every month'),
        NEWSLETTER_CONFIGURATION_NEVER: _('Never send newsletter'), }
    """
    Franck m'a donné toute une liste pour les choix, qui s'est agrandie dans
    le temps, je l'ai donc déplacée ici parce que sinon le code n'est
    plus maintenable :
    """

    ZODIAC_CUSTOM_CAPRICORN = 0
    ZODIAC_CUSTOM_AQUARIUS = 1
    ZODIAC_CUSTOM_PISCES = 2
    ZODIAC_CUSTOM_ARIES = 3
    ZODIAC_CUSTOM_TAURUS = 4
    ZODIAC_CUSTOM_GEMINI = 5
    ZODIAC_CUSTOM_CANCER = 6
    ZODIAC_CUSTOM_LEO = 7
    ZODIAC_CUSTOM_VIRGO = 8
    ZODIAC_CUSTOM_LIBRA = 9
    ZODIAC_CUSTOM_SCORPIO = 10
    ZODIAC_CUSTOM_SAGITTARIUS = 11
    ZODIAC_CUSTOM_NOT_PRECISED = 12

    TAB_CUSTOM_ZODIAC_SIGN = {
        ZODIAC_CUSTOM_NOT_PRECISED: _('Not precised'),
        ZODIAC_CUSTOM_CAPRICORN: _('Capricorn'),
        ZODIAC_CUSTOM_AQUARIUS: _('Aquarius'),
        ZODIAC_CUSTOM_PISCES: _('Pisces'),
        ZODIAC_CUSTOM_ARIES: _('Aries'),
        ZODIAC_CUSTOM_TAURUS: _('Taurus'),
        ZODIAC_CUSTOM_GEMINI: _('Gemini'),
        ZODIAC_CUSTOM_CANCER: _('Cancer'),
        ZODIAC_CUSTOM_LEO: _('Leo'),
        ZODIAC_CUSTOM_VIRGO: _('Virgo'),
        ZODIAC_CUSTOM_LIBRA: _('Libra'),
        ZODIAC_CUSTOM_SCORPIO: _('Scorpio'),
        ZODIAC_CUSTOM_SAGITTARIUS: _('Sagittarius'), }

    SEXE_HOMME = 1
    SEXE_FEMME = 2
    TAB_SEXE = {SEXE_HOMME: _('Male'),
                SEXE_FEMME: _('Female'), }

    EST_NON_FUMEUR = 0
    EST_FUMEUR = 1
    EST_FUMEUR_OCCASIONNEL = 2
    EST_FUMEUR_NOT_PRECISED = 3
    TAB_EST_FUMEUR = {EST_FUMEUR_NOT_PRECISED: _('Not precised'),
                      EST_NON_FUMEUR: _('Non-smoker'),
                      EST_FUMEUR: _('Smoker'),
                      EST_FUMEUR_OCCASIONNEL: _('Social smoker'), }

    STATUT_SOLO = 0
    # STATUT_GROUPE = 1
    # STATUT_COUPLE = 2
    # STATUT_FAMILY = 3
    TAB_STATUT = {STATUT_SOLO: _('Solo'),
                  # STATUT_GROUPE: _(u'Group'),
                  # STATUT_COUPLE: _(u'Couple'),
                  # STATUT_FAMILY: _(u'Family'),
                  }

    NIVEAU_ETUDE_PETITE_ENFANCE = 0
    NIVEAU_ETUDE_PRIMAIRE = 1
    NIVEAU_ETUDE_SECONDAIRE_1ER_CYCLE = 2
    NIVEAU_ETUDE_SECONDAIRE_2ND_CYCLE = 3
    NIVEAU_ETUDE_POST_SECONDAIRE = 4
    NIVEAU_ETUDE_SUPERIEUR_CYCLE_COURT = 5
    NIVEAU_ETUDE_SUPERIEUR_LICENCE = 6
    NIVEAU_ETUDE_MASTER = 7
    NIVEAU_ETUDE_DOCTORAT = 8
    NIVEAU_ETUDES_AUTRE = 9
    NIVEAU_ETUDES_NOT_PRECISED = 10
    TAB_NIVEAU_ETUDES = {
        NIVEAU_ETUDES_NOT_PRECISED: _('Not precised'),
        NIVEAU_ETUDE_PETITE_ENFANCE: _(
            'Nursery school'),
        NIVEAU_ETUDE_PRIMAIRE: _(
            'Primary education'),
        NIVEAU_ETUDE_SECONDAIRE_1ER_CYCLE: _(
            'Lower secondary education'),
        NIVEAU_ETUDE_SECONDAIRE_2ND_CYCLE: _(
            'Upper secondary education'),
        NIVEAU_ETUDE_POST_SECONDAIRE: _(
            'Post-secondary non-tertiary education'),
        NIVEAU_ETUDE_SUPERIEUR_CYCLE_COURT: _(
            'Short-cycle tertiary education'),
        NIVEAU_ETUDE_SUPERIEUR_LICENCE: _(
            'Bachelor\'s Degree or equivalent level'),
        NIVEAU_ETUDE_MASTER: _(
            'Master\'s Degree or equivalent level'),
        NIVEAU_ETUDE_DOCTORAT: _(
            'Ph.D. or equivalent level'),
        NIVEAU_ETUDES_AUTRE: _(
            'Other'), }

    PROFESSION_AGRICULTEUR = 0
    PROFESSION_ARTISAN = 1
    PROFESSION_ARTISTE = 2
    PROFESSION_CADRE = 3
    PROFESSION_CHAUFFEUR = 4
    PROFESSION_CHEF_D_ENTREPRISE = 5
    PROFESSION_CLERGE_RELIGIEUX = 6
    PROFESSION_COMMERCANT_ET_ASSIMILE = 7
    PROFESSION_CONTREMAITRE_AGENT_DE_MAITRISE = 8
    PROFESSION_DIRIGEANT = 9
    PROFESSION_EMPLOYE = 10
    PROFESSION_ETUDIANT = 11
    PROFESSION_FONCTIONNAIRE = 12
    PROFESSION_INGENIEUR = 13
    PROFESSION_INSTITUTEUR = 14
    PROFESSION_OUVRIER = 15
    PROFESSION_POLICIER_OU_MILITAIRE = 16
    PROFESSION_PROFESSEUR = 17
    PROFESSION_PROFESSION_LIBERALE = 18
    PROFESSION_RETRAITE = 19
    PROFESSION_SPORTIF = 20
    PROFESSION_TECHNICIEN = 21
    PROFESSION_NON_DIVULGUE = 22
    PROFESSION_SANS_EMPLOI = 23
    PROFESSION_AUTRE = 24
    PROFESSION_NOT_PRECISED = 25

    TAB_PROFESSION = {
        PROFESSION_NOT_PRECISED: _('Not precised'),
        PROFESSION_AGRICULTEUR: _('Farmer'),
        PROFESSION_ARTISAN: _('Craftsman'),
        PROFESSION_ARTISTE: _('Artist'),
        PROFESSION_CADRE: _('Manager'),
        PROFESSION_CHAUFFEUR: _('Driver'),
        PROFESSION_CHEF_D_ENTREPRISE: _('Chief Executive Officer'),
        PROFESSION_CLERGE_RELIGIEUX: _('Clergyman'),
        PROFESSION_COMMERCANT_ET_ASSIMILE: _('Independent retailer'),
        PROFESSION_CONTREMAITRE_AGENT_DE_MAITRISE: _('Foreman, supervisor'),
        PROFESSION_DIRIGEANT: _('Managing director'),
        PROFESSION_EMPLOYE: _('Employee'),
        PROFESSION_ETUDIANT: _('Student'),
        PROFESSION_FONCTIONNAIRE: _('Civil servant'),
        PROFESSION_INGENIEUR: _('Engineer'),
        PROFESSION_INSTITUTEUR: _('Primary schoolteacher'),
        PROFESSION_OUVRIER: _('Labourer'),
        PROFESSION_POLICIER_OU_MILITAIRE: _('Policeman or Soldier'),
        PROFESSION_PROFESSEUR: _('Teacher'),
        PROFESSION_PROFESSION_LIBERALE: _('Self-employed profession'),
        PROFESSION_RETRAITE: _('Pensioner'),
        PROFESSION_SPORTIF: _('Sportsman'),
        PROFESSION_TECHNICIEN: _('Technician'),
        PROFESSION_NON_DIVULGUE: _('Undisclosed'),
        PROFESSION_SANS_EMPLOI: _('Unemployed'),
        PROFESSION_AUTRE: _('Other'), }

    LANGUE_ALBANAIS = 0
    LANGUE_ALLEMAND = 1
    LANGUE_ANGLAIS = 2
    LANGUE_ARABE = 3
    LANGUE_ARMENIEN = 4
    LANGUE_BENGALI = 5
    LANGUE_CATALAN = 6
    LANGUE_CHINOIS = 7
    LANGUE_COREEN = 8
    LANGUE_CROATE = 9
    LANGUE_DANOIS = 10
    LANGUE_ESPAGNOL = 11
    LANGUE_FINNOIS = 12
    LANGUE_FRANCAIS = 13
    LANGUE_GREC = 14
    LANGUE_HONGROIS = 15
    LANGUE_ITALIEN = 16
    LANGUE_MALAIS = 17
    LANGUE_MONGOL = 18
    LANGUE_NEERLANDAIS = 19
    LANGUE_OCCITAN = 20
    LANGUE_PERSAN = 21
    LANGUE_PORTUGAIS = 22
    LANGUE_ROUMAIN = 23
    LANGUE_RUSSE = 24
    LANGUE_SERBE = 25
    LANGUE_SLOVAQUE = 26
    LANGUE_SLOVENE = 27
    LANGUE_SUEDOIS = 28
    LANGUE_TURC = 29
    LANGUE_AUTRE = 30
    TAB_LANGUE = {
        LANGUE_ALBANAIS: _('Albanian'),
        LANGUE_ALLEMAND: _('German'),
        LANGUE_ANGLAIS: _('English'),
        LANGUE_ARABE: _('Arabic'),
        LANGUE_ARMENIEN: _('Armenian'),
        LANGUE_BENGALI: _('Bengali'),
        LANGUE_CATALAN: _('Catalan'),
        LANGUE_CHINOIS: _('Chinese'),
        LANGUE_COREEN: _('Korean'),
        LANGUE_CROATE: _('Croatian'),
        LANGUE_DANOIS: _('Danish'),
        LANGUE_ESPAGNOL: _('Spanish'),
        LANGUE_FINNOIS: _('Finnish'),
        LANGUE_FRANCAIS: _('French'),
        LANGUE_GREC: _('Greek'),
        LANGUE_HONGROIS: _('Hungarian'),
        LANGUE_ITALIEN: _('Italian'),
        LANGUE_MALAIS: _('Malaysian'),
        LANGUE_MONGOL: _('Mongolian'),
        LANGUE_NEERLANDAIS: _('Dutch'),
        LANGUE_OCCITAN: _('Occitan'),
        LANGUE_PERSAN: _('Persian'),
        LANGUE_PORTUGAIS: _('Portuguese'),
        LANGUE_ROUMAIN: _('Romanian'),
        LANGUE_RUSSE: _('Russian'),
        LANGUE_SERBE: _('Serbian'),
        LANGUE_SLOVAQUE: _('Slovakian'),
        LANGUE_SLOVENE: _('Slovenian'),
        LANGUE_SUEDOIS: _('Swedish'),
        LANGUE_TURC: _('Turkish'),
        LANGUE_AUTRE: _('Other'),
    }

    HOW_DID_I_KNOW_COGOFLY_FACEBOOK = 1
    HOW_DID_I_KNOW_COGOFLY_GOOGLE = 2
    HOW_DID_I_KNOW_COGOFLY_GOOGLE_PLUS = 3
    HOW_DID_I_KNOW_COGOFLY_TWITTER = 4
    HOW_DID_I_KNOW_COGOFLY_FLYERS = 5
    HOW_DID_I_KNOW_COGOFLY_WORD_OF_MOUTH = 6
    HOW_DID_I_KNOW_COGOFLY_OTHER = 7

    TAB_HOW_DID_I_KNOW_COGOFLY = {
        HOW_DID_I_KNOW_COGOFLY_FACEBOOK: 'Facebook',
        HOW_DID_I_KNOW_COGOFLY_GOOGLE: 'Google',
        HOW_DID_I_KNOW_COGOFLY_GOOGLE_PLUS: 'Google Plus',
        HOW_DID_I_KNOW_COGOFLY_TWITTER: 'Twitter',
        HOW_DID_I_KNOW_COGOFLY_FLYERS: _('Flyers'),
        HOW_DID_I_KNOW_COGOFLY_WORD_OF_MOUTH: _('Word of mouth'),
        HOW_DID_I_KNOW_COGOFLY_OTHER: _('Other'),
    }
