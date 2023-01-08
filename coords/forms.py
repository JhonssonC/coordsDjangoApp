
from django import forms

from coords.models import Cliente

CRITERIOS = (
    ('Medidor', 'Medidor'),
    ('Código', 'Código')
)

class CoordsForm(forms.Form):

   buscado_Criterio = forms.Field(

       widget=forms.widgets.Select(choices=CRITERIOS,
           attrs={
            "class": "form-select"
           }
       ),
       label="Criterio de Búsqueda",
   )
   servicio_sico = forms.CharField(
       max_length=11,
       required=False,
       widget=forms.widgets.Input (
           attrs={
               "class": "form-control form-control-lg"
           }
       ),
       label="Código de Cliente / Servicio / Cuenta"

   )
   medidor_bpm = forms.CharField(
       max_length=13,
       required=False,
       widget = forms.widgets.Input(
       attrs={
           "class": "form-control form-control-lg"
       }
   ),
            label = "Número de Medidor"
   )


   class Meta:
      model = Cliente
      exclude = ("user",)