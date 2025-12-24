from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import JsonResponse
import json
from .models import Client, ReportTemplate
from .forms import ClientForm, UserForm, UserEditForm
from django.contrib.auth.models import User
from .utils import generate_medical_certificate

@login_required
def view_certificate(request, client_pk):
    client = get_object_or_404(Client, pk=client_pk)
    template = ReportTemplate.objects.filter(is_active=True).first()
    
    if not template:
        return render(request, 'medical/error.html', {'message': 'No active template found. Please create and activate a template first.'})
    
    cert_url = generate_medical_certificate(client, template)
    
    if request.GET.get('format') == 'image':
        return redirect(cert_url)
        
    return render(request, 'medical/certificate_view.html', {
        'client': client,
        'cert_url': cert_url
    })

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'medical/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            search_query = self.request.GET.get('q')
            if search_query:
                queryset = queryset.filter(
                    Q(client_name__icontains=search_query) |
                    Q(passport_no__icontains=search_query)
                )
            return queryset.order_by('-pk')
        except Exception as e:
            print(f"Error in ClientListView: {e}")
            return Client.objects.none()

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'medical/client_form.html'
    template_name = 'medical/client_form.html'
    
    def get_success_url(self):
        return reverse('view_certificate', kwargs={'client_pk': self.object.pk})

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'medical/client_form.html'
    template_name = 'medical/client_form.html'

    def get_success_url(self):
        return reverse('view_certificate', kwargs={'client_pk': self.object.pk})

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'medical/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class TemplateListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ReportTemplate
    template_name = 'medical/template_list.html'
    context_object_name = 'templates'

class TemplateCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ReportTemplate
    fields = ['name', 'template_image', 'font_size', 'is_active']
    template_name = 'medical/template_form.html'
    success_url = reverse_lazy('template_list')

class TemplateUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ReportTemplate
    fields = ['name', 'template_image', 'font_size', 'is_active']
    template_name = 'medical/template_form.html'
    success_url = reverse_lazy('template_list')

class TemplateDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = ReportTemplate
    template_name = 'medical/template_confirm_delete.html'
    success_url = reverse_lazy('template_list')

class CoordinateFinderView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
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

class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'medical/user_list.html'
    context_object_name = 'users'

class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'medical/user_form.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'medical/user_form.html'
    success_url = reverse_lazy('user_list')
