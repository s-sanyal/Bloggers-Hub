from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.views import generic
from django.views.generic import View
from .forms import UserForm,LoginForm
from .models import Topic,Blogs,Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
def index(request):
    all_topics=Topic.objects.all()
    user=request.user
    return render(request,'posts/index.html',{'all_topics':all_topics,'user':user})

def detail(request , topic_id):
    topic=get_object_or_404(Topic,pk=topic_id)
    all_blogs = topic.blogs_set.all()
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
    form_class=LoginForm
    template_name= 'posts/login_form.html'
    #all_topics=Topic.objects.all()
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('users/'+ str(user.id))
        return render(request,self.template_name,{'form':form})

@login_required(login_url='posts:login')
def loginmode(request,user_id):
    user=User.objects.get(pk=user_id)
    all_topics=Topic.objects.all()
    return render(request,'posts/index2.html',{'all_topics':all_topics,'user':user})