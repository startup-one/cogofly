# coding=utf-8
# Toutes mes classe génériques de l'administration


from django.contrib import admin


class CollapsedStackedInline(admin.StackedInline):
    class Media:
        css = {
            # 'all': ('pretty.css',)
        }
        js = ('js/jquery/jquery-1.11.3.min.js',
              'js/tools/admin_collapsed_stacked_inlines.js',)


class BigSelectMultiplesAdmin(admin.ModelAdmin):
    class Media:
        css = {
        }
        js = ('js/jquery/jquery-1.11.3.min.js',
              'js/tools/admin_big_select_multiples.js',)


class ResizableAdmin(admin.ModelAdmin):
    """
    Les multi select sont hyper petits.
    Ici, solution appliquée dans l'interface d'admin :
    - champ "int" sur lequel on met la classe "resize_src" et un autre champ
    - autre champ sur lequel on met la classe "resize_dst"

    -> en jQuery, je redimensionne "resize_dst" dès que "resize_src" change.
    """
    class Media:
        css = {
        }
        js = ('js/jquery/jquery-1.11.3.min.js',
              'js/tools/admin_resize_widgets.js',)


