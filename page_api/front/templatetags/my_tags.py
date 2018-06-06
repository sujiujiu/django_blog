# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.utils.html import format_html

register = template.Library() 

@register.filter
def haddle_time(time):
    if type(time) == datetime:
        now = datetime.now()
        # 帖子发布的时间距此刻时间的总秒数
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            return u'刚刚'
        elif timestamp > 60 and timestamp < 60*60:
            minutes = timestamp / 60
            return u'%s分钟前'% int(minutes)
        elif timestamp >60*60 and timestamp <60*60*24:
            hours = timestamp / (60*60)
            return u'%s小时前' % int(hours)
        elif timestamp >60*60*24 and timestamp <60*60*24*30:
            days = timestamp / (60*60*24)
            return u'%s天前' % int(days)
        elif now.year == time.year:
            return time.strftime('%m-%d %H:%M:%S')
        else:
            return time.strftime('%Y-%m-%d %H:%M:%S')