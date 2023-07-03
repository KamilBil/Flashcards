from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.urls import reverse
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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"login_form": form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('manage_packs')
        else:
            messages.error(request, 'There was an error with your signup.')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def password_reset(request):
    return render(request, 'password_reset.html')


@login_required
def practise(request):
    packs = Pack.objects.filter(owner=request.user)
    return render(request, 'practise.html', {'packs': packs})


def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


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


@login_required
def create_flashcard(request, pack_id: int):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        question = json_data.get('question')
        answer = json_data.get('answer')
        pack = Pack.objects.get(id=pack_id)
        if question and answer:
            pack = Flashcard(question=question, answer=answer, pack=pack)
            pack.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Question or answer missing'})
    return JsonResponse({'success': False, 'error': 'Invalid method'})


@login_required
@require_http_methods(["POST"])
def edit_flashcard(request, flashcard_id: int):
    try:
        flashcard = Flashcard.objects.get(id=flashcard_id)
    except Flashcard.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Flashcard not found'})

    if flashcard.pack.owner != request.user:
        return JsonResponse({'success': False, 'error': 'Not authorized'})

    json_data = json.loads(request.body)
    question = json_data.get('question')
    answer = json_data.get('answer')

    if question and answer:
        flashcard.question = question
        flashcard.answer = answer
        flashcard.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Question or answer missing'})


@login_required
def review(request, pack_id: int):
    flashcards = list(Flashcard.objects.filter(pack_id=pack_id).values())
    serialized_flashcards = json.dumps(flashcards)
    pack = Pack.objects.get(id=pack_id)
    return render(request, 'review.html', {'pack': pack, 'flashcards': serialized_flashcards})


@login_required
@require_http_methods(["DELETE"])
def delete_flashcard(request, flashcard_id: int):
    try:
        flashcard = Flashcard.objects.get(id=flashcard_id)
    except Flashcard.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Flashcard not found'})

    if flashcard.pack.owner != request.user:
        return JsonResponse({'success': False, 'error': 'Not authorized'})

    flashcard.delete()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["DELETE"])
def delete_pack(request, pack_id: int):
    try:
        pack = Pack.objects.get(id=pack_id)
    except Pack.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pack not found'})

    if pack.owner != request.user:
        return JsonResponse({'success': False, 'error': 'Not authorized'})

    pack.delete()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["POST"])
def edit_pack(request, pack_id: int):
    try:
        pack = Pack.objects.get(id=pack_id)
    except Pack.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Pack not found'})

    if pack.owner != request.user:
        return JsonResponse({'success': False, 'error': 'Not authorized'})

    json_data = json.loads(request.body)
    name = json_data.get('name')
    description = json_data.get('description')

    if name and description:
        pack.name = name
        pack.description = description
        pack.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Name or description missing'})
