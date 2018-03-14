
import unicodecsv

def read_csv(filename):
    with open(filename,'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments_filename = 'enrollments.csv'
engagement_filename = 'daily_engagement.csv'
submissions_filename = 'project_submissions.csv'

enrollments = read_csv(enrollments_filename)
engagement = read_csv(engagement_filename)
submissions = read_csv(submissions_filename)

print(engagement[2])
