from django.urls import path,include
from . import views
from .router import router
urlpatterns = [
    path('', include(router.urls)),
    path('categories', views.GetCategories.as_view()),
    path('product/add_remove', views.AddRemove.as_view()),
    path('product/add_supply', views.AddSupply.as_view()),
    path('product/by_uuid', views.GetProductByUuid.as_view()),


]
