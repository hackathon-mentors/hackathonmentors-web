from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView

from hackathonmentors.views import HackathonMentorsMixin
from hackathon.models import Hackathon

from slugify import slugify


class HackathonListView(HackathonMentorsMixin, ListView):
    model = Hackathon
    context_object_name = 'hackathons'
    paginate_by = 25  # NOTE: TBD
    template_name = "hackathon/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return super().get_queryset().filter(verified=True)


class HackathonDetailsView(HackathonMentorsMixin, DetailView):
    model = Hackathon
    template_name = "hackathon/view.html"
    context_object_name = 'hackathon'


class HackathonCreateView(HackathonMentorsMixin, CreateView):
    model = Hackathon
    fields = [
        "name",
        "location",
        "is_remote",
        "starts",
        "ends",
    ]
    template_name = "hackathon/add.html"

    def validate(self, form):
        pass

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # TODO: add duplicate name validation

        self.object.slug = self.generate_slug()
        self.object.added_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('hackathon_view', args=[self.object.slug])

    def generate_slug(self):
        slug = slugify(self.object.name)
        if self.model.objects.filter(slug=slug).exists():
            # TODO: handle duplicate slug
            pass
        return slug


class HackathonDeleteView(HackathonMentorsMixin, CreateView):
    model = Hackathon
