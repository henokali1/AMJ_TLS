from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
import json
from .models import Client, ReportTemplate
from .forms import ClientForm
from .utils import generate_medical_certificate

def view_certificate(request, client_pk):
    client = get_object_or_404(Client, pk=client_pk)
    template = ReportTemplate.objects.filter(is_active=True).first()
    
    if not template:
        return render(request, 'medical/error.html', {'message': 'No active template found. Please create and activate a template first.'})
    
    cert_url = generate_medical_certificate(client, template)
    return redirect(cert_url)

class ClientListView(ListView):
    model = Client
    template_name = 'medical/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(client_name__icontains=search_query) |
                Q(passport_no__icontains=search_query)
            )
        return queryset.order_by('-date')

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'medical/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'medical/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'medical/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

class TemplateListView(ListView):
    model = ReportTemplate
    template_name = 'medical/template_list.html'
    context_object_name = 'templates'

class TemplateCreateView(CreateView):
    model = ReportTemplate
    fields = ['name', 'template_image', 'font_size', 'is_active']
    template_name = 'medical/template_form.html'
    success_url = reverse_lazy('template_list')

class TemplateUpdateView(UpdateView):
    model = ReportTemplate
    fields = ['name', 'template_image', 'font_size', 'is_active']
    template_name = 'medical/template_form.html'
    success_url = reverse_lazy('template_list')

class TemplateDeleteView(DeleteView):
    model = ReportTemplate
    template_name = 'medical/template_confirm_delete.html'
    success_url = reverse_lazy('template_list')

class CoordinateFinderView(DetailView):
    model = ReportTemplate
    template_name = 'medical/coordinate_finder.html'
    context_object_name = 'template'

    def post(self, request, *args, **kwargs):
        template = self.get_object()
        data = json.loads(request.body)
        
        template.name_x = data.get('name_x', template.name_x)
        template.name_y = data.get('name_y', template.name_y)
        template.passport_x = data.get('passport_x', template.passport_x)
        template.passport_y = data.get('passport_y', template.passport_y)
        template.age_x = data.get('age_x', template.age_x)
        template.age_y = data.get('age_y', template.age_y)
        template.date_x = data.get('date_x', template.date_x)
        template.date_y = data.get('date_y', template.date_y)
        template.photo_x1 = data.get('photo_x1', template.photo_x1)
        template.photo_y1 = data.get('photo_y1', template.photo_y1)
        template.photo_x2 = data.get('photo_x2', template.photo_x2)
        template.photo_y2 = data.get('photo_y2', template.photo_y2)
        
        template.save()
        return JsonResponse({'status': 'success'})
