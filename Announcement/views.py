from django.shortcuts import render,redirect
from django.views import View
from .announcement_form import AnnouncementForm
from .models import Announcement,AnnouncementCategory,Paid_Announcencer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
from Payment.views import make_payment_function,Authenticate
import requests
import random
import string
from Payment.models import Payment,OTP
from django.utils import timezone
import datetime
# Create your views here.
def generate_otp():
    # otp = ''.join(random.choices(string.digits, k=6))
    # return otp
    while True:
        otp = ''.join(random.choices(string.digits, k=6))
        if not Paid_Announcencer.objects.filter(otp=otp).exists():
            return otp
base_url='https://payments.paypack.rw/api'
class AnnouncementView(View):
    def get(self, request, id=None):
        form = AnnouncementForm()
        categories = AnnouncementCategory.objects.all()

        if id is not None:
            category=AnnouncementCategory.objects.get(id=id)
            announcements = Announcement.objects.filter(category=category,deadline__gte=datetime.datetime.now()).order_by('-created_at')[:1000]
            html = render_to_string('announcement_partial.html', {'announcements': announcements})
            return JsonResponse({'html': html})
        
        announcements = Announcement.objects.filter(deadline__gte=datetime.datetime.now()).order_by('-created_at')[:1000]
        context = {'form': form, 'announcements': announcements, 'ann_categories': categories}
        return render(request, 'announcements.html', context)
    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            user =request.user
            chek_valid=Paid_Announcencer.objects.filter(announcer=user,valid=True).exists()
            if chek_valid:
                form.save(user=request.user)
                find_otp=Paid_Announcencer.objects.filter(announcer=user,valid=True).first()
                find_otp.valid=False
                find_otp.save() 
                       

            else:    
                pass
            categories = AnnouncementCategory.objects.all()
            announcements = Announcement.objects.all().order_by('-created_at')[:1000]
            context = {'form': form, 'announcements': announcements, 'ann_categories': categories}
            return redirect('/announcements')
            
        else:
            categories = AnnouncementCategory.objects.all()
            announcements = Announcement.objects.all().order_by('-created_at')[:1000]
            context = {'form': form, 'announcements': announcements, 'ann_categories': categories}
            return render(request, 'announcements.html', context)
def get_announcement_detail( request, announcement_id):
        try:
            current_session_key = request.session.session_key
            previous_session_key = request.session.get('previous_session_key', None)
            
            announcement = Announcement.objects.get(id=announcement_id)
            current_url = request.build_absolute_uri()
            # announcement.views += 1
            related_announcements = Announcement.objects.filter(category=announcement.category).exclude(id=announcement.id).order_by('-created_at')[:10]
            context = {'announcement': announcement,'related_announcements': related_announcements,'url': current_url}
            return render(request, 'announcement_detail.html', context)
        except Announcement.DoesNotExist:
            return JsonResponse({'error': 'Announcement not found'}, status=404)        
def search_announcement(request,text=None):
    if text is not None:
        announcements = Announcement.objects.filter(title__icontains=text).order_by('-created_at')|Announcement.objects.filter(company_name__icontains=text).order_by('-created_at')
    else:
        announcements = Announcement.objects.all().order_by('-created_at')[:1000]    
    
    html = render_to_string('announcement_partial.html', {'announcements': announcements})
    return JsonResponse({'html': html})
@login_required
def CheckUserAnnouncement(request):
    user=request.user
    print(user)
    if request.user.is_authenticated:
        paid_ann=Paid_Announcencer.objects.filter(announcer=user,valid=True)
        if paid_ann.count()>0:
            return JsonResponse({"paid":True},status=200)
        else: return JsonResponse({"paid":False},status=200)
    else:
        return redirect('login')    
@login_required
def payAnnouncement(request):
    phone=request.POST.get('phone')
    user=request.user
    token=Authenticate()
    access_token=token.json()
    # print(access_token.get('access'))
    pay=make_payment_function(55000,phone,access_token.get('access'))
    if pay.status_code == 200:
        otp=generate_otp()
        save_payment=Paid_Announcencer.objects.create(announcer=user,otp=otp)
        
        return JsonResponse({"refrenceKey":pay.json().get('ref'),"phone":phone,'otp':otp},status=200)
    return JsonResponse({"token":'failed To Initiate Payment'},status=200)
def CheckPaymentStatus(request):
    if request.method == "GET":
        payment_auth = Authenticate()
        referenceKey = request.GET.get('ref')
        otp=request.GET.get('otp')
        #referenceKey='af575514-be29-41d2-9d31-40d784ce512e'
        access_token = payment_auth.json().get('access')
        client=request.GET.get('phone')
        # print(otp)
        #client="0782214360"
        url = f"{base_url}/events/transactions?ref={referenceKey}&kind=CASHIN&client={client}"
        payload={}
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.json())
        data=response.json()
        if int(data.get('total',0) )>1:
            status=data.get('transactions')[0].get('data').get('status')
            if status =='failed':
                return JsonResponse({"status": "failed"}, status=200)
            else:
                try:
                    Otp=Paid_Announcencer.objects.get(otp=otp)
                    Otp.valid=True
                    Otp.save()
                    return JsonResponse({"success": True}, status=200)
                except OTP.DoesNotExist:
                    return JsonResponse({"status": "Invalid OTP"}, status=200)
        return JsonResponse({"success": response.json()})
def CheckOtp(request):
    otp=request.POST.get('otp')
    print(otp)
    try:
        Otp=Paid_Announcencer.objects.get(otp=otp)
        print(Otp)
        return JsonResponse({"valid": Otp.valid}, status=200)
    except Paid_Announcencer.DoesNotExist:
        return JsonResponse({"valid": False}, status=200)