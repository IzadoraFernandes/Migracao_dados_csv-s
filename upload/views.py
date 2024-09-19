import csv
from django.shortcuts import render, redirect
from .forms import *
from .models import Rating, Tag, Movie, Link, GenomeScore, GenomeTag
from django.db import transaction
from django.http import HttpResponse

"""def upload_csv(request):

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            dataset = file.read().decode('utf-8').splitlines()
            reader = csv.reader(dataset)

            
            model_name = request.POST.get('model')
            model = None

            if model_name == 'Rating':
                model = Rating
            elif model_name == 'Tag':
                model = Tag
            elif model_name == 'Movie':
                model = Movie
            elif model_name == 'Link':
                model = Link
            elif model_name == 'GenomeScore':
                model = GenomeScore
            elif model_name == 'GenomeTag':
                model = GenomeTag

            if model:
                
                headers = next(reader)

                for row in reader:
                    data = dict(zip(headers, row))
                    # Cria uma nova instância do modelo com os dados do CSV
                    obj = model(**data)
                    obj.save()

            return redirect('success')

    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})
"""
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            dataset = file.read().decode('utf-8').splitlines()
            reader = csv.reader(dataset)

            model_name = request.POST.get('model')
            model = None

            # Mapeia o nome do modelo para a classe
            if model_name == 'Rating':
                model = Rating
            elif model_name == 'Tag':
                model = Tag
            elif model_name == 'Movie':
                model = Movie
            elif model_name == 'Link':
                model = Link
            elif model_name == 'GenomeScore':
                model = GenomeScore
            elif model_name == 'GenomeTag':
                model = GenomeTag

            if model:
                headers = next(reader)  # Lê os cabeçalhos
                data_batch = []

                for row in reader:
                    data = dict(zip(headers, row))
                    data_batch.append(model(**data))  # Acumula as instâncias

                # Salva em lotes
                batch_size = 500000
                for i in range(0, len(data_batch), batch_size):
                    with transaction.atomic():
                        model.objects.bulk_create(data_batch[i:i + batch_size])

            return redirect('success')

    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})

def upload_success(request):
    return render(request, 'success.html')


def rating_list(request):
    ratings = Rating.objects.all()
    return render(request, 'rating_list.html', {'ratings': ratings})

def rating_create(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rating_list')
    else:
        form = RatingForm()
    return render(request, 'rating_form.html', {'form': form})

def rating_update(request, pk):
    rating = Rating.objects.get(pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('rating_list')
    else:
        form = RatingForm(instance=rating)
    return render(request, 'rating_form.html', {'form': form})

def rating_delete(request, pk):
    rating = Rating.objects.get(pk=pk)
    if request.method == 'POST':
        rating.delete()
        return redirect('rating_list')
    return render(request, 'rating_confirm_delete.html', {'object': rating})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})

def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'tag_form.html', {'form': form})

def tag_update(request, pk):
    tag = Tag.objects.get(pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    return render(request, 'tag_form.html', {'form': form})

def tag_delete(request, pk):
    tag = Tag.objects.get(pk=pk)
    if request.method == 'POST':
        tag.delete()
        return redirect('tag_list')
    return render(request, 'tag_confirm_delete.html', {'object': tag})