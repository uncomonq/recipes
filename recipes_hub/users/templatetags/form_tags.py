from django import template

register = template.Library()


@register.filter
def add_class(bound_field, css_classes):
    existing_classes = bound_field.field.widget.attrs.get("class", "")
    merged_classes = f"{existing_classes} {css_classes}".strip()
    return bound_field.as_widget(attrs={"class": merged_classes})
