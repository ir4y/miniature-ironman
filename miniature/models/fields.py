import sys
from funcy import walk_values, compose, merge
from django.db.models.fields import SlugField, Field
from django.db.models.signals import post_save
from django.dispatch import receiver
from pytils.translit import slugify

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^miniature\.models\.fields\.AutoSlugField"])
except ImportError:
    pass

if sys.version_info[0] == 3:
    unicode = str


class AutoSlugField(SlugField):
    def __init__(self, *args, **kwargs):
        self.populate_from = kwargs.pop('populate_from', '')
        kwargs['blank'] = True
        kwargs['null'] = True
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.set_attributes_from_name(name)
        self.model = cls
        cls._meta.add_field(self)

        @receiver(post_save, sender=cls, weak=False)
        def setup_slug(sender, instance, **kwargs):
            data = walk_values(compose(slugify, unicode),
                               instance.__dict__)
            related = {item: data['_{0}_cache'.format(item)]
                       for item in map(lambda u: u[0:-3],
                                       filter(lambda u: u.endswith('_id'),
                                              data.keys()))}
            data = merge(data, related)
            slug = self.populate_from.format(
                **data)[:self.max_length]
            if slug != getattr(instance, name):
                setattr(instance, name, slug)
                instance.save()


class DenormalizeField(Field):
    pass
