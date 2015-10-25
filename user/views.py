from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from product.models import Product, Category
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.db import IntegrityError

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user:dashboard'))
    return render(request, 'index.html', {})

@login_required
def dashboard(request):
    user = request.user
    products = Product.objects.all().order_by('-id')[:5]
    created = request.GET.get('created')
    deleted = request.GET.get('deleted')
    if created == 'False':
        from django.utils.http import unquote_plus
        reason = unquote_plus(request.GET.get('reason'))
    else:
        reason = ""
    cd = {
        'user': user,
        'products': products,
        'created': created,
        'reason': reason,
        'deleted': deleted,
    }
    return render(request, 'dashboard.html', cd)

@login_required
def new_item(request):
    if request.method == 'POST':
        from uuid import uuid4

        sku = escape(request.POST.get('sku').strip())
        model = escape(request.POST.get('model').strip())
        name = escape(request.POST.get('name').strip())
        category_id = escape(request.POST.get('category').strip())
        category = Category.objects.get(id=category_id)
        price = escape(request.POST.get('price').strip())
        length = escape(request.POST.get('length').strip())
        breadth = escape(request.POST.get('breadth').strip())
        height = escape(request.POST.get('height').strip())
        image = request.FILES.get('image')
        image.name = '{}{}'.format(uuid4().hex, image.name[image.name.rfind('.'):])
        product = Product(sku=sku, model=model, name=name, category=category, length=length, breadth=breadth,
                          height=height, price=price, image=image)
        try:
            product.save()
            category.number_of_items += 1
            category.save()
            url = "%s?created=True" % reverse('user:dashboard')
        except IntegrityError:
            from django.utils.http import quote_plus
            r = "SKU needs to be unique"
            url = "%s?created=False&reason=%s" % (reverse('user:dashboard'), quote_plus(r))
        return HttpResponseRedirect(url)

    category = Category.objects.all()
    cd = {'category': category}
    return render(request, 'new.html', cd)

@login_required
def view_items(request):
    products = Product.objects.all()
    cd = {
        'products': products,
    }
    return render(request, 'view_items.html', cd)

@login_required
def view(request, id):
    product = Product.objects.filter(id=id)
    updated = request.GET.get('updated')

    if product:
        product = product.get()
        cd = {
            'product': product,
            'updated': updated,

        }
        return render(request, 'view.html', cd)
    else:
        return HttpResponseRedirect(reverse('user:index'))

@login_required
def search(request):
    return render(request, 'search.html', {})

@login_required
def delete(request, id):
    product = Product.objects.filter(id=id)
    if not product:
        return HttpResponseRedirect(reverse('user:index'))
    from inventory.settings import BASE_DIR
    import os

    try:
        path = BASE_DIR + "/media/" + product.get().image.name
        os.remove(path)
        path = BASE_DIR + "/media/" + product.get().thumbnail.name
        os.remove(path)
        product.delete()
        url = "%s?deleted=True" % reverse('user:dashboard')
    except FileNotFoundError:
        url = "%s?deleted=False" % reverse('user:dashboard')

    return HttpResponseRedirect(url)

@login_required
def edit(request, id):
    product = Product.objects.filter(id=id)
    if not product:
        return HttpResponseRedirect(reverse('user:index'))
    if request.method == 'POST':
        # sku = escape(request.POST.get('sku').strip())
        model = escape(request.POST.get('model').strip())
        name = escape(request.POST.get('name').strip())
        category_id = escape(request.POST.get('category').strip())
        category = Category.objects.get(id=category_id)
        price = escape(request.POST.get('price').strip())
        length = escape(request.POST.get('length').strip())
        breadth = escape(request.POST.get('breadth').strip())
        height = escape(request.POST.get('height').strip())
        product.update(
            model=model,
            name=name,
            category=category,
            price=price,
            length=length,
            breadth=breadth,
            height=height,
        )
        url = "%s?updated=True" % reverse('user:view', args=(id,))
        return HttpResponseRedirect(url)
    else:
        product = product.get()
        category = Category.objects.all()
        cd = {
            'product': product,
            'category': category,
        }
        return render(request, 'edit.html', cd)

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user:
            user = user.get()
            username = user.username
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/dashboard')
                else:
                    return HttpResponse('Your account is disabled')
            else:
                print('Invalid login details: {0}, {1}'.format(username, password))
                return HttpResponseRedirect('/')
        else:
            print("User does not exist")
            return HttpResponseRedirect('/')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')