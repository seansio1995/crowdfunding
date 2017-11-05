class ProviderForm(SignupForm,ModelForm):

    name = forms.CharField(label='Name', strip=True, max_length=50)
    lastname = forms.CharField(label='Last Name', strip=True, max_length=50)
    Provider.isProvider = True

    class Meta:
        model = Provider
        fields = '__all__'
        exclude = GENERAL_EXCLUSIONS + [
        'owner',
        ]

class ClientForm(SignupForm,ModelForm):

    name = forms.CharField(label='Name', strip=True, max_length=50)
    lastname = forms.CharField(label='Last Name', strip=True, max_length=50)

    class Meta:
        model = User
        fields = "__all__"
        exclude = GENERAL_EXCLUSIONS

    def is_active(self):
        return False

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
