

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

# print(enrollments[0])
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

# print(len(enrollments),len(find_unique_student(enrollments)))
# print(len(daily_engagement),len(find_unique_student(daily_engagement)))
# print(len(project_submissions),len(find_unique_student(project_submissions)))
# print(daily_engagement[0]['account_key'])

# find data problem
k = find_unique_student(daily_engagement)
for enroll in enrollments:
    # k.add(enroll['account_key'])
    # if len(k) != kn:
    if enroll['account_key'] not in k:
        # print(enroll)
        break
        # k = find_unique_student(daily_engagement)
        # rr += 1

num_problem_student = 0
for enroll in enrollments:
    student = enroll['account_key']
    days = enroll['days_to_cancel']
    if (student not in k) and (days != 0):
        num_problem_student += 1
        print(enroll)

print(num_problem_student)

udacity_test_accounts = set()
for enroll in enrollments:
    if enroll['is_udacity']:
        udacity_test_accounts.add(enroll['account_key'])
print('# of test account:', len(udacity_test_accounts))

def remove_is_udacity(data):
    non_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_data.append(data_point)
    return non_data

nontest_enrollments = remove_is_udacity(enrollments)
nontest_daily_engagement = remove_is_udacity(daily_engagement)
nontest_project_submissions = remove_is_udacity(project_submissions)

print(len(nontest_enrollments),len(nontest_daily_engagement),len(nontest_project_submissions))


# paid_students
paid_students = {}
for enroll in nontest_enrollments:
    if (enroll['days_to_cancel'] > 7) or (enroll['days_to_cancel'] == None):
        account_key = enroll['account_key']
        enrollment_date = enroll['join_date']

        if (account_key not in paid_students) or (enrollment_date > paid_students[account_key]):
            paid_students[account_key] = enrollment_date

# print(len(paid_students))

def within_one_week(join_date,engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days <7 and time_delta.days >= 0

def remove_free_trial_cancels(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)
    return new_data

paid_enrollments = remove_free_trial_cancels(nontest_enrollments)
paid_engagement = remove_free_trial_cancels(nontest_daily_engagement)
paid_submissions = remove_free_trial_cancels(nontest_project_submissions)
print(nontest_project_submissions[0])
print(paid_submissions[0])
# paid_within_oneweek_engagement = within_one_week(paid_engagement)
# print(len(paid_enrollments),len(paid_engagement),len(paid_submissions))
# print(paid_engagement[0])

paid_within_oneweek_engagement = []
for engagement in paid_engagement:
    engagement_date = engagement['utc_date']
    join_date = paid_students[engagement['account_key']]
    if within_one_week(join_date,engagement_date):
        paid_within_oneweek_engagement.append(engagement)

# print(len(paid_within_oneweek_engagement))


# exploring students' engagement
# dictionary!!

from collections import defaultdict

def engage_by_account(data):
    engagement_by_account = defaultdict(list)
    for engagement in data:
        account_key = engagement['account_key']
        engagement_by_account[account_key].append(engagement)
    return engagement_by_account

engagement_by_account = engage_by_account(paid_within_oneweek_engagement)

def sum_by_account(data,key):
    total_sum_by_account = {}
    for account_key, engagement_for_student in data.items():
        total_sum = 0
        for engagement in engagement_for_student:
            total_sum += engagement[key]
        total_sum_by_account[account_key] = total_sum
    return total_sum_by_account

import numpy as np
def descript_data(data):
    print('Mean:', np.mean(data))
    print ('Standard deviation:', np.std(data))
    print ('Minimum:', np.min(data))
    print ('Maximum:', np.max(data))

total_minutes_by_account = sum_by_account(engagement_by_account,'total_minutes_visited')
total_minutes = total_minutes_by_account.values()
descript_data(total_minutes)

total_lessons_by_account = sum_by_account(engagement_by_account,'lessons_completed')
total_lessons = total_lessons_by_account.values()
descript_data(total_lessons)
# total_minutes_by_account.values()

def has_vistied_by_account(data,key):
    total_vistit_by_account = {}
    for account_key, engagement_for_student in data.items():
        total_sum = 0
        for engagement in engagement_for_student:
            total_sum += (engagement[key]>=1)
        total_vistit_by_account[account_key] = total_sum
    return total_vistit_by_account


total_vistit_by_account = has_vistied_by_account(engagement_by_account,'num_courses_visited')
descript_data(total_vistit_by_account.values())



# split data into pass or not
subway_project_lesson_keys = ['746169184', '3176718735']
pass_subway_project = set()

for submission in paid_submissions:
    project = submission['lesson_key']
    rating = submission['assigned_rating']

    if project in subway_project_lesson_keys and \
            (rating == 'PASSED' or rating == 'DISTINCTION'):
        pass_subway_project.add(submission['account_key'])

print(len(pass_subway_project))

passing_engagemnet = []
non_passing_engagement = []

for engagement in paid_within_oneweek_engagement:
    if engagement['account_key'] in pass_subway_project:
        passing_engagemnet.append(engagement)
    else:
        non_passing_engagement.append(engagement)

print(len(passing_engagemnet))
print(len(non_passing_engagement))
