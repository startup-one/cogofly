# coding=UTF-8

from os.path import basename

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from hijack_admin.admin import HijackUserAdminMixin

from app.admin.generic import CollapsedStackedInline
from app.models.blog import Blog, BlogTraduit
from app.models.conversation import Conversation, Message
from app.models.generic import Langue
from app.models.publicite import Publicite
from app.models.publicite import PubliciteTraduit
from app.models.tag import TagWithValue, TagTraduit, TagBase, TagGoogleMaps, \
    TagGoogleMapsTraduit
from app.models.personne import Personne, PersonnePhoto, PersonneTravel, \
    PersonneRelation, Activite, PersonneLiked, ActiviteComments, Photo, \
    ActiviteShared, ActiviteTestimony, PersonneSearch, ActiviteExpressyourself


class MyAdminSite(admin.AdminSite):
    site_header = _("Cogofly's administration")


class UserPersonneInline(admin.StackedInline):
    can_delete = False
    model = Personne
    extra = 0
    inlines = ()
    raw_id_fields = ('place_of_birth', 'place_i_live',
                     'employer_current', 'employer_previous')
    readonly_fields = ('place_of_birth', 'place_i_live',
                       'employer_current', 'employer_previous')


class HiddenAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Aucune permission = cacher le modèle de l'index principal.
        http://stackoverflow.com/questions/2431727/django-admin-hide-a-model
        """
        return {}


class MyUserSimpleAdmin(UserAdmin):
    search_fields = ('email', 'first_name', 'last_name', )
    # Colonne de droite :
    list_filter = ('is_staff', 'is_active', 'last_login')


class PersonneSearchAdmin(admin.ModelAdmin):
    raw_id_fields = ('personne', 'search',)


class MyUserAdmin(UserAdmin, HijackUserAdminMixin):

    actions_on_bottom = True
    date_hierarchy = 'date_joined'

    def email_nom_prenom(self, r):
        return '{} - {} {}'.format(r.email, r.first_name, r.last_name).strip()
    email_nom_prenom.short_description = _('Email / Last+First name')
    email_nom_prenom.admin_order_field = 'email'

    def p_date_creation(self, r):
        return r.personne.date_creation
    p_date_creation.short_description = _('Created')
    p_date_creation.admin_order_field = 'personne__date_creation'

    def url_edit_personne(self, r):
        return '&raquo;&raquo; <a href="{}">{}</a>'.format(
            reverse('admin:app_personne_change',
                                 args=(r.personne.id,)),
            '{} {}'.format(r.personne.user.first_name,
                            r.personne.user.last_name).strip()
        )
    url_edit_personne.allow_tags = True
    url_edit_personne.short_description = _('Go to details')
    url_edit_personne.admin_order_field = 'personne'

    list_display = ('email_nom_prenom', 'url_edit_personne', 'is_staff',
                    'is_active', 'last_login', 'p_date_creation',
                    'hijack_field', )
    search_fields = ('email', 'first_name', 'last_name', )
    # Colonne de droite :
    list_filter = ('is_staff', 'is_active', 'last_login')

    fieldsets = (
        (None, {
            'fields': (('email',), ('first_name', 'last_name',),
                       ('is_staff',),
                       ('is_active',), ('last_login',))
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('username',)
        }),
    )
    inlines = (UserPersonneInline, )


class PhotoAdmin(admin.ModelAdmin):
    def list_url_image(self, obj):
        if obj and obj.image is not None:
            return '<img src="{}" />'.format(obj.url())
        return None

    list_url_image.short_description = _('Image')
    list_url_image.allow_tags = True

    def list_url(self, obj):
        if obj and obj.image is not None:
            return '<a href="{}">{}</a>'.format(obj.url(), obj.url())
        return None

    list_url.short_description = _('Image')
    list_url.allow_tags = True

    def url_image(self, obj):
        if obj:
            if obj.image is not None:
                return '<img src="{}" />'.format(obj.url())
        return None
    url_image.short_description = _('Image')
    url_image.allow_tags = True

    list_display = ('date_v_debut', 'list_url_image', 'list_url')
    list_display_links = ('list_url_image', 'list_url')

    readonly_fields = ('fichier_origine', 'url_image', 'date_v_debut',)
    fieldsets = (
        (None, {
            'fields': (('fichier_origine',), ('image',))
        }),
        (_('Validity information'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )
    ordering = ('-date_last_modif', '-date_v_debut')


def url_to_edit_object(obj):
    return reverse('admin:%s_%s_change' % (
        obj._meta.app_label, obj._meta.model_name), args=[obj.id])


class PersonnePhotoAdmin(admin.ModelAdmin):

    def list_url_image(self, obj):
        if obj and obj.photo:
            if obj.photo.image is not None:
                return '<img src="{}" />'.format(obj.photo.url())
        return None
    list_url_image.short_description = _('Image')
    list_url_image.allow_tags = True

    def list_url_full(self, obj):
        if obj is None:
            return None
        if obj.photo is None:
            return None
        if obj.photo.image is None:
            return None
        return '<a href="{}" target="_blank">&raquo;&raquo; Full size</a>' \
               '<br><a href="{}" target="_blank">' \
               '&raquo;&raquo; {}' \
               '</a>'.format(
                obj.photo.url().replace('/th/', '/full/'),
                url_to_edit_object(obj.personne.user),
                _("Edit {}").format(str(obj.personne)))

    list_url_full.short_description = _('Image')
    list_url_full.allow_tags = True

    def list_url_thumbnail(self, obj):
        if obj and obj.photo:
            if obj.photo.image is not None:
                return '<a href="{}" target="_blank">{}</a>'.format(
                    obj.photo.url(),
                    basename(obj.photo.url()))
        return None
    list_url_thumbnail.short_description = _('Image thumbnail')
    list_url_thumbnail.allow_tags = True

    def url_image(self, obj):
        if obj:
            if obj.image is not None:
                return '<img src="{}" />'.format(obj.url())
        return None
    url_image.short_description = _('Image full size')
    url_image.allow_tags = True

    list_display = ('date_v_debut',
                    'list_url_image', 'list_url_full', 'list_url_thumbnail', )
    list_display_links = ('list_url_image', 'list_url_full',
                          'list_url_thumbnail')

    readonly_fields = ('url_image', 'date_v_debut',)
    raw_id_fields = ('personne', 'photo',)
    fieldsets = (
        (None, {
            'fields': (('photo_type',), ('personne',), ('photo',))
        }),
        (_('Validity information'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )
    ordering = ('-date_last_modif', '-date_v_debut')
    list_per_page = 200


class PersonnePhotosInline(CollapsedStackedInline):
    model = PersonnePhoto
    fk_name = 'personne'
    raw_id_fields = ('photo',)
    extra = 0
    verbose_name = _("Picture")
    verbose_name_plural = _("Pictures")


"""
(!!) Franck m'a demandé de les supprimer, 15 jours de boulot perdus !!
class PersonneLanguesInline(CollapsedStackedInline):
    model = PersonneLangue
    fk_name = 'personne'
    extra = 0
    verbose_name = _(u"Language")
    verbose_name_plural = _(u"Languages")


"""


class PersonneTravelsInline(CollapsedStackedInline):
    model = PersonneTravel
    fk_name = 'personne'
    raw_id_fields = ('travel', 'photo1', 'photo2', 'photo3')
    extra = 0
    verbose_name = _("Travel")
    verbose_name_plural = _("Travels")


class PersonneRelationsInline(CollapsedStackedInline):
    model = PersonneRelation
    fk_name = 'src'
    fields = ('type_relation', 'src', 'dst', 'opposite',
              'is_reverse', 'raison_refus')
    raw_id_fields = ('src', 'dst', 'opposite')
    extra = 0
    verbose_name = _("Relation")
    verbose_name_plural = _("Relations")


class PersonneLikedsInline(CollapsedStackedInline):
    model = PersonneLiked
    fk_name = 'src'
    fields = ('src', 'dst', 'liked', 'viewed')
    raw_id_fields = ('src', 'dst', 'activite')
    extra = 0
    verbose_name = _("Liked")
    verbose_name_plural = _("Liked's")


################################################################################
################################################################################
################################################################################
class PersonneProgrammes2Inline(CollapsedStackedInline):
    model = Personne.programmes2.through
    raw_id_fields = ('programme',)
    extra = 0
    verbose_name = _("Subject")
    verbose_name_plural = _("Subjects")


class PersonneActivites2Inline(CollapsedStackedInline):
    model = Personne.activites2.through
    raw_id_fields = ('activite',)
    extra = 0
    verbose_name = _("Activity sector")
    verbose_name_plural = _("Activity sectors")


class PersonneHobbies2Inline(CollapsedStackedInline):
    model = Personne.hobbies2.through
    extra = 0
    raw_id_fields = ('hobby',)
    verbose_name = _("Hobby")
    verbose_name_plural = _("Hobbies")


class PersonneTypespermis2Inline(CollapsedStackedInline):
    model = Personne.types_permis2.through
    extra = 0
    raw_id_fields = ('type_permis',)
    verbose_name = _("Licence")
    verbose_name_plural = _("Licences")


# class ActiviteCommentsAdmin(CollapsedStackedInline):
#     model = ActiviteComments
#     fk_name = 'activite'
#     fields = ('activite_dst', 'personne', 'comment')
#     extra = 0
#     verbose_name = _(u"Comment")
#     verbose_name_plural = _(u"Comments")

class ActiviteExpressyourselfAdmin(admin.ModelAdmin):
    raw_id_fields = ('personne',)
    fieldsets = (
        (None, {
            'fields': ('personne', 'message')
        }),
        (_('Administration only'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )


class ActiviteTestimonyAdmin(admin.ModelAdmin):
    raw_id_fields = ('personne',)
    fieldsets = (
        (None, {
            'fields': ('personne', 'testimony_show_name',
                       'testimony',  'validated_by_moderator')
        }),
        (_('Administration only'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )


class ActiviteCommentsAdmin(admin.ModelAdmin):
    raw_id_fields = ('personne', 'activite_dst')
    fieldsets = (
        (None, {
            'fields': ('personne', 'activite_dst', 'comment')
        }),
        (_('Administration only'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )


class ActiviteAdmin(admin.ModelAdmin):
    readonly_fields = ('date_creation', 'date_last_modif',)
    fields = ('activite',
              'comment',
              'travel',
              'relation',
              'blog_traduit',
              'date_publication',
              ('date_v_debut', 'date_v_fin'),
              ('date_creation', 'date_last_modif',))
    raw_id_fields = ('travel', 'blog_traduit', 'relation', 'comment')
    inlines = ()  # (ActiviteCommentsAdmin, )


class ActiviteSharedAdmin(admin.ModelAdmin):
    readonly_fields = ('date_creation', 'date_last_modif',)
    fields = ('src',
              'dst',
              'activite',
              ('date_v_debut', 'date_v_fin'),
              ('date_creation', 'date_last_modif',))
    raw_id_fields = ('src', 'dst', 'activite')
    inlines = ()  # (ActiviteCommentsAdmin, )


class MessageThrough(Conversation.messages.through):
    class Meta:
        proxy = True

    def __unicode__(self):
        return str(self.message)


class ConversationMessagesInline(CollapsedStackedInline):
    model = MessageThrough
    fields = ('message',)
    raw_id_fields = ('message',)
    extra = 0

    verbose_name = "Message"
    verbose_name_plural = "Messages"


class PersonneThrough(Conversation.personnes.through):
    class Meta:
        proxy = True

    def __unicode__(self):
        return str(self.personne.full_name())


class ConversationPersonnesInline(CollapsedStackedInline):
    model = PersonneThrough
    fields = ('personne',)
    raw_id_fields = ('personne',)
    extra = 0

    verbose_name = "Personne"
    verbose_name_plural = "Personnes"


class ConversationAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Administration only'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
        (_('Administration only'), {
            'classes': ('collapse',),
            'fields': ()
        }),
    )
    inlines = (ConversationPersonnesInline, ConversationMessagesInline,)


class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('src', 'src_visible',)
        }),
        (None, {
            'fields': ('dst', 'dst_visible',)
        }),
        (None, {
            'fields': ('is_read', 'message',)
        }),
        (_('Administration only'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )
    raw_id_fields = ('src', 'dst')


class PersonneAdmin(admin.ModelAdmin):
    readonly_fields = ('zodiac_sign',)
    fieldsets = (
        (None, {
            'fields': (('sexe', 'est_fumeur', 'statut',),
                       ('date_naissance', 'zodiac_sign', 'custom_zodiac_sign',),
                       ('place_of_birth',), ('place_i_live',),
                       ('niveau_etudes',), ('profession',), ('langue',),
                       # ('newsletter_configuration', ),
                       ('how_did_i_know_cogofly', ), )
        }),
        (_('Visibility of optional information'), {
            'classes': ('collapse',),
            'fields': (('age_visible',),
                       ('nb_enfants_visible',), ('langue_visible',),
                       ('langues2_visible',),
                       ('niveau_etudes_visible',), ('programme_visible',),
                       ('employer_current_visible',),
                       ('employer_previous_visible',),
                       ('profession_visible',), ('activite_visible',),
                       ('hobbies_visible',), ('conduite_visible',),
                       ('personnalite_visible',), ('est_fumeur_visible',),
                       ('custom_zodiac_sign_visible',),
                       ('self_description_visible',),),
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('est_physique', 'reset_password', 'confirmation_code',
                       'temporary_visible_password', 'champs_supplementaires',
                       'is_beta_tester',)
        }),
        (_('Newsletter'), {
            'classes': ('collapse',),
            'fields': ('newsletter_configuration', 'newsletter_date_sent',)
        }),
        (_('Validity / Registering'), {
            'classes': ('collapse',),
            'fields': ('est_active', 'est_detruit', 'reason_delete',
                       'one_click_login',
                       'reactivate_code', 'date_v_debut', 'date_v_fin',)
        }),
        (_('Administration only'), {
            'classes': ('collapse',),
            'fields': ('user', 'site_web', 'site_language',)
        }),
    )
    raw_id_fields = ('user', 'place_of_birth', 'place_i_live', )
    search_fields = ('user__email', 'user__first_name', 'user__last_name', )
    inlines = (PersonnePhotosInline, PersonneTravelsInline,
               PersonneRelationsInline, PersonneLikedsInline,
               PersonneProgrammes2Inline, PersonneActivites2Inline,
               PersonneHobbies2Inline, PersonneTypespermis2Inline)


class TagWithValueAdmin(admin.ModelAdmin):
    # (!) change le bouton "Enregistrer et ajouter un nouveau" par "
    list_display = ('type_tag', 'description', 'value', 'pk',
                    'date_creation', 'date_last_modif')
    list_display_links = list_display
    save_as = True


class BlogBlogTraduitsInline(CollapsedStackedInline):
    model = BlogTraduit
    extra = 0
    inlines = ()
    fields = ('locale', 'title', 'content', )
    verbose_name = ''
    verbose_name_plural = _('Translations')


class BlogAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('label',), ('date_publication', ), ('ordre_si_top',),
                       ('date_envoi_newsletter',),)
        }),
        (_('Validity'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )
    inlines = (BlogBlogTraduitsInline,)


class PublicitePubliciteTraduitsInline(CollapsedStackedInline):
    model = PubliciteTraduit
    extra = 0
    inlines = ()
    fields = ('locale', 'title', 'content', )
    verbose_name = ''
    verbose_name_plural = _('Ads translated')


class PubliciteAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('label',),
                       ('ordre_si_top', ),
                       ('position', ),
                       ('date_publication', ), )
        }),
        (_('Validity'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )
    inlines = (PublicitePubliciteTraduitsInline,)

    verbose_name = _('Ad')
    verbose_name_plural = _('Ads')


class TagTagTraduitsInline(CollapsedStackedInline):
    model = TagTraduit
    extra = 0
    inlines = ()
    fields = ('langue', 'value', )
    verbose_name = _('Tag traduit')
    verbose_name_plural = _('Tags traduits')


class TagBaseAdmin(admin.ModelAdmin):
    save_as = True
    fieldsets = (
        (None, {
            'fields': (('type_tag',), ('poids',), ('description',),)
        }),
        (_('Validity'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )

    ordering = ('type_tag', 'description', 'poids', )
    inlines = (TagTagTraduitsInline,)


class TagGoogleMapsTagGoogleMapsTraduitsInline(CollapsedStackedInline):
    model = TagGoogleMapsTraduit
    extra = 0
    inlines = ()
    fields = ('langue', 'formatted_address', )
    verbose_name = ''
    verbose_name_plural = _("Tags google maps of a place in a language")


class TagGoogleMapsAdmin(admin.ModelAdmin):
    save_as = True
    fieldsets = (
        (None, {
            'fields': (('type_tag',), ('description',), ('place_id',),)
        }),
        (_('World coordinates (lat/lng)'), {
            'classes': ('collapse',),
            'fields': (('lat', 'lng',),)
        }),
        (_('World coordinates rectangle (lat/lng)'), {
            'classes': ('collapse',),
            'fields': (('viewport_northeast_lat', 'viewport_northeast_lng',),
                       ('viewport_southwest_lat', 'viewport_southwest_lng',),)
        }),
        (_('Validity'), {
            'classes': ('collapse',),
            'fields': ('date_v_debut', 'date_v_fin')
        }),
    )
    inlines = (TagGoogleMapsTagGoogleMapsTraduitsInline,)


admin.site = admin.AdminSite(name='MonAdminRienQuAMoi')

admin.site.register(PersonneTravel, HiddenAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PersonnePhoto, PersonnePhotoAdmin)
admin.site.register(PersonneRelation)

admin.site.register(ActiviteExpressyourself, ActiviteExpressyourselfAdmin)
admin.site.register(ActiviteTestimony, ActiviteTestimonyAdmin)
admin.site.register(ActiviteComments, ActiviteCommentsAdmin)
admin.site.register(Activite, ActiviteAdmin)
admin.site.register(ActiviteShared, ActiviteSharedAdmin)

admin.site.register(Personne, PersonneAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Langue)
admin.site.register(TagWithValue, TagWithValueAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogTraduit)
admin.site.register(Publicite, PubliciteAdmin)
admin.site.register(PubliciteTraduit)

# nouvelle gestion des tags :
admin.site.register(TagBase, TagBaseAdmin)
admin.site.register(TagTraduit)
admin.site.register(TagGoogleMapsTraduit, HiddenAdmin)
admin.site.register(TagGoogleMaps, TagGoogleMapsAdmin)

# admin d'origine de Django
admin.site.register(Group)
admin.site.register(PersonneSearch, PersonneSearchAdmin)
admin.site.register(User, MyUserAdmin)
# admin.site.register(User, MyUserSimpleAdmin)
# admin.site.register(User)
