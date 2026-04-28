from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, TableViewSet, OrderViewSet, InventoryViewSet

router = DefaultRouter()
router.register('menu', MenuViewSet)
router.register('tables', TableViewSet)
router.register('orders', OrderViewSet)
router.register('inventory', InventoryViewSet)

urlpatterns = router.urls