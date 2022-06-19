# -*- coding: utf-8 -*-
import os
from lms.envs.devstack import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "host": "mongodb",
    "port": 27017,
    
    "user": None,
    "password": None,
    
    "db": "openedx",
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

CONTACT_MAILING_ADDRESS = "My Open edX - http://local.overhang.io"

DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)

import warnings
from django.utils.deprecation import RemovedInDjango40Warning, RemovedInDjango41Warning
warnings.filterwarnings("ignore", category=RemovedInDjango40Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango41Warning)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="lms.djangoapps.course_wiki.plugins.markdownedx.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.overhang.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "TIiJYaNu9DR8x60LNUO61gpv"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "EYNohXlvI1Dj9K74xPTtZbeb7RmSx9Nbo8TySgf13oXD3jMFpTYirs9dfitjIiyX8NafeigCTvjFe2Bu2ZLcjAHBFtxvMT9f8x-f9UV6_ln6LAUNyNxNIYO2eJuYw1upj2ia1z6bQkLXFB3ewd7yVXTRi_Ug0GyEH-75cRe-UyioIHf11JCdpL4eZIhxRueZCrnUO_cRyYZ3sQRLJlcVSuOAJ2lWAaAZtz1QWp5uoHgn1r2BpC3NkQEMS40bZeg1P-gAuWXNi4VMhG89KBUOsqNJrvECB-9GIIddSNClV_-KJLshKB8BKgdhmBnniHbackOSnuf7y2g6WTaTh2zkjQ",
        "n": "ycUuuvxcHCxXG1YLM9o2niQfFYLuWq_7o_M4xTb3fl_rTAcafqx99g51qX-qNFOH5_5k4w_5eUOuuyn5vrADMHWY7Pb6sqSKRZnBtgjgpdXEAsFekfLnWj8jf9WUK6wQyhI8ytlXrrqZGTjPiuN_8HsVY43_NvxyawWTI_0A6w6jKxgBWZ1wIeqyUc9LoE64i_w5XQZM0WjcnEwpYDtp9ZrFsVnFN-pXs44U2-ph0DChOoyB9WkzVfVikwkXCyqoD7bRPmHlJTtJT_WoCQWAKhXqLQ05UxSEKwSZ_D3kcSNZvzecwvMS8xEeC0xPm4ifpzRLK5gg20vavRfBZUnB7w",
        "p": "3ZZsdeX4EK1HYoe-hUu4VdLadEKYZqHBQyntt6FH2aaDnVAr5dcscGd_plvgkzsMAwvxF7SjTQSzn6ZDupLXd7b9AiNqEgZQsxVZrzzxwRbj0N3BhjY8_s9OPYSJq0ywddrNcPQKvTlurcRNvUp70OFI55_qoZhEghmeYwW4xf0",
        "q": "6RrjSkN-wDf2RM0-45EZhungRQ5mWYwaH1qnKWuBVwVzxatYPyVsRmsVrEUYChTCUTtCig_Vr0mOY2D-7CRG5V3G_TFmn_XQJVQGQ9kNB0BKF_MH4Zp6C_ipNMoQET2cWqpqfb9fziEd92wfPNyWUZG80Nvp3BXpf2lPng12NVs",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "ycUuuvxcHCxXG1YLM9o2niQfFYLuWq_7o_M4xTb3fl_rTAcafqx99g51qX-qNFOH5_5k4w_5eUOuuyn5vrADMHWY7Pb6sqSKRZnBtgjgpdXEAsFekfLnWj8jf9WUK6wQyhI8ytlXrrqZGTjPiuN_8HsVY43_NvxyawWTI_0A6w6jKxgBWZ1wIeqyUc9LoE64i_w5XQZM0WjcnEwpYDtp9ZrFsVnFN-pXs44U2-ph0DChOoyB9WkzVfVikwkXCyqoD7bRPmHlJTtJT_WoCQWAKhXqLQ05UxSEKwSZ_D3kcSNZvzecwvMS8xEeC0xPm4ifpzRLK5gg20vavRfBZUnB7w",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.overhang.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "TIiJYaNu9DR8x60LNUO61gpv"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}


######## End of settings common to LMS and CMS

######## Common LMS settings
LOGIN_REDIRECT_WHITELIST = ["studio.local.overhang.io"]

# Better layout of honor code/tos links during registration
REGISTRATION_EXTRA_FIELDS["terms_of_service"] = "required"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "hidden"

# Fix media files paths
PROFILE_IMAGE_BACKEND["options"]["location"] = os.path.join(
    MEDIA_ROOT, "profile-images/"
)

COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

# Email settings
DEFAULT_EMAIL_LOGO_URL = LMS_ROOT_URL + "/theming/asset/images/logo.png"

# Create folders if necessary
for folder in [DATA_DIR, LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)


FEATURES["PERSISTENT_GRADES_ENABLED_FOR_ALL_TESTS"] = True


######## End of common LMS settings

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

LMS_BASE = "local.overhang.io:8000"
LMS_ROOT_URL = "http://{}".format(LMS_BASE)
LMS_INTERNAL_ROOT_URL = LMS_ROOT_URL
SITE_NAME = LMS_BASE
CMS_BASE = "studio.local.overhang.io:8001"
CMS_ROOT_URL = "http://{}".format(CMS_BASE)
LOGIN_REDIRECT_WHITELIST.append(CMS_BASE)

# Session cookie
SESSION_COOKIE_DOMAIN = "local.overhang.io"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"

# CMS authentication
IDA_LOGOUT_URI_LIST.append("http://studio.local.overhang.io:8001/complete/logout")

FEATURES['ENABLE_COURSEWARE_MICROFRONTEND'] = False

LOGGING["loggers"]["oauth2_provider"] = {
    "handlers": ["console"],
    "level": "DEBUG"
}



ACCOUNT_MICROFRONTEND_URL = "http://apps.local.overhang.io:1997/account"


WRITABLE_GRADEBOOK_URL = "http://apps.local.overhang.io:1994/gradebook"


LEARNING_MICROFRONTEND_URL = "http://apps.local.overhang.io:2000/learning"


PROFILE_MICROFRONTEND_URL = "http://apps.local.overhang.io:1995/profile/u/"



# account MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:1997")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:1997")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:1997")

# gradebook MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:1994")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:1994")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:1994")

# learning MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:2000")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:2000")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:2000")

# profile MFE
CORS_ORIGIN_WHITELIST.append("http://apps.local.overhang.io:1995")
LOGIN_REDIRECT_WHITELIST.append("apps.local.overhang.io:1995")
CSRF_TRUSTED_ORIGINS.append("apps.local.overhang.io:1995")
