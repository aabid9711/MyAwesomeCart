from django.http import HttpResponse
from django.shortcuts import render
from .models import Blogpost
# Create your views here.

def index(request):
    posts = Blogpost.objects.all()
    print(posts)
    return render(request,'blog/index.html',{'posts':posts})

def blogPost(request,myid):
    post = Blogpost.objects.filter(blog_id=myid)[0]
    print(post)
    return render(request,'blog/blogPost.html',{'post':post})