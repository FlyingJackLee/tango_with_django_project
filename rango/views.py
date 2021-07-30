from django.contrib.auth.models import User
from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    top_5_pages = Page.objects.order_by('-views')[:5]

    context_dict['pages'] = top_5_pages

    request.session.set_test_cookie()

    visitor_cookie_handler(request)

    response = render(request,'rango/index.html',context=context_dict)
    # visitor_cookie_handler(request, response)
    return response

# about view
def about(request):

    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    # return HttpResponse("Rango says here is the about page.<a href=\'/rango/\'>Index</a>")
    context_dict = {'boldmessage': 'This tutorial has been put together by Zumin Li'}

    visitor_cookie_handler(request)
    context_dict['visits'] = int(get_server_side_cookie(request,'visits'))

    return render(request,'rango/about.html',context=context_dict)

#category_name_slug came from the urls.py
def show_category(request,category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request,'rango/category.html',context=context_dict)


@login_required
def add_category(request):

    #first render
    form = CategoryForm()


    #submit
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        
        else:
            print(form.errors)


    return render(request,'rango/add_category.html',{'form':form})

@login_required
def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            #not submit imediately until the data is right
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()

            return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
        
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request,'rango/add_page.html',context_dict)


def register(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'rango/register.html',context= {
        'user_form': user_form,'profile_form': profile_form, 'registered': registered
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request,'rango/restricted.html')

    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits','1'))

    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if(datetime.now() - last_visit_time).days > 0 :
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def get_server_side_cookie(request,cookie,default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val