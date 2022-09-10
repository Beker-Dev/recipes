# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

from .enviroment import BASE_DIR


LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

# install gettext here: https://www.gnu.org/software/gettext/
LOCALE_PATHS = [
    BASE_DIR / 'locale'
]
