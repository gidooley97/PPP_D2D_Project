import datetime
from .models import Query_Manager, Profile
from django.db.models import Sum
from django.contrib.auth.models import User

"""
class that represents the user report.
"""
class UserReport:
    def __init__(self, user_fname,user_lname, q_count):
        self.user_fname= user_fname
        self.user_lname= user_lname
        self.query_count = q_count


"""
represents company report
"""
class CompanyReport:
    def __init__(self, c_name):
        self.company_name=c_name
        self.user_reports = []
        self.total_queries = 0      

"""
gets all company users' activity.

params:
    group: the group that the user belongs to.
    time_range: daily, weekly, monthly,...
returns:
    company_report: company report
"""
def filter_dates(groups, time_range):
    if not groups:
        return None
    companies_report=[]
    for group in groups:
        company_report = CompanyReport(group.name)
        users_in_group = User.objects.filter(groups__name=group) 
        for user in users_in_group:
            profile = Profile.objects.get(user=user)
            query_count = get_query_for_user(time_range, profile)
            user_report = UserReport(user.first_name,user.last_name, query_count)
            company_report.user_reports.append(user_report)
            company_report.total_queries+=query_count
        companies_report.append(company_report)
    return companies_report


"""
gets the number of queries made by user within a speicific time range.

params:
    range: time range
    p: user Profile
returns:
    q_m:number of queries made
"""
def get_query_for_user(range, p ):
    if "w" in range.lower():
        #gets queries made in that week
        datetime.date.today()
        start_date = datetime.date.today() - datetime.timedelta( days=datetime.date.today().weekday())#weekdays:sun 0-sat 6
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
    
    

def get_time_range(range):
    if "d" in range.lower():
        return str(datetime.date.today())
    if "w" in range.lower():
        start_date = datetime.date.today() - datetime.timedelta( days=datetime.date.today().weekday())#weekdays:sun 0-sat 6
        end_date = datetime.date.today() 
        return str(start_date)+"-"+str(end_date)
    if "m" in range.lower():
        month = datetime.date.today().month
        year = datetime.date.today().year
        return str(month)+"/"+str(year)
    if "y" in range.lower():
        year = datetime.date.today().year
        return str(year)
    if "a" in range.lower():
        return "All time"    