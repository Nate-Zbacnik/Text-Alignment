# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 12:32:39 2019

@author: NATE

This program implements a text search algorithm via local alignment, using a 
scoring method and dynamic programming implementation to find good matches in a
long piece of text to an input string given by the user. The comparison between
the input and the best string match is given. The scoring scheme is +20 for a
match, and -30 for a gap in either the text or or the searched string.
"""


import numpy as np



#import the text file
#text_loc = r'C:\Users\NATE\Documents\alignment.txt' UNCOMMENT

#text_op = open(text_loc)
#text = text_op.read() 
text = 'Tennis is a racket sport that can be played individually against a single opponent \
 (singles) or between two teams of two players each (doubles). Each player uses a tennis \
 racket that is strung with cord to strike a hollow rubber ball covered with felt over or \
 around a net and into the opponents court. The object of the game is to maneuver the ball \
 in such a way that the opponent is not able to play a valid return. The player who is  \
 unable to return the ball will not gain a point, while the opposite player will. Tennis\
 is an Olympic sport and is played at all levels of society and at all ages. \
 The sport can be played by anyone who can hold a racket, including wheelchair users.\
 The modern game of tennis originated in Birmingham, England, in the late 19th century\
 as lawn tennis. It had close connections both to various field (lawn) games such as \
 croquet and bowls as well as to the older racket sport today called real tennis. During\
 most of the 19th century, in fact, the term tennis referred to real tennis, not lawn\
 tennis. The rules of modern tennis have changed little since the 1890s. Two exceptions \
 are that from 1908 to 1961 the server had to keep one foot on the ground at all times,\
 and the adoption of the tiebreak in the 1970s. A recent addition to professional tennis\
 has been the adoption of electronic review technology coupled with a point-challenge\
 system, which allows a player to contest the line call of a point, a system known as\
 Hawk-Eye. Tennis is played by millions of recreational players and is also a popular\
 worldwide spectator sport. The four Grand Slam tournaments (also referred to as the\
 Majors) are especially popular: the Australian Open played on hard courts, the French \
 Open played on red clay courts, Wimbledon played on grass courts, and the US Open also\
 played on hard courts.'
 #text.capitalize() #Optional caps for matching without case(doesnt work??)


  
#This function calls text_table and then (not yet) reconstructs the best alignments from the table
def align_text(text,search_str): 
    val_table = fill_table(text,search_str)
    loc = np.argmax(val_table) #best alignment value
    val = np.amax(val_table)
    y_loc = loc % np.shape(val_table)[1]
    x_loc = int((loc -y_loc)/np.shape(val_table)[1])
    
    match_str = ''
    match_txt = ''
    k = 0
    l=0
    i = 0
    while i <len(search_str):
        if x_loc < len(search_str) - i:
            match_str = match_str + search_str[len(search_str)-i - 1]
            match_txt = match_txt + ' ' #text[y_loc+len(search_str)-1-i-x_loc]
        else:
            txt_gap_val = val_table[len(search_str)-i ,y_loc+len(search_str)-1-i-x_loc-l+k]
            str_gap_val = val_table[len(search_str)-i - 1,y_loc+len(search_str)-i-x_loc-l+k]
            match_val = val_table[len(search_str)-i - 1,y_loc+len(search_str)-1-i-x_loc-l+k]
            #print(txt_gap_val, str_gap_val, match_val)
            if match_val >= str_gap_val and match_val >= txt_gap_val:
                match_str = match_str + search_str[len(search_str)-i - 1]
                match_txt = match_txt + text[y_loc+len(search_str)-i-1-x_loc-l+k]
            elif str_gap_val > txt_gap_val:
                
                match_str = match_str + search_str[len(search_str)-i -1] 
                match_txt = match_txt + '_'
                k+=1 #need to just move up, not up n left
                
            else:
                match_str = match_str + '_'
                match_txt = match_txt + text[y_loc+len(search_str)-i-1-x_loc-l+k]
                l+=1 #move left
                i-=1 #but not up
        i+=1
            
            
    #print(loc)
    #print(np.shape(val_table))
    print(x_loc, y_loc)
    print(val)
    print(val_table[:,0:10])
    print('Search String: ' + ''.join(reversed(match_str)))
    print('Best Match:    ' + ''.join(reversed(match_txt)))
    
#This function dynamically creates the table of matching scores from the string and text   
def fill_table(text,search_str):
    val_table = np.zeros((len(search_str)+1,len(text)+1)) #+1 for empty str
    
    for row in range(len(search_str)):
        for col in range(len(text)):
            if search_str[row] == text[col]:
                val_table[row+1,col+1] = max([\
                         val_table[row,col] + 20, \
                         val_table[row+1,col] -30, \
                         val_table[row,col+1] -30, \
                         0 \
                         ])#MAX of case with character agreement
            else:
                val_table[row+1,col+1] =max([\
                         val_table[row,col] - 30, \
                         val_table[row+1,col] -30, \
                         val_table[row,col+1] -30, \
                         0 \
                         ])#MAX of case without agreement
    
    return val_table


#User interface
while True:
    search_str = input('string to search for(input \'break\' to break): ')

    if search_str == 'break':
        break
    #search_str = search_str.capitalize() #Optional caps for matching without case
    align_text(text,search_str)
    

    
