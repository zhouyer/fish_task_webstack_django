from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import FirstLevelMenuItem, SecondLevelMenuItem, WebStack

admin.site.site_header = 'FishTask导航管理'
admin.site.site_title = 'FishTask导航管理'


class FirstLevelMenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'sort', 'create_date', 'update_date')
    search_fields = ['name']
    # 数据层级
    # date_hierarchy = 'create_date'
    # 列表中可直接编辑的字段
    # list_editable = ('sort',)
    # 可点击跳到编辑的字段
    list_display_links = ('name',)
    # 列表过滤条件
    list_filter = ('create_date',)


class SecondLevelMenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name', 'code', 'sort', 'create_date', 'update_date')
    autocomplete_fields = ['parent']
    # 可点击跳到编辑的字段
    list_display_links = ('name',)
    search_fields = ['name','parent__name']
    # 列表过滤条件
    list_filter = ('create_date',)


class WebStackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'menu_item', 'is_show', 'sort', 'create_date', 'update_date')
    # 可点击跳到编辑的字段
    list_display_links = ('name',)
    autocomplete_fields = ['menu_item']


admin.site.register(FirstLevelMenuItem, FirstLevelMenuItemAdmin)
admin.site.register(SecondLevelMenuItem, SecondLevelMenuItemAdmin)
admin.site.register(WebStack, WebStackAdmin)
