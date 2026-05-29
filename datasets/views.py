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
import pandas as pd

def index(request):
    return render(request, "datasets/index.html")

@login_required
def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        title = request.POST.get('title')
        description = request.POST.get('description')
        if file:
            # PONIŻEJ ZACZYNA SIĘ TWÓJ COMMIT: Wyciągnięcie rozszerzenia i walidacja
            file_extension = os.path.splitext(file.name)[1]
            if file_extension.lower() != '.csv':
                messages.error(request, "Nieprawidłowy format. Aplikacja akceptuje wyłącznie pliki z rozszerzeniem .csv.")
                return redirect('upload_csv') # Wracamy do tego samego widoku uploadu po błędzie
            # KONIEC TWOJEGO COMMITA

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
    # Wyszukiwarka plików - Pobieramy nazwę plików wpisane w wyszukiwarkę:
    query = request.GET.get('q')
    if query:
        # Filtrujemy pliki użytkownika po nazwie (name)
        user_files = user_files.filter(name__icontains=query)
        
    print(f"DEBUG: Użytkownik {request.user.username} ma plików: {user_files.count()}")
    
    # 2. POTEM wysyłasz tę zmienną do szablonu pod nazwą 'datasets'
    return render(request, 'datasets/list.html', {
        'datasets': user_files
    })
import pandas as pd

def get_statistics(file_path):
    try:
        # Wczytujemy plik przez Pandas
        df = pd.read_csv(file_path, on_bad_lines='skip')
        print("--- LOCATIONS OF NULLS ---")
        print(df[df.isnull().any(axis=1)])
        print("--------------------------")
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        if df.empty:
            return {'error': 'Plik jest pusty.'}

        # 1. To są te klucze, które Twój HTML wyświetlał wcześniej:
        liczba_wierszy = len(df)
        liczba_kolumn = df.shape[1]
        puste_komorki = int(df.isna().sum().sum())

        # 2. To są nowe statystyki biznesowe:
        best_days = df.groupby('date')['sales_amount'].sum().sort_values(ascending=False)
        top_day = best_days.index[0]
        top_day_amount = round(best_days.iloc[0])

        top_region = df['region'].mode()[0]
        top_payment = df['payment_method'].mode()[0]
        average_sales = round(df['sales_amount'].mean(), 2)
        top_product = df['product'].mode()[0]

        # 3. Zwracamy JEDEN wielki słownik, który ma i stare, i nowe dane:
        return {
            # Stare klucze (znów zaczną działać!)
            'liczba_wierszy': liczba_wierszy,
            'liczba_kolumn': liczba_kolumn,
            'puste': puste_komorki,
            
            # Nowe klucze
            'najlepszy_dzien': f"{top_day} ({top_day_amount} zł)",
            'najlepszy_region': top_region,
            'najczestsza_platnosc': top_payment,
            'srednia_cena': f"{average_sales} zł",
            'najczestszy_produkt': top_product
        }
        
    except Exception as e:
        # Jeśli coś pójdzie nie tak, ten klucz wyłapie błąd w HTML
        return {'error': f"Błąd analizy pliku: {str(e)}"}
def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(UploadedFile, id=dataset_id, user=request.user)
    stats = get_statistics(dataset.file.path)
    return render(request, 'datasets/detail.html', {'plik': dataset, 'statystyki': stats})

def register(request): ################# Poprawione
    if request.method == 'POST':

        un = request.POST.get('username')
        ps = request.POST.get('password')
        em = request.POST.get('email')
        
        print(f"DEBUG: Próba rejestracji: {un}")
        if User.objects.filter(username=un).exists():
            messages.error(request, 'Ta nazwa użytkownika jest już zajęta!')
            return render(request, 'registration/login.html')
        
        if un and ps and em:
            try:
                # Sprawdzamy czy hasło spełnia wymogi
                validate_password(ps, user=User(username=un))
            except ValidationError as e:
                # Jeśli nie spełnia, to wywalamy błąd że za słabe
                messages.error(request, ' '.join(e.messages))
                return render(request, 'registration/login.html')
            
            # Jeśli jest dobre to zapisujemy w bazie użytkownika
            User.objects.create_user(username=un, password=ps, email=em)
            print("DEBUG: Zapisano użytkownika!")
            messages.success(request, 'Konto zostało utworzone! Możesz się teraz zalogować.')
            return redirect('login')
        else:
            print("DEBUG: Brak loginu lub hasła - nie zapisuję!")
    
    return render(request, 'registration/login.html')

    # Ta funkcja na górze przyjmuje ścieżkę pod ogólną nazwą 'file_path'