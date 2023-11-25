from django import template

register = template.Library()
@register.filter()
def mymedia(value):
    if value:
        return f'/media/{value}'
    return f'/media/images/pngtree-a-carton-package-goods-commodity-png-image_356642.jpg'