from alipay import AliPay

def get_alipay_client():
    with open("../nursing_home_backend/keys/app_private_key.pem") as f:
        app_private_key = f.read()
    with open("../nursing_home_backend/keys/app_public_key.pem") as f:
        alipay_public_key = f.read()

    alipay = AliPay(
        appid="9021000133613194",
        app_notify_url="https://82ef-2001-250-4003-4-00-a5ac.ngrok-free.app/api/alipay/notify/",  # 异步通知URL
        app_private_key_string=app_private_key,
        alipay_public_key_string=alipay_public_key,
        sign_type="RSA2",
        debug=True  # True 表示沙箱环境
    )
    return alipay