from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import SignUpForm
from logging import getLogger

logger = getLogger('accounts')

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name ='registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"New user registered - Username: {form.cleaned_data['username']}, Email: {form.cleaned_data['email']}")
        return response

    def form_invalid(self, form):
        logger.warning(f"User registration failed - Errors: {form.errors}")
        return super().form_invalid(form)
