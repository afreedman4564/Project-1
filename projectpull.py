# Dependencies and Setup
import pandas as pd
import requests
from datetime import datetime as dt

# Import API key
from config import spoonacular_key as api_key

#generate url
url = f"https://api.spoonacular.com/recipes/random?"
query_url = url + "apiKey=" + api_key

error_occurrence1 = False
error_occurrence2 = False
try:
    #pull existing data from previous calls from a csv
    recipes_lists = pd.read_csv('Desktop/recipe_stats.csv')    
    
    try:
        #Fill the column lists from the CSV
        Name = recipes_lists['Name'].to_list()
        Cost = recipes_lists['Cost'].to_list()
        Protein = recipes_lists['Protein (g)'].to_list()
        Calories = recipes_lists['Calories'].to_list()
        Fat = recipes_lists['Fat (g)'].to_list()
        Servings = recipes_lists['Servings'].to_list()
        Prep_Time = recipes_lists['Preparation Time (m)'].to_list()
        Health_Score = recipes_lists['Health Score'].to_list()
        Cuisine = recipes_lists['Cuisine'].to_list()
        Gluten_Free = recipes_lists['Gluten Free'].to_list()
        Vegetarian = recipes_lists['Vegetarian'].to_list()
        Dairy_Free = recipes_lists['Dairy Free'].to_list()
        Sustainable = recipes_lists['Sustainable'].to_list()
        Cheap = recipes_lists['Cheap'].to_list()
        record = len(Name)
    
    except:
        #If the code cannot correctly fill the lists from 
        #the CSV even if the CSV was read correctly
        print('An error occurred when filling the CSV values to lists')
        error_occurrence2 = True
        
except:
    #If there is no matching CSV name in the file location 
    #or it cannot be read correctly 
    print('An error occurred when pulling the CSV') 
    error_occurrence1 = True 
    
#create new empty lists if lists could not be imported    
if error_occurrence1 == True or error_occurrence2 ==True:
    print('Making new, empty, lists')
    Name = []
    Cost = []
    Protein = []
    Calories = []
    Fat = []
    Servings = []
    Prep_Time = []
    Health_Score = []
    Cuisine = []
    Gluten_Free = []
    Vegetarian = []
    Dairy_Free = []
    Sustainable = []
    Cheap = []
    record = 1

#make a dictionary of lists to create the dataframe from later
recipes_dict = {
    'Name': Name,
    'Cost': Cost,
    'Protein (g)': Protein,
    'Calories': Calories,
    'Fat (g)':Fat,
    'Servings':Servings,
    'Preparation Time (m)':Prep_Time,
    'Health Score': Health_Score,
    'Cuisine': Cuisine,
    'Gluten Free': Gluten_Free,
    'Vegetarian': Vegetarian,
    'Dairy Free': Dairy_Free,
    'Sustainable': Sustainable,
    'Cheap': Cheap
}

# Create the for loop to query Spoonacular
#create records as inquiries are made

# Set a range and make that many calls to the spoonacular API
for each in range(1450):
    
    #acquire all the relevant stats and partition response
    response = requests.get(query_url).json()
    summary = response["recipes"][0]["summary"]
    
    #attempt to fill the values into the lists
    try:           
        #pull values out of the Summary
        if response['recipes'][0]['title'] not in Name:
            Name.append(response['recipes'][0]['title'])
            
            #calories per serving
            calories = summary.partition("calories")
            before_calories = calories[0]
            partition_calories = before_calories.split(">")
            num = len(partition_calories)
            cals = partition_calories[num-1]
            Calories.append(int(cals))        
            
            #protein values
            protein = summary.partition("g of protein")
            before_protein = protein[0]
            partition_protein = before_protein.split(">")
            num = len(partition_protein)
            prtn = partition_protein[num-1]
            Protein.append(int(prtn))
            
            #fat values
            fat = summary.partition("g of fat")
            before_fat = fat[0]
            partition_fat = before_fat.split(">")
            num = len(partition_fat)
            fat_ = partition_fat[num-1]
            Fat.append(int(fat_))
            
            #acquire values from elsewhere in the JSON
            Prep_Time.append(int(response["recipes"][0]['readyInMinutes']))
            Cost.append(round(float(response["recipes"][0]['pricePerServing']/100),2))
            Health_Score.append(float(response["recipes"][0]["healthScore"]))
            Gluten_Free.append(bool(response["recipes"][0]["glutenFree"]))
            Vegetarian.append(bool(response["recipes"][0]["vegetarian"]))
            Dairy_Free.append(bool(response["recipes"][0]["dairyFree"]))
            Cuisine.append(response["recipes"][0]["cuisines"])
            Servings.append(int(response['recipes'][0]['servings']))
            Sustainable.append(bool(response["recipes"][0]["sustainable"]))
            Cheap.append(bool(response['recipes'][0]['cheap']))
            
            print(f"Acquired Recipe {record}: {Name[-1]}")
            
            #increment the record count
            record += 1
                
        else:
            print (f'Recipe {record} is a duplicate, skipping')
            #increment the record count
        
    #handle exceptions if the data doesn't fill
    except:
        print(f"Lazy exception handling! Recipe {record}. Something messed up!")
        #increment the record count         
        continue
        
#print the notice that the query loop is ending as the list ends
print("That's a lot of recipes!")

#create the dataframe from the populated lists
recipes_df = pd.DataFrame(recipes_dict)

#establish the date for error logging
today = str(dt.today().strftime('%Y-%m-%d'))
#save over the old csv if it successfully pulled the previous
if error_occurrence2 == False:
    print('Saving default readable CSV to desktop')
    recipes_df.to_csv('Desktop/recipe_stats.csv',index=False)
    
#else save a new csv with date if the previous results could not be pulled properly    
else:
    print('Due to previous error flag, saving new CSV to desktop to avoid overwriting data.')
    recipes_df.to_csv(f'Desktop/recipe_stats{today}.csv',index=False)