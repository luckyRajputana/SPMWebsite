import traceback

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from .forms import *
from .models import mainpagetable
from django.core.files.storage import FileSystemStorage
import pandas as pd
from datetime import datetime

def MainPage(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():

            try:
                VENDOR_CHOICES = list(mainpagetable.objects.values_list('VendorType', flat=True).distinct())
                Vendor_list = []
                for vendor in VENDOR_CHOICES:
                    Vendor_list.append((vendor, vendor))
                if len(Vendor_list) == 0:
                    Vendor_list.append(("Vendor1", "Vendor1"))
                if 'other' not in VENDOR_CHOICES:
                    Vendor_list.append(('other', 'other'))
                VENDOR_CHOICES = Vendor_list

                COMPANY_CHOICES = list(mainpagetable.objects.values_list('CompanyType', flat=True).distinct())
                Company_list = []
                for company in COMPANY_CHOICES:
                    Company_list.append((company, company))
                if len(Company_list) == 0:
                    Company_list.append(("Company1", "Company1"))
                if 'other' not in COMPANY_CHOICES:
                    Company_list.append(('other', 'other'))
                COMPANY_CHOICES = Company_list

                ITEM_CHOICES = list(mainpagetable.objects.values_list('ItemType', flat=True).distinct())
                Item_list = []
                for item in ITEM_CHOICES:
                    Item_list.append((item, item))
                if len(Item_list) == 0:
                    Item_list.append(("PLC", "PLC"))

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
    vendors = list(mainpagetable.objects.values_list("VendorType", flat=True))
    vendors = list(sorted(set(vendors)))
    vendors.append("other")
    companies = list(mainpagetable.objects.values_list("CompanyType", flat=True))
    companies = list(sorted(set(companies)))
    companies.append("other")
    items = list(mainpagetable.objects.values_list("ItemType", flat=True))
    items_v = list(sorted(set(items)))
    items_v.append("other")
    return JsonResponse({'vendors':vendors ,'companies': companies,'items_v': items_v})


def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        try:
            print("Inside")
            excel_file = request.FILES['excel_file']
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            uploaded_file_url = fs.url(filename)
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Process the uploaded Excel file
            df = pd.read_excel(excel_file)  # Read the Excel file using pandas
            excel_columns = list(df.columns)
            model_meta = mainpagetable._meta

            # Extract column names from the model's meta information
            expected_columns = [field.name for field in model_meta.get_fields()]
            print(expected_columns[1:-1])
            expected_columns = expected_columns[1:-1]

            # Compare the extracted column names with the expected column names
            missing_columns = [col for col in expected_columns if col not in excel_columns]
            extra_columns = [col for col in excel_columns if col not in expected_columns]
            success = ""
            # Perform validation based on the comparison results
            if missing_columns:
                failure = f"Missing columns: {', '.join(missing_columns)}"
            elif extra_columns:
                failure =  f"Extra columns: {', '.join(extra_columns)}"
            else:
                success =  "Column names validation successful"
            # Do further processing as needed, such as data manipulation, analysis, etc.
            if success == "Column names validation successful":
                failed_ingestions = []
                failed_string = ""
                for index, row in df.iterrows():
                    try:
                        with transaction.atomic():
                            mainpagetable.objects.create(VendorType=row["VendorType"], CompanyType=row["CompanyType"],
                                                 ItemType=row["ItemType"], ModelNo=row["ModelNo"],HSNCode = row["HSNCode"], \
                                                PriceFromChina = row["PriceFromChina"], DeclaredCustomPrice = row["DeclaredCustomPrice"],
                                                SellingPrice = row["SellingPrice"],
                                                 DateTime=current_timestamp)
                    except Exception as e:
                        # If ingestion fails for a row, add it to the list of failed ingestions
                        index_detail = str(e).find("DETAIL:")

                        # Extract the substring after "DETAIL:"
                        if index_detail != -1:
                            detail_string = str(e)[index_detail + len("DETAIL:"):]

                        failing =str(row["VendorType"] )+ ' and ' + str(row["ModelNo"] ), "Error : "+detail_string
                        print(failing)
                        print(type(str(failing)))
                        failed_ingestions.append(str(failing))

                failed_string = ', '.join(failed_ingestions)
                success_message_file_upload = "Excel file uploaded!"
            return render(request, 'MainPageTemplate.html', {
                'success_message_file_upload': success_message_file_upload,
                'error_message_file_upload' : "Failed rows :  "+ failed_string
            })

        except Exception as e:
            return render(request, 'MainPageTemplate.html', {
                'error_message_file_upload' : failure
            })

    return render(request, 'MainPageTemplate.html')
