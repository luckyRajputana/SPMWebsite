import traceback

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from .forms import *
from .models import mainpagetable

def MainPage(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():

            try:
                VENDOR_CHOICES = list(mainpagetable.objects.values_list('VendorType', flat=True).distinct())
                Vendor_list = []
                for vendor in VENDOR_CHOICES:
                    Vendor_list.append((vendor, vendor))
                if 'other' not in VENDOR_CHOICES:
                    Vendor_list.append(('other', 'other'))
                VENDOR_CHOICES = Vendor_list

                COMPANY_CHOICES = list(mainpagetable.objects.values_list('CompanyType', flat=True).distinct())
                Company_list = []
                for company in COMPANY_CHOICES:
                    Company_list.append((company, company))
                if 'other' not in COMPANY_CHOICES:
                    Company_list.append(('other', 'other'))
                COMPANY_CHOICES = Company_list

                ITEM_CHOICES = list(mainpagetable.objects.values_list('ItemType', flat=True).distinct())
                Item_list = []
                for item in ITEM_CHOICES:
                    Item_list.append((item, item))
                if 'other' not in ITEM_CHOICES:
                    Item_list.append(('other', 'other'))
                ITEM_CHOICES = Item_list

                # Process the form data
                VendorType = form.cleaned_data['VendorType']
                CompanyType = form.cleaned_data['CompanyType']
                ItemType = form.cleaned_data['ItemType']
                ModelNo = form.cleaned_data['ModelNo']
                HSNCode = form.cleaned_data['HSNCode']
                PriceFromChina = form.cleaned_data['PriceFromChina']
                DeclaredCustomPrice = form.cleaned_data['DeclaredCustomPrice']
                SellingPrice = form.cleaned_data['SellingPrice']
                DateTime = form.cleaned_data['DateTime']

                other_vendor_name = form.cleaned_data['other_vendor_name']
                other_company_name = form.cleaned_data['other_company_name']
                other_item_name = form.cleaned_data['other_item_name']
                if other_vendor_name not in VENDOR_CHOICES and other_vendor_name != '':
                    VendorType = other_vendor_name
                if other_company_name not in COMPANY_CHOICES and other_company_name != '':
                    CompanyType = other_company_name
                if other_item_name not in ITEM_CHOICES and other_item_name != '':
                    ItemType = other_item_name


                # Do something with the data (e.g., save to a database)
                mainpagetable.objects.create(VendorType=VendorType,CompanyType=CompanyType,ItemType=ItemType,ModelNo=ModelNo,HSNCode=HSNCode,\
                                             PriceFromChina=PriceFromChina,DeclaredCustomPrice=DeclaredCustomPrice,SellingPrice=SellingPrice,\
                                             DateTime=DateTime)
                success_message = "Data added to the database successfully !!"
                return render(request, 'MainPageTemplate.html', {'form': form, 'success_message': success_message})
            except Exception as e:
                error_message = str(e).split('\n', 1)[0]
                return render(request, 'MainPageTemplate.html', {'form': form, 'error_message':"Database entry failed due to mentioned reason : "+error_message})


    else:
        form = MyForm()

    return render(request, 'MainPageTemplate.html', {'form': form})


def FetchModelDetails(request):
    if request.method == 'POST':
        form = FetchModelDetailsForm(request.POST)

        if form.is_valid():
            try:
                # Process the form data
                ModelNo = form.cleaned_data['ModelNo']
                if ModelNo == "":
                    data_from_database = mainpagetable.objects.all()
                    return render(request, 'FetchModelDetails.html', {'form': form, 'data_from_database': data_from_database})
                else:
                    ModelNo =  ModelNo.split()
                    print(ModelNo)

                    # Do something with the data (e.g., save to a database)
                    data_from_database  = mainpagetable.objects.filter(ModelNo__in = ModelNo)
                    # data_from_database = MainPageTable.objects.all()
                    print(data_from_database)

                    return render(request, 'FetchModelDetails.html', {'form': form,'data_from_database': data_from_database})

            except Exception as e:
                error_message = str(e).split('\n', 1)[0]
                return render(request, 'FetchModelDetails.html', {'form': form, 'error_message':"Database entry failed due to mentioned reason : "+error_message})

        else:
            return render(request, 'FetchModelDetails.html', {'form': form})

    else:
        form = FetchModelDetailsForm()

    return render(request, 'FetchModelDetails.html', {'form': form})

def RowDeleteView(request, pk):
    # Retrieve the object to be deleted
    obj = get_object_or_404(mainpagetable, pk=pk)
    obj.delete()
    return redirect('FetchModelDetails')

    # # Check if the request method is POST
    # if request.method == 'POST':
    #     # Delete the object from the database
    #     obj.delete()
    #     # Redirect to a success page or a different view
    #     return redirect('success_page')
    #
    # # If the request method is not POST, render a confirmation template
    # return render(request, 'confirm_delete.html', {'object': obj})


def GetColumnDataView(request):
    column_name = request.GET.get('VendorType', None)

    if column_name:
        data = list(mainpagetable.objects.values_list(column_name, flat=True))
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error': 'Column name not specified'}, status=400)