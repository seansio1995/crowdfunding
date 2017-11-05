class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    provider = models.OneToOneField(Provider, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    SEX = (
        ("M","MALE"),
        ("F","FEMALE"),
    )

    birthdate = models.DateField(_('Birth Date'), default=django.utils.timezone.now, blank=False)
    sex = models.CharField(_('Sex'), choices=SEX, max_length=1, default="M")
    isProvider = models.BooleanField(_('Provider'), default=False)

class Provider(models.Model):

    HAS_BUSINESS = (
        ('YES','YES'),
        ('NO','NO'),
    )

#Resolving asociation 1:1 to User 
#NOTE: AUTH_USER_MODEL = users.User in setting
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    has_business = models.CharField(_('Do you have your own business?'),max_length=2, choices=HAS_BUSINESS, default='NO')
    isProvider = True
