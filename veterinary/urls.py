from django.urls import path
from .views import send_email

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/", views.registerVet, name="registerVet"),
    path("registro/empleado", views.registerEmployee, name="registerEmployee"),
    path("registro/citas", views.registerDate, name="registerDate"),
    path("home/", views.home, name="home"),
    path("actualizar/empleado/<int:id>", views.updateEmployee, name='updateEmployee'),
    path("ver/clientes", views.detailClient, name='detailClient'),
    path("ver/mascotas", views.detailPet, name='detailPet'),
    path("ver/empleados", views.detailEmployee, name='detailEmployee'),
    path("actualizar/clientes/<int:id>", views.updateClient, name='updateClient'),
    path("actualizar/mascota/<int:id>", views.updatePet, name='updatePet'),
    path("actualizar/cita/<int:id>", views.updateDate, name='updateDate'),
    path("eliminar/clientes/<int:id>", views.deleteClient, name="deleteClient"),
    path("eliminar/cita/<int:id>", views.deleteEvent, name="deleteEvent"),
    path("eliminar/empleados/<int:id>", views.deleteEmployee, name="deleteEmployee"),
    path("eliminar/mascotas/<int:id>", views.deletePet, name="deletePet"),
    path("eliminar/servicio/<int:id>", views.deleteService, name='deleteService'),
    path('actualizar/servicio/<int:id>', views.updateService, name="updateService"),
    path("support", views.support, name="support"),
    path("ver/productos", views.detailProduct, name="detailProduct"),
    path("eliminar/producto/<int:id>", views.deleteProduct, name="deleteProduct"),
    path("actualizar/producto/<int:id>", views.updateProduct, name="updateProduct"),
    path("registrar/venta", views.create_sale, name="create_sale"),
    path('send_email/', send_email, name='send_email'),
    path("procesar/factura", views.create_sale2, name="create_sale2"),
    path('search/', views.search, name='search'),
    path('check_sale_data/', views.check_sale_data, name='check_sale_data'),
    path('ver/ventas', views.list_sale, name='list_sale'),
    path('ver/clinica', views.detailClinic, name='detailClinic'),
    path('ver/peluqueria', views.detailSalon, name='detailSalon'),
    path('ver/guarderia', views.detailDaycare, name='detailDaycare'),
    path('manual-usuario/', views.manual_usuario_view, name='manual_usuario'),
    path('reporte/', views.report_sale, name='reportSale')
    
]
