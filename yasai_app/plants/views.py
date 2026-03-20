from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant
from .forms import PlantForm

def plant_list(request):
    plants = Plant.objects.all()  # データベースから全部取得
    return render(request, 'plants/plant_list.html', {'plants': plants})

def plant_create(request):
    if request.method == 'POST': #フォームが送信されたとき
        form = PlantForm(request.POST) #送信されたデータをフォームに入れる
        if form.is_valid(): #入力内容が正しいか確認する
            form.save()
            return redirect('plant_list') #保存後に一覧ページに移動するrequest.method == 'GET'ページを開いただけのとき
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {'form': form})

def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        plant.delete()
        return redirect('plant_list')
    return render(request, 'plants/plant_confirm_delete.html', {'plant': plant})

def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    return render(request, 'plants/plant_detail.html', {'plant': plant})