from typing import Any, Dict
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
from waste.models import user_Registration,waste_pickup,category,CollectionHistory,collector_Registration
# Create your views here.
class indexview(TemplateView):
    template_name='collector/index.html'

class userview:
    def user_list(request):
        user=user_Registration.objects.all()
        return render(request,'collector/user_list.html',{'user':user})

class user_approve(View):
    def dispatch(self, request, *args, **kwargs):

        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name='1'
        user.save()
        user = user_Registration.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')
        return render(request,'collector/user_approvel.html',{'user':user,'message':" Account Approved"})

class user_reject(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name='1'
        user.is_active='0'
        user.save()
        return render(request,'collector/user_approvel.html',{'message':"Account Removed"})
    
class user_verify(TemplateView):
    template_name = 'collector/user_approvel.html'
    def get_context_data(self, **kwargs):
        context = super(user_verify,self).get_context_data(**kwargs)
        user = user_Registration.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')
        context['user'] = user
        return context
    
class pickup_request(TemplateView):
    template_name='collector/pickup_request.html'
    def get_context_data(self, **kwargs):
        context= super(pickup_request,self).get_context_data(**kwargs)
        pickup=waste_pickup.objects.filter(status='requested')
        context['pickup']=pickup
        return context

class waste_collect(TemplateView):
    template_name='collector/waste_collect.html'
    def get_context_data(self, **kwargs):
       context= super(waste_collect,self).get_context_data(**kwargs)
       cat=category.objects.all()
       id=self.request.GET['id']
       obj=waste_pickup.objects.get(id=id)
       context['pickup']=obj
       context['cat']=cat
       return context
    def post(self,request,*args,**kwargs):
        cat = request.POST.getlist('cat[]')
        qty = request.POST.getlist('qty[]')
        print("Category :",cat,"Qty: ",qty)
        pickupid = request.GET['id']
        tpoint=0
        try:
            for cate, quantity in zip(cat, qty):  
                collection=CollectionHistory()
                obj = category.objects.get(name=cate)
                point=obj.point
                totalpoint=int(point)*float(quantity)
                wastepickup=waste_pickup.objects.get(id=pickupid)
                collection.pid=wastepickup
                collection.category=obj
                collection.weight=quantity
                collection.point=totalpoint
                tpoint=tpoint+totalpoint
                print("passed")
                collection.save()
            obj=waste_pickup.objects.get(id=pickupid)
            obj.pdate=timezone.now()
            obj.status='collected'
            collector=collector_Registration.objects.get(collector_id=self.request.session.get('cid'))
            obj.collector=collector
            user=user_Registration.objects.get(id=obj.userid.id)            
            user.point=user.point+tpoint
            user.save()
            obj.save()
            message='SuccessFully Collected'
            messages.info(request,message)
            return redirect('/collector')
        except Exception as e:
            messages.info(request,e)
            return redirect('/collector')

class ViewCollection(TemplateView):
    template_name="collector/collectionhis.html"
    def get_context_data(self, **kwargs):
        context= super(ViewCollection,self).get_context_data(**kwargs)
        col=collector_Registration.objects.get(collector_id=self.request.session.get('cid'))
        collection=CollectionHistory.objects.filter(pid__collector=col.id)
        total_collected = CollectionHistory.objects.filter(pid__collector=col.id).aggregate(total_weight=Sum('weight'))
        context['total']=total_collected['total_weight']
        context['col']=collection
        return context
    
    
    def post(self, request, *args, **kwargs):
        strt_date = request.POST['strt_date']
        end_date = request.POST['end_date']
        col=collector_Registration.objects.get(collector_id=self.request.session.get('cid'))
        host = CollectionHistory.objects.filter(pid__collector=col.id,pid__pdate__gte=strt_date,pid__pdate__lte=end_date)
        total_collected = CollectionHistory.objects.filter(pid__collector=col.id,pid__pdate__gte=strt_date,pid__pdate__lte=end_date).aggregate(total_weight=Sum('weight'))
        return render(request, 'collector/collectionhis.html', {'col':host,'total':total_collected['total_weight']})
    