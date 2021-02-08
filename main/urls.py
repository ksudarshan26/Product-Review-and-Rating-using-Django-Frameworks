from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('',views.home,name="home"),
    path('about',views.about,name="about"),
    path('details/<int:id>/',views.detail,name="detail"),
    path('addproducts/',views.add_products,name="add_products"),
    path('editproducts/<int:id>/',views.edit_products,name="edit_products"),
    path('deleteproducts/<int:id>/',views.delete_products,name="delete_products"),
    path('addreview/<int:id>/',views.add_review,name="add_review"),
    path('editreview/<int:product_id>/<int:review_id>',views.edit_review,name="edit_review"),
    path('deletereview/<int:product_id>/<int:review_id>',views.delete_review,name="delete_review"),


]
