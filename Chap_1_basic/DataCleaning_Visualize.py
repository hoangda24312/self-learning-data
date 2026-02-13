import pandas as pd
import numpy as np
import matplotlib as plt


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

df[count_behavior] = df[count_behavior].fillna(0)

df["Days_Since_Last_Purchase"] = df["Days_Since_Last_Purchase"].isna().astype(int)

df[missing] = df[missing].fillna(df[missing].median())

print("Checking dataframe missing\n",df[missing].describe())



print("Data frame after dealing with missnig value:\n",df.describe())


#Second is dealing with error data
#Third is dealing with outliner data