from django import forms


class StockForm(forms.Form):
    symbol_name = forms.CharField(label='Symbol', 
                                  max_length=20,
                                  widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))


class InvStockForm(forms.Form):
    symbol_name = forms.CharField(label='Symbol',
                                  max_length=20,
                                  widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}))



class SectReturnForm(forms.Form):
    sector_choices = ([('Bank', 'Bank'),
                       ('IT','IT'),
                       ('ETF','ETF'),
                       ('Auto','Auto'),
                       ('NIFTY50','NIFTY50')])
    sector = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                               choices=sector_choices)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))

