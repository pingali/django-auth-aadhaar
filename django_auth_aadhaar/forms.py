from django import forms

class AadhaarAuthForm(forms.Form):
    
    # Required fields. 
    ATTRIBUTE_CHOICES=(
        ("aadhaar_name", "Name"),
        ('aadhaar_dob', "Date of Birth"),
        ('aadhaar_gender',"Gender"), 
        ('aadhaar_email', "Email"),
        ('aadhaar_phone', "Phone"),
        ('aadhaar_co', "Care of"),
        ('aadhaar_house', "House"),
        ('aadhaar_street', "Street"), 
        ('aadhaar_landmark', "Landmark"), 
        ('aadhaar_locality', "Locality"), 
        ('aadhaar_vtc', "VTC"),
        ('aadhaar_subdist', "Sub-District"), 
        ('aadhaar_district', "District"),
        ('aadhaar_state', "State"),
        ('aadhaar_pincode', "Pincode"),
        ('aadhaar_postoffice', "Post Office"),
        )
    aadhaar_id = forms.CharField(max_length=12, 
                                 label="Aadhaar Number",
                                 help_text="12 digit Aadhaar number")
    aadhaar_attributes = \
        forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
                                  label="Authentication Parameters",
                                  choices=ATTRIBUTE_CHOICES,
                                  help_text="Please select one or more of attributes you wish to authenticate")

    # Personally identifiable information
    PI_MATCH_CHOICES =(
        ('E', 'Exact'), 
        ('P', 'Partial')
        )
    GENDER_CHOICES=(
        ('M', 'Male'), 
        ('F', 'Female'),
        ('T', 'Transgender'))
    aadhaar_match = forms.ChoiceField(choices=PI_MATCH_CHOICES,
                                      label="Match",
                                      required=False)
    aadhaar_name = forms.CharField(max_length=120, label="Name",
                                   required=False)
    aadhaar_gender = forms.ChoiceField(choices=GENDER_CHOICES,
                                       label="Gender",
                                       required=False)
    aadhaar_dob = forms.DateField(label="DoB", 
                                  required=False,
                                  help_text="Date of Birth (format: YYYY or YYYY-MM-DD)",
                                  input_formats=['%Y', '%Y-%m-%d'])
    aadhaar_email = forms.EmailField(max_length=64, label="Email", 
                                     required=False)
    aadhaar_phone = forms.IntegerField(label="Phone", 
                                     required=False)
    
    # => Address 
    #<Pa ms="E" co="" house="" street="" lm="" loc=""
    # vtc="" subdist="" dist="" state="" pc="" po=""/>
    aadhaar_co = forms.CharField(max_length=120, label="Careof", 
                                 required=False)
    aadhaar_house = forms.CharField(max_length=120, label="House", 
                                    required=False)
    aadhaar_street = forms.CharField(max_length=120, label="Street", 
                                     required=False)
    aadhaar_landmark = forms.CharField(max_length=120, label="Landmark", 
                                       required=False)
    aadhaar_locality = forms.CharField(max_length=120, label="Locality", 
                                       required=False)
    aadhaar_vtc = forms.CharField(max_length=40, label="VTC", 
                                  required=False)
    aadhaar_subdist = forms.CharField(max_length=40, label="Sub-District", 
                                      required=False)    
    aadhaar_district= forms.CharField(max_length=40, label="District", 
                                      required=False)    
    aadhaar_state = forms.CharField(max_length=140, label="State", 
                                    required=False)
    aadhaar_pincode = forms.IntegerField(label="State", 
                                     required=False)
    aadhaar_postoffice = forms.CharField(max_length=40, label="PostOffice", 
                                         required=False)
    def clean(self):
        
        attributes = self.cleaned_data['aadhaar_attributes']
        # Do something based on the attribtued 

        pincode = self.cleaned_data['aadhaar_pincode']
        if ((pincode != 0) and (pincode < 100000)):
            raise forms.ValidationError("Pincode, if specified, " + 
                                        "should be > 100000")
