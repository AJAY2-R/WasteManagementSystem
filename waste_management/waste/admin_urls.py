from django.urls import path
from waste.admin_views import indexview,collector_registration,add_product,product_list,add_category,view_category,manage_category,ViewOrders
from waste.admin_views import OrderAct,ViewCollection,ViewComplaints,userview,ComplaintSolved,manage_prod,pickup_request,ViewOrdersDeli,ViewCollectionCollector,add_stock,product_edit,CollectorList,PinCodeInsertView,PinCodeListView,RemovePinCodeView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',indexview.as_view()),
    path('collectorRegistration',collector_registration.as_view()),
    path('addproduct',add_product.as_view()),
    path('viewproducts',product_list.as_view()),
    path('AddCategory',add_category.as_view()),
    path('ViewCategory',view_category.as_view()),
    path('ManageCategory',manage_category.as_view()),
    path('ViewOrders',ViewOrders.as_view()),
    path('OrdersDelivered',ViewOrdersDeli.as_view()),
    path('OrderAct',OrderAct.as_view()),
    path('PickupRequest',pickup_request.as_view()),
    path('CollectionHistory',ViewCollection.as_view()),
    path('CollectionHistoryCollector',ViewCollectionCollector.as_view()),
    path('ComplaintSolved',ComplaintSolved.as_view()),
    path('ViewComplaints',ViewComplaints.as_view()),
    path('viewuser',userview.as_view()),
    path('ProductEdit',product_edit.as_view()),
    path('UpdateStock',add_stock.as_view()),
    path('ManageProduct',manage_prod.as_view()),
    path('AddLocation',PinCodeInsertView.as_view()),
    path('ViewLocations',PinCodeListView.as_view()),
    path('remove_pincode', RemovePinCodeView.as_view(),name='remove_pincode'),
    path('CollectorList',CollectorList.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def urls():
    return urlpatterns,'admin','admin'


if settings.DEBUG :
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_URL)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_URL)
    