from django.shortcuts import render

# Create your views here.
def login_view(request):
    template = 'accounts/login.html'
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
        context = {'form': form, 'message': 'User or password is incorrect.'}
        return render(request, template, context)
    if request.user.is_authenticated:
        return redirect('/')
    form = CustomUserLoginForm()
    return render(request, template, {'form': form})


def logout_view(request):
    pass


def register(request):
    pass