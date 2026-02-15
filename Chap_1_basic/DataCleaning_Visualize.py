import pandas as pd
import numpy as np
from matplotlib  import pyplot as plt


#create dataframe by reading csv

df = pd.read_csv("MiniProject.csv")

#see it head and it info

print(df.head()) #default 5 first rows

print(df.info()) #seem like there is a lot of missing 

print("This is describe\n")
print(df.describe())

missing =  df.columns[df.isna().any()].tolist() #all column that has missing value

summary = df[missing].describe().T #Transpose
summary["%missing value"] = df[missing].isna().mean()*100 #check how much percentage data is missing so we can choose a right action


print("This is missing column\n",summary)

#First is dealing with NaN value
#you can manual for example
#df["Age"] = df["Age"].fillna(df["Age"].median()) #value is being right skew which min is 5 but max is 200, so mean is not trustable
#df["Session_Duration_Avg"] = df["Session_Duration_Avg"].fillna(df["Session_Duration_Avg"].median()) #std 10.8 with min 1, 75% 34 but max is 75, maybe skew right so let's use median
#df["Wishlist_Items"] = df["Wishlist_Items"].fillna(df["Wishlist_Items"].median()) #as session, this one might be right skew
#df["Pages_Per_Session"] = df["Pages_Per_Session"].fillna(df["Pages_Per_Session"].median()) #lightly right skew so use median just for sure

#if we look at the summary, we can see that mostly columns is right skew and we should use median to fill in na
#but median is not a wise choice with count behavior, for example 
# product review written, it missing maybe because customer didn't open it or write one

count_behavior = ["Wishlist_Items","Customer_Service_Calls","Product_Reviews_Written"]
important_cols = ["Credit_Balance", "Days_Since_Last_Purchase"]

#divide missing
missing = [col for col in missing
           if col not in count_behavior
           and col not in important_cols
           ]

df[count_behavior] = df[count_behavior].fillna(0)

for col in important_cols:
    df[col+"_missing"] = df[col].isna().astype(int) #flag with column has too high max value, heavily right skew

df[important_cols] = df[important_cols].fillna(df[important_cols].median())

df[missing] = df[missing].fillna(df[missing].median())

print("Data frame after dealing with missnig value:\n",df.info())

#Second is dealing with error data

category_list = [col for col in df if df[col].dtypes == 'object']
float_list = [col for col in df if df[col].dtypes == 'float64']
int_list = [col for col in df if df[col].dtypes == 'int64']

#check if there is any error in string type such as bUnmA instead Bunma

for col in category_list:
    print(df[col].unique())

for col in float_list: #if it < 0, maybe it is because they didn't buy anything
    df.loc[df[col] < 0, col] = 0 

#so we have nothing to do with Object, let's proceed to the next step, outliner
#Third is dealing with outliner data

#deal with float data type first
print(df[float_list].describe().T)

#first is col rate, we only have 0-100 right ? so let's clip it to 0-100
rate_cols = [
    "Cart_Abandonment_Rate",
    "Discount_Usage_Rate",
    "Returns_Rate",
    "Email_Open_Rate"
]

for col in rate_cols:
    df[col] = df[col].clip(0,100)

df["Age"] = df["Age"].clip(18,80) #average human age is different from each country, however they around 73-80

df["Total_Purchases"] = df["Total_Purchases"].round().astype("int64") #no way total purchase is float 

extremely_high_list = ["Lifetime_Value","Credit_Balance","Average_Order_Value"] #value that extremely high, we didn't sure that if it is really error or VIP member

for col in extremely_high_list:
    upper = df[col].quantile(0.99)
    df[col] = df[col].clip(upper=upper)

print("after dealing with outliner\n",df[float_list].describe().T)

print("skewness checking\n",df[float_list].skew().sort_values(ascending=False)) #seem like we have some extremely skew

#dealing with numeric col

numeric_col = [col for col in df if df[col].dtypes == "int64" ]

print("this is numeric_col", numeric_col) #min and max is 0 and 1, there is only one thing we need to worry about is that total purchase

df["Total_Purchases"] = df["Total_Purchases"].clip(upper= df["Total_Purchases"].quantile(0.99))

df = pd.get_dummies(df, drop_first=True)

print(df.describe().T)
print(df.info())

#plot into matplotliab
df.boxplot(column="Age", by="Churned")

plt.show()