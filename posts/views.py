from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from .forms import ImageForm
from posts.models import Topic,Blogs,Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
def index(request):
    all_topics=Topic.objects.all()
    max_blogs=Blogs.objects.all()[:5]
    pair={};i=0
    for blog in max_blogs:
        pair[i]=blog.description
        i+=1
    user=request.user
    all_user=User.objects.all()
    contributors=[]
    for i in all_user:
        if len(Blogs.objects.filter(author=Profile.objects.get(user=i)))>0:
            contributors.append(i)
    #if user.is_authenticated():
     #   return render(request,'posts/index2.html',{'all_topics':all_topics,'user':user})
    #else:
    return render(request,'posts/index.html',{'all_topics':all_topics,'user':user,'all_user':contributors,
                            'max_blogs':max_blogs,'pair':json.dumps(pair)})

def detail(request , topic_id, page):
    topic=get_object_or_404(Topic,pk=topic_id)
    all_blogs = topic.blogs_set.all()
    all_user=User.objects.all()
    contributors=[]
    for i in all_user:
        if len(Blogs.objects.filter(author=Profile.objects.get(user=i)))>0:
            contributors.append(i)

    paginator= Paginator(all_blogs, 5)
    try:
        all_blogs= paginator.page(page)
        pair={};i=0
        for blog in all_blogs.object_list:
            pair[i]=blog.description
            i+=1
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_blogs= paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_blogs= paginator.page(paginator.num_pages)
    return render(request,'posts/detail.html',{'topic':topic,'all_blogs':all_blogs,'pair':json.dumps(pair),
    'all_user':contributors})

def descriptions(request,topic_id,blog_id):
    all_user=User.objects.all()
    contributors=[]
    for i in all_user:
        if len(Blogs.objects.filter(author=Profile.objects.get(user=i)))>0:
            contributors.append(i)
    blog = get_object_or_404(Blogs,pk=blog_id)
    blog.views+=1
    blog.save()
    return render(request, 'posts/descriptions.html', {'blog': blog,'all_user':contributors})

class UserFormView(View):
    #form_class=UserForm
    template_name= 'posts/registration_form.html'
    def get(self,request):
        pass
        # form=self.form_class(None)
        # return render(request,self.template_name,{'form':form})
    def post(self,request):
        # form=self.form_class(request.POST)
        # if form.is_valid():
        #     user=form.save(commit=False)
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        #     user.set_password(password)
        #     user.save()
        #     user.profile.city=form.cleaned_data['city']
        #     user.profile.phone=form.cleaned_data['phone']
        #     user.profile.save()
        user=User.objects.create_user(username=username,email=email,password=password)
        profile=Profile.objects.get(user=user)
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
        return redirect('posts:profile',user_id=user.id)
        #(return render(request,self.template_name,{'form':form})
def check(request):
    username=request.GET.get('name',None)
    mail=request.GET.get('mail',None)
    data = {
        'name_is_taken': User.objects.filter(username__iexact=username).exists(),
        'mail_is_taken': User.objects.filter(email=mail).exists(),
    }
    return JsonResponse(data)
def e_check(request):
    mail=request.GET.get('mail',None)
    data={}
    data['taken']= User.objects.filter(email=mail).exists()
    if User.objects.filter(email=mail).exists():
        data['is_taken']=User.objects.filter(email=mail)[0].id==request.user.id
    # data = {
    #     'is_taken': User.objects.filter(email=mail)[0].id==request.user.id
    # }
    return JsonResponse(data)
class LoginFormView(View):
    #form_class=LoginForm
    template_name= 'posts/login_form.html'
    
    def get(self,request):
        username=request.GET.get('name',None)
        password=request.GET.get('pass',None)
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            k=True
        else:
            k=False
        data={
            'is_valid':k,
        }
        return JsonResponse(data)
        #form=self.form_class(None)
        #return render(request,self.template_name)
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
def logout_view(request):
    logout(request)
    return redirect('posts:index')

@login_required(login_url='posts:login')
def loginmode(request,user_id):
    user=User.objects.get(pk=user_id)
    all_topics=Topic.objects.all()
    all_user=User.objects.all()
    contributors=[]
    for i in all_user:
        if len(Blogs.objects.filter(author=Profile.objects.get(user=i)))>0:
            contibutors.append(i)
    return render(request,'posts/index2.html',{'all_topics':all_topics,'user':user,'all_user':contributors})

class AddFormView(View):
    template_name= 'posts/add_post.html'

    def get(self,request):
        all_topics=Topic.objects.all()
        all_blogs=Blogs.objects.all()
        return render(request,self.template_name,{'all_topics':all_topics,'all_blogs':all_blogs})
    
    def post(self,request):
        try:

            topic=request.POST['topic']
            author=request.user.username
            title=request.POST['title']
            description=request.POST['description']
            Blogs.objects.create(topic=Topic.objects.get(topic_name=topic),
                author=Profile.objects.get(user=User.objects.get(username=author)),title=title,description=description)
            return redirect('posts:index')
        except:
            topic_name=request.POST['topic_new']
            genre=name=request.POST['genre']
            topic_logo=request.FILES['topic_logo']
            topic=Topic.objects.create(topic_name=topic_name,genre=genre,topic_logo=topic_logo)
            author=request.user.username
            title=request.POST['title']
            description=request.POST['description']
            Blogs.objects.create(topic=topic,author=Profile.objects.get(user=User.objects.get(username=author)),
                                    title=title,description=description)
            return redirect('posts:index')
def profile_view(request,user_id):
    user=User.objects.get(id=user_id)
    profile=Profile.objects.get(user=user)
    all_blogs=Blogs.objects.filter(author=profile)
    pair={};i=0
    for blog in all_blogs:
        pair[i]=blog.description
        i+=1
    all_user=User.objects.all()
    contributors=[]
    for i in all_user:
        if len(Blogs.objects.filter(author=Profile.objects.get(user=i)))>0:
            contributors.append(i)
    return render(request,'posts/profile.html',{'user':user,'profile':profile,'all_blogs':all_blogs,
                'pair':json.dumps(pair),'all_user':contributors})
def pp_uploads(request,user_id):
    user=User.objects.get(id=user_id)
    profile=Profile.objects.get(user=user)
    
    data={
            'ok':False
        }
    if request.method=='POST':
        user.profile.profile_pic=request.FILES['file']
        user.save()
        user.profile.save()
        data={
            'ok':True,
            'url':str(user.profile.profile_pic.url)
        }
    return JsonResponse(data)
def bio_saves(request,user_id):
    user=User.objects.get(id=user_id)
    profile=Profile.objects.get(user=user)
    user.profile.phone=request.POST['ph']
    user.email=request.POST['mail']
    user.profile.city=request.POST['city']
    user.save()
    user.profile.save()
    # data={
    #     'ph':user.profile.phone,
    #     'mail':user.email,
    #     'city':user.profile.city,
    #     'status':True,
    # }
    #return JsonResponse(data)
    return redirect('posts:profile',user_id=user.id)
def cp_uploads(request,user_id):
    user=User.objects.get(id=user_id)
    profile=Profile.objects.get(user=user)
    
    data={
            'ok':False
        }
    if request.method=='POST':
        user.profile.cover_pic=request.FILES['file']
        user.save()
        user.profile.save()
        data={
            'ok':True,
            'url':str(user.profile.cover_pic.url)
        }
    return JsonResponse(data)

class DeletePosts(DeleteView):
    model=Blogs
    def delete(self,request,*args,**kwargs):
        self.get_object().delete()
        data={
            'status':True,
            }
        return JsonResponse(data)
    # def get_success_url(self):
    #     prof=self.object.author
    #     return reverse_lazy('posts:profile',kwargs={'user_id':prof.user.id})
    def get(self,request,*args,**kwargs):
        return self.post(request,*args,**kwargs)
class UpdatePost(UpdateView):
    model=Blogs
    def get(self,request,pk):
        blg=self.get_object()
        all_topics=Topic.objects.all()
        all_blogs=Blogs.objects.all()
        data={}
        data['topic']=blg.topic.topic_name
        data['author']=blg.author.user.username
        data['title']=blg.title
        data['description']=blg.description
        return render(request,'posts/update_post.html',{'all_topics':all_topics,'all_blogs':all_blogs,
                            'data':json.dumps(data)})
    def post(self,request,pk):
        blg=self.get_object()
        blg.topic=Topic.objects.get(topic_name=request.POST['topic'])
        blg.author=Profile.objects.get(user=User.objects.get(username=request.user.username))
        blg.title=request.POST['title']
        blg.description=request.POST['description']
        blg.save()
        return redirect('posts:index')
def search_result(request):
    q=request.POST['q']
    if User.objects.filter(username__icontains=q).exists() and Topic.objects.filter(topic_name__icontains=q).exists():
        blg=Blogs.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(author=Profile.objects.get(user=User.objects.get(username__icontains=q))) |
            Q(topic=Topic.objects.filter(topic_name__icontains=q))
            ).distinct()
    elif User.objects.filter(username__icontains=q).exists():
        blg=Blogs.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(author=Profile.objects.get(user=User.objects.get(username__icontains=q))) 
            ).distinct()
    elif Topic.objects.filter(topic_name__icontains=q).exists():
        blg=Blogs.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(topic=Topic.objects.filter(topic_name__icontains=q))
            ).distinct()
    else:
        blg=Blogs.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) 
            ).distinct()
    pair={};i=0
    for blog in blg:
        pair[i]=blog.description
        i+=1
    return render(request,'posts/search.html',{'blg':blg,'pair':json.dumps(pair),'q':q})