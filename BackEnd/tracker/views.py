from django.shortcuts import render ,redirect
from .models import Transaction , Category
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Sum



def home(request):
    # لو المستخدم مش مسجل دخول، وديه للوجين
    if not request.user.is_authenticated:
        return redirect('login')

    # جلب البيانات من الداتابيز
    user_trans = Transaction.objects.filter(user=request.user)
    
    income = user_trans.filter(transaction_type='INC').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = user_trans.filter(transaction_type='EXP').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'transactions': user_trans.order_by('-date')[:4], # آخر 4 عمليات
        'total_income': income,
        'total_expenses': expenses,
        'total_balance': income - expenses,
    }
    return render(request, 'tracker/home.html', context)


def add_transaction(request):
    if request.method == 'POST':
        # 1. سحب البيانات اللي بعتناها من الـ HTML باستخدام الـ name
        title = request.POST.get('description', 'No Title') # اللي ضفنا لها name="description"
        amount_raw = request.POST.get('amount', '0') # اللي ضفنا لها name="amount"
        t_type = request.POST.get('type', 'expense')       # اللي جاي من الـ Hidden Input
        category_name = request.POST.get('category')
        t_date = request.POST.get('date')
        # amount = amount_raw.replace('$', '').replace(',', '')
        try:
                # تنظيف وتحويل المبلغ لرقم عشري
                amount = float(str(amount_raw).replace('$', '').replace(',', ''))
                
                Transaction.objects.create(
                    user=request.user, 
                    title=title,
                    amount=amount,
                    transaction_type='INC' if t_type.lower() == 'income' else 'EXP',
                    date=t_date
                )
                return redirect('transactions')
        except Exception as e:
                # لو حصل إيرور هيطبع لك سببه في الـ Terminal
                print(f"Error saving transaction: {e}")
                return render(request, 'tracker/add-transaction.html', {'error': 'Check your data!'})

    return render(request, 'tracker/add-transaction.html')

def budgets(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # حفظ في الداتابيز (تأكد إن اسم الموديل عندك Budget)
        # Budget.objects.create(
        #     user=request.user,
        #     category=category,
        #     amount=amount,
        #     start_date=start_date,
        #     end_date=end_date
        # )
        return redirect('budgets') # يرجعك لصفحة العرض

    return render(request, 'tracker/budgets.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Trying to login with: {username}")
        
        # بنحاول نلاقي اليوزر في الداتابيز
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user) # تسجيل الدخول في السيشن
            return redirect('home') # هينقلك للداشبورد فوراً
        else:
            # لو البيانات غلط، هيرجع لنفس الصفحة مع رسالة خطأ
            return render(request, 'tracker/login.html', {'error': 'Invalid credentials'})
            
    return render(request, 'tracker/login.html')

def signup_view(request):
    return render(request, 'tracker/signup.html')

def transactions(request):
    return render(request, 'tracker/transactions.html')

def goals(request):
    return render(request, 'tracker/goal.html')