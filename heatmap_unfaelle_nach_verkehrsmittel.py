#!/usr/bin/python3
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import cm
import matplotlib.font_manager as fm
import textwrap
import copy
from matplotlib.colors import LogNorm

filename = sys.argv[1]
tmp_basename = os.path.basename(filename)
stat_type = tmp_basename.replace("_"," ").replace(".csv","")
RLPTH = os.path.realpath(filename)
CWD = os.getcwd()
# print("RLPTH: " + RLPTH)
# print("CWD: " + CWD)
# print("tmp_basename: " + tmp_basename)
# print("stat_type: " + stat_type)

verkehrsmittel_font = fm.FontProperties(fname=CWD+'/verkehrsmittel_font_made_with_icomoon.ttf')

text_to_symbols_dictionary_DataFrame = pd.read_csv(
    CWD+'/Wörterbuch_Verkehrsmittel_Name_zu_Symbol.csv', names=["text", "symbols"], index_col="text")
text_to_symbols_dictionary = text_to_symbols_dictionary_DataFrame.squeeze()

Verkehrsunfaelle_pandas_matrix = pd.read_csv(RLPTH, sep=';', index_col=0, encoding='utf-8')

Verkehrsunfaelle_pandas_matrix.rename(columns={'Unfälle insgesamt':'INSG'}, inplace=True)
Verkehrsunfaelle_pandas_matrix.rename(index={'Unfälle zwischen zwei Beteiligten insg.':'INSG'}, inplace=True)
Verkehrsunfaelle_pandas_matrix.rename(columns={'Unfälle_insgesamt':'INSG'}, inplace=True)
Verkehrsunfaelle_pandas_matrix.rename(index={'Unfälle_zwischen_zwei_Beteiligten_insg':'INSG'}, inplace=True)


# Löschen der Summen-Spalte/Zeile, die die Sicht verzerrt
# falls die Spalte/Zeile nicht existiert, soll aber auch kein Fehler ausgegeben werden
try:
   print("test")
   Verkehrsunfaelle_pandas_matrix.drop("INSG", axis=0, inplace=True)
   Verkehrsunfaelle_pandas_matrix.drop("INSG", axis=1, inplace=True)
except:
   pass

print(Verkehrsunfaelle_pandas_matrix)
print(type(Verkehrsunfaelle_pandas_matrix))


Verkehrsunfaelle_numpy_matrix = Verkehrsunfaelle_pandas_matrix.to_numpy()


Hauptverursacher_series = Verkehrsunfaelle_pandas_matrix.columns.to_series(index=np.arange(0, \
    len(Verkehrsunfaelle_pandas_matrix.columns.to_series())), name="Hauptverursacher_series")
Nebenverursacher_series = Verkehrsunfaelle_pandas_matrix.index.to_series(index=np.arange(0,   \
    len(Verkehrsunfaelle_pandas_matrix.index.to_series())), name="Nebenverursacher_series")

for index, value in Hauptverursacher_series.items():
   for text, symbols in text_to_symbols_dictionary.items():
       Hauptverursacher_series[index] = Hauptverursacher_series[index].replace(text, symbols)

   Hauptverursacher_series[index] = Hauptverursacher_series[index].replace(" ", "")

for index, value in Nebenverursacher_series.items():
   for text, symbols in text_to_symbols_dictionary.items():
       Nebenverursacher_series[index] = Nebenverursacher_series[index].replace(text, symbols)

   Nebenverursacher_series[index] = Nebenverursacher_series[index].replace(" ", "")

Hauptverursacher = Hauptverursacher_series.to_numpy()
Nebenverursacher = Nebenverursacher_series.to_numpy()

for index, value in Hauptverursacher_series.items():
    Hauptverursacher_series[index] = textwrap.fill(Hauptverursacher[index], width=1)

fig, ax = plt.subplots(constrained_layout=True)
# cmap: Wistia, jet, brw, turbo

YlOrRdCmap = copy.deepcopy(cm.get_cmap('YlOrRd'))
YlOrRdCmap.set_bad((1,1,1))

im = ax.imshow(Verkehrsunfaelle_numpy_matrix, cmap=YlOrRdCmap, aspect='equal', \
               norm=colors.LogNorm(vmin=Verkehrsunfaelle_numpy_matrix.min()+1, vmax=Verkehrsunfaelle_numpy_matrix.max()))
#               norm=colors.PowerNorm(gamma=0.5))

fig.suptitle("Anzahl der Verkehrs-Unfälle in Deutschland mit mehreren Beteiligten", fontsize=12)
ax.set_title(stat_type + ",\n laut DESTATIS Fachserie 8 Reihe 7 Seite 99/100", fontsize=9)
ax.set_xticks(np.arange(len(Hauptverursacher)))
ax.set_yticks(np.arange(len(Nebenverursacher)))

ax.set_xticklabels(Hauptverursacher, \
                   fontsize=24, \
                   fontproperties=verkehrsmittel_font, \
                   ha="center",
#                   va="bottom",
                   color="red",
                   wrap=True)
ax.set_yticklabels(Nebenverursacher, \
                   fontsize=24, \
                   fontproperties=verkehrsmittel_font, \
                   va="center",
                   ha="right",
                   color="blue")
ax.set_xlabel("Fortbewegungsmittel des Hauptverursachers/Täters", color="red")
ax.set_ylabel("Fortbewegungsmittel des Nebenverursachers/Opfers", color="blue")

ax.tick_params(axis='x', which='major', pad=3)
ax.tick_params(axis='y', which='major', pad=3)

ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

for i in range(len(Hauptverursacher)):
    for j in range(len(Nebenverursacher)):
        text = ax.text(j, i, Verkehrsunfaelle_numpy_matrix[i, j], ha="center", va="center", color="black", fontsize=8)

ax.grid(axis="x", which="minor", color="grey", alpha=.5, linewidth=3, linestyle=":")
ax.grid(axis="y", which="minor", color="grey", alpha=.5, linewidth=3, linestyle=":")

plt.show()
plt.tight_layout()
