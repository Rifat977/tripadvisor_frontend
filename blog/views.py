from django.shortcuts import redirect, render

from .models import Blog, BlogProfile


def blog(request):

    if request.user.is_authenticated:
    
        blogs = Blog.objects.filter(user=request.user)
        return render(request,'blog.html',context={'blogs':blogs})

    else:
        return redirect('/auth/login')



def create_blog(request):

    if request.user.is_authenticated:

        if request.method == 'GET':

            return render(request,'create-blog.html')
        
        else:
            title = request.POST['title']
            description = request.POST['description']
            imeage = request.FILES['imeage']
            objj = Blog.objects.create(user=request.user,title = title,description=description)


            objj.imeage = imeage
            objj.save()

            return redirect('/blog/all_blog')
        
    else:
        return redirect('/auth/login')