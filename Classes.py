#Classes 
import time
import pandas as pd
import numpy as np
from detectors import *
import re
import os
from sklearn.utils import estimator_checks


#Fix functions

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def replace_line(subject_path,badIndex): # Replace or remove the bad line of the file using the index
    
    #Open the bad file and find the error line
    f=open(subject_path,"r")

    data=f.readlines() 
    badLine = data[badIndex-1]
    del f
    
    if "Trial" in badLine: #If that bad line contains xxx then try to replace it
        print("REPLACING")
        template = "    "+"\t"+"xxx"
        data[badIndex-1] = template
        with open(subject_path, 'w') as fileG:
            fileG.writelines(data)
            del fileG

    else: # If is not gamble then remove it
        print("REMOVING: index %d" %badIndex)
        template = "    "											
        data[badIndex-1] = template
        with open(subject_path, 'w') as fileB:
            fileB.writelines(data)
            del fileB
    

def get_badIndex(e): # Get the index as integer from error
    result = [f for f in re.split("[^0-9]", str(e)) if f != ''] 
    return (max(map(int, result)))

      
def check_et(et_path,subject_nr): # This function will verify the eye tracking file for any problems
    temp = False 
    while temp == False: # Continuosly try to read the file, if worked then stop, otherwise try to fix it
        try:
            et = pd.read_csv(et_path,sep="\t",skiprows=17,low_memory=False) # Read the tab separated file with pandas and skip the first 17 rows
            temp = True # no more bad lines in the code
        except pd.errors.ParserError as e:
            print("Subject %d has a bad line, trying to fix."%subject_nr)
            badIndex = get_badIndex(e) # Get the index of where the error was
            replace_line(et_path,badIndex) # Replace the error line with good or bad
            temp = False
    return et


#Classes
class Trial: # This class creates an object with every table trial from the subject
    def __init__(self,dataframe,stim):
        self.dataframe = dataframe # The trial table or dataframe in pandas
        self.stim = stim
        
        
    def get_fixations_samples(self): #Get the fixations for the given dataframe       
    
        #Convert the necessary rows to list so they can be used by the fixation algorithm
        dfListX = self.dataframe["GazePointX"].tolist() 
        dfListY = self.dataframe["GazePointY"].tolist()
        dfListT = self.dataframe["TimeStamp"].tolist()
        
        
        # Convert to floats
        dfListX =list(map(float, dfListX))
        dfListY =list(map(float, dfListY))
        dfListT =list(map(float, dfListT))
        
        
        #Take the X and Y samples
        gazeX_samples = dfListX 
        gazeY_samples = dfListY
        
    
        subject_totalX = len(gazeX_samples)
        subject_totalY = len(gazeY_samples)
    
        subject_goodX = []
        subject_goodY = []
        
        
        #Add the good samples to a list of good samples
        for vX in gazeX_samples:
            if vX > 0:
                subject_goodX.append(vX)
        
        
        for vY in gazeY_samples:
            if vY > 0:
                subject_goodY.append(vY) 

        #Calculate the percentange
        percx_good = (len(subject_goodX) /len(gazeX_samples))*100
        percy_good = (len(subject_goodY) /len(gazeY_samples))*100
        

        
        results = fixation_detection(dfListX, dfListY, dfListT, missing=0.0, maxdist=25, mindur=16.7) # Calculate the fixations
        fixations = results[1]
        
        #Return the fixations and the samples data
        return [fixations] + [percx_good] +[percy_good] +[len(subject_goodX)] + [len(subject_goodY)]
    
    def get_AOI_MT(self,AOI_p,AOI_q,AOI_x,AOI_y): #Return the the mean and total of the AOIs_perc

        #calculate the means
        p_Meanfix = mean(AOI_p)  
        q_Meanfix = mean(AOI_q)
        x_Meanfix = mean(AOI_x)
        y_Meanfix = mean(AOI_y) 
        
        
        #calculate the length
        p_TotalFix = len(AOI_p)
        q_TotalFix = len(AOI_q)
        x_TotalFix = len(AOI_x)
        y_TotalFix = len(AOI_y)
        
        return [p_Meanfix,q_Meanfix,x_Meanfix,y_Meanfix,p_TotalFix,q_TotalFix,x_TotalFix,y_TotalFix]
                
    
    def get_AOIs_perc_Perc(self): # this is where we need to calc the metrics

        # get the fixations first
        fixations_samples = self.get_fixations_samples()
        
        # get the more comprehensive list (EFIX)
        fixations = fixations_samples[0]
        
        
        # go through the 
        
        
        total_fixations = 0
        bad_fixations = 0
        
        AOI_p = []# List of durations
        AOI_x = []
        AOI_q = []
        AOI_y = []
        for f in fixations:
                endx = f[3]
                endy = f[4]
                duration = f[2]
                
                #AOI 1 coordonates
                a1x_up = 944
                a1x_low = 656
                
                a1y_up = 524
                a1y_low = 236
                
                #AOI 2 coordonates
                a2x_up = 1264
                a2x_low = 976
                
                a2y_up = 524
                a2y_low = 236
                
                #AOI 3 coordonates
                a3x_up = 944
                a3x_low = 656
                
                a3y_up = 844
                a3y_low = 556
                
                #AOI 4 coordonates
                a4x_up = 1264               
                a4x_low = 976
                
                a4y_up = 844
                a4y_low = 556
                
                
                # Determine in which AOI should the fixation be
                if a1x_low  <= endx <= a1x_up and a1y_low <= endy <= a1y_up: # AOI 1
                    if self.x_loc == 1:
                        AOI_p.append(duration)
                        
                        #Add to AOI_p 
                    elif self.x_loc == 2:
                        AOI_x.append(duration)
                        
                        #add to AOI_x 
                    elif self.x_loc == 3:
                        AOI_q.append(duration)
                        
                        #add to AOI Q 
                    elif self.x_loc == 4:
                        AOI_y.append(duration)
                        #add to AOI y 
                        
                    
       
                elif a2x_low  <= endx <= a2x_up and a2y_low <= endy <= a2y_up: # AOI 2*
                    if self.x_loc == 1:
                        AOI_x.append(duration)
                        #add to aoi x 
                        
                    elif self.x_loc == 2:
                        AOI_p.append(duration)
                        #add to aoi p 
                        
                    elif self.x_loc == 3:
                        AOI_y.append(duration)
                        #add to aoi y 
                        
                    elif self.x_loc == 4:
                        AOI_q.append(duration)
                        #add to q AOI
                        
    
                elif a3x_low  <= endx <= a3x_up and a3y_low <= endy <= a3y_up: # AOI 3
                    if self.x_loc == 1:
                        AOI_q.append(duration)
                        
                        #add to aoi q 
                    elif self.x_loc == 2:
                        AOI_y.append(duration)
                        
                        #add to y
                    elif self.x_loc == 3:
                        AOI_p.append(duration)
                        
                        #add to p
                    elif self.x_loc == 4:
                        AOI_x.append(duration)
                        
                        #add to x
    
                elif a4x_low  <= endx <= a4x_up and a4y_low <= endy <= a4y_up: # AOI 4*
                    if self.x_loc == 1:
                        AOI_y.append(duration)
                        
                        #add to y
                    elif self.x_loc == 2:
                        AOI_q.append(duration)
                        
                        #add to q
                    elif self.x_loc == 3:
                        AOI_x.append(duration)
                        
                        #add to x
                    elif self.x_loc == 4:
                        AOI_p.append(duration)

                        
        
        #Bad and Good fixations
        total_fixations = len(fixations)
        good_fixations = len(AOI_p)+len(AOI_q)+len(AOI_x)+len(AOI_y)
        bad_fixations = total_fixations - good_fixations
        

            
        #Percentage for good and bad fixations
        if good_fixations != 0 or total_fixations != 0:
            perc_good_fix = ((good_fixations/total_fixations)*100)
        else:
            perc_good_fix = 0
        
        if bad_fixations != 0 or total_fixations != 0:
            perc_bad_fix = ((bad_fixations/total_fixations)*100)
        else:
            perc_bad_fix = 0
            
            
       
        
        #After every fixation has been put in their particular AOI process and return the AOIs_perc
        AOIs_perc = self.get_AOI_MT(AOI_p,AOI_q,AOI_x,AOI_y)
        
        #Return the AOI, percentanges for fixations and samples data
        return [AOIs_perc] + [perc_good_fix] + [perc_bad_fix] + fixations_samples[1:3]
    
        

      
class Subject: 
    def __init__(self,et_file_path,beh_file_path,subject_nr):
        self.et = et_file_path
        self.beh = beh_file_path
 #       print("Self.beh filepath = %s" %self.beh)
        
        self.subject_nr = subject_nr
        self.read_clean_files()
    
    def read_clean_files(self):
        
        #Load and create the dataframes(tables)
        self.et = check_et(self.et,self.subject_nr) #Clean eye tracking file of any possible errors and return the dataframe 

        self.beh = pd.read_csv(self.beh) #Read the table using pandas - this does not usually cause any problems or need cleaning
        
        # Use loc method in which the first argument (:) takes every row from the table and in the second argument takes only specific columns 
        
        self.beh = self.beh.loc[:,["correct","stimuli","response_time"]] # pick out only the required columns

    def get_trials(self): # This method return a list of indexes representing the start and end  of a trials in the et table
        
        
        trials = [] # a list of trial dataframes containing only the samples within the trial time period (i.e. gets rid of the junk samples between trials)
        trials_indexes = [] # Here we store the tuples with the start-end indexes
        ph = 0 #A place holder for start-trial index
        
        #temp_values = []
        ####   This may be temporary in case other columns have to be used if gamble may not be in the Event column
        self.et = self.et.loc[:,["TimeStamp","Event","GazePointX","GazePointY"]] # change the et dataframe to only include the given columns
        #####
        for i in self.et.index:          # Loop though the et table with the index           
            val = self.et.at[i,"Event"] # Pandas "at" method returns the value at that particular cell using the current row (i) and column name ("Event")
            if "Trial:" in str(val): # If gamble is in value then store the index // we need to not use "gamble" but the "Start_Trial" then we need to extract the 

                # also get the name of the stimuli
                
                
                if ph != 0:   # if ph !=0 then ph is start-Trial
                    trials_indexes.append((ph,i)) #Append the ph and the current index
                    ph = 0 #Reset
                else: # If ph is 0 then take the index of start-gamble
                    ph = i 
        
        if len(trials_indexes) < 150 :
            print("Warning! Subject %d has %d trials instead of 150 "%(self.subject_nr,len(trials_indexes)))
        for trial_index in trials_indexes:
            trials.append(pd.DataFrame(self.et.iloc[(trial_index[0]+1):trial_index[1]])) #Add the trial table to a list of table trials
                                                                                    # "iloc" is similiar to loc but it uses indexes, in this case the start and end of a particular trial in the et table 

        return trials

    def get_beh_data(self,current_trial_index): #This method return values from the beh file at the current index using the "at" method
        
        stim = self.beh.at[current_trial_index,"stimuli"]
        response_time = self.beh.at[current_trial_index,"response_time"]
        accuracy = self.beh.at[current_trial_index,"correct"]
        position = self.beh.at[current_trial_index,"position"]   
        
        return stim,response_time,accuracy,position
        
    def get_output(self):# this should be main method to return the dataframe for this current subject with all of his trials processed
        
        trials = self.get_trials() # Get the trials found from the subject table
        subject_table = []
        
        #Go through the trials tables and create a trial object, return the row for that trial
        for i,trial in enumerate(trials): 
            
            beh_data = self.get_beh_data(i) # Get the current row with the values we want from the beh file
            
            current_trial = Trial(trial,beh_data[0]) # Create an trial object with the trial table and the current x_loc

            AOIs_perc = current_trial.get_AOIs_perc_Perc() # Get the AOIs_perc from that trial
            
            row = [self.subject_nr] + [beh_data[3]] + [beh_data[2]] + AOIs_perc[0]  + [AOIs_perc[1]] + [AOIs_perc[2]] + [AOIs_perc[3]] + [AOIs_perc[4]] + [beh_data[4]]+[beh_data[1]] # Create the trial row using the AOI and the values extracted from beh
            
            subject_table.append(row) # Add the row to the subject table
            
        return subject_table