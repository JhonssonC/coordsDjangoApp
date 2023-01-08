
from django.shortcuts import render

from coords.forms import CoordsForm
from coords.models import Cliente



def index(request):
    data = None
    if request.method == "POST":
        form = CoordsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['buscado_Criterio'])
            print(form.cleaned_data['servicio_sico'])
            print(form.cleaned_data['medidor_bpm'])
            s = Cliente(
                buscado_Criterio=form.cleaned_data['servicio_sico'],
                servicio_sico=form.cleaned_data['servicio_sico'],
                medidor_bpm=form.cleaned_data['medidor_bpm']
            )
            s.query_data()
            s.request_a()

            s.save()

            data = s

    else:
        form = CoordsForm()
    return render(request, "coordenadas.html", {"form": form, "data": data})
