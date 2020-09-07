from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView

from hackathonmentors.views import HackathonMentorsMixin
from mentor.forms import MentorRegistrationForm
from mentor.models import Mentor
from user.models import CustomUser as User


class MentorListView(HackathonMentorsMixin, ListView):
    model = Mentor
    context_object_name = 'mentors'
    paginate_by = 25  # NOTE: TBD
    template_name = "mentor/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MentorDetailsView(HackathonMentorsMixin, DetailView):
    model = Mentor
    template_name = "mentor/view.html"
    context_object_name = 'mentor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        user = User.objects.filter(username=slug)
        mentor = Mentor.objects.filter(user=user.first()) if user else None

        return mentor.first() if mentor else None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            self.template_name = "mentor/not_found.html"
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
class MentorRegistrationView(HackathonMentorsMixin, CreateView):
    model = Mentor
    form_class = MentorRegistrationForm
    template_name = "mentor/register.html"
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if existing := Mentor.objects.filter(user=request.user).first():
                if not existing.is_active:
                    messages.info(self.request, 'You already have a pending mentor application. Please wait until you have been approved!')
                    return redirect(reverse_lazy('user_dashboard'))
                else:
                    messages.info(self.request, 'You already have a mentor profile!')
                    return redirect(reverse_lazy('user_dashboard'))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, 'Your Registration has been submitted! You will be notified once you are approved.')
        return super().form_valid(form)
