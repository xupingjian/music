# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 21:00:46 2022

@author: F413Y
"""

import sys, os, midi, math, string, time


min=sys.maxsize
max=-sys.maxsize

GENRE      = 0
COMPOSER   = 1
SONG_DATA  = 2

# INDICES IN BATCHES:
LENGTH     = 0
FREQ       = 1
VELOCITY   = 2
TICKS_FROM_PREV_START      = 3

# INDICES IN SONG DATA (NOT YET BATCHED):
BEGIN_TICK = 3
CHANNEL    = 4

debug = ''
#debug = 'overfit'


base_tones = {'C':   0,
              'C#':  1, 
              'D':   2,
              'D#':  3,
              'E':   4,
              'F':   5,
              'F#':  6,
              'G':   7,
              'G#':  8,
              'A':   9,
              'A#': 10,
              'B':  11}

scale = {}
#Major scale:
scale['major'] = [0,2,4,5,7,9,11]
#(W-W-H-W-W-W-H)
#(2 2 1 2 2 2 1)

#Natural minor scale:
scale['natural_minor'] = [0,2,3,5,7,8,10]
#(W-H-W-W-H-W-W)
#(2 1 2 2 1 2 2)
 
#Harmonic minor scale:
scale['harmonic_minor'] = [0,2,3,5,7,8,11]
#(W-H-W-W-H-WH-H)
#(2 1 2 2 1 3 1)

tone_names = {}
for tone_name in base_tones:
  tone_names[base_tones[tone_name]] = tone_name


def get_tones(midi_pattern):
  """
  returns a dict of statistics, keys: [scale_distribution,
  """
  
  tones = []
  
  for track in midi_pattern:
    for event in track:
      if type(event) == midi.events.SetTempoEvent:
        pass # These are currently ignored
      elif (type(event) == midi.events.NoteOffEvent) or \
           (type(event) == midi.events.NoteOnEvent and \
            event.velocity == 0):
        pass # not needed here
      elif type(event) == midi.events.NoteOnEvent:
        tones.append(event.data[0])
  return tones 

def get_midi_pattern(filename):
  try:
    return midi.read_midifile(filename)
  except:
    print ('Error reading {}'.format(filename))
    return None

def tones_to_scales(tones):
  """
   Midi to tone name (octave: -5):
   0: C
   1: C#
   2: D
   3: D#
   4: E
   5: F
   6: F#
   7: G
   8: G#
   9: A
   10: A#
   11: B

   Melodic minor scale is ignored.

   One octave is 12 tones.
  """
  counts = {}
  for base_tone in base_tones:
    counts[base_tone] = {}
    counts[base_tone]['major'] = 0
    counts[base_tone]['natural_minor'] = 0
    counts[base_tone]['harmonic_minor'] = 0

  if not len(tones):
    frequencies = {}
    for base_tone in base_tones:
      frequencies[base_tone] = {}
      for scale_label in scale:
        frequencies[base_tone][scale_label] = 0.0
    return frequencies
  for tone in tones:
    for base_tone in base_tones:
      for scale_label in scale:
        if tone%12-base_tones[base_tone] in scale[scale_label]:
          counts[base_tone][scale_label] += 1
  frequencies = {}
  for base_tone in counts:
    frequencies[base_tone] = {}
    for scale_label in counts[base_tone]:
      frequencies[base_tone][scale_label] = float(counts[base_tone][scale_label])/float(len(tones))
  return frequencies

folder = 'data/test'
total_note=[]
for f in os.listdir(folder):
    fp = os.path.join(folder, f)
    note_pattern=get_midi_pattern(fp)
    note_tones=get_tones(note_pattern)
    total_note.append(note_tones)
total_notes=[]
for i in range(len(total_note)):
    for j in total_note[i]:
        if j<min:
            min=j
        if j>max:
            max=j
        total_notes.append(j)
diversity_note=set(total_notes)
showone_note=[]
for i in diversity_note:
    num=total_notes.count(i)
    if num<3:
        showone_note.append(i)
print("独特音符百分比：",len(showone_note)/len(diversity_note))
print("音符种类：",len(diversity_note))
print("音调跨度：",(max-min)/12)
freq=tones_to_scales(total_notes)