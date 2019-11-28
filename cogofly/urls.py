# coding=UTF-8


from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.views import static, defaults
from django.views.generic import TemplateView
from django.urls import re_path, path

import app.views.my_home as app_my_home
import app.views.json as app_json
import app.views
from app.views.static.about import AboutView
from app.views.static.blog import BlogView
from app.views.static.contact_us import ContactUsView
from app.views.static.privacy_policy import PrivacyPolicyView 
from app.views.static.testimonies import TestimoniesView
from app.views.static.the_team import TheTeamView
from applancement.views import register as app_l_r, views as app_l_views
from applancement.views.terms_and_conditions import TermsAndConditionsView
from applancement.views.terms_of_service import TermsOfServiceView

urlpatterns = [

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^login/(\w*)', app_l_views.login, name='login'),
    url(r'^logout/?$', app_l_views.logout, name='logout'),

    # New url's
    url(r'^addtrip/?$', app_l_views.addtrip, name='addtrip'),
    url(r'^tripcard/?$', app_l_views.tripcard, name='tripcard'),
    url(r'^profile/?$', app_l_views.profile, name='profile'),
    url(r'^review/?$', app_l_views.review, name='review'),
    url(r'^tripsdone/?$', app_l_views.tripsdone, name='tripsdone'),
    url(r'^demo/?$', app_l_views.demo, name='demo'),



    url(r'^admin/', admin.site.urls),

    # se connecter à la place d'un utilisateur pour tester les bogues :
    url(r'^hijack/', include('hijack.urls', namespace='hijack')),

    url('^markdown/', include('django_markdown.urls')),

    # 18/03/2016 : Si tout fonctionne sans ça d'ici quelque temps c'est que j'ai
    #              déplacé le code ailleurs, et que je peux le supprimer :
    # url(r'^email$', app_l_views.email, name='email'),

    url(r'^register-validate/(?P<rand_str>[a-zA-Z0-9-_]+)/$',
        app_l_r.RegisterValidateView.as_view(),
        name='register_validate'),

    url(r'^public/(?P<path>.*)$', static.serve, {
        'document_root': settings.MEDIA_ROOT
    }, name='url_public'),

    url(r'^404/$', defaults.page_not_found, name='page_not_found', ),
    url(r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.txt',
                             content_type='text/plain'),
        name='robots_txt'),
]

urlpatterns += i18n_patterns(
    url(r'^$', app.views.IndexView.as_view(), name='app_index'),

    url(r'^register$', app_l_r.RegisterView.as_view(), name='register'),
    url(_(r'^launch'),
        app_l_r.RegisterView.as_view(), name='applancement_index'),

    # ---------------------------------------------------
    # - Pages statiques
    url(_(r'legal/about/$'), AboutView.as_view(),
        name='about'),
    url(_(r'legal/the-team/$'), TheTeamView.as_view(),
        name='the_team'),
    url(_(r'legal/testimonies/$'), TestimoniesView.as_view(),
        name='testimonies'),
    url(_(r'legal/privacy-policy/$'), PrivacyPolicyView.as_view(),
        name='privacy_policy'),
    url(_(r'legal/contact-us/$'), ContactUsView.as_view(),
        name='contact_us'),
    url(_(r'blog/$'), BlogView.as_view(),
        name='blog'),

    url(_(r'legal/terms-and-conditions/$'), TermsAndConditionsView.as_view(),
        name='terms_and_conditions'),
    url(_(r'legal/terms-of-service/$'), TermsOfServiceView.as_view(),
        name='terms_of_service'),

    # ---------------------------------------------------
    # JSON
    url(_(r'^json$'),
        app_json.tags.JsonTagsView.as_view(), name='json'),
    url(_(r'^json/tags/languages$'),
        app_json.tags.JsonTagsLangagesView.as_view(),
        name='json_tag_langages'),
    url(_(r'^json/tags/driving_licences$'),
        app_json.tags.JsonTagsTypesPermisView.as_view(),
        name='json_tag_types_permis'),
    url(_(r'^json/tags/driving_licences$'),
        app_json.tags.JsonTagsTypesPermisView.as_view(),
        name='json_tag_types_permis'),
    url(_(r'^json/tags/diplomas'),
        app_json.tags.JsonTagsDiplomesView.as_view(),
        name='json_tag_diplomes'),
    url(_(r'^json/tags/points_of_interest$'),
        app_json.tags.JsonTagsCentresDInteretView.as_view(),
        name='json_tag_centres_dinteret'),
    url(_(r'^json/tags/hobbies$'),
        app_json.tags.JsonTagsHobbiesView.as_view(),
        name='json_tag_hobbies'),
    url(_(r'^json/liked/(?P<id_activite>[0-9]+)/$'),
        app_json.JsonLikedView.as_view(),
        name='json_liked'),
    url(_(r'^json/liked-profile/(?P<id_profile>[0-9]+)/$'),
        app_json.JsonLikedProfileView.as_view(),
        name='json_liked_profile'),
    url(_(r'^json/liked-read/(?P<id_personne_like>[0-9]+)/$'),
        app_json.JsonLikedReadView.as_view(),
        name='json_liked_read'),
    url(_(r'^json/message-read/(?P<id_message>[0-9]+)/$'),
        app_json.JsonMessageReadView.as_view(),
        name='json_message_read'),
    url(_(r'^json/invite/(?P<id_personne>[0-9]+)/$'),
        app_json.JsonInviteView.as_view(),
        name='json_invite'),
    url(_(r'^json/relationship-remove/(?P<id_personne>[0-9]+)/$'),
        app_json.JsonRelationRemoveView.as_view(),
        name='json_relation_remove'),

    # ---------------------------------------------------
    # my-home
    url(_(r'^my-home$'),
        app_my_home.IndexView.as_view(),
        name='my_home_index'),

    url(_(r'^my-home-error$'),
        app_my_home.ErrorView.as_view(),
        name='my_home_error'),

    # partage d'une activité avec ses contacts :
    url(_(r'^my-home/activity-share/$'),
        app_my_home.ActivityShareView.as_view(),
        name='activity_share_view'),

    # contact support / envoi remarques
    url(_(r'^my-home/remarks-and-testimonies$'),
        app_my_home.RemarksAndTestimoniesView.as_view(),
        name='my_home_remarks_and_testimonies'),

    # my-home / contact(s)
    url(_(r'^my-home/contacts$'),
        app_my_home.contacts.IndexView.as_view(),
        name='my_home_contacts'),
    url(_(r'^my-home/contacts/invite$'),
        app_my_home.contacts.InviteFriendView.as_view(),
        name='my_home_contacts_invite'),
    url(_(r'^my-home/contact/detail/(?P<contact_id>[0-9]+)/$'),
        app_my_home.contact_detail.ContactDetailView.as_view(),
        name='contact_detail'),
    url(_(r'^my-home/contacts/register-validate/(?P<rand_str>[a-zA-Z0-9-_]+)/$'),
        app_my_home.contacts.ContactRegisterValidateView.as_view(),
        name='contact_register_validate'),

    # my-home / profile
    url(_(r'^my-home/profile/account-desactivated/$'),
        app_my_home.profile.AccountDesactivatedView.as_view(),
        name='my_home_profile_account_desactivated'),
    url(_(r'^my-home/profile/account-deleted/$'),
        app_my_home.profile.AccountDeletedView.as_view(),
        name='my_home_profile_account_deleted'),
    url(_(r'^my-home/profile-not-complete/$'),
        app_my_home.profile.NotCompleteView.as_view(),
        name='my_home_profile_not_complete'),
    url(_(r'^my-home/profile/account-reactivate/(?P<rand_str>[a-zA-Z0-9-_]+)/$'),
        app_my_home.profile.AccountReactivateView.as_view(),
        name='my_home_profile_account_reactivate'),
    url(_(r'^my-home/profile/password-recover'),
        app_my_home.profile.PasswordRecoverView.as_view(),
        name='my_home_profile_password_recover'),
    url(_(r'^my-home/profile/password-change'),
        app_my_home.profile.ChangePasswordView.as_view(),
        name='my_home_profile_password_change'),
    url(_(r'^my-home/profile/newsletter-set-configuration'),
        app_my_home.profile.NewsletterConfigurationView.as_view(),
        name='my_home_newsletter_set_configuration'),
    url(_(r'^my-home/profile/visibility-change'),
        app_my_home.profile.ChangeVisibilityView.as_view(),
        name='my_home_profile_visibility_change'),
    url(_(r'^my-home/profile/desactivate$'),
        app_my_home.profile.AccountDesactivateView.as_view(),
        name='my_home_profile_desactivate'),

    url(_(r'^my-home/profile/edit$'),
        app_my_home.profile.EditView.as_view(),
        name='my_home_profile_edit'),

    url(_(r'^my-home/profile/delete$'),
        app_my_home.profile.AccountDeleteView.as_view(),
        name='my_home_profile_delete'),

    url(_(r'^my-home/travels$'),
        app_my_home.travels.IndexView.as_view(),
        name='my_home_travel'),
    url(_(r'^my-home/search$'),
        app_my_home.travels.SearchView.as_view(),
        name='my_home_search'),

    # my-home / notifications
    url(_(r'^my-home/notifications$'),
        app_my_home.NotificationsView.as_view(),
        name='my_home_notifications'),
    url(_(r'^my-home/conversation/delete/(?P<id_conversation>[0-9]+)/$'),
        app_my_home.ConversationDeleteView.as_view(),
        name='my_home_conversation_delete'),

    url(_(r'^my-home/language$'),
        app_my_home.LanguageView.as_view(), name='my_home_language'),
    url(_(r'^my-home/register'),
        app_my_home.RegisterView.as_view(), name='my_home_register'),
    url(_(r'^my-home/login$'),
        app_my_home.LoginView.as_view(), name='my_home_login'),
    url(_(r'^my-home/logout$'),
        app_my_home.LogoutView.as_view(), name='my_home_logout'),
    url(_(r'premium/$'), app_my_home.PremiumView.as_view(),
        name='my_home_premium'),
)
