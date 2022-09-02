# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 16:41:08 2022

@author: F413Y
"""

import os, sys
from music21 import converter, instrument, note, chord, stream
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import sys

min=sys.maxsize
max=-sys.maxsize

input=['C3.E3.G3','G3.B3.D3','A3.C4.E4','E3.G3.B3','F3.A3.C4','C3.E3.G3','F3.A3.C4','G3.B3.D3']

folder = 'data/test'
notes = []

def extract_notes(s):

    as_chords = s.chordify()
    notes = []
    note_list=[]
    input_chords=[]
    for i in as_chords.recurse():
        if isinstance(i, note.Note):
            p = str(i.pitch)
            notes.append((p, i.duration.quarterLength))
        elif isinstance(i, chord.Chord):
            ps = '.'.join(str(n.pitch) for n in i.notes)
            note_list=ps.split('.')
            if(len(note_list)>3):
                ps_chord=note_list[0]+'.'+note_list[1]+'.'+note_list[2]
                input_chords.append((ps_chord,note_list[3]))
                
                # print(input_chords)
            notes.append((ps, i.duration.quarterLength))

    return notes,input_chords

def note_repeat(note_list):
    pre_note=[]
    repeat_num=0
    total_note_length=len(note_list)
    for i in range(len(note_list)):
        now_note=note_list[i][1]
        if i>0 and pre_note==now_note:
            repeat_num+=1
        pre_note=note_list[i][1]
    note_repeat_pro=repeat_num/total_note_length
    return note_repeat_pro

# def scale_consistency(note_list):
    

# def now_pro (X):
#     if(list(X[0][0]).startwith('C')):
#         pro_0+=1

# folder = 'test'
notes = []
for f in os.listdir(folder):
    fp = os.path.join(folder, f)
    midi_stream = converter.parse(fp)
    ns = extract_notes(midi_stream)
    notes += ns


total_note_chord=[]
total_chord=[]
for i in range (1,len(notes),2): 
    for j in range(len(notes[i])):
        total_note_chord.append(notes[i][j])
        total_chord.append(notes[i][j][0])
diversity_chord=set(total_chord)
showone_chord=[]
for i in diversity_chord:
    num=total_chord.count(i)
    if num<=5:
        showone_chord.append(i)
# print("独特和弦百分比：",len(showone_chord)/len(diversity_chord))
properties=note_repeat(total_note_chord)
print("音符的重复比：",properties)