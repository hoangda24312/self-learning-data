import pandas as pd
import datetime as dt

#testing file
data = {
    "order_id": [1001, 1002, 1003, 1004, 1005],
    "customer_name": ["An", "Bình", "Chi", "Dũng", "An"],
    "drink": ["Coffee", "Tea", "Coffee", "Juice", "Coffee"],
    "quantity": [1, 2, 1, 3, 2],
    "price": [30000, 20000, 30000, 25000, 30000],
    "order_date": [
        "2026-01-01",
        "2026-01-01",
        "2026-01-02",
        "2026-01-02",
        "2026-01-03"
    ]
}

df = pd.DataFrame(data)

print(df.describe())  #print descriptive statistic

print(df.head()) #print 5 first row, the number of row is the input

#today = dt.date.today() old

today = pd.to_datetime(dt.date.today()) #new

#print(df[df['order_date'] > today]) #will be error

#let look at the info to see what type of order_date
print(df.info())

#as we can see order_date is an object so string can't be compare with date time type

#make new column to convert string date to date time

df['Date'] = pd.to_datetime(df['order_date'])

#as we can see now Date is a datetime64
print(df.info())

print(df[df['Date'] > today]) #still error, because one is datetime64 and one date, let's fix this

