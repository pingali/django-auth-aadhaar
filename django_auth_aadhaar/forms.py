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
    aadhaar_street = forms.CharField(max_length=120, label="Street", 
                                     required=False)
    
