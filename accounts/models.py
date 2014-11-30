from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.urlresolvers import reverse

def get_profile(user):
    try:
        return user.profile
    except Profile.DoesNotExist:
        return Profile.objects.create(user=user)

# Create your models here.
class Profile(models.Model):
    LEVEL_NAMES = ('NOEMAIL', 'USER', 'MEMBER', 'MOD', 'ADMIN')
    LEVEL_CSS = ('muted', 'normal', 'success', 'warning', 'danger')
    user = models.OneToOneField(User)
    email_verified = models.BooleanField(default=False)

    @property
    def is_member(self):
        return KnownMemberEmail.objects.filter(email=self.user.email).exists()

    @property
    def access_level(self):
        if self.user.is_superuser:
            return 4
        elif False: # group moderator not implemented yet
            return 3
        elif self.email_verified:
            if self.is_member:
                return 2
            else:
                return 1
        else:
            return 0

    @property
    def level_name(self):
        return self.LEVEL_NAMES[self.access_level]

    @property
    def level_css(self):
        return self.LEVEL_CSS[self.access_level]

    @property
    def html_link(self):
        return format_html(
            '<a class="{class_}" href="{href}">{username}</a>',
            class_="text-" + self.level_css,
            href=reverse('profile', args=[self.user.username]),
            username = self.user.get_username(),
        )

class KnownMemberEmail(models.Model):
    email = models.EmailField(unique=True)

    @classmethod
    def load_csv(cls, path):
        import csv
        with open(path, newline='') as file:
            reader = csv.reader(file)

            first = next(reader)
            index = first.index('電子郵件')

            for row in reader:
                email = row[index].strip()
                obj, created = cls.objects.get_or_create(email=email)
                if created:
                    print('Added', email, 'to', cls.__name__)
