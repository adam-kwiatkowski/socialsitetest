from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import modelformset_factory, modelform_factory

from .forms import PostForm, ImageForm
from .models import Post, Image

class PostList(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    queryset = Post.objects.all().order_by('-pub_date')
    template_name = 'posts/index.html'

    ImageFormSet = modelformset_factory(Image, form=ImageForm)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['formset'] = self.ImageFormSet(queryset=Image.objects.none())
        return context


@login_required
@never_cache
def profile_view(request):
    return render(request, 'posts/profile.html')


class Profile(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-pub_date')

    template_name = 'posts/profile.html'


@login_required
def create_post(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm)

    if request.method == 'POST':
        form = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if form.is_valid() and formset.is_valid():
            
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.likes = 0
            post.save()
            
            images = formset.save(commit=False)

            for image in images:
                image.post = post
                image.author = post.author
                image.save()

    return redirect('home')