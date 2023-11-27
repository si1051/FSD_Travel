from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView
from .forms import TripForm
from .models import Destination

User = get_user_model()

class HomeView(LoginRequiredMixin, TemplateView):
    redirect_field_name = 'account:home'
    template_name = 'destinations/dashboard.html'

    def get_context_data(self, **kwargs):
        obj_list = super(HomeView, self).get_context_data(**kwargs)
        qs = Destination.objects.all()
        user_results = qs.filter(users_on_trip=self.request.user)
        others_trips = qs.exclude(users_on_trip=self.request.user)
        obj_list['user_trips'] = user_results
        obj_list['other_users_trips'] = others_trips
        return obj_list

    def post(self, request, *args, **kwargs):
        # You can handle post requests if needed
        return render(request, self.template_name)

class DestinationDetailSlugView(DetailView):
    template_name = "destinations/trip_detail.html"

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = Destination.objects.get(slug=slug)
        except Destination.DoesNotExist:
            raise Http404("Not found..")
        except Destination.MultipleObjectsReturned:
            qs = Destination.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Something broke ")
        return instance

class AddDestinationFormView(LoginRequiredMixin, TemplateView):
    redirect_field_name = 'account:home'
    form_class = TripForm
    initial = {'key': 'value'}
    template_name = 'destinations/trip_add.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = Destination.objects.new(form, request.user)
            if instance:
                return redirect('travel:home')
            else:
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


def UpdateDestinationView(request):
    destination_id = request.POST.get('destination_id')
    is_planner = request.POST.get('planner')
    user = request.user

    if is_planner:
        try:
            destination_obj = Destination.objects.get(id=destination_id)
        except Destination.DoesNotExist:
            messages.error(request, "Destination does not exist.")
            return redirect('travel:home')
        if destination_obj:
            destination_obj.delete()
        return redirect('travel:home')

    if destination_id is not None:
        try:
            destination_obj = Destination.objects.get(id=destination_id)
        except Destination.DoesNotExist:
            messages.error(request, "Destination does not exist.")
            return redirect('travel:home')
        if destination_obj:
            qs = destination_obj.users_on_trip.filter(id=user.id).exists()
            if qs:
                destination_obj.users_on_trip.remove(request.user.id)
                added = False
            else:
                destination_obj.users_on_trip.add(request.user.id)
                added = True

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        json_data = {
            "added": added,
            "remove": not added,
        }
        return JsonResponse(json_data)

    return redirect('travel:home')