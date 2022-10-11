from dataclasses import fields
from django import forms

from aplicacion.models import cliente, producto, ventas

class Formularioproducto(forms.ModelForm):
    class Meta:
        model = producto
        fields='__all__'



class Formulario_clientes(forms.ModelForm):
    class Meta:
        model=cliente
        fields='__all__'



class Formulario_ventas(forms.ModelForm):
    class Meta:
        model=ventas
        fields='__all__'