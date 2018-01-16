from django.template.defaultfilters import register


@register.filter
def to_class_name(value):
    return value.__class__.__name__
