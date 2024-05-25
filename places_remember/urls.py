from django.urls import path
from .views import index, MemoryList, MemoryAddView, logout, UpdateMemory, MemoryDetailView


urlpatterns = [
    path('', index, name='home'),
    path('memory_list/', MemoryList.as_view(), name='memory_list'),
    path('add-memory/', MemoryAddView.as_view(), name='add_memory'),
    path('logout/', logout, name='logout'),
    path('update/<int:pk>/', UpdateMemory.as_view(), name='update_page'),
    path('detail/<int:pk>/', MemoryDetailView.as_view(), name='memory-detail'),
]
