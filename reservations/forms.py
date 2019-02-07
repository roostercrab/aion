from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm

import re
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML

from django.contrib.auth.models import User
from .models import Profile, Resource, TimeBlock, Announcement, Reservation

from .deep_fried_form import DeepFriedForm


class SignUpForm(UserCreationForm):
    '''Extend the UserCreationForm to create a 
    custom signup form
    '''
    
    # Add the email field to the user creation form
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.')
    
    class Meta:
        model = User
        fields = 'username','email', 'password1', 'password2'
    
    def clean_email(self):
        '''Validate teacher email
        '''
        
        email = self.cleaned_data['email']
        domain = re.search("@[\w.]+", email) # must be @worcesterschools.net
        uname = re.search("^student", email) # Must not begin with 'student' (should be None)
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
            
        if(domain.group() == '@worcesterschools.net' and uname is None): 
            return email
        # Invalid. Raise exception
        raise ValidationError("You must register a valid wps teacher email to sign up for this service.")

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms helper and layout objects.
        '''
        super(SignUpForm, self).__init__(*args, **kwargs)
       
        # Create the label for email
        self.fields['email'].label = "Email"
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text='Register',
                cancel_url='/signin/',
                cancel_text='Sign In'
            )
        )
        self.helper.form_show_labels = False # surpress labels


class LogInForm(AuthenticationForm):
    '''Custom Login Form
    '''

    class Meta:
        model = User
        fields = 'username','password'
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(LogInForm, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Sign In",
                cancel_url="/signup/",
                cancel_text="Sign Up"
            )
        )
        self.helper.form_show_labels = False # surpress labels


'''Custom User and Profile Form
'''


class UserForm(forms.ModelForm):
    '''User Form
    '''
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
    
    '''Extend Crispy Forms helper and layout objects.
    '''
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons = False
            )
        )
        self.helper.form_show_labels = False # surpress labels
        self.helper[0:2].wrap_together(Fieldset, '{{ request.user }}')
        self.helper.form_tag=False
        

class ProfileForm(forms.ModelForm):
    '''Profile Form 
    '''
    
    class Meta:
        model = Profile
        fields = ('location', )
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms helper and layout objects.
        '''
        
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Save Profile",
                cancel_url="/home/",
                cancel_text="Cancel"
            )
        )  
        
        self.helper.layout.insert(
            0, # Index of layout items.
            HTML(
                '<small class="helper-text">Choosing a building is required for making reservations.</small>'
            ),
        )
        self.helper.form_tag=False
        self.helper.form_show_labels = False # surpress labels


class EditSchoolAdminForm(forms.ModelForm):
    '''Custom Profile form to edit school admin access
    '''
    class Meta:
        model = Profile 
        fields = ('school_admin',)
    
    def __init__(self, *args, **kwargs):
        '''Extend crispy forms layout objects 
        '''
        super(EditSchoolAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Access",
            )
        )
        self.helper.form_show_labels = False # surpress labels 


class EditTimeBlockForm(forms.ModelForm):
    '''Custom Edit Blocks Form
    for building admins
    '''
    class Meta:
        model = TimeBlock
        fields = ('name','sequence','enabled')
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(EditTimeBlockForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Block",
            )
        )
        
        self.helper.form_show_labels = False # surpress labels 


class DeleteTimeBlockForm(forms.ModelForm):
    '''Custom Delete block Form for building admins
    '''
    class Meta:
        model = TimeBlock
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(DeleteTimeBlockForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons=False,
                render_delete_buttons=True,
            )
        )
        
        self.helper.form_show_labels = False # surpress labels 


# from django.forms import DateField, SelectDateWidget
class NewTimeBlockForm(forms.ModelForm):
    '''Custom Create Block Form  
    for Building Admins
    '''
        
    class Meta:
        model = TimeBlock 
        fields=('name', 'sequence',)

    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects. 
        '''
        super(NewTimeBlockForm, self).__init__(*args, **kwargs)
        # Get the crispy helper
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text='Create New Block',
            )
        )
        self.helper.form_show_labels = False


class DeleteAnnouncementForm(forms.Form):
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(DeleteAnnouncementForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons=False,
                render_delete_buttons=True,
            )
        )
        self.helper.form_show_labels = False # surpress labels
    
    
class NewAnnouncementForm(forms.ModelForm):
    '''Form for building admins to create announcments
    '''
    class Meta:
        model = Announcement
        fields = ('title', 'message', 'publish_on', 'expires_on')
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(NewAnnouncementForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Create Announcement",
            )
        )
        self.helper.form_show_labels = False # surpress labels


class EditAnnouncementForm(forms.ModelForm):
    '''Form for building admins to edit announcments
    '''
    class Meta:
        model = Announcement
        fields = ('title', 'message', 'publish_on', 'expires_on')
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(EditAnnouncementForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Announcement",
            )
        )
        self.helper.form_show_labels = False # surpress labels
        

class AdminNewAnnouncementForm(NewAnnouncementForm):
    class Meta:
        model = Announcement
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(AdminNewAnnouncementForm, self).__init__(*args, **kwargs)
     
        self.helper.form_show_labels = True


class AdminEditAnnouncementForm(EditAnnouncementForm):
    class Meta:
        model = Announcement
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(AdminEditAnnouncementForm, self).__init__(*args, **kwargs)
     
        self.helper.form_show_labels = True
    
        
class NewResourceForm(forms.ModelForm):
    '''Custom Create Resource Form
    for building admins
    '''
    class Meta:
        model = Resource
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(NewResourceForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Create Resource",
            )
        )
        self.helper.form_show_labels = False # surpress labels
        

class EditResourceForm(forms.ModelForm):
    '''Custom Edit Resource Form
    for building admins
    '''
    class Meta:
        model = Resource
        fields = ('name','enabled')
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(EditResourceForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Resource",
            )
        )
        
        self.helper.form_show_labels = False # surpress labels

class DeleteResourceForm(forms.ModelForm):
    '''Custom Delete Resource Form for building admins
    '''
    class Meta:
        model = Resource
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(DeleteResourceForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons=False,
                render_delete_buttons=True,
            )
        )
        
        self.helper.form_show_labels = False # surpress labels

class PasswordResetFormAion(PasswordResetForm):
    '''Custom Password Reset Form
    '''
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(PasswordResetFormAion, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Reset Password",
            )
        )
        self.helper.form_show_labels = False # surpress labels

class PasswordResetConfirmFormAion(SetPasswordForm):
    '''Custom Password Reset Confirm Form 
    '''
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(PasswordResetConfirmFormAion, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Change Password",
            )
        )
        self.helper.form_show_labels = False # surpress labels
        
class PasswordChangeFormAion(PasswordChangeForm):
    '''Custom PasswordChangeForm
    '''
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(PasswordChangeFormAion, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Change Password",
            )
        )
        self.helper.form_show_labels = False

from .models import TimeBlock, Resource
class BulkReservationForm(forms.Form):
    from_date = forms.DateField(required=True)
    to_date = forms.DateField(required=True)
    
    def clean_to_date(self):
        from_date = self.cleaned_data['from_date']
        to_date = self.cleaned_data['to_date']
        if (to_date < from_date):
            raise forms.ValidationError('"To date*" cannot be before the "From date*"' )

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return to_date
    
    def __init__(self, *args, **kwargs):
        '''Add the user to form constructor for use in queries
        '''
        self.user_school = kwargs.pop("user_school")
        super(BulkReservationForm, self).__init__(*args, **kwargs)
        user_school = self.user_school
        time_blocks = TimeBlock.objects.filter(school=user_school)
        time_block_choices = [(tb.id, tb.name) for tb in time_blocks]
        resources = Resource.objects.filter(school=user_school)
        resource_choices = [(r.id, r.name) for r in resources]

        self.fields['time_blocks']=forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple, 
            choices=time_block_choices
        )
        self.fields['resource']=forms.ChoiceField(
            widget=forms.Select, 
            choices=resource_choices
        )

        # Move resources to the beginning of the fields (OrderedDict)
        self.fields.move_to_end('resource', last=False)
        
         # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Reserve",
            )
        )
        
    '''
    # time_blocks = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    # resource = forms.ChoiceField(widget=forms.Select)
    from_date = forms.DateField(required=True)
    to_date = forms.DateField(required=True)
        
    def __init__(self, *args, **kwargs):
        time_block_choices = kwargs.pop('time_block_choices', [])
        resource_choices = kwargs.pop('resource_choices', [])
        
        super(BulkReservationForm, self).__init__(*args, **kwargs)

        self.fields['time_blocks']=forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple, 
            choices=time_block_choices
        )
        self.fields['resource']=forms.ChoiceField(
            widget=forms.Select, 
            choices=resource_choices
        )
        
        # Move resources to the beginning of the fields (OrderedDict)
        self.fields.move_to_end('resource', last=False)

        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Reserve",
            )
        )
    '''
    
class AjaxMakeReservationForm(forms.Form):
    resource_id = forms.IntegerField(required=True)
    time_block_id = forms.IntegerField(required=True)
    date = forms.DateField(required=True)


class AjaxCancelReservationForm(forms.Form):
    reservation_id = forms.IntegerField(required=True)
    