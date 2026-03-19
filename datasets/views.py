import csv
from django.shortcuts import redirect, render, get_object_or_404

from datasets.models import Dataset
def detail(request, plik_id):
    d = get_object_or_404(Dataset, id=plik_id)
    return render(request, 'datasets/detail.html', {'plik': d})

def index(request):
    return render(request, "datasets/index.html")
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        name = request.POST.get('title', 'Untilted')
        description = request.POST.get('description', 'none')
        file = request.FILES['file']
        
        # Zapis do bazy danych
        Dataset.objects.create(name=name, description=description, file=file)
        return redirect('list')  # Przekierowanie na listę po wgraniu
    return render(request, 'datasets/upload.html')
def file_list(request):
    pliki = Dataset.objects.all().order_by('-uploaded_at')
    return render(request, 'datasets/list.html', {'pliki': pliki})
def file_detail(request):
    return render(request, 'datasets/detail.html')
def detail(request, plik_id):
    plik = get_object_or_404(Dataset, id=plik_id)
    return render(request, 'datasets/detail.html', {'plik': plik})
    