#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ian Mortimer'
SITENAME = u'ianmorty.co.uk'
SITEURL = 'https://ianmorty.co.uk'
SITESUBTITLE = "Ian Mortimer"
SITELOGO = "/img/ian_profile_picture.jpg"

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/ianmorty'),
          ('github', 'https://github.com/ianmorty'),
          ('rss', '//ianmorty.co.uk/feeds/all.atom.xml'),
          ('linkedin', 'https://br.linkedin.com/in/ianmortimer/en'),)

TWITTER_USERNAME = "ianmorty"

DEFAULT_PAGINATION = 10

MAIN_MENU = True

MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

COPYRIGHT_YEAR = 2016

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
THEME = "/home/ian/pelican-themes/Flex"

STATIC_PATHS = ['img','pages']
