
# from django.shortcuts import render
#from models import UserProfile
from django.shortcuts import render, redirect
from .forms import UserForm
import os
# from ..djandoapp_2.settings import *
from djandoapp_2.settings import *

def hello(request):
    return render(request, 'index.html')


# Create your views here.



def user_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()  # データベースに保存
            return redirect('success')  # 成功した場合のリダイレクト先
    else:
        form = UserForm()  # GETリクエストの場合、新しいフォームを表示
    return render(request, os.path.join(BASE_DIR, 'second_app/templates/form.html'), {'form': form})

def success_view(request):
    return render(request,  os.path.join(BASE_DIR, 'second_app/templates/success.html'))

# from django.shortcuts import render
from django.views.generic import View

import payjp


# Create your views here.
class PayView(View):
    """
    use PAY.JP API
    """

    def get(self, request):
        # 公開鍵を渡す
        return render(
            request, "pay.html", {"public_key": "pk_test_37c92ccc8f151318b795683c"}
        )

    def post(self, request):
        amount = request.POST.get("amount")
        payjp_token = request.POST.get("payjp-token")

        # トークンから顧客情報を生成
        customer = payjp.Customer.create(email="koriny33@gmail.com", card=payjp_token)
        # 支払いを行う
        charge = payjp.Charge.create(
            amount=amount,
            currency="jpy",
            customer=customer.id,
            description="Django example charge",
        )

        context = {"amount": amount, "customer": customer, "charge": charge}
        return render(request, "pay.html", context)
