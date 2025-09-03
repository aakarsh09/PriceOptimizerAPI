from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'view', viewProducts, basename='view-products')
router.register(r'add', addProduct, basename='add-product')
urlpatterns = router.urls
