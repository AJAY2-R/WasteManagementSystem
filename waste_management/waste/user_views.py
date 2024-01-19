from typing import Any, Dict
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views.generic import TemplateView
from django.db.models import Sum
from waste.models import waste_pickup,user_Registration,CollectionHistory,products,Purchase,OrderUpdates,Comaplaints,locations,stock_his
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
class indexview(TemplateView):
    template_name='user/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('id')
        user = user_Registration.objects.get(user_id=user_id)
        context['user'] = user
        uid=User.objects.get(id=user_id)
        print(uid.last_name)
        context['uid']=uid
        pd=products.objects.all()
        context['pd']=pd
        return context
      
class pickup_request(TemplateView):
    template_name='user/pickup_req.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session.get('id')
        user = user_Registration.objects.get(user_id=userid)
        context['user'] = user
        return context

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.POST['user_id']
            user=user_Registration.objects.get(user_id=user_id)
            print(user)
            obj = waste_pickup()
            if  waste_pickup.objects.filter(userid=user.id,status='requested').exists():
                raise Exception
            obj.userid=user
            obj.save()
            message = 'Requested for pick up'
            messages.info(request, message)
            return redirect('/user')
        
        except Exception:
            message = "Unable to process request"
            messages.info(request, message)
            return redirect('/user')


class view_profile(TemplateView):
    template_name = 'user/view_profile.html'
    def get_context_data(self, **kwargs):
        context = super(view_profile,self).get_context_data(**kwargs)
        
        app_user = user_Registration.objects.filter(user_id=self.request.user.id)

        context['app_user'] = app_user
        return context

class edit_profile_view(TemplateView):
    template_name = 'user/edit_profile_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        app_user = user_Registration.objects.filter(user_id=self.request.user.id).first()

        context['app_user'] = app_user
        return context
    
    def post(self, request, *args, **kwargs):
        id = self.request.session.get('id')
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        pincode = request.POST['pincode']
        
        us = User.objects.get(pk=id)
        usr = user_Registration.objects.get(user_id=id)
        us.first_name = name
        us.email = email
        us.save()
        usr.name = name
        usr.email = email
        usr.address = address
        usr.mobile = mobile
        usr.pincode = pincode
    
        usr.save()
        message = 'Profile Updated'
        messages.success(request, message)
        return redirect('/user')

class history(TemplateView):
    template_name='user/history.html'
    def get_context_data(self, **kwargs):
        context= super(history,self).get_context_data(**kwargs)
        uid=self.request.session.get('id')
        user=user_Registration.objects.get(user_id=uid)
        pickups=waste_pickup.objects.filter(userid=user.id)
        pickup_data=dict()
        for pickup in pickups:
            tpoint = CollectionHistory.objects.filter(pid=pickup.id).aggregate(tpoint=Sum('point'))['tpoint']
            pickup.tpoint = tpoint
            pickup_data[pickup.id] = tpoint
        print(pickup_data)
        context['data'] = pickup_data
        context['his']=pickups
        return context

class full_history(TemplateView):
    template_name='user/fullhistory.html'
    def get_context_data(self, **kwargs):
        context= super(full_history,self).get_context_data(**kwargs)
        uid=self.request.session.get('id')
        user=user_Registration.objects.get(user_id=uid)
        
        if 'id' in self.request.GET and self.request.GET['id']:
            obj=CollectionHistory.objects.filter(pid=self.request.GET['id'])
            context['col']=obj
            return context
        
        pickups=CollectionHistory.objects.filter(pid__userid=user.id) 
        context['col']=pickups
        return context

class shop(TemplateView):
    template_name='user/Shop.html'
    def get_context_data(self, **kwargs):
        context=super(shop,self).get_context_data(**kwargs)
        prod=products.objects.filter(status='1')
        context['prod']=prod
        return context
    
class view_product(TemplateView):
    template_name='product.html'
    def get_context_data(self,**kwargs):
        context=super(view_product,self).get_context_data(**kwargs)
        pid=self.request.GET['id']
        pd=products.objects.get(id=pid)
        user_id=self.request.session.get('id')
        uid=User.objects.get(id=user_id)
        print(uid.last_name)
        context['uid']=uid
        #print("UserId :",uid)
        user=user_Registration.objects.get(user_id=uid)                                                                        
        context['user']=user
        
        context['pd']=pd
        return context
    
class checkout(TemplateView):
    template_name='user/checkout.html'
    def get_context_data(self, **kwargs):
        context=super(checkout,self).get_context_data(**kwargs)
        uid=self.request.session.get('id')
        #print("UserId :",uid)
        pid=self.request.GET['id']
        user=user_Registration.objects.get(user_id=uid) 
        pd=products.objects.get(id=pid)                                                                       
        context['user']=user
        context['pd']=pd
        if self.request.GET['red']=='t':
            opt='redeem'
        elif self.request.GET['red']=='f':
            opt='buy'
            qty=self.request.GET['quantity']
            context['qty']=qty
            total=int(qty)*pd.rate
            context['total']=total
        context['opt']=opt
 
        return context
    def post(self,request,*args,**kwargs):
        pur=Purchase()
        product=products.objects.get(id=self.request.GET['id'])
        stk=stock_his.objects.get(product=product.id)
        user=user_Registration.objects.get(user_id=self.request.session.get('id'))
        pur.user=user
        check_box=request.POST.get('check')
        if check_box=='on':
            pur.address=user.address
            pur.mobile=user.mobile
            pur.pincode=user.pincode
        else:
            pur.address=request.POST['add1']+" "+request.POST['add2']
            pur.mobile=request.POST['number']
            pur.pincode=request.POST['zip']
        pur.product=product   
        if 'redeem' in request.POST:
            user.point=user.point-product.point
            pur.type=pur.REDEEM
            pur.total=product.point
            stk.stock-=1
        else:
            qty=int(request.POST['qty'])
            pur.quantity=qty
            pur.type=pur.PURCHASE
            pur.total=product.rate*qty
            stk.stock-=qty
            print(product.rate*qty)
        pur.save()
        user.save()
        stk.save()
        message = 'Order Placed Successfully'
        messages.success(request, message)
        return redirect('/user')

class OrderHis(TemplateView):
    template_name='user/orderhis.html'
    def get_context_data(self, **kwargs):
        user=user_Registration.objects.get(user_id=self.request.session.get('id'))
        context=super(OrderHis,self).get_context_data(**kwargs)
        order=Purchase.objects.filter(user=user.id)
        context['order']=order
        return context
    
class OrderUpdate(TemplateView):
    template_name='user/orderupdates.html'
    def get_context_data(self, **kwargs):
        context=super(OrderUpdate,self).get_context_data(**kwargs)
        orderid=self.request.GET['id']
        update=OrderUpdates.objects.filter(order=orderid)
        context['update']=update
        return context
    
class ComplaintRegister(TemplateView):
    template_name="user/registercomplaint.html"
    def post(self,request):
        user=user_Registration.objects.get(user_id=self.request.session.get('id'))
        subject=request.POST['subject']
        complaint=request.POST['comp']
        comp=Comaplaints()
        comp.user=user
        comp.subject=subject
        comp.complaint=complaint
        comp.save()
        message = 'Comaplaint registerd Successfully'
        messages.success(request, message)
        return redirect('/user')

class complaint_Status(TemplateView):
    template_name="user/complaintstatus.html"
    def get_context_data(self, **kwargs):
        context=super(complaint_Status,self).get_context_data(**kwargs)
        user=self.request.session.get('id')
        uid=user_Registration.objects.get(user_id=user)
        comp=Comaplaints.objects.filter(user=uid)
        context['update']=comp
        return context

class Bill(TemplateView):
    template_name="user/bill.html"
    def get_context_data(self, **kwargs):
        context=super(Bill,self).get_context_data(**kwargs)
        id=self.request.GET['id']
        pur=Purchase.objects.get(id=id)
        context['pur']=pur
        return context
    
class JoinUs(TemplateView):
    template_name="user/joinus.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.session.get('id')
        user = user_Registration.objects.get(user_id=userid)
        if locations.objects.filter(pincode=user.pincode).exists():
            context['check']=True
        else:
            context['check']=False
        
        context['user'] = user
        print(context['check'])
        return context
    def post(self,request):
        user=User.objects.get(id=self.request.session.get("id"))
        user.last_name='0'
        user.save()
        message = 'Wait for verification'
        messages.success(request, message)
        return redirect('/user')