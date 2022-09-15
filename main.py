### Start solution here
import pandas as pd
import os

df = pd.DataFrame()
#Reads the 3 sample_files.* in Input/data_source_1/ and Input/data_source_2/ folders into a dataframe

paths = "C:/Users/premc/python_training/coding/CodingExercises/etl_example_exercise/Input/"
filelist = []
arr = os.walk(paths)
for root, dirs, files in arr:
    for file in files:
        print(file)
        if file=="material_reference.txt":
            df_txt = pd.read_csv(os.path.join(root,file),sep = ',')
            continue
        df1 = pd.read_csv(os.path.join(root,file), sep='[\s+|,]', engine='python')
        df1.insert(4, 'Data_source', file)    #Create a new column that will help track which data source the products originally came from
        df = pd.concat([df, df1], ignore_index=True)    #Consolidates the data from each file into a single dataframe

#Bonus 1: Load and use the material_reference data file to get the material name for each product in the final dataframe
df['material_id'] = df['material_id'].map(df_txt.set_index('id')['material_name'])

#The sample_data.1 file has a number of products we do not want in our output. Filter this data so that the only products that remain are products with a worth of MORE than 1.00
df.drop(df.index[(df["worth"] < 1.00)],axis=0,inplace=True)
print(df)

if df['Data_source'] == 'sample_data.2.dat':
    result = df.groupby(['product_name','quality']).aggregate({'material_id':'max','worth':'sum'})
    print(result)
#Saves to a new output file in the Output dir using the name consolidated_output.1.csv
#df.to_csv('C:/Users/premc/python_training/coding/CodingExercises/etl_example_exercise/consolidated_output.1.csv', index=False)
