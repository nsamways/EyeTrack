import time
import pandas as pd
import numpy as np
import re
import os
import logging
import csv
from detectors import *


from Classes import Trial,Subject


def get_subject_nr(subject_path): # Return the subject number from the file name (string)
    return int(''.join(filter(str.isdigit, subject_path)))


def get_subjects(): # Returns a list of tuples of eye tracking and behavioural data
    
    fullList = os.listdir() # list every file in current directory
    subject_numbers = {}
    subject_pairs = []

    # Loop though the files and process those with 'subject' in the filename
    for file in fullList:
        if "subject" in file:
            try:
                nr = get_subject_nr(file) # Get the subject number
                subject_numbers[file]=nr # Add the file and it's number to the dictionary
            except ValueError:
                logging.error("ERROR: Check for files with name containing 'subject' without number")
                
    # Combine the subject behavioural and eye tracking data by finding the common subject number
    
    for file,number in subject_numbers.items(): # Nested loop to compare each file and append those with the same number
        for file_2,number_2 in subject_numbers.items():
            if file != file_2: # The keys are named differently
                if number == number_2: # They have the same subject number value 
                    if (file_2,file) not in subject_pairs:  # ensure they aren't listed already the other way around
                        subject_pairs.append((file,file_2)) # Append the file pair with identical subject numbers in a tuple

    return subject_pairs

def get_AOIs():
     
    AOI_Dict = {}   # dictionary of AOIs
    # get the CSV
    full_list = os.listdir()
    
    for file in full_list:
        if "AOI" in file:
            aoi_file = file
    
    with open(aoi_file, "r") as f:
        aoi_reader = csv.reader(f)
        next(aoi_reader)
    
        aoi_full = list(aoi_reader)

    for items in aoi_full:
    # check if name in dict. If not, create it

        if items[0] not in AOI_Dict:
            AOI_Dict[items[0]] = []
            AOI_Dict[items[0]].append([items[1],int(float(items[2])),int(float(items[3])),int(float(items[4])),int(float(items[5]))]) 

        else:
        # push the value on the end
            AOI_Dict[items[0]].append([items[1],int(float(items[2])),int(float(items[3])),int(float(items[4])),int(float(items[5]))]) 

    # return the completed dictionary        
    return AOI_Dict
    
def main():

    # Get the list of subjects from the current folder
    subject_list = get_subjects()
    
    # Get the AOI information
    AOI_collection = get_AOIs()
    
    # create a dataframe for the complete results
    final_output = pd.DataFrame() 
    #Loop though the list of subject file pairs to create the subjects
    
    for subject_files in subject_list:
    
        start = time.perf_counter()
    
        print("Processing subject: " , get_subject_nr(subject_files[1]))
    
        subject = Subject(subject_files[1],subject_files[0],get_subject_nr(subject_files[1])) #Create the subject object with the eye tracking and behavioural files
    #
    #     subject_raw = subject.get_output()   # Get a dataframe with all relevant information
    #
    #     # Create an empty table using pandas and set the column names
    #     subject = pd.DataFrame(subject_raw) 
    #     subject.columns = ["Subject","Gamble","Domain","p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix","Good Fix %","Bad Fix %","Good X %","Good Y %","risk_selected","response_time"]
    #
    #     #Add the new table with the old one by combining them using pandas
    #     final_output = pd.concat([final_output, subject])
    #
    # #Export the table to a csv file
    # final_output.to_csv("Final-Output.csv", index = False)
    #

    #show the timing metrics

    print(AOI_collection["100_c_24_12g_a_3.jpg"][0][0])

    end = time.perf_counter()  
    print("Program ended. Duration: ", end-start)
        

#Start the program if called 

if __name__ == "__main__":
    main()
    
 







