from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.http import JsonResponse
from .models import Pack, Flashcard
import json


def home(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            ...
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def password_reset(request):
    return render(request, 'password_reset.html')


@login_required
def practise(request):
    return render(request, 'practise.html')


@login_required
def manage_packs(request):
    packs = Pack.objects.filter(owner=request.user)
    return render(request, 'manage_packs.html', {'packs': packs})


@login_required
def manage_flashcards(request, pack_id: int):
    pack = Pack.objects.get(id=pack_id)
    flashcards = Flashcard.objects.filter(pack_id=pack_id)
    return render(request, 'manage_flashcards.html', {'pack': pack, 'flashcards': flashcards})


@login_required
def create_pack(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        name = json_data.get('name')
        description = json_data.get('description')
        if name and description:
            pack = Pack(name=name, description=description, owner=request.user)
            pack.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Name or description missing'})
    return JsonResponse({'success': False, 'error': 'Invalid method'})
