# Create your views here.

from . models import Brand, Clients, Expenses, Products, Orders, Departments, Positions, Staff, Documents, myUser, Assignments, Supplier, Images
from django.db.models import F, ExpressionWrapper, FloatField
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
import os

User = get_user_model()


def home(request):
    return render(request, 'home.html')


def main(request):
    return render(request, 'main_layout.html')


def basic(request):
    return render(request, 'basic.html')


def upload(request):
    if 'filetodelete' in request.POST:
        code = request.POST['filetodelete']
        img = Images.objects.get(image=code)
        os.remove('media/'+str(img.image))
        img.delete()

    if request.method == 'POST' and request.FILES.get('file'):
        upload = request.FILES['file']
        uploaded_photo = request.FILES['file']
        file_storage = FileSystemStorage()
        saved_file = file_storage.save(uploaded_photo.name, uploaded_photo)
        file_url = file_storage.url(saved_file)
        daxilet = Images(image=file_url, dropzone=request.POST['code'])
        daxilet.save()
        return HttpResponse('File uploaded successfully.')
    else:
        return JsonResponse({'success': False})


def loader(request):
    data = ''
    brands = ''
    suppliers = ''
    client = ''
    product = ''
    departments = ''
    staffs = ''
    positions = ''
    edit_data = ''

    if 'x' in request.POST:
        # Brand add without refresh.
        if request.POST['x'] == 'brands':

            if 'save' in request.POST:
                brand_name = request.POST['brand_name']

                if brand_name:
                    if Brand.objects.filter(brand_name=request.POST['brand_name']).exists():
                        messages.info(request, "Brand already exists.",
                                      extra_tags='warning')
                    elif 'brand_photo' in request.FILES:

                        upload = request.FILES['brand_photo']
                        fs = FileSystemStorage()
                        file = fs.save(upload.name, upload)
                        file_url = fs.url(file)

                        save_data = Brand(
                            brand_name=request.POST['brand_name'],
                            brand_pic=file_url
                        )
                        save_data.save()
                        messages.info(request, "Brand saved.",
                                      extra_tags='success')
                    else:
                        messages.info(request, "Photo is required.",
                                      extra_tags='error')
                else:
                    messages.info(request, "Brand name is required.",
                                  extra_tags='warning')

            data = Brand.objects.all().order_by('-id')
            # Brand add end

            # Brand edit without refresh
            if 'edit_id' in request.POST:
                edit_data = Brand.objects.get(id=request.POST['edit_id'])
            # Brand edit done

            # Brand update without refresh
            if 'update' in request.POST:
                if 'update':
                    update = Brand.objects.get(id=request.POST['id'])
                    if Brand.objects.filter(brand_name=request.POST['id']).exclude(id=request.POST['id']).exists():
                        messages.info(
                            request, "Brand already exists.", extra_tags='error')
                    else:
                        if 'brand_photo' in request.FILES:
                            new_photo = request.FILES['brand_photo']
                            update.brand_pic = new_photo
                            fs = FileSystemStorage()
                            file = fs.save(new_photo.name, new_photo)
                            file_url = fs.url(file)
                            update.brand_pic = file_url
                        update.brand_name = request.POST['brand_name']
                        update.save()
                        messages.info(request, "Brand update was successful.",
                                      extra_tags='success')
                else:
                    messages.info(
                        request, "Brand name is required", extra_tags='error')
            # Brand update done

            # Brand single deletion without refresh
            if 'del_id' in request.POST:
                brand = Brand.objects.get(id=request.POST['del_id'])
                number = Products.objects.filter(
                    brand_id=request.POST['del_id']).count()

                if number > 0:
                    messages.info(
                        request, f"Brand '{brand.brand_name}' cannot be deleted. There are {number} active products in it.", extra_tags='error')
                else:
                    os.remove('media/'+str(brand.brand_pic))
                    brand.delete()
                    messages.info(
                        request, "The brand has been successfully deleted.", extra_tags='success')
            # Brand delete end

        # Clients add without refresh
        elif request.POST['x'] == 'clients':

            if 'save' in request.POST:
                name = request.POST['name'],
                surname = request.POST['surname'],
                email = request.POST['email'],
                phone = request.POST['phone'],
                company = request.POST['company']

                if name and surname and email and phone and company:
                    if Clients.objects.filter(email=request.POST['email']).exists():
                        messages.info(request, "E-mail already exists.",
                                      extra_tags='warning')
                    elif Clients.objects.filter(phone=request.POST['phone']).exists():
                        messages.info(
                            request, "Phone number already exists.", extra_tags='warning')
                    else:
                        save_data = Clients(
                            name=request.POST['name'],
                            surname=request.POST['surname'],
                            email=request.POST['email'],
                            phone=request.POST['phone'],
                            company=request.POST['company'],
                        )

                        save_data.save()
                        messages.info(
                            request, "Customer information saved successfully.", extra_tags='success')
                else:
                    messages.info(request, "Empty fields.", extra_tags='error')

            data = Clients.objects.all().order_by('-id')
            # Client add end

            # Client edit without refresh
            if 'edit_id' in request.POST:
                edit_data = Clients.objects.get(id=request.POST['edit_id'])
            # Client edit done

            # Client update without refresh
            if 'update' in request.POST:
                if 'update':
                    update = Clients.objects.get(id=request.POST['id'])
                    if Clients.objects.filter(email=request.POST['id']).exclude(id=request.POST['id']).exists():
                        messages.info(request, "E-mail already exists.")
                    elif Clients.objects.filter(phone=request.POST['id']).exclude(id=request.POST['id']).exists():
                        messages.info(request, "Phone number already exists.")
                    else:
                        update.name = request.POST['name']
                        update.surname = request.POST['surname']
                        update.email = request.POST['email']
                        update.phone = request.POST['phone']
                        update.company = request.POST['company']
                        update.save()
                        messages.info(request, "Client update was successful.",
                                      extra_tags='success')
                else:
                    messages.info(request, "Empety fields.",
                                  extra_tags='error')
            # Client update done

            # Client single deletion without refresh
            if 'del_id' in request.POST:
                clients = Clients.objects.get(id=request.POST['del_id'])
                active_orders = Orders.objects.filter(
                    client_id=request.POST['del_id']).count()

                if active_orders > 0:
                    messages.info(
                        request, f"Client '{clients.name} {clients.surname}' cannot be deleted. There are {active_orders} active products in it.", extra_tags='error')
                else:
                    clients.delete()
                    messages.info(
                        request, "Customer's data has been deleted successfully.", extra_tags='success')
            # Client delete end

        # Expens add without refresh
        elif request.POST['x'] == 'expenses':

            if 'save' in request.POST:
                if request.POST['assignment'] != '' and request.POST['amount'] != '':

                    save_data = Expenses(
                        assignment=request.POST['assignment'],
                        amount=request.POST['amount']
                    )
                    save_data.save()
                    messages.info(request, "Expens saved successfully.",
                                  extra_tags='success')
                else:
                    messages.info(request, "Empty field.", extra_tags='error')

            data = Expenses.objects.all().order_by('-id')
        # Expens end

            # Expens edit without refresh
            if 'edit_id' in request.POST:
                edit_data = Expenses.objects.get(id=request.POST['edit_id'])
            # Expens edit done

            # Expens update without refresh
            if 'update' in request.POST:
                if 'update':
                    expens = Expenses.objects.get(id=request.POST['id'])
                    expens.assignment = request.POST['assignment']
                    expens.amount = request.POST['amount']

                    expens.save()
                    messages.info(request, "Update was successful.",
                                  extra_tags='success')

                else:
                    messages.info(request, "Empty field.", extra_tags='error')

            # Expens single deletion without refresh
            if 'del_id' in request.POST:
                Expenses.objects.get(id=request.POST['del_id']).delete()
                messages.info(
                    request, "Expens data has been deleted successfully.", extra_tags='success')
            # Expens delete end

            # Expens multi deletion without refresh
            if 'delete_all' in request.GET:
                del_all = request.GET.getlist('x[]')
                if not del_all:
                    messages.info(request, "Please select to delete.",
                                  extra_tags='error')
            elif 'confirm_delete_all' in request.GET:
                choosen = request.GET.getlist('x[]')
                if choosen:
                    for selected in choosen:
                        picked = Expenses.objects.filter(id=selected)
                        if picked.exists():
                            picked.delete()
                    messages.info(
                        request, "Expens data has been deleted successfully.", extra_tags='success')
            # Expens multi deletion end

        # Product add without refresh.
        elif request.POST['x'] == 'products':
            #Images.objects.all().delete()
            if 'save' in request.POST:
                if request.POST['brand_id'] != '' and request.POST['product'] != '' and request.POST['buy'] != '' and request.POST['sell'] != '' and request.POST['quantity'] != '':
                    # instance
                    brand = Brand.objects.get(id=request.POST['brand_id'])
                    supplier = Supplier.objects.get(id=request.POST['supp_id'])

                    save_date = Products(
                        brand=brand,
                        supplier_id=supplier,
                        product=request.POST['product'],
                        buy=request.POST['buy'],
                        sell=request.POST['sell'],
                        quantity=request.POST['quantity'],
                        dropzone=request.POST['code']
                    )
                    save_date.save()
                    messages.info(
                        request, "Product saved successfully.", extra_tags='success')
                else:
                    messages.info(request, "Empty field", extra_tags='error')

            data = Products.objects.all().order_by('-id')
            brands = Brand.objects.all().order_by('-id')
            suppliers = Supplier.objects.all().order_by('-id')
        # Product add end

            # Products edit without refresh
            if 'edit_id' in request.POST:
                edit_data = Products.objects.get(id=request.POST['edit_id'])

            # Products edit done
            if 'update' in request.POST:
                if 'update':
                    product = Products.objects.get(id=request.POST['id'])
                    product.product = request.POST['product']
                    product.buy = request.POST['buy']
                    product.sell = request.POST['sell']
                    product.quantity = request.POST['quantity']
                    product.brand = Brand.objects.get(
                        id=request.POST['brand_id'])

                    product.save()
                    messages.info(request, "Update was successful.",
                                  extra_tags='success')
                else:
                    messages.info(request, "Empty field.", extra_tags='error')
                return redirect('products')

            # Products update without refresh
            if 'update' in request.POST:
                if 'update':
                    expens = Expenses.objects.get(id=request.POST['id'])
                    expens.assignment = request.POST['assignment']
                    expens.amount = request.POST['amount']

                    expens.save()
                    messages.info(request, "Update was successful.",
                                  extra_tags='success')
                else:
                    messages.info(request, "Empty field.", extra_tags='error')
            # Product edit end

            # Product single deletion without refresh
            if 'del_id' in request.POST:
                products = Products.objects.get(id=request.POST['del_id'])
                active_order = Orders.objects.filter(
                    product_id=request.POST['del_id']).count()
                images = Images.objects.all().filter(dropzone=products.dropzone)

                if active_order > 0:
                    messages.info(
                        request, f"Product '{products.product}' cannot be deleted. There are {active_order} active products in it.", extra_tags='error')
                else:
                    for img in images:
                        os.remove('media/'+str(img.image))
                    products.delete()
                    messages.info(
                        request, "Products data has been deleted successfully.", extra_tags='success')
            # Product delete end

        # Order add without refresh.
        if request.POST['x'] == 'orders':
            if 'save' in request.POST:
                if request.POST['client_id'] != '' and request.POST['product_id'] != '' and request.POST['amount'] != '':

                    client = Clients.objects.get(
                        id=request.POST['client_id'])
                    product = Products.objects.get(
                        id=request.POST['product_id'])

                    save_data = Orders(
                        client=client,
                        product=product,
                        amount=request.POST['amount']
                    )
                    save_data.save()
                    messages.info(request, "Order saved successfully.",
                                  extra_tags='success')
                else:
                    messages.info(request, "Empty field", extra_tags='error')

            data = Orders.objects.all().order_by('-id')
            client = Clients.objects.all().order_by('-id')
            product = Products.objects.all().order_by('-id')
            orders_num = Orders.objects.all().count()
        # Order add end

            # Order single deletion without refresh
            if 'del_id' in request.POST:
                Orders.objects.get(id=request.POST['del_id']).delete()
                messages.info(
                    request, "Order data has been deleted successfully.", extra_tags='success')
            # Order delete end

        # Supplier add without refresh.
        if request.POST['x'] == 'suppliers':

            if 'save' in request.POST:
                supp_name = request.POST['sup_name']
                supp_surname = request.POST['sup_surname']
                supp_comp_name = request.POST['sup_comp_name']
                supp_email = request.POST['supp_email']
                supp_phone = request.POST['supp_phone']
                supp_address = request.POST['supp_address']

                if supp_name and supp_surname and supp_comp_name and supp_email and supp_phone and supp_address and 'sup_photo' in request.FILES:
                    if Supplier.objects.filter(supplier_email=request.POST['supp_email']).exists():
                        messages.info(request, "Email already exists.",
                                      extra_tags='warning')
                    elif Supplier.objects.filter(supplier_phone=request.POST['supp_phone']).exists():
                        messages.info(request, "Phone already exists.",
                                      extra_tags='warning')
                    else:
                        upload = request.FILES['sup_photo']
                        file_ss = FileSystemStorage()
                        file = file_ss.save(upload.name, upload)
                        file_url = file_ss.url(file)

                        supplier = Supplier(
                            supplier_name=supp_name,
                            supplier_surname=supp_surname,
                            supplier_company_name=supp_comp_name,
                            supplier_email=supp_email,
                            supplier_phone=supp_phone,
                            supplier_address=supp_address,
                            supplier_photo=file_url
                        )
                        supplier.save()
                        messages.info(
                            request, "Supplier added successfully.", extra_tags='success')
                else:
                    messages.info(request, "Empty fields.", extra_tags='error')

            data = Supplier.objects.all().order_by('-id')
            supplier_num = Supplier.objects.all().count()
        # Suplplier add end

            # Supplier single deletion without refresh
            if 'del_id' in request.POST:
                supplier = Supplier.objects.get(id=request.POST['del_id'])
                number = Products.objects.filter(
                    supplier_id_id=request.POST['del_id']).count()

                if number > 0:
                    messages.info(
                        request, f"Supplier '{supplier.supplier_name}' cannot be deleted. There are {number} active products in it.", extra_tags='error')
                else:
                    os.remove('media/'+str(supplier.supplier_photo))
                    supplier.delete()
                    messages.info(
                        request, "Supplier has been deleted successfully.", extra_tags='success')
            # Supplier delete end

        # Department add without refresh.
        if request.POST['x'] == 'departments':

            if 'save' in request.POST:
                department_name = request.POST['department_name']

                if department_name:
                    if Departments.objects.filter(department_name=request.POST['department_name']).exists():
                        messages.info(
                            request, "Departments already exists.", extra_tags='warning')
                    else:
                        save_data = Departments(
                            department_name=request.POST['department_name']
                        )
                        save_data.save()
                        messages.info(
                            request, "Departments added successfully.", extra_tags='success')
                else:
                    messages.info(request, "Departments name is required.",
                                  extra_tags='error')
            data = Departments.objects.all().order_by('-id')
        # Department add end

            # Departmen single deletion without refresh
            if 'del_id' in request.POST:
                departments = Departments.objects.get(
                    id=request.POST['del_id'])
                position = Positions.objects.filter(
                    dep_id_id=request.POST['del_id']).count()

                if position > 0:
                    messages.info(
                        request, f"Department '{departments.department_name}' cannot be deleted. There are {position} active position in it.", extra_tags='error')
                else:
                    departments.delete()
                    messages.info(
                        request, "Department  has been deleted successfully.", extra_tags='success')
            # Department delete end

        # Position add without refresh.
        if request.POST['x'] == 'positions':

            if 'save' in request.POST:

                if request.POST['department_id'] != '' and request.POST['position_name'] != '':

                    department = Departments.objects.get(
                        id=request.POST['department_id'])

                    save_data = Positions(
                        dep_id=department,
                        positions=request.POST['position_name']
                    )

                    save_data.save()
                    messages.info(request, "Position saved.",
                                  extra_tags='success')

                else:
                    messages.info(request, "Position name is required.",
                                  extra_tags='error')

            data = Positions.objects.all().order_by('-id')
            departments = Departments.objects.all().order_by('-id')
        # Position add end

            # Position single deletion without refresh
            if 'del_id' in request.POST:
                positions = Positions.objects.get(
                    id=request.POST['del_id'])
                staffs = Staff.objects.filter(
                    pos_id=request.POST['del_id']).count()

                if staffs > 0:
                    messages.info(
                        request, f"Position '{positions.positions}' cannot be deleted. There are {staffs} active staff in it.", extra_tags='error')
                else:
                    positions.delete()
                    messages.info(
                        request, "Positions has been deleted successfully.", extra_tags='success')
            # Position delete end

        # Staff add without refresh.
        if request.POST['x'] == 'staffs':

            if 'save' in request.POST:

                if request.POST['s_name'] != '' and request.POST['s_surname'] != '' and request.POST['s_birth_d'] != '' and request.POST['s_email'] != '' and request.POST['s_phone'] != '' and request.POST['s_sallary'] != '' and request.POST['s_start_d'] != '':
                    positions = Positions.objects.get(
                        id=request.POST['position_id'])

                    if Staff.objects.filter(email=request.POST['s_email']).exists():
                        messages.info(request, 'Email already exists.',
                                      extra_tags='warning')
                    elif Staff.objects.filter(phone=request.POST['s_phone']).exists():
                        messages.info(request, 'Phone already exists.',
                                      extra_tags='warning')
                    elif 'photo' in request.FILES:
                        # FOTO START
                        upload = request.FILES['photo']
                        fs = FileSystemStorage()
                        file = fs.save(upload.name, upload)
                        file_url = fs.url(file)
                        # FOTO END

                        save_info = Staff(
                            name=request.POST['s_name'],
                            surname=request.POST['s_surname'],
                            birth_date=request.POST['s_birth_d'],
                            email=request.POST['s_email'],
                            phone=request.POST['s_phone'],
                            sallary=request.POST['s_sallary'],
                            j_start_d=request.POST['s_start_d'],
                            photo=file_url,
                            pos_id=positions,
                        )
                        save_info.save()
                        messages.info(
                            request, "Employee  saved successfully.", extra_tags='success')

                    if 'documents' in request.POST:
                        return redirect('documents')
                else:
                    messages.info(request, "Empty fields.", extra_tags='error')

            data = Staff.objects.all().order_by('-id')
            positions = Positions.objects.all().order_by('-id')
        # Staff add end

            # Staff single deletion without refresh
            if 'del_id' in request.POST:
                staffs = Staff.objects.get(id=request.POST['del_id'])
                documents = Documents.objects.filter(
                    staff_id_id=request.POST['del_id']).count()

                if documents > 0:
                    messages.info(
                        request, f"Staff '{staffs.name}' cannot be deleted. There are {documents} active staff in it.", extra_tags='error')
                else:
                    os.remove('media/'+str(staffs.photo))
                    staffs.delete()
                    messages.info(
                        request, "Employee has been deleted successfully.", extra_tags='success')
            # Staff delete end

        # Document add without refresh.
        if request.POST['x'] == 'documents':
            if 'save' in request.POST:
                title = request.POST['doc_name']
                doc_num = request.POST['doc_num']
                if title and doc_num:
                    name = Staff.objects.get(id=request.POST['staff_id'])

                    if Documents.objects.filter(doc_num=request.GET['doc_num']).exists():
                        messages.info(request, "Document already exists.",
                                      extra_tags='error')
                    else:
                        save_info = Documents(
                            title=request.POST['doc_name'],
                            doc_num=request.POST['doc_num'],
                            about=request.POST['about'],
                            staff_id=name,
                            dropzone=request.POST['code']
                        )
                        save_info.save()
                        messages.info(
                            request, "Document  saved successfully.", extra_tags='success')
                else:
                    messages.info(request, "Empty fields",
                                  extra_tags='warning')

            data = Documents.objects.all().order_by('-id')
            staffs = Staff.objects.get(id=request.POST['staff_id'])
        # Document add end

            # Document single deletion without refresh
            if 'del_id' in request.POST:
                doc = Documents.objects.get(id=request.POST['del_id'])
                images = Images.objects.all().filter(dropzone=doc.dropzone)
                for img in images:
                    os.remove('media/'+str(img.image))
                doc.delete()
                messages.info(
                    request, "Document has been deleted successfully.", extra_tags='success')
                return HttpResponseRedirect('/documents/'+str(doc.staff_id))
            # Document delete end

        # Assignment add without refresh.
        if request.POST['x'] == 'assignments':

            if 'save' in request.POST:
                assignment_name = request.POST['assign_n']
                sontarix = request.POST['deadline'].replace('T', ' ')

                if assignment_name and sontarix:

                    staffs = Staff.objects.get(id=request.POST['staff_id'])

                    assignment = Assignments(
                        assignment_name=request.POST['assign_n'],
                        deadline=sontarix,
                        staff_id=staffs
                    )
                    assignment.save()
                    messages.info(request, "Assignment successfully aded.",
                                  extra_tags='success')
                else:
                    messages.info(request, "Empty fields.", extra_tags='error')

            data = Assignments.objects.all().order_by('-id')
            staffs = Staff.objects.all().order_by('-id')
            assignment_num = Assignments.objects.all().count()
        # Assignment add end

            # Assignment single deletion without refresh
            if 'del_id' in request.POST:
                Assignments.objects.get(id=request.POST['del_id']).delete()
                messages.info(
                    request, "Assignment has been deleted successfully.", extra_tags='success')
            # Assignment delete end
    return render(request, 'loader.html', {'edit_data': edit_data, 'data': data, 'brands': brands, 'suppliers': suppliers, 'client': client, 'product': product, 'departments': departments, 'staffs': staffs, 'positions': positions})


def brand(request):
    data = ''
    del_all = []
    section = 'brands'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            delete_successful = True
            for selected in choosen:
                picked = Brand.objects.filter(id=selected)
                active_products = Products.objects.filter(brand=selected)
                if picked.exists() and active_products.exists():
                    delete_successful = True
                    m = "Some brands could not be deleted due to active orders."
                elif picked.exists():
                    delete_successful = False
                    picked.delete()
                    m = ""

        if delete_successful:
            messages.info(
                request, m, extra_tags='error')
        else:
            messages.info(
                request, "Brand(s) data has been deleted successfully.", extra_tags='success')

    if 'question' in request.GET:
        data = Brand.objects.filter(
            Q(brand_name__contains=request.GET['question'])).order_by('-id')
    else:
        if 'order' in request.GET:
            if request.GET['order'] == 'a':
                data = Brand.objects.all().order_by('brand_name')
            elif request.GET['order'] == 'z':
                data = Brand.objects.all().order_by('-brand_name')
            elif request.GET['order'] == 'd':
                data = Brand.objects.all().order_by('add_date')
            elif request.GET['order'] == 'e':
                data = Brand.objects.all().order_by('-add_date')
        else:
            data = Brand.objects.all().order_by('-id')

    return render(request, 'brand.html', {'section': section, 'del_all': del_all, 'data': data, })


def delete(request, id):
    brand = Brand.objects.get(id=id)
    data = Brand.objects.all().order_by('-id')
    return render(request, 'brand.html', {'brand': brand, 'data': data})


def delete_config(request, id):
    brand = Brand.objects.get(id=id)
    number = Products.objects.filter(brand_id=id).count()

    if number > 0:
        messages.info(
            request, f"Brand '{brand.brand_name}' cannot be deleted. There are {number} active products in it.", extra_tags='error')
    else:
        brand.delete()
        messages.info(
            request, "The brand has been successfully deleted.", extra_tags='success')
    return redirect('brand')


def edit(request, id):
    edit = Brand.objects.get(id=id)
    data = Brand.objects.all().order_by('-id')
    return render(request, 'brand.html', {'edit': edit, 'data': data, })


def update(request, id):
    update = Brand.objects.get(id=id)
    brand_name = request.GET['brand_name']

    if brand_name:
        if Brand.objects.filter(brand_name=brand_name).exclude(id=id).exists():
            messages.info(request, "Brand already exists.", extra_tags='error')
        else:
            if 'brand_photo' in request.FILES:
                new_photo = request.FILES['brand_photo']
                update.brand_pic = new_photo
                fs = FileSystemStorage()
                file = fs.save(new_photo.name, new_photo)
                file_url = fs.url(file)
                update.brand_pic = file_url
            update.brand_name = request.GET['brand_name']
            update.save()
            messages.info(request, "Brand update was successful.",
                          extra_tags='success')
    else:
        messages.info(request, "Brand name is required", extra_tags='error')
    return redirect('brand')


def client(request):
    data = ''
    del_all = []
    section = 'clients'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            delete_successful = True
            for selected in choosen:
                picked = Clients.objects.filter(id=selected)
                active_orders = Orders.objects.filter(client=selected)
                if picked.exists() and active_orders.exists():
                    delete_successful = True
                    m = "Some clients could not be deleted due to active orders."
                elif picked.exists():
                    delete_successful = False
                    picked.delete()
                    m = ""

        if delete_successful:
            messages.info(
                request, m, extra_tags='error')
        else:
            messages.info(
                request, "Client data has been deleted successfully.", extra_tags='success')

    if 'save' in request.GET:
        name = request.GET['name'],
        surname = request.GET['surname'],
        email = request.GET['email'],
        phone = request.GET['phone'],
        company = request.GET['company']

        if name and surname and email and phone and company:
            if Clients.objects.filter(email=request.GET['email']).exists():
                messages.info(request, "E-mail already exists.",
                              extra_tags='warning')
            elif Clients.objects.filter(phone=request.GET['phone']).exists():
                messages.info(
                    request, "Phone number already exists.", extra_tags='warning')
            else:
                save_data = Clients(
                    name=request.GET['name'],
                    surname=request.GET['surname'],
                    email=request.GET['email'],
                    phone=request.GET['phone'],
                    company=request.GET['company'],
                )

                save_data.save()
                messages.info(
                    request, "Customer information saved successfully.", extra_tags='success')
        else:
            messages.info(request, "Empty fields.", extra_tags='error')
    if 'search' in request.GET:
        data = Clients.objects.filter(Q(name__contains=request.GET['question']) | Q(surname__contains=request.GET['question']) | Q(phone__contains=request.GET['question']) | Q(
            email__contains=request.GET['question']) | Q(phone__contains=request.GET['question']) | Q(company__contains=request.GET['question'])).order_by('-id')
    else:
        if 'order' in request.GET:
            if request.GET['order'] == 'a':
                data = Clients.objects.all().order_by('name')
            elif request.GET['order'] == 'b':
                data = Clients.objects.all().order_by('-name')
            elif request.GET['order'] == 'c':
                data = Clients.objects.all().order_by('surname')
            elif request.GET['order'] == 'd':
                data = Clients.objects.all().order_by('-surname')
            elif request.GET['order'] == 'e':
                data = Clients.objects.all().order_by('email')
            elif request.GET['order'] == 'f':
                data = Clients.objects.all().order_by('-email')
            elif request.GET['order'] == 'g':
                data = Clients.objects.all().order_by('phone')
            elif request.GET['order'] == 'k':
                data = Clients.objects.all().order_by('-phone')
            elif request.GET['order'] == 'l':
                data = Clients.objects.all().order_by('company')
            elif request.GET['order'] == 'm':
                data = Clients.objects.all().order_by('-company')
            elif request.GET['order'] == 'n':
                data = Clients.objects.all().order_by('add_date')
            elif request.GET['order'] == 'o':
                data = Clients.objects.all().order_by('-add_date')
        else:
            data = Clients.objects.all().order_by('-id')

    return render(request, 'client.html', {'section': section, 'del_all': del_all, 'data': data, })


def client_delete(request, id):
    client = Clients.objects.get(id=id)
    data = Clients.objects.all().order_by('-id')
    return render(request, 'client.html', {'client': client, 'data': data})


def client_delete_config(request, id):
    clients = Clients.objects.get(id=id)
    active_orders = Orders.objects.filter(client_id=id).count()

    if active_orders > 0:
        messages.info(
            request, f"Client '{clients.name} {clients.surname}' cannot be deleted. There are {active_orders} active products in it.", extra_tags='error')
    else:
        clients.delete()
        messages.info(
            request, "Customer's data has been deleted successfully.", extra_tags='success')
    return redirect('client')


def client_edit(request, id):
    edit = Clients.objects.get(id=id)
    data = Clients.objects.all().order_by('-id')
    return render(request, 'client.html', {'edit': edit, 'data': data})


def client_update(request, id):
    name = request.GET['name']
    surname = request.GET['surname']
    email = request.GET['email']
    phone = request.GET['phone']
    company = request.GET['company']

    if name and surname and email and phone and company:
        if Clients.objects.filter(email=email).exclude(id=id).exists():
            messages.info(request, "E-mail already exists.")
        elif Clients.objects.filter(phone=phone).exclude(id=id).exists():
            messages.info(request, "Phone number already exists.")
        else:
            client = Clients.objects.get(id=id)
            client.name = request.GET['name']
            client.surname = request.GET['surname']
            client.email = request.GET['email']
            client.phone = request.GET['phone']
            client.company = request.GET['company']

            client.save()
            messages.info(request, "Client update was successful.",
                          extra_tags='success')
    else:
        messages.info(request, "Empety fields.", extra_tags='error')
    return redirect('client')


def expens(request):
    data = ''
    del_all = []
    section = 'expenses'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            for selected in choosen:
                picked = Expenses.objects.filter(id=selected)
                if picked.exists():
                    picked.delete()
            messages.info(
                request, "Expens data has been deleted successfully.", extra_tags='success')

    if 'save' in request.GET:
        if request.GET['assignment'] != '' and request.GET['amount'] != '':

            save_data = Expenses(
                assignment=request.GET['assignment'],
                amount=request.GET['amount']
            )
            save_data.save()
            messages.info(request, "Expens saved successfully.",
                          extra_tags='success')
        else:
            messages.info(request, "Empty field.", extra_tags='error')
    if 'search' in request.GET:
        data = Expenses.objects.filter(
            Q(assignment__contains=request.GET['question'])).order_by('-id')
    elif 'search' in request.GET:
        data = Expenses.objects.filter(
            Q(amount__contains=request.GET['question'])).order_by('-id')
    else:
        if 'order' in request.GET:
            if request.GET['order'] == 'a':
                data = Expenses.objects.all().order_by('assignment')
            elif request.GET['order'] == 'b':
                data = Expenses.objects.all().order_by('-assignment')
            elif request.GET['order'] == 'c':
                data = Expenses.objects.all().order_by('amount')
            elif request.GET['order'] == 'd':
                data = Expenses.objects.all().order_by('-amount')
            elif request.GET['order'] == 'e':
                data = Expenses.objects.all().order_by('add_date')
            elif request.GET['order'] == 'f':
                data = Expenses.objects.all().order_by('-add_date')
        else:
            data = Expenses.objects.all().order_by('-id')

    return render(request, 'expens.html', {'section': section, 'del_all': del_all, 'data': data, })


def expens_delete(request, id):
    expens = Expenses.objects.get(id=id)
    data = Expenses.objects.all().order_by('-id')
    return render(request, 'expens.html', {'expens': expens, 'data': data})


def expens_delete_config(request, id):
    Expenses.objects.get(id=id).delete()
    messages.info(
        request, "Expens data has been deleted successfully.", extra_tags='success')
    return redirect('expens')


def expens_edit(request, id):
    edit = Expenses.objects.get(id=id)
    data = Expenses.objects.all().order_by('-id')
    return render(request, 'expens.html', {'edit': edit, 'data': data})


def expens_update(request, id):
    assignment = request.GET['assignment']
    amount = request.GET['amount']

    if assignment and amount:
        expens = Expenses.objects.get(id=id)
        expens.assignment = request.GET['assignment']
        expens.amount = request.GET['amount']

        expens.save()
        messages.info(request, "Update was successful.", extra_tags='success')

    else:
        messages.info(request, "Empty field.", extra_tags='error')
    return redirect('expens')


def products(request):
    data = ''
    del_all = []
    section = 'products'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            delete_successful = True
            for selected in choosen:
                picked = Products.objects.filter(id=selected)
                active_orders = Orders.objects.filter(product=selected)
                if picked.exists() and active_orders.exists():
                    delete_successful = True
                    m = "Some product(s) could not be deleted due to active orders."
                elif picked.exists():
                    delete_successful = False
                    picked.delete()
                    m = ""

        if delete_successful:
            messages.info(
                request, m, extra_tags='error')
        else:
            messages.info(
                request, "Product(s) data has been deleted successfully.", extra_tags='success')

    if 'search' in request.GET:
        data = Products.objects.filter(
            Q(product=request.GET['question'])).order_by('-id')
    else:
        if 'order' in request.GET:
            if request.GET['order'] == 'a':
                data = Products.objects.all().order_by('product')
            elif request.GET['order'] == 'b':
                data = Products.objects.all().order_by('-product')
            elif request.GET['order'] == 'c':
                data = Products.objects.all().order_by('buy')
            elif request.GET['order'] == 'd':
                data = Products.objects.all().order_by('-buy')
            elif request.GET['order'] == 'e':
                data = Products.objects.all().order_by('sell')
            elif request.GET['order'] == 'f':
                data = Products.objects.all().order_by('-sell')
            elif request.GET['order'] == 'g':
                data = Products.objects.all().order_by('quantity')
            elif request.GET['order'] == 'h':
                data = Products.objects.all().order_by('-quantity')
            elif request.GET['order'] == 'i':
                data = Products.objects.all().order_by('add_date')
            elif request.GET['order'] == 'j':
                data = Products.objects.all().order_by('-add_date')
            elif request.GET['order'] == 'k':
                data = Products.objects.all().order_by('supplier_id_id')
            elif request.GET['order'] == 'l':
                data = Products.objects.all().order_by('-supplier_id_id')
            elif request.GET['order'] == 'm':
                data = Products.objects.all().order_by('brand_id')
            elif request.GET['order'] == 'n':
                data = Products.objects.all().order_by('-brand_id')
            elif request.GET['order'] == 'o':
                data = Products.objects.annotate(
                    calculated_profit=ExpressionWrapper(
                        F('sell') - F('buy') * F('quantity'),
                        output_field=FloatField()
                    )
                ).order_by('calculated_profit')
            elif request.GET['order'] == 'p':
                data = Products.objects.annotate(
                    calculated_profit=ExpressionWrapper(
                        F('sell') - F('buy') * F('quantity'),
                        output_field=FloatField()
                    )
                ).order_by('-calculated_profit')
        else:
            data = Products.objects.all().order_by('-id')
    brands = Brand.objects.all().order_by('brand_name')
    suppliers = Supplier.objects.all().order_by('supplier_name')

    return render(request, 'products.html', {'section': section, 'del_all': del_all, 'data': data, 'brands': brands, 'suppliers': suppliers, })


def products_delete(request, id):
    products = Products.objects.get(id=id)
    data = Products.objects.all().order_by('-id')
    return render(request, 'products.html', {'products': products, 'data': data})


def products_delete_config(request, id):
    products = Products.objects.get(id=id)
    active_order = Orders.objects.filter(product_id=id).count()

    if active_order > 0:
        messages.info(
            request, f"Product '{products.product}' cannot be deleted. There are {active_order} active products in it.", extra_tags='error')
    else:
        products.delete()
        messages.info(
            request, "Products data has been deleted successfully.", extra_tags='success')
    return redirect('products')


def products_edit(request, id):
    edit = Products.objects.get(id=id)
    brands = Brand.objects.all().order_by('brand_name')
    data = Products.objects.all().order_by('-id')
    suppliers = Supplier.objects.all().order_by('-id')
    return render(request, 'products.html', {'edit': edit, 'data': data, 'brands': brands, 'suppliers': suppliers})


def products_update(request, id):
    product = request.GET['product']
    buy = request.GET['buy']
    sell = request.GET['sell']
    quantity = request.GET['quantity']
    brand = Brand.objects.get(id=request.GET['brand_id'])

    if product and buy and sell and quantity and brand:
        product = Products.objects.get(id=id)
        product.buy = request.GET['buy']
        product.sell = request.GET['sell']
        product.quantity = request.GET['quantity']
        product.brand = brand

        product.save()
        messages.info(request, "Update was successful.", extra_tags='success')
    else:
        messages.info(request, "Empty field.", extra_tags='error')
    return redirect('products')


def orders(request):
    data = ''
    del_all = []
    section = 'orders'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            for selected in choosen:
                picked = Orders.objects.filter(id=selected)
                if picked.exists():
                    picked.delete()
            messages.info(
                request, "Orders data has been deleted successfully.", extra_tags='success')

    if 'enter' in request.GET:

        if request.GET['client_id'] != '' and request.GET['product_id'] != '' and request.GET['amount'] != '':

            client = Clients.objects.get(id=request.GET['client_id'])
            product = Products.objects.get(id=request.GET['product_id'])

            save_data = Orders(
                client=client,
                product=product,
                amount=request.GET['amount']
            )
            save_data.save()
            messages.info(request, "Order saved successfully.",
                          extra_tags='success')
        else:
            messages.info(request, "Empty field", extra_tags='error')
    if 'search' in request.GET:
        data = Orders.objects.filter(
            Q(orders__contains=request.GET['question'])).order_by('-id')
    else:
        if 'order' in request.GET:
            if request.GET['order'] == 'a':
                data = Orders.objects.all().order_by('client_id')
            elif request.GET['order'] == 'b':
                data = Orders.objects.all().order_by('-client_id')
            elif request.GET['order'] == 'c':
                data = Orders.objects.all().order_by('product__brand__brand_name')
            elif request.GET['order'] == 'd':
                data = Orders.objects.all().order_by('-product__brand__brand_name')
            elif request.GET['order'] == 'e':
                data = Orders.objects.all().order_by('product_id')
            elif request.GET['order'] == 'f':
                data = Orders.objects.all().order_by('-product_id')
            elif request.GET['order'] == 'g':
                data = Orders.objects.all().order_by('amount')
            elif request.GET['order'] == 'h':
                data = Orders.objects.all().order_by('-amount')
            elif request.GET['order'] == 'i':
                data = Orders.objects.all().order_by('product__buy')
            elif request.GET['order'] == 'j':
                data = Orders.objects.all().order_by('-product__buy')
            elif request.GET['order'] == 'k':
                data = Orders.objects.all().order_by('product__sell')
            elif request.GET['order'] == 'l':
                data = Orders.objects.all().order_by('-product__sell')
            elif request.GET['order'] == 'm':
                data = Orders.objects.all().order_by('product__quantity')
            elif request.GET['order'] == 'n':
                data = Orders.objects.all().order_by('-product__quantity')
            elif request.GET['order'] == 'o':
                data = Orders.objects.annotate(
                    calculated_profit=ExpressionWrapper(
                        F('product__sell') - F('product__buy') * F('amount'),
                        output_field=FloatField()
                    )
                ).order_by('calculated_profit')
            elif request.GET['order'] == 'p':
                data = Orders.objects.annotate(
                    calculated_profit=ExpressionWrapper(
                        F('product__sell') - F('product__buy') * F('amount'),
                        output_field=FloatField()
                    )
                ).order_by('-calculated_profit')
            elif request.GET['order'] == 'q':
                data = Orders.objects.all().order_by('add_date')
            elif request.GET['order'] == 'r':
                data = Orders.objects.all().order_by('-add_date')
        else:
            data = Orders.objects.all().order_by('-id')

    client = Clients.objects.all().order_by('name')
    product = Products.objects.all().order_by('product')

    return render(request, 'orders.html', {'section': section, 'del_all': del_all, 'client': client, 'product': product, 'data': data, })


def orders_delete(request, id):
    orders = Orders.objects.get(id=id)
    data = Orders.objects.all().order_by('-id')
    return render(request, 'orders.html', {'orders': orders, 'data': data})


def orders_delete_config(request, id):
    orders = Orders.objects.get(id=id)
    orders.delete()
    messages.info(
        request, "Order data has been deleted successfully.", extra_tags='success')
    return redirect('orders')


def orders_edit(request, id):
    edit = Orders.objects.get(id=id)
    client = Clients.objects.all()
    product = Products.objects.all()
    brands = Brand.objects.all().order_by('brand_name')
    data = Orders.objects.all().order_by('-id')
    return render(request, 'orders.html', {'product': product, 'client': client, 'edit': edit, 'data': data, 'brands': brands})


def orders_update(request, id):
    client = Clients.objects.get(id=request.GET['client_id'])
    product = Products.objects.get(id=request.GET['product_id'])
    amount = Orders.objects.get(id=id)

    if client and product and amount:
        orders = Orders.objects.get(id=id)
        orders.client = client
        orders.product = product
        orders.amount = request.GET['amount']

        orders.save()
        messages.info(request, "Update was successful.", extra_tags='success')
    else:
        messages.info(request, "Empty field.", extra_tags='error')
    return redirect('orders')


def orders_tesdiq(request, id):

    order = Orders.objects.get(id=id)

    if order.amount <= order.product.quantity:

        result = order.product.quantity - order.amount

        product = Products.objects.get(id=order.product.id)
        product.quantity = result
        product.save()

        order.tesdiq = 1
        order.save()

        messages.info(request, "Confirm was successful.", extra_tags='success')
    else:
        messages.info(
            request, "There is no enough products in stock to confirm this order.", extra_tags='error')

    return redirect('orders')


def orders_cancel(request, id):

    order = Orders.objects.get(id=id)
    result = order.product.quantity + order.amount

    product = Products.objects.get(id=order.product.id)
    product.quantity = result
    product.save()

    order.tesdiq = 0
    order.save()
    messages.info(
        request, "Product confirm was successfully terminated", extra_tags='success')

    return redirect('orders')


def departments(request):
    data = ''
    del_all = []
    section = 'departments'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            delete_successful = True
            for selected in choosen:
                picked = Departments.objects.filter(id=selected)
                active_positions = Positions.objects.filter(dep_id_id=selected)
                if picked.exists() and active_positions.exists():
                    delete_successful = True
                    m = "Some department(s) could not be deleted due to active positions."
                elif picked.exists():
                    delete_successful = False
                    picked.delete()
                    m = ""

        if delete_successful:
            messages.info(
                request, m, extra_tags='error')
        else:
            messages.info(
                request, "Department(s) data has been deleted successfully.", extra_tags='success')

    if 'add' in request.GET:
        department_name = request.GET['department_name']

        if department_name:
            if Departments.objects.filter(department_name=request.GET['department_name']).exists():
                messages.info(
                    request, "Departments already exists.", extra_tags='warning')
            else:
                save_data = Departments(
                    department_name=request.GET['department_name']
                )
                save_data.save()
                messages.info(
                    request, "Departments added successfully.", extra_tags='success')
        else:
            messages.info(request, "Departments name is required.",
                          extra_tags='error')
    if 'search' in request.GET:
        data = Departments.objects.filter(
            Q(department_name__contains=request.GET['question'])).order_by('-id')
    else:
        if 'order' in request.GET:
            if request.GET['order'] == 'a':
                data = Departments.objects.all().order_by('department_name')
            elif request.GET['order'] == 'b':
                data = Departments.objects.all().order_by('-department_name')
            elif request.GET['order'] == 'c':
                data = Departments.objects.all().order_by('date')
            elif request.GET['order'] == 'd':
                data = Departments.objects.all().order_by('-date')
        else:
            data = Departments.objects.all().order_by('-id')

    return render(request, 'department.html', {'section': section, 'del_all': del_all, 'data': data, })


def department_del(request, id):
    departments = Departments.objects.get(id=id)
    data = Departments.objects.all().order_by('-id')
    return render(request, 'department.html', {'departments': departments, 'data': data})


def department_del_conf(request, id):
    departments = Departments.objects.get(id=id)
    position = Positions.objects.filter(dep_id_id=id).count()

    if position > 0:
        messages.info(
            request, f"Department '{departments.department_name}' cannot be deleted. There are {position} active position in it.", extra_tags='error')
    else:
        departments.delete()
        messages.info(
            request, "Department  has been deleted successfully.", extra_tags='success')
    return redirect('departments')


def department_edit(request, id):
    edit = Departments.objects.get(id=id)
    data = Departments.objects.all().order_by('-id')
    return render(request, 'department.html', {'edit': edit, 'data': data})


def department_update(request, id):
    department_name = request.GET['department_name']

    if department_name:
        departments = Departments.objects.get(id=id)
        departments.department_name = request.GET['department_name']

        departments.save()
        messages.info(request, "Update was successful.", extra_tags='success')
    else:
        messages.info(request, "Empty field.", extra_tags='error')
    return redirect('departments')


def positions(request):
    data = ''
    number = ''
    del_all = []
    section = 'positions'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            delete_successful = True
            for selected in choosen:
                picked = Positions.objects.filter(id=selected)
                active_staff = Staff.objects.filter(pos_id_id=selected)
                if picked.exists() and active_staff.exists():
                    delete_successful = True
                    m = "Some position(s) could not be deleted due to active staff member in it."
                elif picked.exists():
                    delete_successful = False
                    picked.delete()
                    m = ""
        if delete_successful:
            messages.info(
                request, m, extra_tags='error')
        else:
            messages.info(
                request, "Position(s) data has been deleted successfully.", extra_tags='success')

    if 'add' in request.GET:
        if request.GET['department_id'] != '' and request.GET['position_name'] != '':

            departments = Departments.objects.get(
                id=request.GET['department_id'])

            save_data = Positions(
                dep_id=departments,
                positions=request.GET['position_name']
            )
            save_data.save()
            messages.info(request, "Position saved.", extra_tags='success')

        else:
            messages.info(request, "Position name is required.",
                          extra_tags='error')
    if 'search' in request.GET:
        data = Positions.objects.filter(
            Q(position_name___contains=request.GET['question'])).order_by('-id')
    else:
        if 'order' in request.GET:
            if request.GET['order'] == 'a':
                data = Positions.objects.all().order_by('dep_id__department_name')
            elif request.GET['order'] == 'b':
                data = Positions.objects.all().order_by('-dep_id__department_name')
            elif request.GET['order'] == 'c':
                data = Positions.objects.all().order_by('positions')
            elif request.GET['order'] == 'd':
                data = Positions.objects.all().order_by('-positions')
            elif request.GET['order'] == 'e':
                data = Positions.objects.all().order_by('date')
            elif request.GET['order'] == 'f':
                data = Positions.objects.all().order_by('-date')
        else:
            data = Positions.objects.all().order_by('-id')
    number = Positions.objects.count()
    departments = Departments.objects.all().order_by('department_name')

    return render(request, 'positions.html', {'section': section, 'del_all': del_all, 'data': data, 'number': number, 'departments': departments})


def position_del(request, id):
    positions = Positions.objects.get(id=id)
    data = Positions.objects.all().order_by('-id')
    return render(request, 'positions.html', {'positions': positions, 'data': data})


def position_del_conf(request, id):
    positions = Positions.objects.get(id=id)
    staffs = Staff.objects.filter(pos_id=id).count()
    if staffs > 0:
        messages.info(
            request, f"Position '{positions.positions}' cannot be deleted. There are {staffs} active staff in it.", extra_tags='error')
    else:
        positions.delete()
        messages.info(
            request, "Positions has been deleted successfully.", extra_tags='success')
    return redirect('positions')


def position_edit(request, id):
    edit = Positions.objects.get(id=id)
    departments = Departments.objects.all().order_by('department_name')
    data = Positions.objects.all().order_by('-id')
    return render(request, 'positions.html', {'edit': edit, 'departments': departments, 'data': data})


def position_update(request, id):
    position = request.GET['position_name']
    departments = Departments.objects.get(id=request.GET['departments_id'])

    if position and departments:
        update = Positions.objects.get(id=id)
        update.positions = request.GET['position_name']
        update.dep_id = departments

        update.save()
        messages.info(request, "Update was successful.", extra_tags='success')
    else:
        messages.info(request, "Empty field.", extra_tags='error')
    return redirect('positions')


def staff(request):
    data = ''
    file_url = ''
    del_all = ''
    section = 'staffs'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            delete_successful = True
            for selected in choosen:
                picked = Staff.objects.filter(id=selected)
                active_doc = Documents.objects.filter(staff_id_id=selected)
                if picked.exists() and active_doc.exists():
                    delete_successful = True
                    m = "Some staff(s) could not be deleted due to active document(s) in it."
                elif picked.exists():
                    delete_successful = False
                    picked.delete()
                    m = ""
        if delete_successful:
            messages.info(
                request, m, extra_tags='error')
        else:
            messages.info(
                request, "Staff(s) data has been deleted successfully.", extra_tags='success')

    if 'add' in request.GET:

        if request.GET['s_name'] != '' and request.GET['s_surname'] != '' and request.GET['s_birth_d'] != '' and request.GET['s_email'] != '' and request.GET['s_phone'] != '' and request.GET['s_sallary'] != '' and request.GET['s_start_d'] != '':
            positions = Positions.objects.get(id=request.GET['position_id'])

            if Staff.objects.filter(email=request.GET['s_email']).exists():
                messages.info(request, 'Email already exists.',
                              extra_tags='warning')
            elif Staff.objects.filter(phone=request.GET['s_phone']).exists():
                messages.info(request, 'Phone already exists.',
                              extra_tags='warning')
            elif 'photo' in request.FILES:
                # FOTO START
                upload = request.FILES['photo']
                fs = FileSystemStorage()
                file = fs.save(upload.name, upload)
                file_url = fs.url(file)
                # FOTO END

                save_info = Staff(
                    name=request.GET['s_name'],
                    surname=request.GET['s_surname'],
                    birth_date=request.GET['s_birth_d'],
                    email=request.GET['s_email'],
                    phone=request.GET['s_phone'],
                    sallary=request.GET['s_sallary'],
                    j_start_d=request.GET['s_start_d'],
                    photo=file_url,
                    pos_id=positions,
                )
                save_info.save()
                messages.info(
                    request, "Employee  saved successfully.", extra_tags='success')

            if 'documents' in request.GET:
                return redirect('documents')
        else:
            messages.info(request, "Empty fields.", extra_tags='error')
    if 'search' in request.GET:
        data = Staff.objects.filter(
            Q(staff__contains=request.GET['question'])).order_by('-id')
    else:
        if 'order' in request.GET:
            if request.GET['order'] == 'a':
                data = Staff.objects.all().order_by('name')
            elif request.GET['order'] == 'b':
                data = Staff.objects.all().order_by('-name')
            elif request.GET['order'] == 'c':
                data = Staff.objects.all().order_by('surname')
            elif request.GET['order'] == 'd':
                data = Staff.objects.all().order_by('-surname')
            elif request.GET['order'] == 'e':
                data = Staff.objects.all().order_by('birth_date')
            elif request.GET['order'] == 'f':
                data = Staff.objects.all().order_by('-birth_date')
            elif request.GET['order'] == 'g':
                data = Staff.objects.all().order_by('email')
            elif request.GET['order'] == 'h':
                data = Staff.objects.all().order_by('-email')
            elif request.GET['order'] == 'i':
                data = Staff.objects.all().order_by('phone')
            elif request.GET['order'] == 'j':
                data = Staff.objects.all().order_by('-phone')
            elif request.GET['order'] == 'k':
                data = Staff.objects.all().order_by('sallary')
            elif request.GET['order'] == 'l':
                data = Staff.objects.all().order_by('-sallary')
            elif request.GET['order'] == 'm':
                data = Staff.objects.all().order_by('j_start_d')
            elif request.GET['order'] == 'n':
                data = Staff.objects.all().order_by('-j_start_d')
            elif request.GET['order'] == 'o':
                data = Staff.objects.all().order_by('pos_id__dep_id__department_name')
            elif request.GET['order'] == 'p':
                data = Staff.objects.all().order_by('-pos_id__dep_id__department_name')
            elif request.GET['order'] == 'q':
                data = Staff.objects.all().order_by('pos_id__positions')
            elif request.GET['order'] == 'r':
                data = Staff.objects.all().order_by('-pos_id__positions')
        else:
            data = Staff.objects.all().order_by('-id')

    departments = Departments.objects.all().order_by('department_name')
    positions = Positions.objects.all().order_by('positions')
    return render(request, 'staff.html', {'section': section, 'del_all': del_all, 'data': data, 'departments': departments, 'positions': positions})


def staff_delete(request, id):
    staff = Staff.objects.get(id=id)
    data = Staff.objects.all().order_by('-id')
    return render(request, 'staff.html', {'staff': staff, 'data': data})


def staff_del_conf(request, id):
    staffs = Staff.objects.get(id=id)
    documents = Documents.objects.filter(staff_id_id=id).count()
    if documents > 0:
        messages.info(
            request, f"Staff '{staffs.name}' cannot be deleted. There are {documents} active staff in it.", extra_tags='error')
    else:
        messages.info(
            request, "Employee has been deleted successfully.", extra_tags='success')
    return redirect('staff')


def staff_edit(request, id):
    edit = Staff.objects.get(id=id)
    data = Staff.objects.all().order_by('-id')
    positions = Positions.objects.all().order_by('positions')
    return render(request, 'staff.html', {'positions': positions, 'edit': edit, 'departments': departments, 'data': data})


def staff_update(request, id):
    update = Staff.objects.get(id=id)

    name = request.GET.get('s_name')
    surname = request.GET.get('s_surname')
    birth_date_str = request.GET.get('s_birth_d')
    email = request.GET.get('s_email')
    phone = request.GET.get('s_phone')
    sallary = request.GET.get('s_sallary')
    j_start_d_str = request.GET.get('s_start_d')
    position_id = request.GET.get('position_id')

    position = Positions.objects.get(id=position_id)

    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
    j_start_d = datetime.strptime(j_start_d_str, '%Y-%m-%d').date()

    if not (name and surname and birth_date_str and email and phone and sallary and j_start_d_str):
        messages.error(request, "All fields are required.", extra_tags='error')
    else:
        if 'photo' in request.FILES:
            new_photo = request.FILES['photo']
            update.photo = new_photo
            fs = FileSystemStorage()
            file = fs.save(new_photo.name, new_photo)
            file_url = fs.url(file)
            update.photo = file_url
        # Update other fields
        update.name = name
        update.surname = surname
        update.birth_date = birth_date
        update.email = email
        update.phone = phone
        update.sallary = sallary
        update.j_start_d = j_start_d
        update.pos_id = position
        update.save()
        messages.success(request, "Update was successful.",
                         extra_tags='success')
    return redirect('staff')


def documents(request, staf_id):
    data = ''
    file_url = ''
    del_all = []
    section = 'documents'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            for selected in choosen:
                picked = Documents.objects.filter(id=selected)
                if picked.exists():
                    picked.delete()
                messages.info(
                    request, "Document(s) data has been deleted successfully.", extra_tags='success')

    if 'upload' in request.GET:
        title = request.GET['doc_name']
        doc_num = request.GET['doc_num']
        about = request.GET['about']

        if title and doc_num and 'doc_photo' in request.FILES:

            name = Staff.objects.get(id=staf_id)

            if Documents.objects.filter(doc_num=request.GET['doc_num']).exists():
                messages.info(request, "Document already exists.",
                              extra_tags='error')
            else:
                upload = request.FILES['doc_photo']
                fs = FileSystemStorage()
                file = fs.save(upload.name, upload)
                file_url = fs.url(file)

                save_info = Documents(
                    title=request.GET['doc_name'],
                    doc_num=request.GET['doc_num'],
                    about=request.GET['about'],
                    scan_photo=file_url,
                    staff_id=name,
                )
                save_info.save()

                messages.info(
                    request, "Document  saved successfully.", extra_tags='success')
        else:
            messages.info(request, "Empty fields", extra_tags='warning')

    if 'search' in request.GET:
        data = Documents.objects.filter(Q(documents__contains=request.GET['question'])).filter(
            staff_id=staf_id).order_by('-id')
    else:
        if 'order' in request.GET:
            if request.GET['order'] == 'a':
                data = Documents.objects.order_by('staff_id__name')
            elif request.GET['order'] == 'b':
                data = Documents.objects.order_by('-staff_id__name')
            elif request.GET['order'] == 'c':
                data = Documents.objects.order_by('title')
            elif request.GET['order'] == 'd':
                data = Documents.objects.order_by('-title')
            elif request.GET['order'] == 'e':
                data = Documents.objects.order_by('doc_num')
            elif request.GET['order'] == 'f':
                data = Documents.objects.order_by('-doc_num')
            elif request.GET['order'] == 'g':
                data = Documents.objects.order_by('about')
            elif request.GET['order'] == 'e':
                data = Documents.objects.order_by('-about')
        else:
            data = Documents.objects.all().filter(staff_id=staf_id).order_by('-id')

    staff = Staff.objects.get(id=staf_id)
    return render(request, 'documents.html', {'section': section, 'del_all': del_all, 'data': data, 'staff': staff})


def document_delete(request, doc_id):
    doc = Documents.objects.get(id=doc_id)
    staff = Staff.objects.get(id=doc.staff_id.id)
    data = Documents.objects.filter(staff_id=staff.id).order_by('-id')
    return render(request, 'documents.html', {'doc': doc, 'data': data, 'staff': staff})


def doc_del_conf(request, doc_d_id):
    doc = Documents.objects.get(id=doc_d_id)
    staff = Staff.objects.get(id=doc.staff_id.id)
    doc.delete()
    messages.info(
        request, "Document has been deleted successfully.", extra_tags='success')
    return HttpResponseRedirect('/documents/'+str(staff.id))


def doc_edit(request, doc_id):
    edit = Documents.objects.get(id=doc_id)
    staff = Staff.objects.get(id=edit.staff_id.id)
    data = Documents.objects.all().order_by('-id')
    return render(request, 'documents.html', {'edit': edit, 'data': data, 'staff': staff})


def doc_update(request, doc_id):
    update = Documents.objects.get(id=doc_id)

    title = request.GET['doc_name']
    doc_num = request.GET['doc_num']
    about = request.GET['about']

    if title and doc_num and about:

        if Documents.objects.filter(doc_num=request.GET['doc_num']).exclude(id=doc_id).exists():
            messages.info(request, 'Document already exists.',
                          extra_tags='error')
        else:
            if 'doc_photo' in request.FILES:
                new_photo = request.FILES['doc_photo']
                update.scan_photo = new_photo
                fs = FileSystemStorage()
                file = fs.save(new_photo.name, new_photo)
                file_url = fs.url(file)
                update.scan_photo = file_url

            update.title = title
            update.doc_num = doc_num
            update.about = about
            update.save()
            messages.success(request, "Update was successful.",
                             extra_tags='success')
    staff_id = update.staff_id.id
    return HttpResponseRedirect('/documents/'+str(staff_id))


def user_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confrim_p = request.POST['r_password']
        birth_d = request.POST['u_birth']
        phone = request.POST['phone']

        if 'signup' in request.POST:
            if name and phone and birth_d and surname and username and email and password and confrim_p:
                if password == confrim_p:
                    if myUser.objects.filter(username=username).exists():
                        messages.info(
                            request, 'Username already exists.', extra_tags='warning')
                        return redirect('user_register')
                    elif myUser.objects.filter(phone=phone).exists():
                        messages.info(
                            request, 'Phone already exists.', extra_tags='warning')
                    elif myUser.objects.filter(email=email).exists():
                        messages.info(
                            request, 'Email already exists.', extra_tags='warning')
                        return redirect('user_register')
                    else:
                        user_data = myUser.objects.create_user(
                            first_name=name,
                            last_name=surname,
                            username=username,
                            password=password,
                            phone=phone,
                            birth_date=birth_d,
                            email=email,
                        )
                        user_data.save()
                        messages.info(
                            request, "Registration was succesfull", extra_tags='success')
                        return redirect('user_profile')
                else:
                    messages.info(
                        request, "Passwords do not match.", extra_tags='warning')
                    return redirect('home')
            else:
                messages.info(request, "Empty fields.", extra_tags='error')
    return render(request, 'home.html')


def login_user(request):
    username = ''
    password = ''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.info(
                    request, "Welcome!", extra_tags='success')
                return redirect('user_profile')
            else:
                messages.info(
                    request, "Username and password are incorrect.", extra_tags='warning')
                return redirect('login_user')
        else:
            messages.info(request, "Empty fields.", extra_tags='error')
    return render(request, 'home.html')


def logout_user(request):
    auth.logout(request)
    return redirect('home')


def user_profile(request):
    return render(request, 'profile.html')


def user_profile_update(request):
    file_url = ''
    password = request.POST['password']
    new_password = request.POST['n_password']
    c_password = request.POST['c_password']
    birth_date_str = request.POST.get('u_birth')
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

    if 'update' in request.POST:
        if password:
            if User.objects.filter(email=request.POST['email']).exclude(id=request.user.id).exclude(email=request.POST['email']):
                messages.info(request, "Email already exists.",
                              extra_tags='warning')
            elif User.objects.filter(phone=request.POST['tel_n']).exclude(id=request.user.id).exclude(phone=request.POST['tel_n']):
                messages.info(
                    request, "Phone number already exists.", extra_tags='warning')
            elif User.objects.filter(username=request.POST['user_name']).exclude(id=request.user.id).exclude(username=request.POST['user_name']):
                messages.info(request, "Username already exists.",
                              extra_tags='warning')
            elif check_password(request.POST['password'], request.user.password):
                user = myUser.objects.get(id=request.user.id)
                user.first_name = request.POST['name']
                user.last_name = request.POST['surname']
                user.birth_date = birth_date
                user.email = request.POST['email']
                user.phone = request.POST['tel_n']
                user.comp_name = request.POST['company_n']
                user.save()
                messages.info(request, "Profile updated.",
                              extra_tags='success')

            if 'p_photo' in request.FILES:
                upload = request.FILES['p_photo']
                fs = FileSystemStorage()
                file = fs.save(upload.name, upload)
                file_url = fs.url(file)
                user.profile_photo = file_url
                user.save()
                messages.info(request, "Profile picture updated.",
                              extra_tags='success')

            if new_password != '':
                if new_password == c_password:
                    user = myUser.objects.get(id=request.user.id)
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, request.user)
                    user_auth = auth.authenticate(
                        request, username=request.POST['name'], password=new_password)
                    auth.login(request, user_auth)
                    messages.info(
                        request, "Password updated successfully.", extra_tags='success')
                else:
                    messages.info(request, "Password don't match.",
                                  extra_tags='error')

        else:
            messages.info(request, "Incorrect password", extra_tags='error')
    return redirect('user_profile')


def assignments(request):
    data = ''
    number = ''
    del_all = []
    section = 'assignments'

    if 'delete_all' in request.GET:
        del_all = request.GET.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.GET:
        choosen = request.GET.getlist('x[]')
        if choosen:
            for selected in choosen:
                picked = Assignments.objects.filter(id=selected)
                if picked.exists():
                    picked.delete()
            messages.info(
                request, "Assignments data has been deleted successfully.", extra_tags='success')

    if 'add' in request.GET:
        assignment_name = request.GET['assign_n']
        sontarix = request.GET['deadline'].replace('T', ' ')

        if assignment_name and sontarix:

            staffs = Staff.objects.get(id=request.GET['staff_id'])

            assignment = Assignments(
                assignment_name=request.GET['assign_n'],
                deadline=sontarix,
                staff_id=staffs
            )
            assignment.save()
            messages.info(request, "Assignment successfully aded.",
                          extra_tags='success')
        else:
            messages.info(request, "Empty fields.", extra_tags='error')

    data = Assignments.objects.all().order_by('-id')
    number = Assignments.objects.count()

    staffs = Staff.objects.all().order_by('name')
    departments = Departments.objects.all().order_by('department_name')
    positions = Positions.objects.all().order_by('positions')
    return render(request, 'assignments.html', {'section': section, 'del_all': del_all, 'data': data, 'departments': departments, 'positions': positions, 'number': number, 'staffs': staffs})


def assignments_del(request, assign_id):
    assignment = Assignments.objects.get(id=assign_id)
    data = Assignments.objects.all().order_by('-id')
    return render(request, 'assignments.html', {'assignment': assignment, 'data': data})


def assignments_del_conf(request, assign_id):
    Assignments.objects.get(id=assign_id).delete()
    messages.info(
        request, "Assignment has been deleted successfully.", extra_tags='success')
    return redirect('assignments')


def assignment_edit(request, assign_id):
    staffs = Staff.objects.all().order_by('name')
    edit = Assignments.objects.get(id=assign_id)
    data = Assignments.objects.all().order_by('-id')
    return render(request, 'assignments.html', {'edit': edit, 'data': data, 'staffs': staffs})


def assignment_update(request, assign_id):
    update = Assignments.objects.get(id=assign_id)
    assignment_name = request.GET['assign_n']
    deadline_d_str = request.GET['deadline']
    staffs = Staff.objects.get(id=request.GET['staff_id'])

    if assignment_name and deadline:

        deadline = datetime.strptime(deadline_d_str, '%Y-%m-%dT%H:%M')
        update.assignment_name = assignment_name
        update.deadline = deadline
        update.staff_id = staffs

        update.save()
        messages.info(request, "Assignment updated successfully.",
                      extra_tags='success')
    else:
        messages.info(request, "Empty fields.", extra_tags='error')
    return redirect('assignments')


def assignments_approve(request, assign_id):

    assignments = Assignments.objects.get(id=assign_id)

    if assignments.time_remaining != 'Finished':
        assignments.approve = 1
        assignments.save()
        messages.info(request, "Task complete successfully.",
                      extra_tags='success')

    else:
        messages.info(request, "Task time expired.", extra_tags='warning')

    return redirect('assignments')


def assignment_cancel(request, assign_id):

    assignments = Assignments.objects.get(id=assign_id)
    assignments.approve = 0
    assignments.save()
    messages.info(request, "The task was added again.", extra_tags='success')

    return redirect('assignments')


def supplier(request):
    file_url = ''
    data = ''
    del_all = []
    section = 'suppliers'

    if 'delete_all' in request.POST:
        del_all = request.POST.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.POST:
        choosen = request.POST.getlist('x[]')
        if choosen:
            delete_successful = True
            for selected in choosen:
                picked = Supplier.objects.filter(id=selected)
                active_products = Products.objects.filter(
                    supplier_id_id=selected)
                if picked.exists() and active_products.exists():
                    delete_successful = True
                    m = "Some supplier(s) could not be deleted due to active product(s)."
                elif picked.exists():
                    delete_successful = False
                    picked.delete()
                    m = ""

        if delete_successful:
            messages.info(
                request, m, extra_tags='error')
        else:
            messages.info(
                request, "Supplier(s) data has been deleted successfully.", extra_tags='success')

    if 'save' in request.POST:
        supp_name = request.POST['sup_name']
        supp_surname = request.POST['sup_surname']
        supp_comp_name = request.POST['sup_comp_name']
        supp_email = request.POST['supp_email']
        supp_phone = request.POST['supp_phone']
        supp_address = request.POST['supp_address']

        if supp_name and supp_surname and supp_comp_name and supp_email and supp_phone and supp_address and 'sup_photo' in request.FILES:
            if Supplier.objects.filter(supplier_email=request.POST['supp_email']).exists():
                messages.info(request, "Email already exists.",
                              extra_tags='warning')
            elif Supplier.objects.filter(supplier_phone=request.POST['supp_phone']).exists():
                messages.info(request, "Phone already exists.",
                              extra_tags='warning')
            else:
                upload = request.FILES['sup_photo']
                file_ss = FileSystemStorage()
                file = file_ss.save(upload.name, upload)
                file_url = file_ss.url(file)

                supplier = Supplier(
                    supplier_name=supp_name,
                    supplier_surname=supp_surname,
                    supplier_company_name=supp_comp_name,
                    supplier_email=supp_email,
                    supplier_phone=supp_phone,
                    supplier_address=supp_address,
                    supplier_photo=file_url
                )
                supplier.save()
                messages.info(
                    request, "Supplier added successfully.", extra_tags='success')
        else:
            messages.info(request, "Empty fields.", extra_tags='error')
    if 'serach' in request.POST:
        data = Supplier.objects.filter(Q(supplier_name__contains=request.POST['question']) | Q(supplier_surname__contains=request.POST['question']) | Q(supplier_email__contains=request.POST['question']) | Q(
            supplier_phone__contains=request.POST['question']) | Q(supplier_address__contains=request.POST['question']) | Q(supplier_add_d__contains=request.POST['question']) | Q(supplier_company_name__contains=request.POST['question'])).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Supplier.objects.all().order_by('-supplier_name')
            elif request.POST['order'] == 'b':
                data = Supplier.objects.all().order_by('supplier_name')
            elif request.POST['order'] == 'c':
                data = Supplier.objects.all().order_by('-supplier_surname')
            elif request.POST['order'] == 'd':
                data = Supplier.objects.all().order_by('-supplier_company_name')
            elif request.POST['order'] == 'e':
                data = Supplier.objects.all().order_by('supplier_company_name')
            elif request.POST['order'] == 'f':
                data = Supplier.objects.all().order_by('-supplier_email')
            elif request.POST['order'] == 'g':
                data = Supplier.objects.all().order_by('supplier_email')
            elif request.POST['order'] == 'h':
                data = Supplier.objects.all().order_by('-supplier_phone')
            elif request.GET['order'] == 'i':
                data = Supplier.objects.all().order_by('supplier_phone')
            elif request.POST['order'] == 'j':
                data = Supplier.objects.all().order_by('-supplier_address')
            elif request.POST['order'] == 'k':
                data = Supplier.objects.all().order_by('supplier_address')
            elif request.POST['order'] == 'l':
                data = Supplier.objects.all().order_by('-supplier_add_d')
            elif request.POST['order'] == 'm':
                data = Supplier.objects.all().order_by('supplier_add_d')
        else:
            data = Supplier.objects.all().order_by('-id')
    return render(request, 'suppliers.html', {'section': section, 'del_all': del_all, 'data': data, })


def supplier_delete(request, supp_id):
    supplier = Supplier.objects.get(id=supp_id)
    data = Supplier.objects.all().order_by('-id')
    return render(request, 'suppliers.html', {'supplier': supplier, 'data': data})


def supplier_del_conf(request, supp_id):
    supplier = Supplier.objects.get(id=supp_id)
    number = Products.objects.filter(supplier_id_id=supp_id).count()

    if number > 0:
        messages.info(
            request, f"Supplier '{supplier.supplier_name}' cannot be deleted. There are {number} active products in it.", extra_tags='error')
    else:
        supplier.delete()
        messages.info(
            request, "Supplier has been deleted successfully.", extra_tags='success')
    return redirect('supplier')


def supplier_edit(request, supp_id):
    edit = Supplier.objects.get(id=supp_id)
    data = Supplier.objects.all().order_by('-id')
    return render(request, 'suppliers.html', {'edit': edit, 'data': data})


def supplier_update(request, supp_id):
    file_url = ''
    update = Supplier.objects.get(id=supp_id)

    if 'update' in request.GET:
        if Supplier.objects.filter(supplier_email=request.GET['supp_email']).exclude(id=update.id).exclude(supplier_email=request.GET['supp_email']):
            messages.info(request, "Email already exists.",
                          extra_tags='warning')
        elif Supplier.objects.filter(supplier_phone=request.GET['supp_phone']).exclude(id=update.id).exclude(supplier_phone=request.GET['supp_phone']):
            messages.info(request, "Phone already exists.",
                          extra_tags='warning')
        if 'sup_photo' in request.FILES:
            upload = request.FILES['sup_photo']
            filesystem = FileSystemStorage()
            file = filesystem.save(upload.name, upload)
            file_url = filesystem.url(file)
            update.supplier_photo = file_url
            update.save()
            messages.info(request, "Photo updated.", extra_tags='success')
        else:
            update.supplier_name = request.GET['sup_name']
            update.supplier_surname = request.GET['sup_surname']
            update.supplier_company_name = request.GET['sup_comp_name']
            update.supplier_email = request.GET['supp_email']
            update.supplier_phone = request.GET['supp_phone']
            update.supplier_address = request.GET['supp_address']
            update.save()
            messages.info(request, "Profile updated.", extra_tags='success')
    return redirect('supplier')
