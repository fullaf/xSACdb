

import reversion
from actstream import action
from django.utils.functional import cached_property
from reversion.signals import post_revision_commit

from xsd_frontend.versioning import XSDVersion


class DoAction:
    """Wrapper for things that do things to record the doing of the thing."""

    def __enter__(self):
        self.action = {}
        self.revision = {}
        post_revision_commit.connect(self.post_revision_commit)
        return self

    def set(self, **kwargs):
        self.action = kwargs

        if 'actor' not in kwargs:
            raise ValueError("You need an actor")

        # If in a reversion block, set comment
        if reversion.is_active() and 'verb' in kwargs:
            reversion.set_comment(kwargs['verb'])
            reversion.set_user(self.action['actor'])

    def post_revision_commit(self, **kwargs):
        self.revision = kwargs

    @property
    def actor(self):
        if not 'actor' in self.action:
            print((self.action))
            raise RuntimeError("Missing actor from action set")
        return self.action['actor']

    @property
    def verb(self):
        return self.action['verb']

    @property
    def action_object(self):
        return self.action.get('action_object', None)

    @property
    def target(self):
        return self.action.get('target', None)

    @property
    def style(self):
        return self.action.get('style', None)

    @property
    def revision_pk(self):
        if 'revision' in self.revision:
            return self.revision['revision'].pk
        else:
            return None

    @property
    def version_pks(self):
        if 'versions' in self.revision:
            return [v.pk for v in self.revision['versions']]
        else:
            return None

    def version_pks_for_object(self, object):
        if 'versions' in self.revision:
            return [v.pk for v in self.revision['versions'] if v.object == object]
        else:
            return None

    def __exit__(self, exception_type, exception_value, traceback):
        # Can handle multiple targets or action_objects. Just not both.
        post_revision_commit.disconnect(self.post_revision_commit)

        if exception_type:
            raise exception_type(exception_value)

        if self.action == {}:
            raise RuntimeError("You haven't called action.set in your action block")

        if isinstance(self.target, list):
            for target in self.target:
                action.send(self.actor, verb=self.verb, target=target, action_object=self.action_object,
                            style=self.style, revision_pk=self.revision_pk,
                            version_pks=self.version_pks_for_object(target))
        elif isinstance(self.action_object, list):
            for action_object in self.action_object:
                action.send(self.actor, verb=self.verb, target=self.target, action_object=action_object,
                            style=self.style, revision_pk=self.revision_pk,
                            version_pks=self.version_pks_for_object(action_object))
        else:
            action.send(self.actor, verb=self.verb, target=self.target, action_object=self.action_object,
                        style=self.style, revision_pk=self.revision_pk, version_pks=self.version_pks)


from actstream.models import Action


class XSDAction(Action):
    """Our proxy for Action to enable access to versions."""

    class Meta:
        proxy = True

    @cached_property
    def versions(self):
        if self.data and not isinstance(self.data, str) and self.data.get('version_pks', None) is not None:
            return list(XSDVersion.objects.in_bulk(self.data['version_pks']).values())
        else:
            return []
