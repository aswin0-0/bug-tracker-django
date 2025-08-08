from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import bugs_report

# Create your views here.

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already in use'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = full_name
        user.save()
        return redirect('login')

    return render(request, 'register.html')



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ this is the correct usage
            return redirect('bugs')
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")



@login_required(login_url='login')
def bugs(request):
    if request.method == "POST":

        data=request.POST
        bug_title=data.get('bug_title')
        bug_description=data.get('bug_description')
        status=data.get('status')


        bugs_report.objects.create(
            bug_title=bug_title,
            bug_description=bug_description,
            status=status
        )


    all_bugs = bugs_report.objects.all().order_by('-id')
    return render(request,'bug.html', context={'all_bugs':all_bugs})

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@require_POST
@login_required(login_url='login')
def update_bug_status(request, bug_id):
    new_status = request.POST.get('status')
    bug = get_object_or_404(bugs_report, id=bug_id)

    if new_status in ['cleared', 'ongoing', 'remained']:
        bug.status = new_status
        bug.save()

    return redirect('bugs')


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer, BugSerializer
from .models import bugs_report
from django.contrib.auth.models import User

# 👤 Register API
@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"})
    return Response(serializer.errors, status=400)

#  Get all bugs
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_bugs(request):
    bugs = bugs_report.objects.all().order_by('-id')
    serializer = BugSerializer(bugs, many=True)
    return Response(serializer.data)

#  Add new bug
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_bug(request):
    serializer = BugSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Bug added"})
    return Response(serializer.errors, status=400)
