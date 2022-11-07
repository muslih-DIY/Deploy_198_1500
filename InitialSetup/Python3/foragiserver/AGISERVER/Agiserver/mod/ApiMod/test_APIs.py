import pytest
from .APIs import *

@pytest.mark.skip
@pytest.mark.parametrize("number,flag,msg",[('123','N','mobile is not valid'),('9188334706','N','mobile not start with 0'),('09188334706','Y','mobile start with 0..')])
def test_sendotp(number,flag,msg):
    sendotp = SendOtp()
    response = sendotp.arginput_call_clean_map([number])
    assert response.get('OTP_Flag',None)==flag,msg

@pytest.mark.skip
@pytest.mark.parametrize("id,otp,flag,msg",[('123','12','N','random otpid and otp'),])
def test_validate(id,otp,flag,msg):
    validate = ValidateOtp()
    response = validate.arginput_call_clean_map([id,otp])
    assert response.get('V_Flag',None)==flag,msg
    print(response)

@pytest.mark.skip
@pytest.mark.parametrize("PHONE_NO,NewMN,flag",[('020-00000051','09188334706','901'),])
def test_UpdateRmn(PHONE_NO,NewMN,flag):
    sendotp = SendOtp()
    response = sendotp.arginput_call_clean_map([NewMN])
    print(response)
    assert response.get('OTP_Flag',None)=='Y'
    OTPId=response.get('OtpId')

    updatermn = UpdateRmn()
    OTPCode = input('enter  otp :')

    response = updatermn.arginput_call_clean_map([PHONE_NO,OTPId,OTPCode,NewMN])
    print(response)
    assert response.get('URMN_Flag',None)==flag
    

@pytest.mark.skip
def test_sendotpvalidate(number='09188334706'):
    sendotp = SendOtp()
    response = sendotp.arginput_call_clean_map([number])
    assert response.get('OTP_Flag',None)=='Y'
    id=response.get('OtpId')
    validate = ValidateOtp()
    otp = input('enter  otp :')
    response = validate.arginput_call_clean_map([id,otp])
    assert response.get('V_Flag',None)=='Y'




@pytest.mark.skip
@pytest.mark.parametrize("number,orderstate",[('020-42352079','R'),('020-42352079','U'),('020-42352079','')])
def test_Get_appeal_docket(number,orderstate):
    get_docket = Get_Appeal_docket()
    print(get_docket.arginput_call_clean_map([number,orderstate]))

@pytest.mark.skip
#@pytest.mark.parametrize()
def test_BookAppeal():
    appeal = BookAppeal()
    response = appeal.arginput_call_clean_map(['020-42352098',"102042","08542044038"])
    print(response)

@pytest.mark.skip
@pytest.mark.parametrize("number",[('07183-299029'),('020-42352079'),('020-42352098'),('020-00000051')])
def test_BillApi(number):
    Bill = BillApi(debug=debug)
    print(Bill.generate_input_dict([number]))
    response =Bill.arginput_call_clean_map([number])
    print(response)

@pytest.mark.skip
def test_ttstatus():
    api = TTstatus()
    print(api.arginput_call_clean_map(['020-42352079','101415']))

@pytest.mark.skip
def test_complaint_book():
    api = ComplaintBook()
    print(api.arginput_call_clean_map(['02160-299025','ZZ','91883347066']))

@pytest.mark.skip
def test_check_vip():
    api = CheckVip()
    print(api.arginput_call_clean_map(['020-42352079']))

@pytest.mark.skip
def test_changed_no():
    api = ChdNoApi()
    print(api.arginput_call_clean_map(['020-42352079']))

#@pytest.mark.skip
def test_getrmn():
    api = GetRmn()
    print(api.arginput_call_clean_map(['02169-298491']))


