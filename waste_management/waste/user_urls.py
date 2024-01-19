from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from waste.user_views import indexview,pickup_request,view_profile,edit_profile_view,history,JoinUs,full_history,shop,view_product,checkout,Bill,OrderHis,OrderUpdate,ComplaintRegister,complaint_Status

urlpatterns = [
    path('',indexview.as_view(),name='index'),
    path('PickupRequest',pickup_request.as_view()),
    path('ViewProfile',view_profile.as_view()),
    path('EditProfile',edit_profile_view.as_view()),
    path('ReqestHistory',history.as_view()),
    path('PointHistory',full_history.as_view()),
    path('Shop',shop.as_view()),
    path('Product',view_product.as_view()),
    path('Checkout',checkout.as_view()),
    path('OrderHistory',OrderHis.as_view()),
    path('OrderUpdates',OrderUpdate.as_view()),
    path('ComplaintRegister',ComplaintRegister.as_view()),
    path('TrackComplaints',complaint_Status.as_view()),
    path('Bill',Bill.as_view()),
    path('JoinUs',JoinUs.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def urls():
    return urlpatterns,'user','user'
