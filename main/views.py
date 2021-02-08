from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg

# Create your views here.
def home(request):
	query = request.GET.get("title")
	allproducts = None
	if query:
		allproducts = Product.objects.filter(name__icontains=query)
	else:	
		allproducts = Product.objects.all()
	context = {
    	"product":allproducts,
    }
	return render(request,'main/index.html',context)

def detail(request,id):
	product=Product.objects.get(id=id)
	reviews = Review.objects.filter(product=id).order_by("-comment")

	average = reviews.aggregate(Avg("rating"))["rating__avg"]
	if average == None:
		average=0
	else:
		average = round(average,2)
	context={
		"prod":product,
		"reviews":reviews,
		"average":average,
	}
	return render(request,'main/details.html',context)

def add_products(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			if request.method == "POST":
				form = ProductForm(request.POST or None)

				if form.is_valid():
					data = form.save(commit=False)
					data.save()
					return redirect("main:home")
			else:
				form = ProductForm()
			return render(request,'main/addproducts.html',{"form":form,"controller":"Add Products"})
		else:
			return redirect("main:home")
	return redirect("accounts:login")

def edit_products(request,id):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			produ = Product.objects.get(id=id)
			if request.method == "POST":
				form = ProductForm(request.POST or None, instance=produ)
				if form.is_valid():
					data = form.save(commit=False)
					data.save()
					return redirect("main:detail",id)
			else:
				form =ProductForm(instance=produ)
				return render(request,'main/addproducts.html',{'form':form, "controller":"Edit Products"})
		else:
			return redirect("main:home")
	return redirect("accounts:login")

def delete_products(request,id):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			produ = Product.objects.get(id=id)
			produ.delete()
			return redirect("main:home")
		else:
			return redirect("accounts:login")

def add_review(request,id):
	if request.user.is_authenticated:
		product = Product.objects.get(id=id)
		if request.method == "POST":
			form = ReviewForm(request.POST or None)
			if form.is_valid():
				data = form.save(commit=False)
				data.comment = request.POST["comment"]
				data.rating = request.POST["rating"]
				data.user = request.user
				data.product = product
				data.save()
				return redirect("main:detail",id)
		else:
			form = ReviewForm()
		return render(request,'main/details.html',{'form':form})
	else:
		return redirect("accounts:login")

def edit_review(request,product_id,review_id):
	if request.user.is_authenticated:
		product = Product.objects.get(id=product_id)
		review = Review.objects.get(product=product, id=review_id)
		if request.user == review.user:
			if request.method == "POST":
				form = ReviewForm(request.POST,instance=review)
				if form.is_valid():
					data = form.save(commit=False)
					if (data.rating>10) or (data.rating<0):
						error="Out of range. Please select rating from 0 to 10."
						return render(request,'main/editreview.html',{'error':error, "form":form})
					else:
						data.save()
						return redirect("main:detail",product_id)
			else:
				form = ReviewForm(instance=review)
			return render(request,'main/editreview.html',{"form":form})
		else:
			return redirect("main:detail",product_id)
	else:
		return redirect("accounts:login")

def delete_review(request,product_id,review_id):
	if request.user.is_authenticated:
		product = Product.objects.get(id=product_id)
		review = Review.objects.get(product=product, id=review_id)
		if request.user == review.user:
			review.delete()
		return redirect("main:detail",product_id)
	else:
		return redirect("accounts:login")

def about(request):
	return render(request,'main/about.html')