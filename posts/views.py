from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.views import generic
from django.views.generic import View
from .forms import UserForm,LoginForm
from .models import Topic,Blogs,Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def index(request):
    all_topics=Topic.objects.all()
    max_blogs=Blogs.objects.all()[:5]
    pair={};i=0
    for blog in max_blogs:
        pair[i]=blog.description
        i+=1
    user=request.user
    #if user.is_authenticated():
     #   return render(request,'posts/index2.html',{'all_topics':all_topics,'user':user})
    #else:
    return render(request,'posts/index.html',{'all_topics':all_topics,'user':user,
                            'max_blogs':max_blogs,'pair':json.dumps(pair)})

def detail(request , topic_id, page):
    topic=get_object_or_404(Topic,pk=topic_id)
    all_blogs = topic.blogs_set.all()
    paginator= Paginator(all_blogs, 5)
    try:
        all_blogs= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_blogs= paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_blogs= paginator.page(paginator.num_pages)
    return render(request,'posts/detail.html',{'topic':topic,'all_blogs':all_blogs})

def descriptions(request,topic_id,blog_id):
    blog = get_object_or_404(Blogs,pk=blog_id)
    blog.views+=1
    blog.save()
    return render(request, 'posts/descriptions.html', {'blog': blog})

class UserFormView(View):
    form_class=UserForm
    template_name= 'posts/registration_form.html'
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user.profile.city=form.cleaned_data['city']
            user.profile.phone=form.cleaned_data['phone']
            user.profile.save()

            return redirect('posts:index')

class LoginFormView(View):
    #form_class=LoginForm
    template_name= 'posts/login_form.html'
    
    def get(self,request):
        #form=self.form_class(None)
        return render(request,self.template_name)
    def post(self,request):
        all_topics=Topic.objects.all()
        #form=self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            #return render(request,'posts/index2.html',{'all_topics':all_topics,'user':user})
            return redirect('posts:index')
        return render(request,self.template_name)

@login_required(login_url='posts:login')
def loginmode(request,user_id):
    user=User.objects.get(pk=user_id)
    all_topics=Topic.objects.all()
    return render(request,'posts/index2.html',{'all_topics':all_topics,'user':user})

class AddFormView(View):
    template_name= 'posts/add_post.html'

    def get(self,request):
        all_topics=Topic.objects.all()
        all_blogs=Blogs.objects.all()
        return render(request,self.template_name,{'all_topics':all_topics,'all_blogs':all_blogs})
    
    def post(self,request):
        topic=request.POST['topic']
        author=request.user.username
        title=request.POST['title']
        description=request.POST['description']
        Blogs.objects.create(topic=Topic.objects.get(topic_name=topic),author=Profile.objects.get(user=User.objects.get(username=author)),title=title,description=description)
        return redirect('posts:index')