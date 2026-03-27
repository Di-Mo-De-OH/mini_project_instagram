from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse
from post.forms import PostCreateForm,PostImageFormSet
from django.shortcuts import render
from post.models import Post

# Create your views here.
class PostListView(ListView):
    queryset = Post.objects.all().select_related("user").prefetch_related("images")
    template_name = "post/list.html"
    paginate_by = 5
    ordering = ("-created_at",)

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = "post/form.html"
    form_class = PostCreateForm

    def get_context_data(self,**kwargs):
        data = super().get_context_data(**kwargs)
        data["formset"] =PostImageFormSet()
        return data

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        image_formset = PostImageFormSet(self.request.POST,self.request.FILES,instance = self.object)
        if image_formset.is_valid():
            image_formset.save()
        return HttpResponseRedirect(reverse("main"))


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = "post/form.html"
    form_class = PostCreateForm

    def get_context_data(self,**kwargs):
        data = super().get_context_data(**kwargs)
        data["formset"] =PostImageFormSet(instance=self.object)
        return data

    def form_valid(self,form):
        self.object = form.save(commit=False)
        image_formset = PostImageFormSet(self.request.POST,self.request.FILES,instance = self.object)
        if image_formset.is_valid():
            image_formset.save()
        return HttpResponseRedirect(reverse("main"))

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)