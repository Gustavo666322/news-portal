from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

BAD_WORDS = ['редиска', 'плохой']

@register.filter(name='censor')
@stringfilter
def censor(value):
    result = value
    for word in BAD_WORDS:
        word_lower = word.lower()
        if word_lower in result.lower():
            censored_word = word_lower[0] + '*' * (len(word_lower) - 1)
            result = result.replace(word_lower, censored_word)
            result = result.replace(word_lower.title(), censored_word)
    return result