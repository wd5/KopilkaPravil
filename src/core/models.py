# -*- coding: utf-8 -*-

from datetime import datetime
from BeautifulSoup import BeautifulSoup, Comment as HtmlComment

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from yafotki.fields import YFField


def sanitizeHTML(value, mode='none'):
    """ Удаляет из value html-теги.
        Если mode==none - все теги
        Если mode==strict - все теги кроме разрешенных
    """
    if mode == 'strict':
        valid_tags = 'ol ul li p i strong b u a h1 h2 h3 pre br div span img blockquote youtube object param embed iframe'.split()
    else:
        valid_tags = []
    valid_attrs = 'href src pic user page class text title alt'.split()
    # параметры видеороликов
    valid_attrs += 'width height classid codebase id name value flashvars allowfullscreen allowscriptaccess quality src type bgcolor base seamlesstabbing swLiveConnect pluginspage data frameborder'.split()

    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, HtmlComment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        tag.attrs = [(attr, val) for attr, val in tag.attrs
                                 if attr in valid_attrs]
    result = soup.renderContents().decode('utf8')
    return result


class Game(models.Model):
    author = models.ForeignKey(User, verbose_name=u"Автор")
    month = models.PositiveIntegerField(verbose_name=u"Месяц")
    year = models.PositiveIntegerField(verbose_name=u"Год")
    title = models.CharField(max_length=255, verbose_name=u"Название")
    GAME_TYPES = (
        (u'кабинетная', 1),
        (u'в городе', 2),
        (u'на базе', 3),
        (u'на полигоне', 4),
    )
    type = models.IntegerField(choices=GAME_TYPES, verbose_name=u"Тип")
    description = models.TextField(verbose_name=u"Описание", null=True, blank=True, default=None)

    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.year)

    class Meta:
        verbose_name = u"Игра"
        verbose_name_plural = u"Игры"


class RuleCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Название")

    class Meta:
        verbose_name = u"Категория правил"
        verbose_name_plural = u"Категории правил"


class Rule(models.Model):
    author = models.ForeignKey(User, verbose_name=u"Автор")
    game = models.ForeignKey(Game, verbose_name=u"Игра")
    category = models.ForeignKey(RuleCategory, verbose_name=u"Тип")
    description = models.TextField(verbose_name=u"Краткое описание", null=True, blank=True, default=None)
    context = models.TextField(verbose_name=u"Содержание")
    dt = models.DateTimeField(verbose_name=u"Дата добавления")

    def __save__(self, *args, **kwargs):
        if not self.dt:
            self.dt = datetime.now()

        super(Rule, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Правило"
        verbose_name_plural = u"Правила игр"


class RuleHistory(models.Model):
    rule = models.ForeignKey(Rule, verbose_name=u"Правила")
    context = models.TextField(verbose_name=u"Содержание")
    dt = models.DateTimeField(verbose_name=u"Дата добавления")

    def __save__(self, *args, **kwargs):
        if not self.dt:
            self.dt = datetime.now()

        super(RuleHistory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Предыдущая редакция"
        verbose_name_plural = u"История изменений"