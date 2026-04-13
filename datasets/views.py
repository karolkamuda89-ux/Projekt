from django.shortcuts import render, redirect
from .utils import get_statistics
from .models import Dataset
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, "datasets/index.html")

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