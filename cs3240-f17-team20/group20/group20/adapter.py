#Per allauth documentation, settings changed:
#ACCOUNT_ADAPTER = 'projectname.users.adapters.RegisterUserAdapter'

class RegisterUserAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.first_name = data['name']
        user.last_name = data['lastname']
        #Saving Client info
        user.sex = data['sex']
        user.birthdate = data['birthdate']
        #Normal allauth saves
        user.username = data['username']
        user.email = data['email']
        if user.isProvider:
            p = Provider()
            p.owner = user
            p.has_business = data['has_business']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            #Save user
            user.save()
            #If it's also a Provider, save the Provider 
            if user.isProvider:
                p.save()
        return user
