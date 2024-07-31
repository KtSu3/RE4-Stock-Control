from django.contrib import admin
from django.urls import path, include
from App import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login_view'),
    path('index/', login_required(views.index), name='index'),
    path('logout/', views.logout_view, name='logout_view'), 
    path('menu/', login_required(views.menu_view), name='menu_view'),
    path('registrar/', views.register, name='register'),
    path('em_teste/', login_required(views.em_teste), name='em_teste'),
    path('mudar_status_equipamento/', login_required(views.mudar_status_equipamento), name='mudar_status_equipamento'),
    path('mudar_status_retestado/', login_required(views.mudar_status_retestado), name='mudar_status_retestado'),
    path('add_equipamento/', login_required(views.add_equipamento), name='add_equipamento'),
    path('lista_registrados/', login_required(views.list_equipamentos), name='list_equipamentos'),
    path('testar/', login_required(views.testar), name='testar'),
    path('teste_concluido/', login_required(views.teste_concluido), name='teste_concluido'),
    path('equipamento_testado/', login_required(views.testado), name='equipamento_testado'),
    path('reteste/', login_required(views.list_reteste), name='equipamento_reteste'),
    path('retestado/', login_required(views.retestado), name='retestado'),
    path('mudar_status_campo/', views.mudar_status_campo, name='mudar_status_campo'),
    path('campo/', login_required(views.campo), name='campo'),
    path('cv/', views.cv, name='cv'),
    path('AddViabilidade/', views.AddViabilidade, name='AddViabilidade'),
    path('AddTecnico/', views.AddTecnico, name='AddTecnico'),
    path('vc/', views.vc, name='vc'),
    path('menu_projeto/', login_required(views.menu_projeto), name='menu_projeto'),
    path('ct/', login_required(views.ct), name='ct'),
    path('tc/', login_required(views.tc), name='tc'),
    path('api/', include('App.urls')),
    
]   

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)