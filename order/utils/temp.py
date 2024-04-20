import random
import datetime

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2022, 12, 31)

random_number_of_days = random.randint(0, (end_date - start_date).days)
random_date = start_date + datetime.timedelta(days=random_number_of_days)

print( random_date)