from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import requests
import json
from django.shortcuts import get_object_or_404
from .models import Payment,Subscription,OTP
from Quiz.models import Quiz
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random,string
# Create your views here.
def generate_otp():
    # otp = ''.join(random.choices(string.digits, k=6))
    # return otp
    while True:
        otp = ''.join(random.choices(string.digits, k=6))
        if not OTP.objects.filter(otp=otp).exists():
            return otp
base_url='https://payments.paypack.rw/api'
def Authenticate():
  

    url = f"{base_url}/auth/agents/authorize"

    payload = json.dumps({
    "client_id": "65d44ab6-24cd-11ef-82a6-deade826d28d",
    "client_secret": "3d165349ce84512f0adb79f4dc42fbd9da39a3ee5e6b4b0d3255bfef95601890afd80709"
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response
class PaymentView(View):

    @method_decorator(csrf_exempt)
    # @method_decorator(login_required(login_url='/account/'))
    def post(self, request):
        # print(request.POST)
        exam_id = request.POST.get('exam_id')
        amount = self.get_amount(request.POST.get('subsciption_type'))
        Subscription_type=request.POST.get('subsciption_type')
        phone = request.POST.get('Phone_number')
        # print(self.authenticate())
        payment_auth=Authenticate()
        
        if payment_auth.status_code == 200:
            otp=generate_otp()
            
            make_payment=self.make_payment_request(amount,phone,payment_auth.json().get('access'))
            print(make_payment.json())
            if make_payment.status_code == 200:
                print(f'{make_payment.json()} message')
                otp_save=OTP.objects.create(otp=otp,valid=False)
                if exam_id:
                    exam=get_object_or_404(Quiz,pk=exam_id)
                    
                   
                    # 
                    # print("otp_save")
                    if otp_save and request.user.is_authenticated:

                        save_payment=Payment.objects.create(user=request.user,otp=otp_save,ref=make_payment.json().get('ref'))
                    else:
                        save_payment=Payment.objects.create( otp=otp_save,ref=make_payment.json().get('ref'))    
                else:    
                    if request.user.is_authenticated:
                        save_payment=Payment.objects.create(user=request.user,otp=otp_save, ref=make_payment.json().get('ref'),type=Subscription_type)
                    else:    
                        save_payment=Payment.objects.create(otp=otp_save,ref=make_payment.json().get('ref'),type=Subscription_type)    
                if save_payment:
                    return JsonResponse({"status": "success","ref":make_payment.json().get('ref'),"phone":phone,"otp":otp_save.otp}, status=200)
                return JsonResponse({"status": "error", "message":"Failed to save payment"},status=200)
            # print(make_payment.json())
            return JsonResponse({"status": "error","user_message":"Please check your balance and your internet"}, status=200)
            
        
        return JsonResponse({"message": "failed to authenticate","status":"error"}, status=200)

    def get_amount(self, subscription_type):
        if subscription_type == "one":
            return 500
        elif subscription_type == "day":
            return 5000
        elif subscription_type == "week":
            return 10000
        elif subscription_type == "month":
            return 20000
        return None

    # def get_exam(self, exam_id):
    #     try:
    #         return Quiz.objects.get(id=exam_id)
    #     except Quiz.DoesNotExist:
    #         return None

    def authenticate(self):
        url = f"{base_url}/auth/agents/authorize"
        payload = {
            "client_id": "65d44ab6-24cd-11ef-82a6-deade826d28d",
            "client_secret": "3d165349ce84512f0adb79f4dc42fbd9da39a3ee5e6b4b0d3255bfef95601890afd80709"
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        response= requests.request("POST",url, json=payload, headers=headers)
        return response

    def make_payment_request(self, amount, phone, access_token):
        
        url = f"{base_url}/transactions/cashin"
        payload =json.dumps({
            "amount": amount,
            "number":phone
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
            "X-Webhook-Mode":"development"
        }
        # url="https://payments.paypack.rw/api/transactions/cashin"
        response = requests.request("POST", url, headers=headers, data=payload)

        return response

    def handle_authentication_error(self, payment_auth):
        error_data = {
            "error": "Failed to authenticate",
            "status_code": payment_auth.status_code,
            "response": payment_auth.content
        }
        return JsonResponse(error_data, status=payment_auth.status_code)   
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
                    Otp=OTP.objects.get(otp=otp)
                    Otp.valid=True
                    Otp.save()
                    payment=Payment.objects.get(ref=referenceKey,otp=Otp)
                
                    payment.valid=True
                    payment.save()
                    return JsonResponse({"status": "success","otp":Otp.otp}, status=200)
                except OTP.DoesNotExist:
                        return JsonResponse({"status": "failed"}, status=200)
                except Payment.DoesNotExist:
                    return JsonResponse({"status": "failed"}, status=200)
        return JsonResponse({"success": response.json()})
def Webhook(request):
    if request.method == "POST":
        print(request.POST)
        return JsonResponse({"success": "success"}, status=200)
    return JsonResponse({"success": "failed"}, status=200)