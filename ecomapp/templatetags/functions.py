from django import template

register = template.Library()


@register.filter(name="split")
def split(value):
    z = " ".join(value.split()[:3])
    return "{}".format(z)
