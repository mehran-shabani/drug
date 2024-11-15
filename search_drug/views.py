from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, Drug
from .forms import OrderForm, DrugPrescriptionForm
from .utils import create_prescription

@login_required
def create_order_with_search(request):
    """View to create order with drug search and prescription instructions."""
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        drug_forms = [DrugPrescriptionForm(request.POST, prefix=f"drug_{i}") for i in range(len(request.POST.getlist('drugs')))]

        if order_form.is_valid() and all([form.is_valid() for form in drug_forms]):
            order = order_form.save()
            medications = []

            for i, drug_form in enumerate(drug_forms):
                drug = Drug.objects.get(id=request.POST.getlist('drugs')[i])
                prescription_instruction = drug_form.cleaned_data['prescription_instruction'] or 'No instruction'
                medications.append(f"{drug.generic_name_eng} - {drug.drug_dose or 'Unknown dose'} - {prescription_instruction}")

            pdf_file = create_prescription(order.patient_first_name, order.patient_last_name,
                                           order.patient_national_code, order.disease_name, medications,
                                           verification_url=f"http://example.com/orders/{order.id}/verify")
            return JsonResponse({'message': 'Prescription created successfully!', 'pdf_url': pdf_file.url}, status=201)
    else:
        order_form = OrderForm()
        drug_forms = [DrugPrescriptionForm(prefix=f"drug_{i}") for i in range(1)]  

    return render(request, 'create_order.html', {'order_form': order_form, 'drug_forms': drug_forms})

@login_required
def search_drug(request):
    """AJAX view to search and return drugs matching a query."""
    query = request.GET.get('q', '')
    drugs = Drug.objects.filter(generic_name_eng__icontains=query)[:10]  # Limiting to top 10 results
    results = [{'id': drug.id, 'name': drug.generic_name_eng} for drug in drugs]
    return JsonResponse(results, safe=False)
