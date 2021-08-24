from django import forms


class StockForm(forms.Form):
    symbol_name = forms.CharField(label='Symbol', max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
#    series = forms.CharField(label='Series', max_length=5,widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))


class InvStockForm(forms.Form):
    symbol_name = forms.CharField(label='Symbol', max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
#    series = forms.CharField(label='Series', max_length=5,widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control'}))
    no_of_shares = forms.IntegerField(label='No OF shares',min_value=1, widget=forms.NumberInput(
                attrs={'size':'3','class':'form-control'}))
    multiply = forms.FloatField(label='Multiplication Factor',widget=forms.TextInput(attrs={'class':'form-control'}))
    moving_average = forms.IntegerField(label='Moving Average',min_value=10, widget=forms.NumberInput(
                attrs={'size':'3','class':'form-control'},))


class SectReturnForm(forms.Form):
    sector_choices = ([('Bank', 'Bank'),('IT','IT'),('ETF','ETF'),('Auto','Auto'),('NIFTY50','NIFTY50')])
    sector = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),choices=sector_choices)
    #sector = forms.ChoiceField(required=True,choices=sector_choices)
#    series = forms.CharField(label='Series', max_length=5)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    no_of_shares = forms.IntegerField(label='No OF shares',min_value=1, widget=forms.NumberInput(
                attrs={'size':'3','class':'form-control'}))
    multiply = forms.FloatField(label='Multiplication Factor',widget=forms.TextInput(attrs={'class':'form-control'}))
    moving_average = forms.IntegerField(label='Moving Average',min_value=10, widget=forms.NumberInput(
                attrs={'size':'3','class':'form-control'}))
