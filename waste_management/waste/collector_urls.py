from django.urls import path
from waste.collector_views import indexview,user_verify,userview,user_approve,user_reject,pickup_request,waste_collect,ViewCollection
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',indexview.as_view()),
    path('UserVerify/',user_verify.as_view()),
    path('viewuser',userview.user_list),
    path('UserVerify/approve',user_approve.as_view()),
    path('UserVerify/reject',user_reject.as_view()),
    path('PickupRequest',pickup_request.as_view()),
    path('Collection',waste_collect.as_view()),
    path('CollectionHistory',ViewCollection.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def urls():
    return urlpatterns,'collector','collector'
