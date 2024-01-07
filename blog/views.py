from django.shortcuts import render

from .models import Blog, BlogProfile


def blog(request):

    if request.user.is_authenticated:
    
        blogs = Blog.objects.filter(user=request.user)
        return render(request,'blog.html',context={'blogs':blogs})
