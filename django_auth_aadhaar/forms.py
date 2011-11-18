from django import forms

class AadhaarAuthForm(forms.Form):
    aadhaar_id = forms.CharField(max_length=12, 
                                 label="Aadhaar Number")
    aadhaar_auth_type = forms.ChoiceField(choices=(('Pi', 'Name'),
                                                   ('Pa', 'Address')))
    aadhaar_name = forms.CharField(max_length=120, label="Name", required=False)
    aadhaar_address = forms.CharField(max_length=120, label="Address", required=False)
    
