from typing import Any, Dict
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import auth,User 
from django.contrib.auth import login
from django.http import JsonResponse
from waste.models import user_Registration,userType,products,locations
from django.contrib import messages

class indexview(TemplateView):
    template_name="home.html"
    def get_context_data(self, **kwargs):
        context=super(indexview,self).get_context_data(**kwargs)
        context['product']=products.objects.all()
        return context
    
class login_view(TemplateView):
    template_name="login.html"
    def post(self,request,*args,**kwargs):
        username=request.POST['username']
        print(username)
        password =request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not  None:
            login(request,user)
            if user.last_name=='1' :
                request.session['id']=user.id
                request.session.save()
                if user.is_superuser:
                    return redirect('/admin')
                elif userType.objects.get(user_id=user.id).type=="collector":
                    request.session['cid']=user.id
                    request.session.save()
                    return redirect('/collector')
                elif userType.objects.get(user_id=user.id).type == "user":
                   return redirect('/user')
                else:
                    request.session['id']=user.id
                    request.session.save()
                    return redirect('/user')

            else:
                request.session['id']=user.id
                request.session.save()
                return redirect('/user')
        else:
            return render(request,'login.html',{'message':"Invalid Username or Password"})
        
class userRegistration(TemplateView):
    template_name = 'register.html'
    
    def post(self, request, *args, **kwargs):
        fullname = request.POST['name']
        address = request.POST['address']
        
        email = request.POST['email']
        phone = request.POST['phone']
        pincode = request.POST['pincode']
        password = request.POST['password']

        reg = user_Registration()

        reg.name=fullname
        reg.email=email
        reg.password=password
        reg.address = address       
        reg.mobile = phone
        reg.pincode = pincode
        try:
            if "checkbox" in request.POST:
                user = User.objects.create_user(username=email, password=password, first_name=fullname, email=email,last_name=0)
                user.save()
                reg.user = user
                reg.save()
                usertype = userType()
                usertype.user = user
                usertype.type = 'user'
                usertype.save()
                message = "Register Successfully."
                return render(request, 'login.html', {'message': message}) 
            
            else:
                user = User.objects.create_user(username=email, password=password, first_name=fullname, email=email,last_name=4)
                user.save()
                reg.user = user
                reg.save()
                usertype = userType()
                usertype.user = user
                usertype.type = 'user'
                usertype.save()
                message = "Register Successfully."
                return render(request, 'login.html', {'message': message}) 
            
        except Exception as a:
            messages = "Username already used!.."
            return render(request, 'home.html', {'message': messages})   


class shop(TemplateView):
    template_name='shop-guest.html'
    def get_context_data(self, **kwargs):
        context=super(shop,self).get_context_data(**kwargs)
        prod=products.objects.filter(status='1')
        context['prod']=prod
        return context
    
class view_product(TemplateView):
    template_name='product-guest.html'
    def get_context_data(self,**kwargs):
        context=super(view_product,self).get_context_data(**kwargs)
        pid=self.request.GET['id']
        pd=products.objects.get(id=pid)
        uid=self.request.session.get('id')
        #print("UserId :",uid)
        user=user_Registration.objects.get(user_id=uid)                                                                        
        context['user']=user
        context['pd']=pd
        return context
    
def check_pincode_view(request):
    if request.method == 'GET':
        pincode = request.GET.get('pincode', '')
        exists = locations.objects.filter(pincode=pincode).exists()
        return JsonResponse({'exists': exists})
    
class view_product(TemplateView):
    template_name='product.html'
    def get_context_data(self,**kwargs):
        context=super(view_product,self).get_context_data(**kwargs)
        pid=self.request.GET['id']
        pd=products.objects.get(id=pid)
        context['pd']=pd
        return context
        
from django.views import View
class CheckPincodeView(View):
    def get(self, request):
        pincode = request.GET.get('pincode')
        
        # Replace this with your actual pincode validation logic
        valid_pincodes = locations.objects.all()
        for i in valid_pincodes:
            if pincode == i.pincode:
                message = 'Valid pincode'
                print( i.pincode)
                return JsonResponse({'message': message})
            else:
                print( i.pincode)
                message = 'Invalid pincode'
        
        return JsonResponse({'message': message})
class Check(TemplateView):
    template_name="chech.html"