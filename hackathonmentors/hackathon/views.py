from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView

from hackathonmentors.views import HackathonMentorsMixin
from hackathon.models import Hackathon

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset
from slugify import slugify


class HackathonListView(HackathonMentorsMixin, ListView):
    model = Hackathon
    context_object_name = 'hackathons'
    paginate_by = 25  # NOTE: TBD
    template_name = "hackathon/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class HackathonEditView(HackathonMentorsMixin, UpdateView):
    model = Hackathon
    fields = [
        "name",
        "location",
        "is_remote",
        "starts",
        "ends",
        "link",
        "img"
    ]
    template_name = "hackathon/edit.html"
    context_object_name = 'hackathon'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

    def get_success_url(self):
        return reverse_lazy('hackathon_view', args=[self.object.slug])

    def validate(self, form):
        pass

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'name',
                'location',
                'is_remote'
            ),
            Field('starts', template="structure/datetimefield.html", data_date_format="dd-MM-yyyy HH:ii:ss"),
            Field('ends', template="structure/datetimefield.html", data_date_format="dd-MM-yyyy HH:ii:ss"),
        )
    

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
