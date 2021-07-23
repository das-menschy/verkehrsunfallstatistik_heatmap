#!/usr/bin/python3

import pandas as pd
import os
import sys

file = sys.argv[1] 
dir_name = os.path.dirname(file) 
filename = os.path.basename(file) 
filename_without_ending = filename.replace(".csv", "") 



df = pd.read_csv(file, sep=";") 
df_reorder = df[['Unfälle mit Getöteten - Innerhalb von Ortschaften', 'Fußgänger', 'Fahrrad', 'Mofa, Moped', 'Motorrad', 'Personenkraftwagen', 'Kraftomnibus, Obus', 'Liefer- und Lastkraftw.', 'Sattelschlepper', 'Landwirt. Zugmaschine', 'andere Zugmaschine', 'LKW mit Spezialaufbau', 'anderes Fahrzeug', 'sonstige Person', 'Unfälle insgesamt']]

df_reorder.to_csv(dir_name + "/" + filename_without_ending + "_-_reordered.csv", index=False, sep=";") 
