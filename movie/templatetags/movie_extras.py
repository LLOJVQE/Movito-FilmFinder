
from django.utils.safestring import mark_safe

from django import template

register = template.Library()

@register.filter('hash')
def hash(h, key):
    if h:
        return h[key]
    else:
        return 0


@register.simple_tag
def action_all(current_url):
    """
    获取当前url，.../detail/tt000000-1/
    :param current_url:.../detail/tt000000-1/
    :return: all
    """
    url_part_list = current_url.split('-')

    if url_part_list[1].strip('/') == "50":
        temp = "<a href='%s' class='active'>ALL</a>"
    else:
        temp = "<a href='%s'>ALL</a>"

    url_part_list[1] = "50"

    href = '-'.join(url_part_list)

    temp = temp % (href,) #把链接填进去
    return mark_safe(temp)


@register.simple_tag
def action(current_url, item):
    # .../detail/tt000000-1/
    # item: genres_id genre_name
    url_part_list = current_url.split('-')

    if str(item['movie__genres']) == url_part_list[1].strip('/'):
        temp = "<a href='%s' class='active'>%s</a>"
    else:
        temp = "<a href='%s'>%s</a>"

    url_part_list[1] = str(item['movie__genres'])

    ur_str = '-'.join(url_part_list)  # 拼接整体url
    temp = temp % (ur_str, item['movie__genres__name'])  # 生成对应的a标签
    return mark_safe(temp)  # 返回安全的html