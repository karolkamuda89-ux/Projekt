import os
from django.shortcuts import render, redirect
from .utils import get_statistics
from .models import UploadedFile
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def index(request):
    context = {}
    if request.user.is_authenticated:
        user_files = UploadedFile.objects.filter(user=request.user)
        context['files_count'] = user_files.count()
        context['last_upload'] = user_files.order_by('-uploaded_at').first()
    return render(request, "datasets/index.html", context)


@login_required
def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        title = request.POST.get('title')
        description = request.POST.get('description')
        if file:
            file_extension = os.path.splitext(file.name)[1]
            if file_extension.lower() != '.csv':
                messages.error(request, "Nieprawidłowy format. Aplikacja akceptuje wyłącznie pliki z rozszerzeniem .csv.")
                return redirect('upload_csv')

            new_file = UploadedFile.objects.create(
                description=description,
                file=file,
                name=title,
                user=request.user
            )
            return redirect('dataset_detail', dataset_id=new_file.id)

    return render(request, 'datasets/upload.html')


@login_required
def file_list(request):
    user_files = UploadedFile.objects.filter(user=request.user)
    query = request.GET.get('q')
    if query:
        user_files = user_files.filter(name__icontains=query)

    return render(request, 'datasets/list.html', {
        'datasets': user_files
    })


@login_required
def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(UploadedFile, id=dataset_id, user=request.user)
    stats = get_statistics(dataset.file.path)
    return render(request, 'datasets/detail.html', {'plik': dataset, 'statystyki': stats})


def register(request):
    if request.method == 'POST':
        un = request.POST.get('username')
        ps = request.POST.get('password')
        em = request.POST.get('email')

        if User.objects.filter(username=un).exists():
            messages.error(request, 'Ta nazwa użytkownika jest już zajęta!')
            return render(request, 'registration/login.html')

        if un and ps and em:
            try:
                validate_password(ps, user=User(username=un))
            except ValidationError as e:
                messages.error(request, ' '.join(e.messages))
                return render(request, 'registration/login.html')

            User.objects.create_user(username=un, password=ps, email=em)
            messages.success(request, 'Konto zostało utworzone! Możesz się teraz zalogować.')
            return redirect('login')

    return render(request, 'registration/login.html')


@login_required
def delete_dataset(request, dataset_id):
    dataset = get_object_or_404(UploadedFile, id=dataset_id, user=request.user)

    if dataset.file:
        dataset.file.delete()

    dataset.delete()

    messages.success(request, f'Plik "{dataset.name}" został pomyślnie usunięty.')
    return redirect('list')