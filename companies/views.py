from django.views.generic import CreateView, ListView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Company 
from .forms import CompanyForm
from rest_framework import viewsets
from .serializers import  CompanySerializer
from rest_framework import generics
class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/company_form.html"
    success_url = "/companies/companylist" # change this to your desired url

class CompanyListView(ListView):
    model = Company
    template_name = "companies/company_list.html"
    
class CompanyAPIView(generics.ListAPIView):
  queryset = Company.objects.all()
  serializer_class = CompanySerializer
  
def edit_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect(reverse('companylist'))
    else:
        form = CompanyForm(instance=company)
    return render(request, 'companies/edit_company.html', {'form': form})