# Create your views here.

from . models import Brand, Clients, Expenses, Products, Orders, Departments, Positions, Staff, Documents, myUser, Assignments, Supplier
from django.db.models import F, ExpressionWrapper, FloatField
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from datetime import datetime
from django.http import HttpRequest

User = get_user_model()


brand_num = Brand.objects.all().count()
product_num = Products.objects.all().count()
client_num = Clients.objects.all().count()
expens_num = Expenses.objects.all().count()
orders_num = Orders.objects.all().count()
department_num = Departments.objects.all().count()
position_num = Positions.objects.all().count()
sraff_num = Staff.objects.all().count()
document_num = Documents.objects.all().count()
assignment_num = Assignments.objects.all().count()
supplier_num = Supplier.objects.all().count()


def home(request):
    return render(request, 'home.html')


def main(request):
    return render(request, 'main_layout.html')


def basic(request):
    return render(request, 'basic.html')


def brand(request):
    data = ''
    del_all = []

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

    if 'save1' in request.POST:
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
                messages.info(request, "Brand saved.", extra_tags='success')
            else:
                messages.info(request, "Photo is required.",
                              extra_tags='error')
        else:
            messages.info(request, "Brand name is required.",
                          extra_tags='warning')
    if 'question' in request.POST:
        data = Brand.objects.filter(
            Q(brand_name__contains=request.POST['question'])).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Brand.objects.all().order_by('brand_name')
            elif request.POST['order'] == 'z':
                data = Brand.objects.all().order_by('-brand_name')
            elif request.POST['order'] == 'd':
                data = Brand.objects.all().order_by('add_date')
            elif request.POST['order'] == 'e':
                data = Brand.objects.all().order_by('-add_date')
        else:
            data = Brand.objects.all().order_by('-id')

    return render(request, 'brand.html', {'orders_num': orders_num, 'brand_num': brand_num, 'product_num': product_num, 'del_all': del_all, 'data': data, })


def delete(request, id):
    brand = Brand.objects.get(id=id)
    data = Brand.objects.all().order_by('-id')
    return render(request, 'brand.html', {'brand': brand, 'data': data, })


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
    brand_name = request.POST['brand_name']

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
            update.brand_name = request.POST['brand_name']
            update.save()
            messages.info(request, "Brand update was successful.",
                          extra_tags='success')
    else:
        messages.info(request, "Brand name is required", extra_tags='error')
    return redirect('brand')


def client(request):
    data = ''
    del_all = []

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
    if 'search' in request.POST:
        data = Clients.objects.filter(Q(name__contains=request.POST['question']) | Q(surname__contains=request.POST['question']) | Q(phone__contains=request.POST['question']) | Q(
            email__contains=request.POST['question']) | Q(phone__contains=request.POST['question']) | Q(company__contains=request.POST['question'])).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Clients.objects.all().order_by('name')
            elif request.POST['order'] == 'b':
                data = Clients.objects.all().order_by('-name')
            elif request.POST['order'] == 'c':
                data = Clients.objects.all().order_by('surname')
            elif request.POST['order'] == 'd':
                data = Clients.objects.all().order_by('-surname')
            elif request.POST['order'] == 'e':
                data = Clients.objects.all().order_by('email')
            elif request.POST['order'] == 'f':
                data = Clients.objects.all().order_by('-email')
            elif request.POST['order'] == 'g':
                data = Clients.objects.all().order_by('phone')
            elif request.POST['order'] == 'k':
                data = Clients.objects.all().order_by('-phone')
            elif request.POST['order'] == 'l':
                data = Clients.objects.all().order_by('company')
            elif request.POST['order'] == 'm':
                data = Clients.objects.all().order_by('-company')
            elif request.POST['order'] == 'n':
                data = Clients.objects.all().order_by('add_date')
            elif request.POST['order'] == 'o':
                data = Clients.objects.all().order_by('-add_date')
        else:
            data = Clients.objects.all().order_by('-id')

    return render(request, 'client.html', {'del_all': del_all, 'data': data, 'client_num': client_num})


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
    name = request.POST['name']
    surname = request.POST['surname']
    email = request.POST['email']
    phone = request.POST['phone']
    company = request.POST['company']

    if name and surname and email and phone and company:
        if Clients.objects.filter(email=email).exclude(id=id).exists():
            messages.info(request, "E-mail already exists.")
        elif Clients.objects.filter(phone=phone).exclude(id=id).exists():
            messages.info(request, "Phone number already exists.")
        else:
            client = Clients.objects.get(id=id)
            client.name = request.POST['name']
            client.surname = request.POST['surname']
            client.email = request.POST['email']
            client.phone = request.POST['phone']
            client.company = request.POST['company']

            client.save()
            messages.info(request, "Client update was successful.",
                          extra_tags='success')
    else:
        messages.info(request, "Empety fields.", extra_tags='error')
    return redirect('client')


def expens(request):
    data = ''
    del_all = []

    if 'delete_all' in request.POST:
        del_all = request.POST.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.POST:
        choosen = request.POST.getlist('x[]')
        if choosen:
            for selected in choosen:
                picked = Expenses.objects.filter(id=selected)
                if picked.exists():
                    picked.delete()
            messages.info(
                request, "Expens data has been deleted successfully.", extra_tags='success')

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
    if 'search' in request.POST:
        data = Expenses.objects.filter(
            Q(assignment__contains=request.POST['question'])).order_by('-id')
    elif 'search' in request.POST:
        data = Expenses.objects.filter(
            Q(amount__contains=request.POST['question'])).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Expenses.objects.all().order_by('assignment')
            elif request.POST['order'] == 'b':
                data = Expenses.objects.all().order_by('-assignment')
            elif request.POST['order'] == 'c':
                data = Expenses.objects.all().order_by('amount')
            elif request.POST['order'] == 'd':
                data = Expenses.objects.all().order_by('-amount')
            elif request.POST['order'] == 'e':
                data = Expenses.objects.all().order_by('add_date')
            elif request.POST['order'] == 'f':
                data = Expenses.objects.all().order_by('-add_date')
        else:
            data = Expenses.objects.all().order_by('-id')

    return render(request, 'expens.html', {'del_all': del_all, 'data': data, 'expens_num': expens_num})


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
    assignment = request.POST['assignment']
    amount = request.POST['amount']

    if assignment and amount:
        expens = Expenses.objects.get(id=id)
        expens.assignment = request.POST['assignment']
        expens.amount = request.POST['amount']

        expens.save()
        messages.info(request, "Update was successful.", extra_tags='success')

    else:
        messages.info(request, "Empty field.", extra_tags='error')
    return redirect('expens')


def products(request):
    data = ''
    del_all = []

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

    if 'save' in request.POST:

        if request.POST['brand_id'] != '' and request.POST['product'] != '' and request.POST['buy'] != '' and request.POST['sell'] != '' and request.POST['quantity'] != '' and 'photo' in request.FILES:
            # instance
            brand = Brand.objects.get(id=request.POST['brand_id'])
            supplier = Supplier.objects.get(id=request.POST['supp_id'])

            if 'photo' in request.FILES:
                upload = request.FILES['photo']
                file_ss = FileSystemStorage()
                file = file_ss.save(upload.name, upload)
                file_url = file_ss.url(file)

                save_date = Products(
                    brand=brand,
                    supplier_id=supplier,
                    product=request.POST['product'],
                    buy=request.POST['buy'],
                    sell=request.POST['sell'],
                    quantity=request.POST['quantity'],
                    product_photo=file_url
                )
                save_date.save()
                messages.info(request, "Product saved successfully.",
                              extra_tags='success')
            else:
                messages.info(
                    request, "Please fill in all required fields and provide a photo.", extra_tags='error')
        else:
            messages.info(request, "Empty field", extra_tags='error')

    if 'search' in request.POST:
        data = Products.objects.filter(
            Q(product=request.POST['question'])).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Products.objects.all().order_by('product')
            elif request.POST['order'] == 'b':
                data = Products.objects.all().order_by('-product')
            elif request.POST['order'] == 'c':
                data = Products.objects.all().order_by('buy')
            elif request.POST['order'] == 'd':
                data = Products.objects.all().order_by('-buy')
            elif request.POST['order'] == 'e':
                data = Products.objects.all().order_by('sell')
            elif request.POST['order'] == 'f':
                data = Products.objects.all().order_by('-sell')
            elif request.POST['order'] == 'g':
                data = Products.objects.all().order_by('quantity')
            elif request.POST['order'] == 'h':
                data = Products.objects.all().order_by('-quantity')
            elif request.POST['order'] == 'i':
                data = Products.objects.all().order_by('add_date')
            elif request.POST['order'] == 'j':
                data = Products.objects.all().order_by('-add_date')
            elif request.POST['order'] == 'k':
                data = Products.objects.all().order_by('supplier_id_id')
            elif request.POST['order'] == 'l':
                data = Products.objects.all().order_by('-supplier_id_id')
            elif request.POST['order'] == 'm':
                data = Products.objects.all().order_by('brand_id')
            elif request.POST['order'] == 'n':
                data = Products.objects.all().order_by('-brand_id')
            elif request.POST['order'] == 'o':
                data = Products.objects.annotate(
                    calculated_profit=ExpressionWrapper(
                        F('sell') - F('buy') * F('quantity'),
                        output_field=FloatField()
                    )
                ).order_by('calculated_profit')
            elif request.POST['order'] == 'p':
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

    return render(request, 'products.html', {'del_all': del_all, 'data': data, 'brands': brands, 'suppliers': suppliers, 'brand_num': brand_num, 'orders_num': orders_num, 'product_num': product_num})


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
    product = request.POST['product']
    buy = request.POST['buy']
    sell = request.POST['sell']
    quantity = request.POST['quantity']
    brand = Brand.objects.get(id=request.POST['brand_id'])

    if product and buy and sell and quantity and brand:
        product = Products.objects.get(id=id)
        product.buy = request.POST['buy']
        product.sell = request.POST['sell']
        product.quantity = request.POST['quantity']
        product.brand = brand

        product.save()
        messages.info(request, "Update was successful.", extra_tags='success')
    else:
        messages.info(request, "Empty field.", extra_tags='error')
    return redirect('products')


def orders(request):
    data = ''
    del_all = []

    if 'delete_all' in request.POST:
        del_all = request.POST.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.POST:
        choosen = request.POST.getlist('x[]')
        if choosen:
            for selected in choosen:
                picked = Orders.objects.filter(id=selected)
                if picked.exists():
                    picked.delete()
            messages.info(
                request, "Orders data has been deleted successfully.", extra_tags='success')

    if 'enter' in request.POST:

        if request.POST['client_id'] != '' and request.POST['product_id'] != '' and request.POST['amount'] != '':

            client = Clients.objects.get(id=request.POST['client_id'])
            product = Products.objects.get(id=request.POST['product_id'])

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
    if 'search' in request.POST:
        data = Orders.objects.filter(
            Q(orders__contains=request.POST['question'])).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Orders.objects.all().order_by('client_id')
            elif request.POST['order'] == 'b':
                data = Orders.objects.all().order_by('-client_id')
            elif request.POST['order'] == 'c':
                data = Orders.objects.all().order_by('product__brand__brand_name')
            elif request.POST['order'] == 'd':
                data = Orders.objects.all().order_by('-product__brand__brand_name')
            elif request.POST['order'] == 'e':
                data = Orders.objects.all().order_by('product_id')
            elif request.POST['order'] == 'f':
                data = Orders.objects.all().order_by('-product_id')
            elif request.POST['order'] == 'g':
                data = Orders.objects.all().order_by('amount')
            elif request.POST['order'] == 'h':
                data = Orders.objects.all().order_by('-amount')
            elif request.POST['order'] == 'i':
                data = Orders.objects.all().order_by('product__buy')
            elif request.POST['order'] == 'j':
                data = Orders.objects.all().order_by('-product__buy')
            elif request.POST['order'] == 'k':
                data = Orders.objects.all().order_by('product__sell')
            elif request.POST['order'] == 'l':
                data = Orders.objects.all().order_by('-product__sell')
            elif request.POST['order'] == 'm':
                data = Orders.objects.all().order_by('product__quantity')
            elif request.POST['order'] == 'n':
                data = Orders.objects.all().order_by('-product__quantity')
            elif request.POST['order'] == 'o':
                data = Orders.objects.annotate(
                    calculated_profit=ExpressionWrapper(
                        F('product__sell') - F('product__buy') * F('amount'),
                        output_field=FloatField()
                    )
                ).order_by('calculated_profit')
            elif request.POST['order'] == 'p':
                data = Orders.objects.annotate(
                    calculated_profit=ExpressionWrapper(
                        F('product__sell') - F('product__buy') * F('amount'),
                        output_field=FloatField()
                    )
                ).order_by('-calculated_profit')
            elif request.POST['order'] == 'q':
                data = Orders.objects.all().order_by('add_date')
            elif request.POST['order'] == 'r':
                data = Orders.objects.all().order_by('-add_date')
        else:
            data = Orders.objects.all().order_by('-id')

    client = Clients.objects.all().order_by('name')
    product = Products.objects.all().order_by('product')

    return render(request, 'orders.html', {'del_all': del_all, 'client': client, 'product': product, 'data': data, 'expens_num': expens_num, 'brand_num': brand_num, 'client_num': client_num, 'product_num': product_num})


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
    client = Clients.objects.get(id=request.POST['client_id'])
    product = Products.objects.get(id=request.POST['product_id'])
    amount = Orders.objects.get(id=id)

    if client and product and amount:
        orders = Orders.objects.get(id=id)
        orders.client = client
        orders.product = product
        orders.amount = request.POST['amount']

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
    number = ''
    del_all = []

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

    if 'add' in request.POST:
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
    if 'search' in request.POST:
        data = Departments.objects.filter(
            Q(department_name__contains=request.POST['question'])).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Departments.objects.all().order_by('department_name')
            elif request.POST['order'] == 'b':
                data = Departments.objects.all().order_by('-department_name')
            elif request.POST['order'] == 'c':
                data = Departments.objects.all().order_by('date')
            elif request.POST['order'] == 'd':
                data = Departments.objects.all().order_by('-date')
        else:
            data = Departments.objects.all().order_by('-id')

    return render(request, 'department.html', {'del_all': del_all, 'data': data, 'department_num': department_num})


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
    department_name = request.POST['department_name']

    if department_name:
        departments = Departments.objects.get(id=id)
        departments.department_name = request.POST['department_name']

        departments.save()
        messages.info(request, "Update was successful.", extra_tags='success')
    else:
        messages.info(request, "Empty field.", extra_tags='error')
    return redirect('departments')


def positions(request):
    data = ''
    number = ''
    del_all = []

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

    if 'add' in request.POST:
        if request.POST['department_id'] != '' and request.POST['position_name'] != '':

            departments = Departments.objects.get(
                id=request.POST['department_id'])

            save_data = Positions(
                dep_id=departments,
                positions=request.POST['position_name']
            )
            save_data.save()
            messages.info(request, "Position saved.", extra_tags='success')

        else:
            messages.info(request, "Position name is required.",
                          extra_tags='error')
    if 'search' in request.POST:
        data = Positions.objects.filter(
            Q(position_name___contains=request.POST['question'])).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Positions.objects.all().order_by('dep_id__department_name')
            elif request.POST['order'] == 'b':
                data = Positions.objects.all().order_by('-dep_id__department_name')
            elif request.POST['order'] == 'c':
                data = Positions.objects.all().order_by('positions')
            elif request.POST['order'] == 'd':
                data = Positions.objects.all().order_by('-positions')
            elif request.POST['order'] == 'e':
                data = Positions.objects.all().order_by('date')
            elif request.POST['order'] == 'f':
                data = Positions.objects.all().order_by('-date')
        else:
            data = Positions.objects.all().order_by('-id')
    number = Positions.objects.count()
    departments = Departments.objects.all().order_by('department_name')

    return render(request, 'positions.html', {'del_all': del_all, 'data': data, 'number': number, 'departments': departments})


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
    position = request.POST['position_name']
    departments = Departments.objects.get(id=request.POST['departments_id'])

    if position and departments:
        update = Positions.objects.get(id=id)
        update.positions = request.POST['position_name']
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

    if 'add' in request.POST:

        if request.POST['s_name'] != '' and request.POST['s_surname'] != '' and request.POST['s_birth_d'] != '' and request.POST['s_email'] != '' and request.POST['s_phone'] != '' and request.POST['s_sallary'] != '' and request.POST['s_start_d'] != '':
            positions = Positions.objects.get(id=request.POST['position_id'])

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
    if 'search' in request.POST:
        data = Staff.objects.filter(
            Q(staff__contains=request.POST['question'])).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Staff.objects.all().order_by('name')
            elif request.POST['order'] == 'b':
                data = Staff.objects.all().order_by('-name')
            elif request.POST['order'] == 'c':
                data = Staff.objects.all().order_by('surname')
            elif request.POST['order'] == 'd':
                data = Staff.objects.all().order_by('-surname')
            elif request.POST['order'] == 'e':
                data = Staff.objects.all().order_by('birth_date')
            elif request.POST['order'] == 'f':
                data = Staff.objects.all().order_by('-birth_date')
            elif request.POST['order'] == 'g':
                data = Staff.objects.all().order_by('email')
            elif request.POST['order'] == 'h':
                data = Staff.objects.all().order_by('-email')
            elif request.POST['order'] == 'i':
                data = Staff.objects.all().order_by('phone')
            elif request.POST['order'] == 'j':
                data = Staff.objects.all().order_by('-phone')
            elif request.POST['order'] == 'k':
                data = Staff.objects.all().order_by('sallary')
            elif request.POST['order'] == 'l':
                data = Staff.objects.all().order_by('-sallary')
            elif request.POST['order'] == 'm':
                data = Staff.objects.all().order_by('j_start_d')
            elif request.POST['order'] == 'n':
                data = Staff.objects.all().order_by('-j_start_d')
            elif request.POST['order'] == 'o':
                data = Staff.objects.all().order_by('pos_id__dep_id__department_name')
            elif request.POST['order'] == 'p':
                data = Staff.objects.all().order_by('-pos_id__dep_id__department_name')
            elif request.POST['order'] == 'q':
                data = Staff.objects.all().order_by('pos_id__positions')
            elif request.POST['order'] == 'r':
                data = Staff.objects.all().order_by('-pos_id__positions')
        else:
            data = Staff.objects.all().order_by('-id')

    departments = Departments.objects.all().order_by('department_name')
    positions = Positions.objects.all().order_by('positions')
    return render(request, 'staff.html', {'del_all': del_all, 'data': data, 'sraff_num': sraff_num, 'departments': departments, 'positions': positions})


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

    name = request.POST.get('s_name')
    surname = request.POST.get('s_surname')
    birth_date_str = request.POST.get('s_birth_d')
    email = request.POST.get('s_email')
    phone = request.POST.get('s_phone')
    sallary = request.POST.get('s_sallary')
    j_start_d_str = request.POST.get('s_start_d')
    position_id = request.POST.get('position_id')

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

    if 'delete_all' in request.POST:
        del_all = request.POST.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.POST:
        choosen = request.POST.getlist('x[]')
        if choosen:
            for selected in choosen:
                picked = Documents.objects.filter(id=selected)
                if picked.exists():
                    picked.delete()
                messages.info(
                    request, "Document(s) data has been deleted successfully.", extra_tags='success')

    if 'upload' in request.POST:
        title = request.POST['doc_name']
        doc_num = request.POST['doc_num']
        about = request.POST['about']

        if title and doc_num and 'doc_photo' in request.FILES:

            name = Staff.objects.get(id=staf_id)

            if Documents.objects.filter(doc_num=request.POST['doc_num']).exists():
                messages.info(request, "Document already exists.",
                              extra_tags='error')
            else:
                upload = request.FILES['doc_photo']
                fs = FileSystemStorage()
                file = fs.save(upload.name, upload)
                file_url = fs.url(file)

                save_info = Documents(
                    title=request.POST['doc_name'],
                    doc_num=request.POST['doc_num'],
                    about=request.POST['about'],
                    scan_photo=file_url,
                    staff_id=name,
                )
                save_info.save()

                messages.info(
                    request, "Document  saved successfully.", extra_tags='success')
        else:
            messages.info(request, "Empty fields", extra_tags='warning')

    if 'search' in request.POST:
        data = Documents.objects.filter(Q(documents__contains=request.POST['question'])).filter(
            staff_id=staf_id).order_by('-id')
    else:
        if 'order' in request.POST:
            if request.POST['order'] == 'a':
                data = Documents.objects.order_by('staff_id__name')
            elif request.POST['order'] == 'b':
                data = Documents.objects.order_by('-staff_id__name')
            elif request.POST['order'] == 'c':
                data = Documents.objects.order_by('title')
            elif request.POST['order'] == 'd':
                data = Documents.objects.order_by('-title')
            elif request.POST['order'] == 'e':
                data = Documents.objects.order_by('doc_num')
            elif request.POST['order'] == 'f':
                data = Documents.objects.order_by('-doc_num')
            elif request.POST['order'] == 'g':
                data = Documents.objects.order_by('about')
            elif request.POST['order'] == 'e':
                data = Documents.objects.order_by('-about')
        else:
            data = Documents.objects.all().filter(staff_id=staf_id).order_by('-id')

    staff = Staff.objects.get(id=staf_id)
    return render(request, 'documents.html', {'del_all': del_all, 'data': data, 'staff': staff})


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

    title = request.POST['doc_name']
    doc_num = request.POST['doc_num']
    about = request.POST['about']

    if title and doc_num and about:

        if Documents.objects.filter(doc_num=request.POST['doc_num']).exclude(id=doc_id).exists():
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

    if 'delete_all' in request.POST:
        del_all = request.POST.getlist('x[]')
        if not del_all:
            messages.info(request, "Please select to delete.",
                          extra_tags='error')
    elif 'confirm_delete_all' in request.POST:
        choosen = request.POST.getlist('x[]')
        if choosen:
            for selected in choosen:
                picked = Assignments.objects.filter(id=selected)
                if picked.exists():
                    picked.delete()
            messages.info(
                request, "Assignments data has been deleted successfully.", extra_tags='success')

    if 'add' in request.POST:
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
    number = Assignments.objects.count()

    staffs = Staff.objects.all().order_by('name')
    departments = Departments.objects.all().order_by('department_name')
    positions = Positions.objects.all().order_by('positions')
    return render(request, 'assignments.html', {'del_all': del_all, 'data': data, 'departments': departments, 'positions': positions, 'number': number, 'staffs': staffs})


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
    assignment_name = request.POST['assign_n']
    deadline_d_str = request.POST['deadline']
    staffs = Staff.objects.get(id=request.POST['staff_id'])

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
            elif request.POST['order'] == 'i':
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
    return render(request, 'suppliers.html', {'del_all': del_all, 'data': data, 'supplier_num': supplier_num, 'product_num': product_num, 'orders_num': orders_num})


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

    if 'update' in request.POST:
        if Supplier.objects.filter(supplier_email=request.POST['supp_email']).exclude(id=update.id).exclude(supplier_email=request.POST['supp_email']):
            messages.info(request, "Email already exists.",
                          extra_tags='warning')
        elif Supplier.objects.filter(supplier_phone=request.POST['supp_phone']).exclude(id=update.id).exclude(supplier_phone=request.POST['supp_phone']):
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
            update.supplier_name = request.POST['sup_name']
            update.supplier_surname = request.POST['sup_surname']
            update.supplier_company_name = request.POST['sup_comp_name']
            update.supplier_email = request.POST['supp_email']
            update.supplier_phone = request.POST['supp_phone']
            update.supplier_address = request.POST['supp_address']
            update.save()
            messages.info(request, "Profile updated.", extra_tags='success')
    return redirect('supplier')


def loader(request):
    data = ''

    if 'del_brand' in request.GET:
        brand = Brand.objects.get(id=request.GET['del_brand'])
        data = Brand.objects.all().order_by('-id')
        number = Products.objects.filter(
            brand_id=request.GET['del_brand']).count()

        if number > 0:
            messages.info(
                request, f"Brand '{brand.brand_name}' cannot be deleted. There are {number} active products in it.", extra_tags='error')
        else:
            brand.delete()
            messages.info(
            request, "The brand has been successfully deleted.", extra_tags='success')
    
    if 'del_client' in request.GET:
        clients = Clients.objects.get(id=request.GET['del_client'])
        data = Clients.objects.all().order_by('-id')
        active_orders = Orders.objects.filter(
            client_id=request.GET['del_client']).count()
        
        if active_orders > 0:
            messages.info(
            request, f"Client '{clients.name} {clients.surname}' cannot be deleted. There are {active_orders} active products in it.", extra_tags='error')
        else:
            clients.delete()
            messages.info(
            request, "Customer's data has been deleted successfully.", extra_tags='success')

    if 'del_expense' in request.GET:
        Expenses.objects.get(id=request.GET['del_expense']).delete()
        data = Expenses.objects.all().order_by('-id')
        messages.info(
            request, "Expens data has been deleted successfully.", extra_tags='success')

    if 'del_product' in request.GET:
        products = Products.objects.get(id=request.GET['del_product'])
        data = Products.objects.all().order_by('-id')
        active_order = Orders.objects.filter(
            product_id=request.GET['del_product']).count()

        if active_order > 0:
            messages.info(
                request, f"Product '{products.product}' cannot be deleted. There are {active_order} active products in it.", extra_tags='error')
        else:
            products.delete()
            messages.info(
                request, "Products data has been deleted successfully.", extra_tags='success')

    if 'del_order' in request.GET:
        Orders.objects.get(id=request.GET['del_order']).delete()
        data = Orders.objects.all().order_by('-id')
        messages.info(
            request, "Order data has been deleted successfully.", extra_tags='success')

    if 'del_departments' in request.GET:
        departments = Departments.objects.get(
            id=request.GET['del_departments'])
        data = Departments.objects.all().order_by('-id')
        position = Positions.objects.filter(
            dep_id_id=request.GET['del_departments']).count()

        if position > 0:
            messages.info(
                request, f"Department '{departments.department_name}' cannot be deleted. There are {position} active position in it.", extra_tags='error')
        else:
            departments.delete()
            messages.info(
                request, "Department  has been deleted successfully.", extra_tags='success')

    if 'del_positions' in request.GET:
        positions = Positions.objects.get(id=request.GET['del_positions'])
        data = Positions.objects.all().order_by('-id')
        staffs = Staff.objects.filter(
            pos_id=request.GET['del_positions']).count()
        if staffs > 0:
            messages.info(
                request, f"Position '{positions.positions}' cannot be deleted. There are {staffs} active staff in it.", extra_tags='error')
        else:
            positions.delete()
            messages.info(
                request, "Positions has been deleted successfully.", extra_tags='success')

    if 'del_staff' in request.GET:
        staff = Staff.objects.get(id=request.GET['del_staff'])
        documents = Documents.objects.filter(
            staff_id_id=request.GET['del_staff']).count()
        if documents > 0:
            messages.info(
                request, f"Staff '{staff.name}' cannot be deleted. There are {documents} active staff in it.", extra_tags='error')
        else:
            Staff.objects.get(id=request.GET['del_staff']).delete()
            messages.info(
                request, "Employee has been deleted successfully.", extra_tags='success')

    if 'del_documents' in request.GET:
        Documents.objects.get(id=request.GET['del_documents']).delete()
        data = Documents.objects.all().order_by('-id')
        messages.info(
            request, "Document has been deleted successfully.", extra_tags='success')

    if 'del_assignment' in request.GET:
        Assignments.objects.get(id=request.GET['del_assignment']).delete()
        data = Assignments.objects.all().order_by('-id')
        messages.info(
            request, "Assignment has been deleted successfully.", extra_tags='success')

    if 'del_supplier' in request.GET:
        supplier = Supplier.objects.get(id=request.GET['del_supplier'])
        data = Supplier.objects.all().order_by('-id')
        number = Products.objects.filter(
            supplier_id_id=request.GET['del_supplier']).count()

        if number > 0:
            messages.info(
                request, f"Supplier '{supplier.supplier_name}' cannot be deleted. There are {number} active products in it.", extra_tags='error')
        else:
            supplier.delete()
            messages.info(
                request, "Supplier has been deleted successfully.", extra_tags='success')
            
    if request.GET['section'] == 'brands':
        data = Brand.objects.all().order_by('-id')
    elif request.GET['section'] == 'clients':
        data = Clients.objects.all().order_by('-id')
    elif request.GET['section'] == 'expenses':
        data = Expenses.objects.all().order_by('-id')
    elif request.GET['section'] == 'products':
        data = Products.objects.all().order_by('-id')
    elif request.GET['section'] == 'orders':
        data = Orders.objects.all().order_by('-id')
    elif request.GET['section'] == 'suppliers':
        data = Supplier.objects.all().order_by('-id')
    elif request.GET['section'] == 'departments':
        data = Departments.objects.all().order_by('-id')
    elif request.GET['section'] == 'positions':
        data = Positions.objects.all().order_by('-id')
    elif request.GET['section'] == 'staffs':
        data = Staff.objects.all().order_by('-id')
    elif request.GET['section'] == 'documents':
        data = Documents.objects.all().order_by('-id')
    elif request.GET['section'] == 'assignments':
        data = Assignments.objects.all().order_by('-id')

    return render(request, 'loader.html', {'data': data, })