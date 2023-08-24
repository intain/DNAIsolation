from django import forms
from . import models


class CompanySelectForm(forms.Form):
    selected_company = forms.ModelChoiceField(
        queryset=models.Company.objects.all(),
        label="",
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 80%;'})
    )


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderCreationForm(forms.ModelForm):
    number = forms.IntegerField(label="Numer")
    contractor = forms.ChoiceField(label="Wykonawca",
       choices=[
            ("Genomed", "Genomed"),
            ("A&A", "A&A")])
    receiveDate = forms.DateField(label="Data otrzymania", widget=DateInput)
    status = forms.ChoiceField(label="Status",
       choices=[
            ("Oczekuje", "Oczekuje"),
            ("Otrzymano", "Otrzymano"),
            ("W realizacji", "W realizacji"),
            ("Wysłano", "Wysłano"),
            ("Zakończono", "Zakończono"),
            ("Anulowano","Anulowano")])
    notes = forms.CharField(label='Uwagi', widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)
    files = forms.FileField(
        label="Załączniki",
        widget=forms.FileInput(attrs={"multiple": True}),
        required=False)



    class Meta:
        model = models.Order
        fields = ['number', 'contractor', 'receiveDate', 'status', 'notes', 'files']
        widgets = {
            'receiveDate': forms.widgets.DateInput(attrs={'type': 'date'})
        }


class OrderEditForm(OrderCreationForm):
    files_to_delete = forms.ModelMultipleChoiceField(
        queryset=models.LinkedFile.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Załączniki do usunięcia"
    )

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset')
        super().__init__(*args, **kwargs)
        self.fields['files_to_delete'].queryset = queryset

class CompanyCreateForm(forms.ModelForm):
    name = forms.CharField(label="Nazwa")
    pointOfContact = forms.CharField(label="Osoba kontaktowa")
    email = forms.EmailField(label="E-mail")
    phoneNumber = forms.CharField(label="Telefon")

    class Meta:
        model = models.Company
        fields = ['name', 'pointOfContact', 'email', 'phoneNumber']


class OrderSearchForm(forms.Form):
    commissioner = forms.CharField(label="Zlecający", required=False)
    status = forms.ChoiceField(label="Status", required=False,
        choices=[
            ("Dowolny", "Dowolny"),
            ("Oczekuje", "Oczekuje"),
            ("Otrzymano", "Otrzymano"),
            ("W realizacji", "W realizacji"),
            ("Wysłano", "Wysłano"),
            ("Zakończono", "Zakończono"),
            ("Anulowano", "Anulowano")])

# *** MATERIALS ***


class MaterialSearchForm(forms.Form):
    name = forms.CharField(label="Nazwa", required=False)


class MaterialCreateForm(forms.ModelForm):
        number = forms.IntegerField(label="Numer")
        name = forms.CharField(label="Nazwa odczynnika")
        unit = forms.ChoiceField(
            label="Jednostka", choices=[
                ("Liczba reakcji", "Liczba reakcji"),
                ("Zestaw", "Zestaw")])
        notes = forms.CharField(label='Uwagi', widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)

        class Meta:
            model = models.Material
            fields = ['number', 'name', 'unit', 'notes']

# *** FILES ***


class FileSearchForm(forms.Form):
    name = forms.CharField(label="Nazwa", required=False)


class FileAddForm(forms.ModelForm):
    name = forms.CharField(label="Nazwa")
    file = forms.FileField(label="Plik")

    class Meta:
        model = models.SimpleFile
        fields = ['name', 'file']


class OperationForm(forms.ModelForm):
    flight = forms.CharField(label="Lot")
    deliveryDate = forms.DateField(label="Data dostawy", widget=DateInput)
    expirationDate = forms.DateField(label="Data ważności", widget=DateInput)
    openDate = forms.DateField(label="Data otwarcia", widget=DateInput, required=False)
    count = forms.IntegerField(label="Stan")

    class Meta:
        model = models.Operation
        fields = ['flight', 'deliveryDate', 'expirationDate', 'openDate', 'count']
        widgets = {
            'deliveryDate': forms.widgets.DateInput(attrs={'type': 'date'}),
            'expirationDate': forms.widgets.DateInput(attrs={'type': 'date'}),
            'openDate': forms.widgets.DateInput(attrs={'type': 'date'})
        }