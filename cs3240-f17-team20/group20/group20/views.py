class ProviderRegisterView(SignupView):
    template_name = 'account/form_provider.html'
    form_class = ProviderForm
    redirect_field_name = 'next'
    view_name = 'registerprovider'
    success_url = None

    def get_context_data(self, **kwargs):
        ret = super(ProviderRegisterView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret

registerprovider = ProviderRegisterView.as_view()


#View para el formulario de registro de usuarios clientes
class ClientRegisterView(SignupView):

    template_name = 'account/form_client.html'
    form_class = ClientForm
    redirect_field_name = 'next'
    view_name = 'registerclient'
    success_url = None

    def get_context_data(self, **kwargs):
        ret = super(ClienteRegisterView, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret

registerclient = ClienteRegisterView.as_view()
