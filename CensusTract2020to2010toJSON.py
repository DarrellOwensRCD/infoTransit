import json
import csv
import statistics
import os.path
from os import path
def main():
    decade = '2020to2010CensusTracts.geojson' #list of tracts
    #xlsx file with all Census Tract data
    file2010 = '/Users/darrell/Desktop/Census2020/Census2010NHGIS/nhgis0047_ds171_2010_tract.csv' #2010 statistics for each tract
    file2020 = '/Users/darrell/Desktop/Census2020/Census2020NHGIS/nhgis0048_ds248_2020_tract.csv' #2020 stats for each tract
    d = open(file2010, encoding = "ISO-8859-1")
    e = open(file2020, encoding = "ISO-8859-1")
    bc = open(decade)
    fileLines = csv.reader(d, delimiter=',')
    fileLines2 = csv.reader(e, delimiter=',')
    Lines = list(fileLines)
    Lines2 = list(fileLines2)
    tract_names = json.load(bc) #The JSON file
    #Helper Vars
    tract_multi = 0
    county = 0
    tract = 0
    #Step 1, Iterate through every tract in the 2010s
    print("Filling Values....")
    for line10 in Lines:
        tract_multi = 1
        if(line10[4] == "California"): #only procede if Line is in California
            for line20 in Lines2: #now iterate thru 2020 Census
                if(tract_multi == 0): #if we currently did some iterations and we need to save the val
                    tract_multi = int(line10[10]) #filling tract multi
                if(line20[36] == line10[10] and line20[3] == "CA" and int(line20[18]) == int(line10[7])) : #If the Tract ID's and county match...go
                    #if(int(line20[18]) == 93):
                        #print("Value from 2010: ",line10[10]) 
                        #print("2020 match ", line20[36])
                        #print("County ", line20[18])
                    tract_multi = 0 #resetting to ZERO
                    #set county
                    county = line10[6] #County Name
                    tract = line10[31] # "Census Tract [Tract Name]"
                    #iterate through JSON file
                    for tract in tract_names['features']: #iterate through JSON map
                        if(tract["properties"]["TRACTCE10"] == line10[10] and int(tract["properties"]["COUNTYFP10"]) == int(line10[7])): #if it matches the tract, proceed with data filling
                            #print("\n")
                            tract["properties"]["Population20"] = int(line20[103]) #Population
                            tract["properties"]["Latino20"] = int(line20[104]) #Latinos
                            tract["properties"]["White20"]= int(line20[107]) #Whites
                            tract["properties"]["Black20"]= int(line20[108]) #Black
                            tract["properties"]["Native American20"]= int(line20[109]) #Natives
                            tract["properties"]["Asian20"]= int(line20[110]) #Asian
                            tract["properties"]["Pacific Islander20"] = int(line20[111]) #Hawaii
                            tract["properties"]["Other20"] = int(line20[112]) #Other
                            tract["properties"]["Multi-Race20"] = int(line20[113]) #Multiracial
                            tract["properties"]["Homes20"] = int(line20[176]) #housing units
                            tract["properties"]["Vacant20"] = int(line20[178]) #Vacants
                            if(int(line20[176]) > 0):
                                tract["properties"]["VacancyRate20"] = round(int(line20[178]) / int(line20[176]),1) #vacancy rate
                            #Now calculate net diff
                            tract["properties"]["PopulationNet"] = tract["properties"]["Population20"] - int(line10[33]) #Population
                            tract["properties"]["LatinoNet"] = tract["properties"]["Latino20"] - int(line10[34]) #Latinos
                            tract["properties"]["WhiteNet"] = tract["properties"]["White20"] - int(line10[37]) #Whites
                            tract["properties"]["BlackNet"] = tract["properties"]["Black20"]  - int(line10[38]) #Black
                            tract["properties"]["Native AmericanNet"] = tract["properties"]["Native American20"] - int(line10[39]) #Natives
                            tract["properties"]["AsianNet"] = tract["properties"]["Asian20"] - int(line10[40]) #Asian
                            tract["properties"]["Pacific IslanderNet"] = tract["properties"]["Pacific Islander20"] - int(line10[41]) #Hawaii
                            tract["properties"]["OtherNet"] = tract["properties"]["Other20"] - int(line10[42]) #Other
                            tract["properties"]["Multi-RaceNet"] = tract["properties"]["Multi-Race20"] - int(line10[43]) #Multiracial
                            tract["properties"]["HomesNet"] = tract["properties"]["Homes20"] - int(line10[106]) #housing units
                            tract["properties"]["VacantNet"] = tract["properties"]["Vacant20"] - int(line10[108]) #Vacants
                            #Now calculate net diff in percent
                            if(int(line10[33])):
                                tract["properties"]["PopulationNetPer"] = round(tract["properties"]["PopulationNet"] / int(line10[33]) * 100,1) #Population
                            if(int(line10[34])):
                                tract["properties"]["LatinoNetPer"] = round(tract["properties"]["LatinoNet"] / int(line10[34]) * 100,1) #Latinos
                            if(int(line10[37])):
                                tract["properties"]["WhiteNetPer"] = round(tract["properties"]["WhiteNet"] / int(line10[37]) * 100,1) #Whites
                            if(int(line10[38])):
                                tract["properties"]["BlackNetPer"] = round(tract["properties"]["BlackNet"]  / int(line10[38]) * 100,1) #Black
                            if(int(line10[39])):
                                tract["properties"]["Native AmericanNetPer"] = round(tract["properties"]["Native AmericanNet"] / int(line10[39]) * 100,1) #Natives
                            if(int(line10[40])):
                                tract["properties"]["AsianNetPer"] = round(tract["properties"]["AsianNet"] / int(line10[40]) * 100,1) #Asian
                            if(int(line10[41])):
                                tract["properties"]["Pacific IslanderNetPer"] = round(tract["properties"]["Pacific IslanderNet"] / int(line10[41]) * 100,1) #Hawaii
                            if(int(line10[42])):
                               tract["properties"]["OtherNetPer"] = round(tract["properties"]["OtherNet"] / int(line10[42]) * 100,1) #Other
                            if(int(line10[43])):
                                tract["properties"]["Multi-RaceNetPer"] = round(tract["properties"]["Multi-RaceNet"] / int(line10[43]) * 100,1) #Multiracial
                            if(int(line10[106])):
                                tract["properties"]["HomesNetPer"] = round(tract["properties"]["HomesNet"] / int(line10[106]) * 100,1) #housing units
                            if(int(line10[108])):
                                tract["properties"]["VacantNetPer"] = round(tract["properties"]["VacantNet"] / int(line10[108]) * 100,1) #Vacants
                            #print(tract["properties"])
                            #print("\n")
                            break #break out JSON loop
                    break #break out the 2020s loop
                else:
                    if(line20[36] != "TRACTA"):                            
                        if((int(line10[7]) == int(line20[18])) and line20[3] == "CA" and (int(line10[10]) + tract_multi == int(line20[36]))):   #If this tract was split up in 2020
                            if(int(line20[36]) % 10 == 1 or tract_multi > 1): #if its a .01 or we've been looping
                                for tract in tract_names['features']: #iterate through JSON map
                                    if(tract["properties"]["TRACTCE10"] == line10[10] and int(tract["properties"]["COUNTYFP10"]) == int(line10[7])): #if it matches the 2010 tract, proceed with data filling
                                        #and int(tract["properties"]["COUNTYFP10"]) == int(line20[18])
                                        if(tract_multi == 1):
                                            tract["properties"]["Population20"] = int(line20[103]) #Population
                                            tract["properties"]["Latino20"] = int(line20[104]) #Latinos
                                            tract["properties"]["White20"] = int(line20[107]) #Whites
                                            tract["properties"]["Black20"] = int(line20[108]) #Black
                                            tract["properties"]["Native American20"] = int(line20[109]) #Natives
                                            tract["properties"]["Asian20"] = int(line20[110]) #Asian
                                            tract["properties"]["Pacific Islander20"] = int(line20[111]) #Hawaii
                                            tract["properties"]["Other20"] = int(line20[112]) #Other
                                            tract["properties"]["Multi-Race20"] = int(line20[113]) #Multiracial
                                            tract["properties"]["Homes20"] = int(line20[176]) #housing units
                                            tract["properties"]["Vacant20"] = int(line20[178]) #Vacants

                                        else:
                                            tract["properties"]["Population20"] += int(line20[103]) #Population
                                            tract["properties"]["Latino20"] += int(line20[104]) #Latinos
                                            tract["properties"]["White20"] += int(line20[107]) #Whites
                                            tract["properties"]["Black20"] += int(line20[108]) #Black
                                            tract["properties"]["Native American20"] += int(line20[109]) #Natives
                                            tract["properties"]["Asian20"] += int(line20[110]) #Asian
                                            tract["properties"]["Pacific Islander20"] += int(line20[111]) #Hawaii
                                            tract["properties"]["Other20"] += int(line20[112]) #Other
                                            tract["properties"]["Multi-Race20"] += int(line20[113]) #Multiracial
                                            tract["properties"]["Homes20"] += int(line20[176]) #housing units
                                            tract["properties"]["Vacant20"] += int(line20[178]) #Vacants
                                        if(int(line20[176]) > 0):
                                            tract["properties"]["VacancyRate20"] = round(tract["properties"]["Vacant20"] / tract["properties"]["Homes20"] * 100,1) #vacancy rate
                                        #Now calculate net diff (will cummulatively at the 20s while 10 stays, so proper vals overwrite correctly
                                        tract["properties"]["PopulationNet"] = tract["properties"]["Population20"] - int(line10[33]) #Population
                                        tract["properties"]["LatinoNet"] = tract["properties"]["Latino20"] - int(line10[34]) #Latinos
                                        tract["properties"]["WhiteNet"] = tract["properties"]["White20"] - int(line10[37]) #Whites
                                        tract["properties"]["BlackNet"] = tract["properties"]["Black20"]  - int(line10[38]) #Black
                                        tract["properties"]["Native AmericanNet"] = tract["properties"]["Native American20"] - int(line10[39]) #Natives
                                        tract["properties"]["AsianNet"] = tract["properties"]["Asian20"] - int(line10[40]) #Asian
                                        tract["properties"]["Pacific IslanderNet"] = tract["properties"]["Pacific Islander20"] - int(line10[41]) #Hawaii
                                        tract["properties"]["OtherNet"] = tract["properties"]["Other20"] - int(line10[42]) #Other
                                        tract["properties"]["Multi-RaceNet"] = tract["properties"]["Multi-Race20"] - int(line10[43]) #Multiracial
                                        tract["properties"]["HomesNet"] = tract["properties"]["Homes20"] - int(line10[106]) #housing units
                                        tract["properties"]["VacantNet"] = tract["properties"]["Vacant20"] - int(line10[108]) #Vacants
                                        #Now calculate net diff in percent
                                        if(int(line10[33])):
                                            tract["properties"]["PopulationNetPer"] = round(tract["properties"]["PopulationNet"] / int(line10[33]) * 100, 1) #Population
                                        if(int(line10[34])):
                                            tract["properties"]["LatinoNetPer"] = round(tract["properties"]["LatinoNet"] / int(line10[34]) * 100, 1) #Latinos
                                        if(int(line10[37])):
                                            tract["properties"]["WhiteNetPer"] = round(tract["properties"]["WhiteNet"] / int(line10[37]) * 100, 1) #Whites
                                        if(int(line10[38])):
                                            tract["properties"]["BlackNetPer"] = round(tract["properties"]["BlackNet"]  / int(line10[38]) * 100, 1) #Black
                                        if(int(line10[39])):
                                            tract["properties"]["Native AmericanNetPer"] = round(tract["properties"]["Native AmericanNet"] / int(line10[39]) * 100, 1) #Natives
                                        if(int(line10[40])):
                                            tract["properties"]["AsianNetPer"] = round(tract["properties"]["AsianNet"] / int(line10[40]) * 100, 1) #Asian
                                        if(int(line10[41])):
                                            tract["properties"]["Pacific IslanderNetPer"] = round(tract["properties"]["Pacific IslanderNet"] / int(line10[41]) * 100,1) #Hawaii
                                        if(int(line10[42])):
                                            tract["properties"]["OtherNetPer"] = round(tract["properties"]["OtherNet"] / int(line10[42]) * 100, 1) #Other
                                        if(int(line10[43])):
                                            tract["properties"]["Multi-RaceNetPer"] = round(tract["properties"]["Multi-RaceNet"] / int(line10[43]) * 100, 1) #Multiracial
                                        if(int(line10[106])):
                                            tract["properties"]["HomesNetPer"] = round(tract["properties"]["HomesNet"] / int(line10[106]) * 100,1) #housing units
                                        if(int(line10[108])):
                                            tract["properties"]["VacantNetPer"] = round(tract["properties"]["VacantNet"] / int(line10[108]) * 100,1) #Vacants
                                        tract_multi += 1
                                        #print(tract["properties"])
                                        #print("\n")
                                        break #only break out of the JSON loop, move onto next 2020 tract
                                
    print("Done. Writing results")
    ############
    #Close up shop, append new JSON to JSON File
    bc.close()
    with open(decade, 'w') as k: #Writing the new data into the GJ file CONSIDER NEW JSON FILE 
        json.dump(tract_names, k)
        k.close()
    d.close()
    e.close()
    print("OVER")
