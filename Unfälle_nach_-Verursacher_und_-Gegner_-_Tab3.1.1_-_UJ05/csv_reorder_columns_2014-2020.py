#!/usr/bin/python3

import pandas as pd
import os
import sys

file = sys.argv[1] 
dir_name = os.path.dirname(file) 
filename = os.path.basename(file) 
filename_without_ending = filename.replace(".csv", "") 



df = pd.read_csv(file, sep=";") 
df_reorder = df[['Unfälle mit Getöteten - Innerhalb von Ortschaften', 'Fußgänger 5', 'Fahrrad 4', 'Kraftrad mit Versicherungskennzeichen 1', 'Kraftrad mit amtlichem Kennzeichen 2', 'Personenkraftwagen', 'Bus', 'Lastkraftwagen 3 bis einschließlich 3,5t', 'Lastkraftwagen 3 über 3,5t', 'Sattelzugmaschine', 'übriges Güterkraftfahrzeug', 'Landwirt. Zugmaschine', 'Straßenbahn', 'anderer Verkehrsteilnehmer', 'Unfälle insgesamt']]

df_reorder.to_csv(dir_name + "/" + filename_without_ending + "_-_reordered.csv", index=False, sep=";") 
