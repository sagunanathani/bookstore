from django.shortcuts import render, redirect  
#to protect function-based views
from django.contrib.auth.decorators import login_required
from .forms import SalesSearchForm
from .models import Sale
import pandas as pd
from .utils import get_bookname_from_id, get_chart
#Django authentication libraries           
from django.contrib.auth import authenticate, login, logout
#Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib.auth.models import User
from .forms import RegistrationForm

# Create your views here.
def home(request):
   return render(request, 'sales/home.html')

#keep protected
@login_required
#define function-based view - records()
def records(request):
   #create an instance of SalesSearchForm that you defined in sales/forms.py
   form = SalesSearchForm(request.POST or None)
   sales_df=None   #initialize dataframe to None
   chart = None    #initialize chart to None
   #check if the button is clicked
   if request.method =='POST':
       #read book_title and chart_type
       book_title = request.POST.get('book_title')
       chart_type = request.POST.get('chart_type')

       #apply filter to extract data
       qs =Sale.objects.filter(book__name=book_title)
       if qs:      #if data found
           #convert the queryset values to pandas dataframe
           sales_df=pd.DataFrame(qs.values()) 
           #convert the ID to Name of book
           sales_df['book_id']=sales_df['book_id'].apply(get_bookname_from_id)

           #call get_chart by passing chart_type from user input, sales dataframe and labels
           chart=get_chart(chart_type, sales_df, labels=sales_df['date_created'].values)

          #convert the dataframe to HTML
           sales_df=sales_df.to_html()

       '''
       The following block is to get introduced to querysets
       #display in terminal - needed for debugging during development only
       print (book_title, chart_type)

       print ('Exploring querysets:')
       print ('Output of Sale.objects.all()')
       qs=Sale.objects.all()
       print (qs)

       print ('Output of Sale.objects.filter(book__name=book_title)')
       qs =Sale.objects.filter(book__name=book_title)
       print (qs)

       print ('Output of qs.values()')
       print (qs.values())

       print ('Output of qs.values_list()')
       print (qs.values_list())

       print ('Output of Sale.objects.get(id=1)')
       obj = Sale.objects.get(id=1)
       print (obj)
       '''

   #pack up data to be sent to template in the context dictionary
   context={
           'form': form,
           'sales_df': sales_df,
           'chart': chart
           }

   #load the sales/record.html page using the data that you just prepared
   return render(request, 'sales/records.html', context)


#define a function view called login_view that takes a request from user
def login_view(request):
   #initialize:
   #error_message to None                                 
   error_message = None   
   #form object with username and password fields                             
   form = AuthenticationForm()                            

   #when user hits "login" button, then POST request is generated
   if request.method == 'POST':       
       #read the data sent by the form via POST request                   
       form =AuthenticationForm(data=request.POST)

       #check if form is valid
       if form.is_valid():                                
           username=form.cleaned_data.get('username')      #read username
           password = form.cleaned_data.get('password')    #read password

           #use Django authenticate function to validate the user
           user=authenticate(username=username, password=password)
           if user is not None:                    #if user is authenticated
          #then use pre-defined Django function to login
               login(request, user)                
               return redirect('sales:home') #& send the user to desired page
       else:                                               #in case of error
           error_message ='ooops.. something went wrong'   #print error message

   #prepare data to send from view to template
   context ={                                             
       'form': form,                                 #send the form data
       'error_message': error_message                     #and the error_message
   }
   #load the login page using "context" information
   return render(request, 'auth/login.html', context)

#define a function view called logout_view that takes a request from user
def logout_view(request):                                  
   logout(request)          #the use pre-defined Django function to logout
   return redirect('login') #after logging out go to login form (or whichever page you want)

#define a function view called register_view that takes a request from user
def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            login(request, user)  # auto-login after registration
            return redirect('sales:home')  # redirect to Records page
    else:
        form = RegistrationForm()

    return render(request, 'sales/registration.html', {'form': form})