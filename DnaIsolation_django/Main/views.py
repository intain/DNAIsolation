import os

from django.db.models import Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . import forms, models
from django.contrib import messages


@login_required
def orders(request):
    ordersToDisplay = models.Order.objects.all()

    if request.method == 'POST':
        form = forms.OrderSearchForm(request.POST)
        if form.is_valid():
            commissioner = form.cleaned_data['commissioner']
            status = form.cleaned_data['status']

            if status == "Dowolny":
                ordersToDisplay = models.Order.objects.filter(
                    Q(commissioner__name__icontains=commissioner)
                )
            else:
                ordersToDisplay = models.Order.objects.filter(
                    Q(commissioner__name__icontains=commissioner) & Q(status__icontains=status)
                )

            messages.add_message(request, messages.SUCCESS, f'Znaleziono {ordersToDisplay.count()} rezultatów.')

            # return render(request, 'order_.html', {'search_results': objects})
    else:
        form = forms.OrderSearchForm()

    context = {
        'orders': ordersToDisplay,
        'search_form': form
    }

    return render(request, 'Main/orders.html', context)


@login_required
def orderSelectCompany(request):
    if request.method == 'POST':
        form = forms.CompanySelectForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data.get('selected_company')
            return redirect('order-create', pk=company.id)

    else:
        form = forms.CompanySelectForm()

    return render(request, 'Main/Orders/orderSelectCompany.html', {'company_select_form': form })


def linkFiles(order, request):
    for file in request.FILES.getlist('files'):
        linked_file = models.LinkedFile()
        linked_file.order = order
        linked_file.file = file
        linked_file.save()


@login_required
def orderCreate(request, pk):
    if request.method == 'POST':
        form = forms.OrderCreationForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            company = get_object_or_404(models.Company, pk=pk)
            order.commissioner = company
            linkFiles(order, request)
            order.save()

            messages.add_message(request, messages.SUCCESS, f'Pomyślnie dodano zamówienie.')
            return redirect('main-orders')
    else:
        form = forms.OrderCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'Main/Orders/orderCreate.html', context)


@login_required
def orderCreateNewCompany(request):
    if request.method == 'POST':
        order_form = forms.OrderCreationForm(request.POST, request.FILES, prefix='order')
        company_form = forms.CompanyCreateForm(request.POST, prefix='company')
        if order_form.is_valid() and company_form.is_valid():
            company = company_form.save()
            order = order_form.save()
            order.commissioner = company
            order.save()
            linkFiles(order, request)

            messages.add_message(request, messages.SUCCESS, f'Pomyślnie dodano zamówienie.')
            redirect('main-orders')
    else:
        order_form = forms.OrderCreationForm(prefix='order')
        company_form = forms.CompanyCreateForm(prefix='company')

    context = {
        'order_form': order_form,
        'company_form': company_form
    }

    return render(request, 'Main/Orders/orderCreateNewCompany.html', context)


@login_required
def orderDetailView(request, pk):
    order = get_object_or_404(models.Order, pk=pk)
    files = models.LinkedFile.objects.filter(order=order)

    for file in files:
        print(file.file.name)

    context = {
        "order": order,
        "files": files
    }

    return render(request, 'Main/Orders/orderDetails.html', context)


@login_required
def orderDeleteConfirm(request, pk):
    order = get_object_or_404(models.Order, pk=pk)

    context = {
        "order": order,
    }

    return render(request, 'Main/Orders/orderDeleteConfirm.html', context)


def deleteAttachedFiles(order):
    files_attached = models.LinkedFile.objects.filter(Q(order__number=order.number))
    for file in files_attached:
        removeFileObject(file)

@login_required
def orderDelete(request, pk):
    obj = get_object_or_404(models.Order, pk=pk)
    deleteAttachedFiles(obj)
    obj.delete()
    messages.add_message(request, messages.SUCCESS, 'Pomyślnie usunięto zlecenie')
    return redirect('main-orders')


@login_required
def orderEdit(request, pk):
    order = get_object_or_404(models.Order, pk=pk)
    form = forms.OrderEditForm(
        request.POST or None, instance=order, queryset=models.LinkedFile.objects.filter(Q(order__number=order.number)))

    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Pomyślnie zaktualizowano zlecenie.')
        selected_files = form.cleaned_data['files_to_delete']
        for file in selected_files:
            removeFileObject(file)

        linkFiles(order, request)

        return redirect(reverse('order-details', args=[pk]))

    context = {
        'form': form
    }

    return render(request, 'Main/Orders/orderEdit.html', context)


@login_required
def orderEditCompanyCheck(request, pk):
    order = get_object_or_404(models.Order, pk=pk)

    if request.method == 'POST':
        form = forms.CompanySelectForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data.get('selected_company')
            order.commissioner = company
            order.save()
            messages.add_message(request, messages.SUCCESS, 'Pomyślnie zaktualizowano zleceniodawcę.')
            return redirect(reverse('order-details', args=[pk]))

    else:
        form = forms.CompanySelectForm()

    return render(request, 'Main/Orders/orderEditCompanyCheck.html', {'company_select_form': form, 'company': order.commissioner})


@login_required
def orderEditCompany(request, pk):
    company = get_object_or_404(models.Company, pk=pk)

    form = forms.CompanyCreateForm(request.POST or None, instance=company)
    if form.is_valid():
        form.save()
        # redirect to a success page
        messages.add_message(request, messages.SUCCESS, 'Pomyślnie zaktualizowano zleceniodawcę.')
        return redirect('main-orders')

    context = {
        'form': form
    }

    return render(request, 'Main/companyEdit.html', context)

# *** MATERIALS ***


@login_required
def materials(request):
    materialsToDisplay = models.Material.objects.all()

    if request.method == 'POST':
        form = forms.MaterialSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            supplier_name = form.cleaned_data['supplier_name']

            materialsToDisplay = models.Material.objects.filter(
                Q(name__icontains=name) & Q(supplier__name__icontains=supplier_name)
            )

            messages.add_message(request, messages.SUCCESS, f'Znaleziono {materialsToDisplay.count()} rezultatów.')

            # return render(request, 'order_.html', {'search_results': objects})
    else:
        form = forms.MaterialSearchForm()

    context = {
        'materials': materialsToDisplay,
        'search_form': form
    }

    return render(request, 'Main/materials.html', context)


@login_required
def materialSelectCompany(request):
    if request.method == 'POST':
        form = forms.CompanySelectForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data.get('selected_company')
            return redirect('material-create', pk=company.id)

    else:
        form = forms.CompanySelectForm()

    return render(request, 'Main/Materials/materialSelectCompany.html', {'company_select_form': form })


@login_required
def materialCreateNewCompany(request):
    if request.method == 'POST':
        material_form = forms.MaterialCreateForm(request.POST, prefix='material')
        company_form = forms.CompanyCreateForm(request.POST, prefix='company')
        if material_form.is_valid() and company_form.is_valid():
            company = company_form.save()
            material = material_form.save()
            material.commissioner = company
            material.save()

            messages.add_message(request, messages.SUCCESS, f'Pomyślnie dodano materiał.')
            redirect('main-orders')
    else:
        material_form = forms.MaterialCreateForm(prefix='material')
        company_form = forms.CompanyCreateForm(prefix='company')

    context = {
        'material_form': material_form,
        'company_form': company_form
    }

    return render(request, 'Main/Materials/materialCreateNewCompany.html', context)


@login_required
def materialCreate(request, pk):
    if request.method == 'POST':
        form = forms.MaterialCreateForm(request.POST)
        if form.is_valid():
            material = form.save()
            company = get_object_or_404(models.Company, pk=pk)
            material.supplier = company
            material.save()

            messages.add_message(request, messages.SUCCESS, f'Pomyślnie dodano materiał.')
            return redirect('main-materials')
    else:
        form = forms.MaterialCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'Main/Materials/materialCreate.html', context)


@login_required
def materialDetailView(request, pk):
    material = get_object_or_404(models.Material, pk=pk)
    return render(request, 'Main/Materials/materialDetails.html', {'material': material})


@login_required
def materialDeleteConfirm(request, pk):
    material = get_object_or_404(models.Material, pk=pk)

    context = {
        "material": material,
    }

    return render(request, 'Main/Materials/materialDeleteConfirm.html', context)


@login_required
def materialDelete(request, pk):
    material = get_object_or_404(models.Material, pk=pk)
    material.delete()
    messages.add_message(request, messages.SUCCESS, 'Pomyślnie usunięto materiał')
    return redirect('main-materials')


@login_required
def materialEdit(request, pk):
    material = get_object_or_404(models.Material, pk=pk)

    form = forms.MaterialCreateForm(request.POST or None, instance=material)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Pomyślnie zaktualizowano materiał.')
        return redirect(reverse('material-details', args=[pk]))

    context = {
        'form': form
    }

    return render(request, 'Main/Materials/materialEdit.html', context)


@login_required
def materialEditCompanyCheck(request, pk):
    material = get_object_or_404(models.Material, pk=pk)

    if request.method == 'POST':
        form = forms.CompanySelectForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data.get('selected_company')
            material.supplier = company
            material.save()
            messages.add_message(request, messages.SUCCESS, 'Pomyślnie zaktualizowano dostawcę.')
            return redirect(reverse('material-details', args=[pk]))

    else:
        form = forms.CompanySelectForm()

    return render(request, 'Main/Materials/materialEditCompanyCheck.html', {'company_select_form': form, 'company': material.supplier})

# *** FILES ****


@login_required
def files(request):

    if request.method == 'POST':
        form = forms.FileSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            files_to_display = models.SimpleFile.objects.filter(Q(name__icontains=name))

            messages.add_message(request, messages.SUCCESS, f'Znaleziono {files_to_display.count()} rezultatów.')

            # return render(request, 'order_.html', {'search_results': objects})
        else:
            files_to_display = models.SimpleFile.objects.all()
    else:
        form = forms.FileSearchForm()
        files_to_display = models.SimpleFile.objects.all()

    context = {
        'files': files_to_display,
        'search_form': form
    }

    return render(request, 'Main/files.html', context)


@login_required
def downloadLinkedFile(request, pk):
    linked_file = get_object_or_404(models.LinkedFile, pk=pk)
    response = HttpResponse(linked_file.file)
    response['Content-Disposition'] = f'attachment; filename="{linked_file.file.name}"'
    return response


@login_required
def downloadSimpleFile(request, pk):
    file = get_object_or_404(models.SimpleFile, pk=pk)
    response = HttpResponse(file.file)
    response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
    return response


@login_required
def fileDeleteConfirm(request, pk):
    file = get_object_or_404(models.SimpleFile, pk=pk)

    context = {
        "file": file,
    }

    return render(request, 'Main/Files/fileDeleteConfirm.html', context)


def removeFileObject(obj):
    if obj.file:
        if os.path.isfile(obj.file.path):
            os.remove(obj.file.path)

    obj.delete()

@login_required
def fileDelete(request, pk):
    obj = get_object_or_404(models.SimpleFile, pk=pk)

    removeFileObject(obj)
    messages.add_message(request, messages.SUCCESS, 'Pomyślnie usunięto plik')
    return redirect('main-files')


@login_required
def fileAdd(request):
    if request.method == 'POST':
        form = forms.FileAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f'Pomyślnie dodano plik.')
            return redirect('main-files')
    else:
        form = forms.FileAddForm()

    context = {
        'form': form,
    }

    return render(request, 'Main/Files/fileAdd.html', context)