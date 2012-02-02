from django import forms

class AadhaarAuthForm(forms.Form):

    PII_ATTRIBUTES=(
        ('aadhaar_pi_match', "PII Match Strategy"),
        ("aadhaar_name", "Name"),
        ('aadhaar_dob', "Date of Birth"),
        ('aadhaar_age', "Age"),
        ('aadhaar_gender',"Gender"), 
        ('aadhaar_email', "Email"),
        ('aadhaar_phone', "Phone"),
        )
    PA_ATTRIBUTES=(
        ('aadhaar_pa_match', "PA Match Strategy"),
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

    def __init__(self, *args, **kwargs):
        print "AadhaarAuthForm detail = "
        print "kwargs = ", kwargs
        print "args = ", args 
        try: 
            detail = kwargs.pop('detail', None)
            if (detail not in ['personal', 'address', 'all']):
                raise Exception("Invalid detail")
        except:
            raise forms.ValidationError("Invalid form detail requested")

        super(AadhaarAuthForm, self).__init__(*args, **kwargs)

        self.detail = detail

        if detail == "personal": 
            ATTRIBUTE_CHOICES = AadhaarAuthForm.PII_ATTRIBUTES[1:]
        elif detail == "address":
            ATTRIBUTE_CHOICES = AadhaarAuthForm.PA_ATTRIBUTES[1:]
        else:
            ATTRIBUTE_CHOICES = AadhaarAuthForm.PII_ATTRIBUTES[1:] + AadhaarAuthForm.PA_ATTRIBUTES[1:]

        self.fields['aadhaar_attributes'] = \
            forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
                                  label="Authentication Parameters",
                                  choices=ATTRIBUTE_CHOICES,
                                  help_text="Please select one or more of attributes you wish to authenticate",
                                  required=True)
    
    aadhaar_id = forms.CharField(max_length=12, 
                                 label="Aadhaar Number",
                                 help_text="12 digit Aadhaar number")

    # Personally identifiable information
    PI_MATCH_CHOICES =(
        ('E', 'Exact'), 
        ('P', 'Partial')
        )
    GENDER_CHOICES=(
        ('M', 'Male'), 
        ('F', 'Female'),
        ('T', 'Transgender'))
    aadhaar_pi_match = forms.ChoiceField(choices=PI_MATCH_CHOICES,
                                         label="PII Match Strategy",
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
    aadhaar_age = forms.IntegerField(label="Age", 
                                     required=False)
    aadhaar_email = forms.EmailField(max_length=64, label="Email", 
                                     required=False)
    aadhaar_phone = forms.IntegerField(label="Phone", 
                                     required=False)
    
    # => Address 
    #<Pa ms="E" co="" house="" street="" lm="" loc=""
    # vtc="" subdist="" dist="" state="" pc="" po=""/>
    PA_MATCH_CHOICES =(
        ('E', 'Exact'), 
        )
    aadhaar_pa_match = forms.ChoiceField(choices=PA_MATCH_CHOICES,
                                         label="Address Match Strategy",
                                         required=False)
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
    aadhaar_pincode = forms.IntegerField(label="Pincode", 
                                     required=False)
    aadhaar_postoffice = forms.CharField(max_length=40, label="PostOffice", 
                                         required=False)
    
    @staticmethod 
    def humanize(attr_name): 
        """
        Get the label for an attribute name
        """
        for e in AadhaarAuthForm.PII_ATTRIBUTES + AadhaarAuthForm.PA_ATTRIBUTES:
            if e[0] == attr_name: 
                return e[1] 
        return None 

    def clean(self):
        
        if not self.cleaned_data.has_key('aadhaar_attributes'):
            raise forms.ValidationError("Please select one or more attributes")
        
        attributes = self.cleaned_data['aadhaar_attributes']
        print "Attributes selected = ", attributes
        for attr_name in attributes: 
            if not self.cleaned_data.has_key(attr_name):
                raise forms.ValidationError("Please enter valid data for %s " % attr_name)

        if 'aadhaar_pincode' in attributes: 
            pincode = self.cleaned_data['aadhaar_pincode']
            if ((pincode != 0) and (pincode < 100000)):
                raise forms.ValidationError("Pincode, if specified, " + 
                                            "should be > 100000")

        if 'aadhaar_age' in attributes: 
            age= self.cleaned_data['aadhaar_age']
            if ((age == 0) or ( age > 110)):
                raise forms.ValidationError("Invalid age specified")
            
        # Make sure match strategies are included. 
        match_strategies = [] 
        valid_pi_attributes = [x[0] for x in AadhaarAuthForm.PII_ATTRIBUTES]
        valid_pa_attributes = [x[0] for x in AadhaarAuthForm.PA_ATTRIBUTES]
        for attribute in attributes:
            if ((attribute in valid_pi_attributes) and 
                ('aadhaar_pi_match' not in match_strategies)):
                match_strategies += ['aadhaar_pi_match'] 

            if ((attribute in valid_pa_attributes) and 
                ('aadhaar_pa_match' not in match_strategies)):
                match_strategies += ['aadhaar_pa_match'] 

        print "match strategies = ", match_strategies 
        attributes += match_strategies 
        print "after adding match_strategies ", attributes 
        for attribute in attributes:
            humanized_attribute = AadhaarAuthForm.humanize(attribute) 
            if ((not self.cleaned_data.has_key(attribute)) or 
                (self.cleaned_data[attribute] == "")):
                raise forms.ValidationError("Attribute '%s' not specified or incorrect" % humanized_attribute)

        return self.cleaned_data 
