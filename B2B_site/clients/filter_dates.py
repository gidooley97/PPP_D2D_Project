import datetime
from .models import Query_Manager, Profile
from django.db.models import Sum
from django.contrib.auth.models import User

class UserReport:
    def __init__(self, user_fname,user_lname, q_count):
        self.user_fname= user_fname
        self.user_lname= user_lname
        self.query_count = q_count


class CompanyReport:
    def __init__(self, c_name):
        self.company_name=c_name
        self.user_reports = []
        self.total_queries = 0

            



def filter_dates(group, time_range):
    company_report = CompanyReport(group.name)
    users_in_group = User.objects.filter(groups__name=group) 
    for user in users_in_group:
        profile = Profile.objects.get(user=user)
        query_count = get_query_for_user(time_range, profile)
        user_report = UserReport(user.first_name,user.last_name, query_count)
        company_report.user_reports.append(user_report)
        company_report.total_queries+=query_count

    return company_report



def get_query_for_user(range, p ):
    if "w" in range.lower():
        #gets queries made in that week
        datetime.date.today()
        start_date = datetime.date.today() - datetime.timedelta( days=datetime.date.today().weekday()+1)#weekdays:sun 0-sat 6
        end_date = datetime.date.today() 
        print("end", start_date)
        q_m = Query_Manager.objects.filter(user=p,  last_date__gte=start_date, last_date__lte=end_date )
    elif "d" in range.lower():
        q_m = Query_Manager.objects.filter(user=p, last_date=datetime.date.today())
    elif "m" in range.lower():
        q_m = Query_Manager.objects.filter(user=p, last_date__month=datetime.date.today().month)
    elif "y" in range.lower():
        q_m = Query_Manager.objects.filter(user=p, last_date__year=datetime.date.today().year)
    elif "a" in range.lower():
        q_m = Query_Manager.objects.filter(user=p)
    if not q_m:
        return 0
    return  q_m.aggregate(Sum('num_queries'))['num_queries__sum']#gets the count of queries made within time range 
    
    

