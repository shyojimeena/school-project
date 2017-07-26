import uuid

from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, RedirectView, TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Prefetch
from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import SetHeadlineMixin

from django.contrib.auth.models import User

from .models import UserProfile,SavedResource, TopicFollow
from courses.models import Resource
from comments.models import Comment
from .forms import UserForm, UserProfileForm

# user list
class UsersView(TemplateView):
    template_name = 'authapp/users.html'

    def get_context_data(self,**kwargs):
        context = super(UsersView,self).get_context_data(**kwargs)
        context['object_list'] = User.objects.all()
        return context



class UserProfileView(DetailView):
    template_name = 'authapp/user_profile.html'
    model = UserProfile
    context_object_name = 'profile'
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get_queryset(self):
        queryset = self.model.objects.select_related(
            'user', 'user__blog').prefetch_related('user__posts')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        userprofile = get_object_or_404(UserProfile, user=user) #redundancy check for user may exist but his profile not
        saved_resources = SavedResource.objects.filter(user=user)
        topics_follow = TopicFollow.objects.filter(user=user)
        context['userprofile'] = userprofile
        context['saved_resources'] = saved_resources
        context['topics_follow'] = topics_follow
        return context    


@login_required
def profile_redirector(request):
    return redirect('authapp:profile', username=request.user.username)


class UserComments(SingleObjectMixin, ListView):
    template_name = 'authapp/user_comments.html'
    model = UserProfile
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=self.model.objects.select_related(
                'user', 'user__blog').prefetch_related(
                    Prefetch(
                        'user__comments',
                        queryset=Comment.objects.select_related(
                            'post').filter(is_public=True)
                    ),
                    'user__posts')
            )
        return super(UserComments, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserComments, self).get_context_data(**kwargs)
        context['profile'] = self.object
        context['comments'] = self.get_queryset()
        return context

    def get_queryset(self):
        qs = self.object.user.comments.all()
        return qs


class UserProfileUpdateView(UpdateView):

    template_name = 'authapp/edit_profile.html'
    form_class = UserForm
    form_class_2 = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.request.user)
        if 'form2' not in context:
            context['form2'] = self.form_class_2(instance=self.request.user.profile)  # noqa
        return context

    def get(self, request, *args, **kwargs):
        super(UserProfileUpdateView, self).get(request, *args, **kwargs)
        self.object = self.get_object()
        form = self.form_class(instance=self.request.user)
        form2 = self.form_class_2(instance=self.request.user.profile)

        return self.render_to_response(self.get_context_data(
            form=form, form2=form2
        ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.request.user)
        form2 = self.form_class_2(request.POST, request.FILES,
                                  instance=self.request.user.profile)

        if form.is_valid() and form2.is_valid():
            form.save()
            data = form2.save(commit=False)
            if request.FILES.get('avatar', None):
                data.avatar = request.FILES['avatar']
                data.avatar.name = '{0}_p.jpg'.format(str(uuid.uuid4()))
            data.save()
            return redirect('authapp:user_profile')
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2)
                )

    def get_object(self, queryset=None):
        return self.request.user





# Newly added views


class UserInfoMixin(object):
    def get_context_data(self,**kwargs):
        context = super(UserInfoMixin, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        context['userinfo'] = user
        return context


class UserResourcesView(SetHeadlineMixin, UserInfoMixin, ListView):
    context_object_name = 'resources'
    template_name = 'authapp/user_resources.html'
    paginate_by = 12

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        self.headline = unicode(user.username) + ' shared Resources'
        return user.resource_set.all()

class MyResourcesView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        user = self.request.user
        return reverse('user_resources', kwargs={'username':user.username})