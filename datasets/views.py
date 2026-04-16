from django.shortcuts import render, redirect
from .utils import get_statistics
from .models import Dataset
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "datasets/index.html")
@login_required
def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            dataset = Dataset.objects.create(file=file, name=file.name)
            return redirect('dataset_detail', dataset_id=dataset.id)
    return render(request, 'datasets/upload.html')

def file_list(request):
    datasets = Dataset.objects.all() # Pobierasz listę z bazy
    return render(request, 'datasets/list.html', {'datasets': datasets})

def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    stats = get_statistics(dataset.file.path)
    return render(request, 'datasets/detail.html', {'plik': dataset, 'statystyki': stats})
def register(request): ################# DO POPRAWY ALE DZIAŁA
    if request.method == 'POST':
        un = request.POST.get('username')
        ps = request.POST.get('password')
        em = request.POST.get('email')
        print(f"DEBUG: Próba rejestracji: {un}, hasło: {ps}") # To pojawi się w konsoli (czarne okno)
        if User.objects.filter(username=un).exists():
            messages.error(request, 'Ta nazwa użytkownika jest już zajęta!')
            return render(request, 'datasets/login.html')
        
        if un and ps and em:
            User.objects.create_user(username=un, password=ps , email=em)
            print("DEBUG: Zapisano użytkownika!")
            return redirect('login')
        else:
            print("DEBUG: Brak loginu lub hasła - nie zapisuję!")
    
    return render(request, 'registration/login.html')