import random
import time

from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


# Create your models here.

def generate_id():
    return f"{int(time.time())}-{random.randint(10000, 99999)}"


# 菜单模型
class Menu(models.Model):
    name = models.CharField(verbose_name='名称', max_length=20)
    code = models.SlugField(unique=True, default=generate_id)
    icon = models.CharField(verbose_name='图标', max_length=100, help_text='Font Awesome图标库格式，如:fa fa-star-o')
    sort = models.IntegerField(verbose_name='顺序', default=100, help_text='自定义顺序')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 一级菜单项
class FirstLevelMenuItem(Menu):
    class Meta:
        verbose_name = '一级菜单项'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def has_webstack(self):
        '''判断一级菜单下是否有网站'''
        count = 0
        for second_level_menu in self.second_level_menus.all():
            count += WebStack.objects.filter(menu_item=second_level_menu, is_show=True).count()
        return count

    def get_second_level_menus(self):
        return SecondLevelMenuItem.objects.filter(parent=self).exclude(name=self.name).order_by('sort')


# 二级菜单项
class SecondLevelMenuItem(Menu):
    # 在父级菜单中获取所有的子级菜单，使用second_level_menus
    parent = models.ForeignKey(FirstLevelMenuItem, verbose_name='父级菜单', on_delete=models.PROTECT,
                               related_name='second_level_menus')

    class Meta:
        verbose_name = '二级菜单项'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def get_webstack_list(self):
        return WebStack.objects.filter(menu_item=self, is_show=True).order_by('sort')


# 网站
class WebStack(models.Model):
    name = models.CharField(verbose_name='名称', max_length=35)
    description = models.TextField(verbose_name='描述', max_length=100)
    url = models.URLField(verbose_name='网站地址')
    image = ProcessedImageField(upload_to='web/upload/%Y/%m/%d/',
                                default='web/default/default.png',
                                verbose_name='Logo图片',
                                processors=[ResizeToFill(120, 120)],
                                help_text='上传图片大小建议使用1:1的宽高比，为了清晰度原始图片宽度应该超过50px'
                                )
    sort = models.IntegerField(verbose_name='顺序', default=100, help_text='自定义顺序')
    enable_use = models.BooleanField(verbose_name='是否可用', default=True, blank=True, null=True)
    disable_use_reason = models.CharField('不可用原因', max_length=100, blank=True, null=True)
    is_show = models.BooleanField('是否展示', blank=True, null=True, default=True)
    menu_item = models.ForeignKey(SecondLevelMenuItem, verbose_name='所属二级菜单', on_delete=models.PROTECT,
                                  related_name='webstack_list')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        verbose_name = '网站'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.name
