

# read csv to list
import unicodecsv

def read_csv(filename):
    with open(filename,'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments_filename = 'enrollments.csv'
engagement_filename = 'daily_engagement.csv'
submissions_filename = 'project_submissions.csv'

enrollments = read_csv(enrollments_filename)
daily_engagement = read_csv(engagement_filename)
project_submissions = read_csv(submissions_filename)

### change data type

# date
from datetime import datetime as dt
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date,'%Y-%m-%d')

# int
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

for enroll in enrollments:
    enroll['cancel_date'] = parse_date(enroll['cancel_date'])
    enroll['days_to_cancel'] = parse_maybe_int(enroll['days_to_cancel'])
    enroll['is_canceled'] = (enroll['is_canceled'] == 'True')
    enroll['is_udacity'] = (enroll['is_udacity'] == 'True')
    enroll['join_date'] = parse_date(enroll['join_date'])

print(enrollments[0])
for engagement in daily_engagement:
    engagement['lessons_completed'] = int(float(engagement['lessons_completed']))
    engagement['num_courses_visited'] = int(float(engagement['num_courses_visited']))
    engagement['projects_completed'] = int(float(engagement['projects_completed']))
    engagement['total_minutes_visited'] = float(engagement['total_minutes_visited'])
    engagement['utc_date'] = parse_date(engagement['utc_date'])
    engagement['account_key'] = engagement['acct']
    del(engagement['acct'])



for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])


def find_unique_student(ddata):
    uniqq = set()
    for dd in ddata:
        uniqq.add(dd['account_key'])
    return uniqq

print(len(enrollments),len(find_unique_student(enrollments)))
print(len(daily_engagement),len(find_unique_student(daily_engagement)))
print(len(project_submissions),len(find_unique_student(project_submissions)))
print(daily_engagement[0]['account_key'])

# find data problem
k = find_unique_student(daily_engagement)
for enroll in enrollments:
    # k.add(enroll['account_key'])
    # if len(k) != kn:
    if enroll['account_key'] not in k:
        print(enroll)
        break
        # k = find_unique_student(daily_engagement)
        # rr += 1

num_problem_student = 0
for enroll in enrollments:
    student = enroll['account_key']
    days = enroll['days_to_cancel']
    if (student not in k) and (days != 0):
        num_problem_student += 1

print(num_problem_student)





#
# print(len(set(project_submissions['account_key'])))
