from django import forms
from .models import *

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('name','typ','size','cost','description','release_date','image','averagerating')

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ("comment","rating")