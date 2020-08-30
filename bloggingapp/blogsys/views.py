from PIL import Image
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,Http404,HttpResponseRedirect
from . models import User,Blogs,UserComments,UserLikes
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User as MUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User as DUser
from .forms import NewUserForm,NewBlogForm
from datetime import date

def register(request):
    form = NewUserForm()
    return render(request = request,
                  template_name = "blogsys/register.html",
                  context={"form":form})

def registration(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        print(type(form))
        username=request.POST['username']
        if form.is_valid():
            email=NewUserForm.clean_email(form)
            password=NewUserForm.clean_password2(form)
            username=request.POST['username']
            user = DUser.objects.create_user(username,email,password)
            user.save()
            User.objects.create(username=username,email=email,password=password)
        return HttpResponseRedirect(reverse("login"))
    else:
        form=NewUserForm()
        return render(request = request,
                          template_name = "blogsys/register.html",
                          context={"form":form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            #print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                print("Invalid username or password.")
        else:
            print("Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "blogsys/login.html",
                    context={"form":form})


def logout_request(request):
    logout(request)
    #form = AuthenticationForm()
    return HttpResponseRedirect(reverse("login"))
    #return render(request,"blogsys/login.html",context={"message":"Logged out","form":form})

def index(request):
    if not request.user.is_authenticated:
        return render(request,"blogsys/login.html",{"message":None})
    context={
        "user":request.user,
        "blogs":Blogs.objects.all().order_by('-postdate')
    }
    #print(request.user.email)
    return render(request,"blogsys/index.html",context)


def newblog(request):
    form=NewBlogForm()
    context={
    "user":request.user,
    "form":form
    }
    return render(request,"blogsys/createblog.html",context)

def create_blog(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewBlogForm(request.POST, request.FILES)
        if form.is_valid():
            id=User.objects.get(email=request.user.email)
            blogname = form.cleaned_data.get("blogtitle")
            blogtext = form.cleaned_data.get("blogcontent")
            blogimg = form.cleaned_data.get("blogimg")
            obj = Blogs.objects.create(blogname=blogname,blogtext=blogtext,creatorid=id,blogimage=blogimg,postdate=date.today())
            obj.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))


def blog(request,blogid):
    try:
        blog=Blogs.objects.get(pk=blogid)
        usercomments=UserComments.objects.filter(blogid=blog)
    except Blogs.DoesNotExist:
        raise Http404("Blog does not exist")
    context={
        "user":request.user,
        "blog":blog,
        "usercomments":usercomments
    }
    return render(request,"blogsys/blogdesc.html",context)

def submit_comment(request,blogid):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        comment = request.POST.get('comment')
        id=User.objects.get(email=request.user.email)
        blog=Blogs.objects.get(pk=blogid)
        no_of_comments=blog.commentno
        if comment is not None:
            no_of_comments=no_of_comments+1
            Blogs.objects.filter(pk=blogid).update(commentno=no_of_comments)
            UserComments.objects.create(userid=id,blogid=blog,comments=comment,postedon=date.today())
            return HttpResponseRedirect(reverse("blogd",args=[blogid]))
        else:
            return HttpResponseRedirect(reverse("index"))

def submit_like(request,blogid,userpreference):
    if request.method == 'POST':
        userpreference= int(userpreference)
        print(userpreference)
        id=User.objects.get(email=request.user.email)
        blog=Blogs.objects.get(blogid=blogid)
        try:
            obj=UserLikes.objects.get(userid=id,blogid=blog)
            existing_like=obj.like
            if existing_like == 0:
                UserLikes.objects.filter(userid=id,blogid=blog).update(like=userpreference)
                if userpreference == 1:
                    likeno=Blogs.objects.get(pk=blogid).likeno+1
                    Blogs.objects.filter(pk=blogid).update(likeno=likeno)
                else:
                    dislikeno=Blogs.objects.get(pk=blogid).dislikeno+1
                    Blogs.objects.filter(pk=blogid).update(dislikeno=dislikeno)
            else:
                if userpreference != existing_like:
                    UserLikes.objects.filter(userid=id,blogid=blog).update(like=userpreference)
                    if existing_like == 1:
                        likeno=Blogs.objects.get(pk=blogid).likeno-1
                        Blogs.objects.filter(pk=blogid).update(likeno=likeno)
                        dislikeno=Blogs.objects.get(pk=blogid).dislikeno+1
                        Blogs.objects.filter(pk=blogid).update(dislikeno=dislikeno)
                    else:
                        likeno=Blogs.objects.get(pk=blogid).likeno+1
                        Blogs.objects.filter(pk=blogid).update(likeno=likeno)
                        dislikeno=Blogs.objects.get(pk=blogid).dislikeno-1
                        Blogs.objects.filter(pk=blogid).update(dislikeno=dislikeno)
        except:
            UserLikes.objects.create(userid=id,blogid=blog,like=userpreference)
            if userpreference == 1:
                likeno=Blogs.objects.get(pk=blogid).likeno+1
                Blogs.objects.filter(pk=blogid).update(likeno=likeno)
            else:
                dislikeno=Blogs.objects.get(pk=blogid).dislikeno+1
                Blogs.objects.filter(pk=blogid).update(dislikeno=dislikeno)
    return HttpResponseRedirect(reverse("blogd",args=[blogid]))

def submit_dislike(request,blogid):
    if request.method == 'POST':
        dislikeno=request.POST.get('dislikeno')
        Blogs.objects.filter(pk=blogid).update(dislikeno=dislikeno)
        id=User.objects.get(email=request.user.email)
        dislikes=UserLikes.objects.filter(userid=id,blogid=blogid).dislike+1
        UserLikes.objects.filter(userid=id,blogid=blogid).update(dislike=dislikes)
    return HttpResponseRedirect(reverse("blogd"))
