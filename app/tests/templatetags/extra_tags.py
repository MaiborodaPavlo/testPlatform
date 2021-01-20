from django import template

register = template.Library()


@register.filter
def right_answers_count(test, user_id):
    """Returns right_answers value.
    Usage::

        {% if test|right_answers_count:user_id %}
        ...
        {% endif %}
    """
    try:
        return test.results.get(user_id=user_id).right_answers
    except test.DoesNotExist:
        return 0


@register.simple_tag
def proportion(_max, current):
    return 100 * current / _max
