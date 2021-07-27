from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse("Rango says hey there partner!<a href=\'/rango/about/\'>About</a>")

    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    
    return render(request,'rango/index.html',context=context_dict)



# about view
def about(request):
    # return HttpResponse("Rango says here is the about page.<a href=\'/rango/\'>Index</a>")
    context_dict = {'boldmessage': 'This tutorial has been put together by Zumin Li'}

    return render(request,'rango/about.html',context=context_dict)

