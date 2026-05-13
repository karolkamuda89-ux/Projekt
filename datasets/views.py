from django.shortcuts import render, redirect
from .utils import get_statistics
from .models import UploadedFile
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
        title = request.POST.get('title')
        description = request.POST.get('description')
        if file:
            # Tworzymy obiekt UploadedFile i przypisujemy zalogowanego użytkownika
            new_file = UploadedFile.objects.create(
                description = description,
                file= file, 
                name= title, 
                user= request.user
            )
            # Przekierowujemy do detali (upewnij się, że nazwa parametru w urls.py pasuje)
            return redirect('dataset_detail', dataset_id=new_file.id)
            
    return render(request, 'datasets/upload.html')

@login_required
def file_list(request):
    # 1. NAJPIERW pobierasz dane z bazy i zapisujesz do zmiennej
    user_files = UploadedFile.objects.filter(user=request.user)
    print(f"DEBUG: Użytkownik {request.user.username} ma plików: {user_files.count()}")
    
    # 2. POTEM wysyłasz tę zmienną do szablonu
    return render(request, 'datasets/list.html', {
        'datasets': user_files
    })

def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(UploadedFile, id=dataset_id, user=request.user)
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