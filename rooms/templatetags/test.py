from django import template

register = template.Library()


@register.filter()
def test(value):
    print(value)
    return "custom filter test"
