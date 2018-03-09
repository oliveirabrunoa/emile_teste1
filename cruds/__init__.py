from flask import abort
import settings
import validators


def get_paginated_list(results, url, start, size, page_size=settings.PAGINATION_SIZE):
    # check if page exists
    count = size
    # make response
    obj = {}
    obj['start'] = start
    obj['page_size'] = page_size
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - page_size)
        page_size_copy = start - 1
        obj['previous'] = url + '?start=%d' % (start_copy)
    # make next url
    if start + page_size > count:
        obj['next'] = ''
    else:
        start_copy = start + page_size
        obj['next'] = url + '?start=%d' % (start_copy)
    # finally extract result according to bounds
    obj['results'] = results
    return obj


def format_urls_in_text(text):
    new_text = []

    accepted_protocols = ['http://', 'https://', 'ftp://', 'ftps://']

    for word in str(text).split():
        new_word = word
        accepted = [protocol for protocol in accepted_protocols if protocol in new_word]

        if not accepted:
            new_word = 'http://{0}'.format(new_word)

        if validators.url(new_word)==True:
            new_word = '<a href="{0}">{1}</a>'.format(new_word, word)
        else:
            new_word = word
        new_text.append(new_word)

    return ' '.join(new_text)
