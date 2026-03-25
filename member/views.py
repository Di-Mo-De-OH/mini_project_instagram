from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import FormView
from member.forms import SignUpForm


# Create your views here.
class SignUpView(FormView):
    template_name = "auth/signup.html"
    form_class = SignUpForm


    def form_valid(self,form):
        user = form.save()
        return render(
            self.request,
            template_name = "accounts/signup.done.html",
        )