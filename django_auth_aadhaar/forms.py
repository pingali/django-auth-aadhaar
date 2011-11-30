from django import forms

class AadhaarAuthForm(forms.Form):
    GENDER_CHOICES=(
        ('M', 'Male'), 
        ('F', 'Female'),
        ('T', 'Transgender'))
    ATTRIBUTE_CHOICES=(
        ("aadhaar_name", "Name"),
        ("aadhaar_dob", "Date of Birth"),
        ("aadhaar_email", "Email")
        )
    aadhaar_id = forms.CharField(max_length=12, 
                                 label="Aadhaar Number",
                                 help_text="12 digit Aadhaar number")
    aadhaar_attributes = \
        forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
                                  label="Authentication Parameters",
                                  choices=ATTRIBUTE_CHOICES,
                                  help_text="Please select one or more of attributes you wish to authenticate"
                                           )
    aadhaar_name = forms.CharField(max_length=120, label="Name",
                                   required=False)
    aadhaar_gender = forms.ChoiceField(choices=GENDER_CHOICES,
                                       label="Gender",
                                       required=False)
    aadhaar_dob = forms.DateField(label="DoB", 
                                  required=False,
                                  #help_text="Date of Birth (format: YYYY or YYYY-MM-DD)",
                                  input_formats=['%Y', '%Y-%m-%d'])
    aadhaar_email = forms.EmailField(max_length=64, label="Email", 
                                     required=False)
    aadhaar_landmark = forms.CharField(max_length=120, label="Landmark", 
                                       default="", required=False)
    aadhaar_street = forms.CharField(max_length=120, label="Street", 
                                     default="",   required=False)
    aadhaar_locality = forms.CharField(max_length=120, label="Locality", 
                                     default="",   required=False)
    aadhaar_vtc = forms.CharField(max_length=40, label="VTC", 
                                     default="",   required=False)
    aadhaar_subdist = forms.CharField(max_length=40, label="Sub-District", 
                                     default="",   required=False)    
    aadhaar_district= forms.CharField(max_length=40, label="District", 
                                     default="",   required=False)    
    aadhaar_state = forms.CharField(max_length=140, label="State", 
                                     default="",   required=False)
    aadhaar_pincode = forms.IntegerField(max_length=6, label="State", 
                                     default=0,   required=False)
    
    def clean_aadhaar_pincode(self): 
        pincode = self.cleaned_data['aadhaar_pincode']
        if ((pincode != 0) and (pincode < 100000)):
            raise forms.ValidationError("Pincode, if specified, " + 
                                        "should be > 100000")
