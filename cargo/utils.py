from eskiz_sms import EskizSMS



def send_verify_code(phone_number, code):
    context = f"Tasdidlash kodi: {code}"
    eskiz = EskizSMS('sbexruz2001@gmail.com', 'OJtu8eDGlmgkJgooTnpOdGeBHdQi1r2O1OcEBpwp')
    eskiz.send_sms(phone_number, context)

def send_reset_password(phone_number, code):
    context = f"Tizimga kirish uchun Doimiy Parolingiz: {code}"
    eskiz = EskizSMS('sbexruz2001@gmail.com', 'OJtu8eDGlmgkJgooTnpOdGeBHdQi1r2O1OcEBpwp')
    eskiz.send_sms(phone_number, context)

def hide_phone_number_nums(phone_number):
    return phone_number[:4] + '*'*5 + phone_number[9:]


