#!/usr/bin/python
import csv
import re
from scipy.sparse import csr_matrix 

def getWinDict(path):
    teams={}
    map={}
    count=0
    winSparse={}
    losses={}    
    
    with open(path,'rb') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        for row in csv_reader:
            ### remove rankings, create map of teams/integer ###
            win = re.sub("^\(.*\) ", "",row[5])
            lose = re.sub("^\(.*\) ", "",row[8])
           # get the map from team name to id, id to team name 
            if win not in teams:
                teams[win]=count
                map[count]=win
                losses[count]=0
                count+=1
            if lose not in teams:
                teams[lose]=count
                map[count]=lose
                losses[count]=0
                count+=1   
            value = 1
            #### extra point for a blowout ###
            #if int(row[6])-int(row[9])>10: value+=0.5
            #### extra point for a win on the road ###
            #if row[7]=="@": value+=0.5       
            ### create sparse matrix for each loser - increment number of wins ###
            if teams[lose] not in winSparse: 
                winSparse[teams[lose]]={} 
    	    #winSparse[teams[lose]][teams[lose]]=1
            if teams[win] not in winSparse[teams[lose]]:
                winSparse[teams[lose]][teams[win]]=0
            winSparse[teams[lose]][teams[win]]+=value
            losses[teams[lose]]+=value 
      
    return([teams, losses, winSparse, map])

### to generate a scipy sparse matrix 
def getH(dict_list):    
    teams = dict_list[0]
    losses = dict_list[1]
    winSparse = dict_list[2]
    
    col = []
    row = []
    data = []
    for i in range(0, len(teams)):
        for j in range(0, len(teams)):        
            if (i in winSparse) and (j in winSparse[i]):
                data.append((float(winSparse[i][j])/max(13,losses[i])))
                row.append(i)
                col.append(j) 
                
    N = len(teams)
    H = csr_matrix((data, ( row, col)), shape = (N,N))      
    return(H)               

