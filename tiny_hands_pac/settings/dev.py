from .base import *


DEBUG = True

COMPRESS_ENABLED = True

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS += (
    'django_medusa',
    'wagtail.contrib.wagtailmedusa',
    )

# Medusa settings
MEDUSA_RENDERER_CLASS = 'django_medusa.renderers.DiskStaticSiteRenderer'
MEDUSA_DEPLOY_DIR = os.path.join(PROJECT_ROOT, 'static_build')
SENDFILE_BACKEND = 'sendfile.backends.simple'

SECRET_KEY = '7nn(g(lb*8!r_+cc3m8bjxm#xu!q)6fidwgg&$p$6a+alm+eex'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'trumphands',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Process all tasks synchronously.
# Helpful for local development and running tests
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True

try:
    from .local import *
except ImportError:
    pass
