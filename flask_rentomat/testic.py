from flask import Flask
from flask_babel import Babel
from flask_babel import gettext, ngettext
from flask import g, request

babel = Babel()


LANGUAGES = {
    'en': 'English',
    'sr' : 'Srpski',
    'ru' : 'Russian'
}








def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(['en', 'sr', 'ru'])

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

app = Flask(__name__)
babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)


nesto = gettext(u'A simple string')
gettext(u'Value: %(value)s', value=42)

print(nesto)


