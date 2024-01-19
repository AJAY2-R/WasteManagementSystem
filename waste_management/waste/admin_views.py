from typing import Any, Dict
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from django.views.generic import TemplateView,RedirectView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from waste.models import collector_Registration,user_Registration,userType,products,category,Purchase,OrderUpdates,CollectionHistory,locations,Comaplaints,stock_his,waste_pickup
from waste.forms import ImageUploadForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import F,Sum
# Create your models here.
# Create your views here.
class indexview(TemplateView):
    template_name='admin/index.html'
    def get_context_data(self, **kwargs):
        date=timezone.now()
        context=super(indexview,self).get_context_data(**kwargs)
        pd=products.objects.all()
        context['user']=user_Registration.objects.all().count()
        context['collection']=CollectionHistory.objects.filter(pid__pdate__year=date.year,pid__pdate__month=date.month).aggregate(total_weight=Sum('weight'))['total_weight']
        context['product_count']=pd.count()
        context['pd']=pd        
        context['orders']=Purchase.objects.filter(status='Ordered').count()
        context['Shipped']=Purchase.objects.filter(status='Delivered').count()

        print(context)
        return context

class collector_registration(TemplateView):
    template_name='admin/collectorregister.html' 
    def post(self, request, *args, **kwargs):
        fullname = request.POST['name']
        address = request.POST['address']
        
        email = request.POST['email']
        phone = request.POST['phone']
        
        password = request.POST['password']
    
        try:
            user = User.objects.create_user(username=email, password=password, first_name=fullname, email=email,last_name=1)
            user.save()
            reg = collector_Registration()
            reg.user = user
            reg.password=password
            reg.name=fullname
            reg.address = address          
            reg.mobile = phone      
            reg.email=email       
            reg.save()

            usertype = userType()
            usertype.user = user
            usertype.type = 'collector'
            usertype.save()
            messages = "Register Successfully."

            return render(request, 'admin/index.html', {'message': messages})
        except Exception as a:
            messages = "Username already used!.."
            return render(request, 'admin/index.html', {'message': a})   
        
class add_product(TemplateView):
    template_name='admin/add_product.html'
    def post(self,request,*args, **kwargs):
        try:
            name=request.POST['name']
            desc=request.POST['desc']
            rate=request.POST['rate']
            point=request.POST['point']
            stock=request.POST['stock']
            form=ImageUploadForm(request.POST,request.FILES)
            if form.is_valid():
                image=form.cleaned_data['image']
            else:
                return redirect('admin')
            prod=products()
            prod.name=name
            prod.desc=desc
            prod.rate=rate
            prod.point=point
            prod.image=image
            prod.status='1'
            prod.save()
            st =stock()
            st.product=prod
            st.stock=stock
            st.save()
            message = 'Product Added'
            messages.success(request, message)
            return redirect('/admin')
        except:
            message='Unable to add..'
            return render(request,'admin/add_product.html',{'message':message})
        
class add_stock(TemplateView):
    template_name="admin/update_stock.html"
    def get_context_data(self, **kwargs):
        context=super(add_stock,self).get_context_data(**kwargs)
        pd=products.objects.get(id=self.request.GET['id'])
        context['pd']=pd
        return context
    
    def post(self,request,*args, **kwargs):
        qty=request.POST['qty']
        stock=stock_his.objects.get(product=self.request.GET['id'])
        stock.stock+=int(qty)
        stock.save()
        message = 'Stock Added'
        messages.success(request, message)
        return redirect('/admin')

class manage_prod(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        pd=products.objects.get(id=id)
        
        if pd.status == 1 :
            pd.status=0
        else:
            st=stock_his.objects.get(id=id)
            if st.stock==0:
                message = 'Can\'t update becuase no stock '
                messages.success(request, message)
                return redirect('/admin/viewproducts')
                        
            pd.status=1
        
        pd.save()
        message = 'Status Updated'
        messages.success(request, message)
        return redirect('/admin/viewproducts')


    
class product_edit(TemplateView):
    template_name="admin/product_update.html"
    def get_context_data(self, **kwargs):
        context=super(product_edit,self).get_context_data(**kwargs)
        pd=products.objects.get(id=self.request.GET['id'])
        context['pd']=pd
        return context
    def post(self,request,*args, **kwargs):
        try:
            name=request.POST['name']
            desc=request.POST['desc']
            rate=request.POST['rate']
            point=request.POST['point']
            exclude_image = request.POST.get("exclude_image", "0")

            if exclude_image == "0":
                form=ImageUploadForm(request.POST,request.FILES)
                if form.is_valid():
                    image=form.cleaned_data['image']
                    prod.image=image
                else:
                    raise Exception("Error")
            
            prod=products.objects.get(id=request.GET['id'])
            prod.name=name
            prod.desc=desc
            prod.rate=rate
            prod.point=point
            
            prod.save()
            message = 'Product Updated'
            messages.success(request, message)
            return redirect('/admin')
        except Exception as e:
            message='Unable to Update..'
            messages.info(request, e)
            return redirect('/admin')
        
class product_list(TemplateView):
    template_name='admin/products_list.html'
    def get_context_data(self, **kwargs):
        context=super(product_list,self).get_context_data(**kwargs)
        pd=products.objects.annotate(stock=F('stock_his__stock'))
        context['pd']=pd
        return context

class add_category(TemplateView):
    template_name='admin/addcategory.html'
    def post(self,request,*args,**kwargs):
        name=request.POST['name']
        point=request.POST['point']
        cat=category()
        cat.name=name
        cat.point=point
        cat.save()
        message = 'Category Added'
        messages.success(request, message)
        return redirect('/admin')
    
class view_category(TemplateView):
    template_name='admin/view_category.html'
    def get_context_data(self,**kwargs):
        context=super(view_category,self).get_context_data(**kwargs)
        cat=category.objects.all()
        context['cat']=cat
        return context

class manage_category(TemplateView):
    template_name='admin/managecategory.html'
    def get_context_data(self, **kwargs):
        context=super(manage_category,self).get_context_data(**kwargs)
        cat=category.objects.get(id=self.request.GET['id'])
        context['cat']=cat
        return context
    def post(self,request,*args,**kwargs):
        id=self.request.GET['id']
        name=request.POST['name']
        point=request.POST['point']

        cat=category.objects.get(id=id)
        cat.name=name
        cat.point=point
        cat.save()
        message = 'Category Updated'
        messages.success(request, message)
        return redirect('/admin')
    
class ViewOrders(TemplateView):
    template_name='admin/orderhis.html'
    def get_context_data(self, **kwargs):
        context= super(ViewOrders,self).get_context_data(**kwargs)
        sts=['Ordered','Shipped']
        order=Purchase.objects.filter(status__in= sts)
        print(order)
        context['order']=order
        return context
    
class ViewOrdersDeli(TemplateView):
    template_name='admin/orderhis-Delivered.html'
    def get_context_data(self, **kwargs):
        context= super(ViewOrdersDeli,self).get_context_data(**kwargs)
        order=Purchase.objects.filter(status='Delivered')
        print(order)
        context['order']=order
        return context
    
class OrderAct(TemplateView):
    template_name='admin/OrderUpdate.html'
    def get_context_data(self, **kwargs):
        context= super(OrderAct,self).get_context_data(**kwargs)
        order=Purchase.objects.get(id=self.request.GET['id'])
        context['order']=order
        return context
    def post(self,request):
        order=Purchase.objects.get(id=self.request.GET['id'])
        up=OrderUpdates()
        up.order=order
        up.update=request.POST['message']
        update=request.POST['update']
        if update=='Shipped' or update=='Delivered' or update=='Canceled':
            order.status=update
            up.status=update
            order.save()
        up.save()
        message = 'Order Updated'
        messages.success(request, message)
        return redirect('/admin')

class ViewCollection(TemplateView):
    template_name="admin/collectionhis.html"
    def get_context_data(self, **kwargs):
        context= super(ViewCollection,self).get_context_data(**kwargs)
        

        if "id" in  self.request.GET:
            pickup=CollectionHistory.objects.filter(pid=self.request.GET['id'])
            context['col']=pickup
            total_collected = CollectionHistory.objects.filter(pid=self.request.GET['id']).aggregate(total_weight=Sum('weight'))
            context['total']=total_collected['total_weight']
        else:
            pickup=CollectionHistory.objects.all()
            total_collected = CollectionHistory.objects.aggregate(total_weight=Sum('weight'))
            context['col']=pickup
            context['total']=total_collected['total_weight'] or 0.0
        return context
    
    
    def post(self, request, *args, **kwargs):
        strt_date = request.POST['strt_date']
        end_date = request.POST['end_date']
        host = CollectionHistory.objects.filter(pid__pdate__gte=strt_date,pid__pdate__lte=end_date)
        total_collected = CollectionHistory.objects.filter(pid__pdate__gte=strt_date,pid__pdate__lte=end_date).aggregate(total_weight=Sum('weight'))
        return render(request, 'admin/collectionhis.html', {'col':host,'total':total_collected['total_weight']})
    
class ViewCollectionCollector(TemplateView):
    template_name="admin/collectionhis_cl.html"
    def get_context_data(self, **kwargs):
        context= super(ViewCollectionCollector,self).get_context_data(**kwargs)
        obj=CollectionHistory.objects.filter(pid__collector=self.request.GET['cid'])
        context['col']=obj
        total_collected = CollectionHistory.objects.filter(pid__collector=self.request.GET['cid']).aggregate(total_weight=Sum('weight'))
        context['total']=total_collected['total_weight']
        return context
    
    def post(self, request, *args, **kwargs):
        strt_date = request.POST['strt_date']
        end_date = request.POST['end_date']
        host = CollectionHistory.objects.filter(pid__collector=self.request.GET['cid'],pid__pdate__gte=strt_date,pid__pdate__lte=end_date)
        total_collected = CollectionHistory.objects.filter(pid__collector=self.request.GET['cid'],pid__pdate__gte=strt_date,pid__pdate__lte=end_date).aggregate(total_weight=Sum('weight'))
        return render(request, 'admin/collectionhis.html', {'col':host,'total':total_collected['total_weight']})
    

class ViewComplaints(TemplateView):
    template_name="admin/viewcomplaints.html"
    def get_context_data(self, **kwargs):
        context= super(ViewComplaints,self).get_context_data(**kwargs)
        comp=Comaplaints.objects.all()
        context['comp']=comp
        return context
    
class ComplaintSolved(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        id=self.request.GET['id']
        comp=Comaplaints.objects.get(id=id)
        comp.status="Solved"
        comp.sdate=timezone.now()
        comp.save()
        message = 'Complaint  Updated'
        messages.success(request, message)
        return redirect('/admin')




class PinCodeInsertView(TemplateView):
    template_name = 'admin/insert_pincode.html'

    def post(self, request, *args, **kwargs):
        pincode = request.POST.get('pincode')
        locations.objects.create(pincode=pincode)
        message = 'Pin Code Inserted'
        messages.success(request, message)
        return redirect('ViewLocations')

class PinCodeListView(TemplateView):
    template_name = 'admin/view_pincode.html'

    def get_context_data(self, **kwargs):
        context = super(PinCodeListView,self).get_context_data(**kwargs)
        context['pincode_list'] = locations.objects.all()
        return context
    
class RemovePinCodeView(TemplateView):
     def dispatch(self, request, *args, **kwargs):
        pincode_id =self.request.GET['id']
        pincode = locations.objects.get(id=pincode_id)
        pincode.delete()
        messages.success(self.request, 'Pin Code removed successfully.')
        return redirect('ViewLocations')

class CollectorList(TemplateView):
    template_name="admin/collector_list.html"
    def get_context_data(self, **kwargs):
        context=super(CollectorList,self).get_context_data(**kwargs)
        context['collector']=collector_Registration.objects.all()
        return context
    
   
class pickup_request(TemplateView):
    template_name='admin/pickup_request.html'
    def get_context_data(self, **kwargs):
        context= super(pickup_request,self).get_context_data(**kwargs)
        pickup=waste_pickup.objects.order_by("-rdate").all()
        context['pickup']=pickup
        return context
    
    def post(self, request, *args, **kwargs):
        strt_date = request.POST['strt_date']
        end_date = request.POST['end_date']
        pickups = waste_pickup.objects.filter(pdate__gte=strt_date, pdate__lte=end_date)
        return render(request, 'admin/pickup_request.html', {'pickup':pickups})
    

class userview(TemplateView):
    template_name='admin/user_list.html'
    def get_context_data(self, **kwargs):
        context= super(userview,self).get_context_data(**kwargs)
        user=user_Registration.objects.all()
        context['user']=user
        return context
        
