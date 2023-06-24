from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import UserLoginForm,UserRegisterForm,NewPostForm

def login_view(request):
    form=UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        messages.success(request, f'Login Successfully')
        login(request,user)
        return render(request,'blogApp/home.html')
    context={
        'form':form,
    }
    return render(request,"blogApp/login.html",context)

def register_view(request):
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        messages.success(request, f'User Registered Successfully')
        new_user=authenticate(username=user.username,password=password)
        login(request,new_user)
        return render(request,'blogApp/login.html')
    context={
        'form':form,
    }
    return render(request,"blogApp/signup.html",context)

@login_required
def createPost(request):
    user=request.user
    if request.method=="POST":
        form=NewPostForm(request.POST,request.FILES)
        if form.is_valid():
            data=form.save(commit=False)
            data.username=user
            data.save()
            messages.success(request,f'Posted Successfully')
            return render(request,'blogApp/createpost.html')
    else:
        form=NewPostForm()
    return render(request,'blogApp/createpost.html',{'form':form})

class PostListView(ListView):
    model=BlogPost
    template_name='blogApp/home.html'
    context_object_name='posts'
    ordering=['-createdDate']
    paginate_by=10
    def get_context_data(self,**kwargs):
        context=super(PostListView,self).get_context_data(**kwargs)
        return context


def logout(request):
    if request.method=="POST":
        auth.logout(request)
        return redirect('login')

# Create your views here.
