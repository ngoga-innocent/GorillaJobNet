from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import requests
import json
from.models import Payment,Subscription
from Quiz.models import Quiz
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

base_url='https://payments.paypack.rw/api'
def Authenticate():
  

    url = f"{base_url}/auth/agents/authorize"

    payload = json.dumps({
    "client_id": "c9c2d000-22b7-11ef-bfa1-deade826d28d",
    "client_secret": "7c1afe90ce4704c0578f4470e3490e1eda39a3ee5e6b4b0d3255bfef95601890afd80709"
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response
class PaymentView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(login_required(login_url='/account/'))
    def post(self, request):
        user = request.user
        exam_id = request.POST.get('exam')
        amount = self.get_amount(request.POST.get('subsciption_type'))
        Subscription_type=request.POST.get('subsciption_type')
        phone = request.POST.get('phone_number')
        # print(self.authenticate())
        payment_auth=self.authenticate()
        
        if payment_auth.status_code == 200:
            make_payment=self.make_payment_request(amount,phone,payment_auth.json().get('access'))
            print(make_payment.json())
            if make_payment.status_code == 200:
                save_payment=Payment.objects.create(user=request.user, ref=make_payment.json().get('ref'))
                if save_payment:
                    return JsonResponse({"status": "success","ref":make_payment.json().get('ref')}, status=200)
                return JsonResponse({"status": "error", "message":"Failed to create payment"},status=200)
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
            "client_id": "c9c2d000-22b7-11ef-bfa1-deade826d28d",
            "client_secret": "7c1afe90ce4704c0578f4470e3490e1eda39a3ee5e6b4b0d3255bfef95601890afd80709"
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        response= requests.request("POST",url, json=payload, headers=headers)
        return response

    def make_payment_request(self, amount, phone, access_token):
        print(access_token)
        url = f"{base_url}/transactions/cashin"
        payload =json.dumps({
            "amount": 100,
            "number": '0782214360'
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
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
def CheckPaymentStatus(referenceKey,access_token,client):
    #payment_auth = Authenticate()
    referenceKey = referenceKey
    access_token = access_token
    client=client
    url =url = f"https://payments.paypack.rw/api/events/transactions?ref={referenceKey}&kind=CASHIN&client={client}"
    payload={}
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.request("GET", url, headers=headers, data=payload)
    return JsonResponse({"success": response.json()})
     