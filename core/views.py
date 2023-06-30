from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
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


@login_required
def create_flashcard(request, pack_id: int):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        print('json_Data: ', json_data)
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
@require_http_methods(["DELETE"])
def delete_flashcard(request, flashcard_id: int):
    print('debug')
    try:
        flashcard = Flashcard.objects.get(id=flashcard_id)
    except Flashcard.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Flashcard not found'})

    if flashcard.pack.owner != request.user:
        return JsonResponse({'success': False, 'error': 'Not authorized'})

    flashcard.delete()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["POST"])
def edit_flashcard(request, flashcard_id: int):
    print('tutaj?')
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
