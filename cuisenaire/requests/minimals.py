#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
last modified: aug 9, 2022

@author: katie

double false minimal polynomials with the same largest rod
"""

import pandas as pd
import ast

blank = pd.DataFrame({'seed': [''], 'growth': [''],
                      'minimal': [''], 'shift': ['']},
                     columns = ['seed', 'growth', 'minimal', 'shift'])

df = pd.read_csv('/Users/katie/Desktop/max5_35.txt', sep = '\t',
                 names = ['seed', 'growth', 'minimal', 'shift'],
                 converters = {'seed': ast.literal_eval})

grouped = df.groupby('growth')

gathered = []
for growth, shift in grouped:
    if ('1' not in shift['shift'].values) and (shift.shape[0] > 1):
        gathered.append(shift)
        
interest = pd.concat(gathered)

grouped = interest.groupby('growth')

gathered = []
for growth, shift in grouped:
    if not shift.seed.apply(max).is_unique:
        maxes = shift.seed.apply(max)
        repeats = maxes[maxes.duplicated(keep = False)]
        
        if min(maxes.to_list()) == min(repeats.to_list()):
            gathered.append(shift)
            gathered.append(blank)
        
second_interest = pd.concat(gathered)