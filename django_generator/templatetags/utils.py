from django.template.defaultfilters import register, safe


@register.filter
def pop_relations(model):
    text = ""
    for field in model.get_fields():
        if field.__class__.__name__ == "ManyToOneRel" or field.__class__.__name__ == "ManyToManyRel":
            text += "        " + field.name + "_data = validated_data.pop('" + field.name + "_set',None)\n"
            text += "        " + field.name + "_data = self.context['request'].data.get('" + field.name + "_set',None)\n"
        elif field.__class__.__name__ == "ForeignKey" or field.__class__.__name__ == "ManyToManyField" or field.__class__.__name__ == "OneToOneField" or field.__class__.__name__ == "OneToOneRel":
            text += "        " + field.name + "_data = validated_data.pop('" + field.name + "',None)\n"
            text += "        " + field.name + "_data = self.context['request'].data.get('" + field.name + "',None)\n"
    return safe(text)


@register.filter
def pre_create_inserts(model):
    text = ""
    for field in model.get_fields():
        if (field.__class__.__name__ == "ForeignKey" or field.__class__.__name__ == "OneToOneField") and not field.null:
            text += "        " + field.related_model.__name__.lower() + " = " + field.related_model.__name__ + ".objects.get_or_create(id = " + field.name + "_data.get('id',None),defaults={**" + field.name + "_data})[0]\n"
    return safe(text)


@register.filter
def create_object(model):
    text = "serializer_object = " + model.__class__.__name__ + ".objects.create("
    for field in model._meta.get_fields():
        if (field.__class__.__name__ == "ForeignKey" or field.__class__.__name__ == "OneToOneField") and not field.null:
            text += field.name + " = " + field.related_model.__name__.lower() + ","
    text += "**validated_data)\n"

    return safe(text)


@register.filter
def many_add(model, field):
    for field2 in field.related_model._meta.get_fields():
        # print(vars(field2))
        if field2.is_relation and field2.related_model.__name__ == model.__class__.__name__:
            if field.__class__.__name__ == "ManyToManyField":
                return field.related_model.__name__.lower() + "." + field2.name + "_set.add(serializer_object)"
            else:
                return field.related_model.__name__.lower() + "." + field2.name + ".add(serializer_object)"


@register.filter
def get_field_name(field):
    if field.__class__.__name__ == "ManyToManyRel" or field.__class__.__name__ == "ManyToOneRel":
        return field.name + "_set"
    else:
        return field.name


@register.filter
def get_type(field):
    types = {
        "CharField": "string",
        "IntegerField": "number",
        "BooleanField": "boolean",
        "EmailField": "string",
        "FloatField": "number",
        "TextField": "string",
    }
    if hasattr(field, "primary_key") and field.primary_key:
        return "number"
    elif field.__class__.__name__ in types:
        # print(vars(field))
        return types[field.__class__.__name__]
    elif field.__class__.__name__ == "ManyToOneRel" or field.__class__.__name__ == "ManyToManyField" or field.__class__.__name__ == "ManyToManyRel":
        return field.related_model.__name__ + "[]"
    elif field.__class__.__name__ == "ForeignKey" or field.__class__.__name__ == "OneToOneRel" or field.__class__.__name__ == "OneToOneField":
        return field.related_model.__name__
    else:
        print(field.__class__.__name__)
        return "any"


@register.filter
def get_default_values(field):
    types = {
        "CharField": "''",
        "IntegerField": "0",
        "BooleanField": "false",
        "EmailField": "''",
        "FloatField": "0",
        "TextField": "''",
    }
    if hasattr(field, "primary_key") and field.primary_key:
        return "0"
    elif field.__class__.__name__ in types:
        return types[field.__class__.__name__]
    elif field.__class__.__name__ == "ManyToOneRel" or field.__class__.__name__ == "ManyToManyField" or field.__class__.__name__ == "ManyToManyRel":
        return "[new " + field.related_model.__name__ + "(true)]"
    elif field.__class__.__name__ == "ForeignKey" or field.__class__.__name__ == "OneToOneRel" or field.__class__.__name__ == "OneToOneField":
        return "new " + field.related_model.__name__ + "(true)"
    else:
        print(field.__class__.__name__)
        return "''"


@register.filter
def get_app_name(value):
    return value.__module__.split(".")[0]
