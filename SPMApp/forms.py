from django import forms
from .models import mainpagetable


class MyForm(forms.Form):
    VENDOR_CHOICES = list(mainpagetable.objects.values_list('VendorType', flat=True).distinct())
    VENDOR_CHOICES = [item for item in VENDOR_CHOICES if item != ""]
    Vendor_list = []
    for vendor in VENDOR_CHOICES:
        Vendor_list.append((vendor, vendor))
    if len(Vendor_list) == 0:
        Vendor_list.append(("Vendor1","Vendor1"))
    if 'other' not in VENDOR_CHOICES:
        Vendor_list.append(('other', 'other'))

    VENDOR_CHOICES = Vendor_list

    COMPANY_CHOICES = list(mainpagetable.objects.values_list('CompanyType', flat=True).distinct())
    COMPANY_CHOICES = [item for item in COMPANY_CHOICES if item != ""]
    Company_list = []
    for company in COMPANY_CHOICES:
        Company_list.append((company, company))
    if len(Company_list) == 0:
        Company_list.append(("Company1", "Company1"))
    if 'other' not in COMPANY_CHOICES:
        Company_list.append(('other', 'other'))

    COMPANY_CHOICES = Company_list

    ITEM_CHOICES = list(mainpagetable.objects.values_list('ItemType', flat=True).distinct())
    ITEM_CHOICES = [item for item in ITEM_CHOICES if item != ""]

    Item_list = []
    for item in ITEM_CHOICES:
        Item_list.append((item, item))
    if len(Item_list) == 0:
        Item_list.append(("PLC","PLC"))
    if 'other' not in ITEM_CHOICES:
        Item_list.append(('other', 'other'))
    ITEM_CHOICES = Item_list

    VendorType = forms.ChoiceField(choices=VENDOR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    other_vendor_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}))
    CompanyType = forms.ChoiceField(choices=COMPANY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    other_company_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}))
    ItemType = forms.ChoiceField(choices=ITEM_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    other_item_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}))
    ModelNo = forms.CharField(max_length=100)
    HSNCode = forms.CharField(max_length=100)
    PriceFromChina = forms.FloatField()
    DeclaredCustomPrice = forms.FloatField()
    SellingPrice = forms.FloatField()
    DateTime = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_my_field(self):
        PriceFromChina = self.cleaned_data.get('PriceFromChina')

        if PriceFromChina is not None and PriceFromChina < 0:
            raise forms.ValidationError("Value must be non-negative.")

        return PriceFromChina

class FetchModelDetailsForm(forms.Form):

    ModelNo = forms.CharField(max_length=100,required=False)
