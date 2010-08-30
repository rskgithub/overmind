from django import forms
from django.forms import ModelForm
from overmind.provisioning.models import Provider, Instance

class ProviderForm(ModelForm):
    class Meta:
        model = Provider


class InstanceForm(ModelForm):
    provider = forms.ModelChoiceField(
        queryset = Provider.objects.all(),
        widget   = forms.HiddenInput,
    )
    
    realm    = forms.ChoiceField()
    flavor   = forms.ChoiceField()
    image    = forms.ChoiceField()
    iamge_id = forms.CharField(required=False)
    
    def __init__(self, provider, *args, **kwargs):
        super(InstanceForm, self).__init__(*args, **kwargs)
        p = Provider.objects.get(id=provider)
        self.fields['provider'].initial = p.id
        self.fields['realm'].choices = [(realm.id, realm.country + " - " + realm.name) for realm in p.get_realms()]
        self.fields['image'].choices = [(img.id, img.name) for img in p.get_images()]
        self.fields['flavor'].choices = [(flavor.id, flavor.name) for flavor in p.get_flavors()]
    
    class Meta:
        model  = Instance
        fields = ('provider', 'name')
