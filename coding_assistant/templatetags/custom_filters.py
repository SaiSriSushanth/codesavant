from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiplies the value by the argument
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter(name='modulo')
def modulo(value, arg):
    """
    Returns the remainder of value divided by arg
    """
    try:
        return int(value) % int(arg)
    except (ValueError, TypeError):
        return 0