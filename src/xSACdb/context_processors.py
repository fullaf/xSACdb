import json

from django.conf import settings
from django.urls import resolve, Resolver404

from xSACdb import environment, version
from xSACdb.roles.functions import *
from xsd_frontend.forms import UpdateRequestMake
from xsd_members.forms import MyUserAccountForm


def xsd_vars(request):
    # General template variables used by our templates

    try:
        current_url = resolve(request.path)
        if len(current_url.namespaces) > 0:
            namespace = current_url.namespaces[0]
        else:
            namespace = None
    except Resolver404:
        current_url = None
        namespace = None

    global_obj = {
        'env': {
            'name': environment.get_environment_name(),
            'release': version.get_release(),
            'sentryRelease': version.get_sentry_release(),
        },
        'site': {
            'name': settings.CLUB['name'],
        },
        'sentry': {
            'dsn': settings.RAVEN_CONFIG.get('dsn_public', None),
        },
        'user': None,
    }

    context = {
        'current_url': current_url,
        'namespace': namespace,

        'l10n_club': settings.CLUB,

        'DEBUG': settings.DEBUG,
        'BROWSER_THEME_COLOUR': settings.BROWSER_THEME_COLOUR,
    }

    if request.user.is_authenticated:
        # Only if user is logged in

        # TODO remove when we have a ticket framework
        update_request_form = UpdateRequestMake()
        my_user_account_form = MyUserAccountForm()

        global_obj['user'] = {
            'id': request.user.pk,
            'username': request.user.username,
            'email': request.user.email,
        }

        context.update({
            'profile': request.user.memberprofile,

            'update_request_form': update_request_form,
            'my_user_account_form': my_user_account_form,

            'is_verified': is_verified(request.user),
            'is_training': is_training(request.user),
            'is_trips': is_trips(request.user),
            'is_sites': is_sites(request.user),
            'is_members': is_members(request.user),
            'is_diving_officer': is_diving_officer(request.user),
            'is_admin': is_admin(request.user),
            'is_trusted': is_trusted(request.user),
        })

    context.update({
        'global_json': json.dumps(global_obj),
    })

    return context
