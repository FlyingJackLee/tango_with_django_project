from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from django.urls import reverse

# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    top_5_pages = Page.objects.order_by('-views')[:5]

    context_dict['pages'] = top_5_pages

    return render(request,'rango/index.html',context=context_dict)


# about view
def about(request):
    # return HttpResponse("Rango says here is the about page.<a href=\'/rango/\'>Index</a>")
    context_dict = {'boldmessage': 'This tutorial has been put together by Zumin Li'}

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


