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

traffic_accident_stat_filename = sys.argv[1]
distance_travelled_by_means_of_transport_filename = sys.argv[2]

traffic_accident_stat_tmp_basename = os.path.basename(traffic_accident_stat_filename)
distance_travelled_by_means_of_transport_tmp_basename = \
    os.path.basename(distance_travelled_by_means_of_transport_filename)

traffic_accident_stat_stat_type = traffic_accident_stat_tmp_basename.replace("_"," ").replace(".csv","")
distance_travelled_by_means_of_transport_stat_type = \
    distance_travelled_by_means_of_transport_tmp_basename.replace("_"," ").replace(".csv","")
print(distance_travelled_by_means_of_transport_stat_type)

RLPTH_traffic_accidents = os.path.realpath(traffic_accident_stat_filename)
RLPTH_distance_travelled_by_means_of_transport = os.path.realpath(distance_travelled_by_means_of_transport_filename)
CWD = os.getcwd()
# print("RLPTH: " + RLPTH)
# print("CWD: " + CWD)
# print("tmp_basename: " + tmp_basename)
# print("stat_type: " + stat_type)

means_of_transport_font = fm.FontProperties(fname=CWD+'/verkehrsmittel_font_made_with_icomoon.ttf')

text_to_symbols_dictionary_DataFrame = pd.read_csv(
    CWD+'/Wörterbuch_Verkehrsmittel_Name_zu_Symbol.csv', names=["text", "symbols"], index_col="text")
text_to_symbols_dictionary = text_to_symbols_dictionary_DataFrame.squeeze()

traffic_accident_stat_pandas_matrix = pd.read_csv(RLPTH_traffic_accidents, sep=';', index_col=0, encoding='utf-8')

distance_travelled_by_means_of_transport_Series = pd.read_csv(RLPTH_distance_travelled_by_means_of_transport, \
            sep=';', encoding='utf-8', decimal=",", \
            index_col="entsprechendes Verkehrsmittel in der Unfallstatistik 2014-2019", usecols=[1, 2], squeeze=True)

distance_travelled_by_means_of_transport_reciprocal_Series = 1/(distance_travelled_by_means_of_transport_Series)
distance_travelled_by_means_of_transport_diag_matrix = pd.DataFrame(
    np.diag(distance_travelled_by_means_of_transport_reciprocal_Series),
    index=distance_travelled_by_means_of_transport_reciprocal_Series.index,
    columns=distance_travelled_by_means_of_transport_reciprocal_Series.index
)

print(distance_travelled_by_means_of_transport_diag_matrix)

traffic_accident_stat_pandas_matrix.rename(columns={'Unfälle insgesamt':'INSG'}, inplace=True)
traffic_accident_stat_pandas_matrix.rename(index={'Unfälle zwischen zwei Beteiligten insg.':'INSG'}, inplace=True)
traffic_accident_stat_pandas_matrix.rename(columns={'Unfälle_insgesamt':'INSG'}, inplace=True)
traffic_accident_stat_pandas_matrix.rename(index={'Unfälle_zwischen_zwei_Beteiligten_insg':'INSG'}, inplace=True)


# Löschen der Summen-Spalte/Zeile, die die Sicht verzerrt
# falls die Spalte/Zeile nicht existiert, soll aber auch kein Fehler ausgegeben werden
try:
   print("test")
   traffic_accident_stat_pandas_matrix.drop("INSG", axis=0, inplace=True)
   traffic_accident_stat_pandas_matrix.drop("INSG", axis=1, inplace=True)
except:
   pass

print(traffic_accident_stat_pandas_matrix)
print(type(traffic_accident_stat_pandas_matrix))


traffic_accident_stat_numpy_matrix = traffic_accident_stat_pandas_matrix.to_numpy()

traffic_accident_stat_per_billion_kms_pandas_matrix = \
    distance_travelled_by_means_of_transport_diag_matrix.dot(
        traffic_accident_stat_pandas_matrix.dot(distance_travelled_by_means_of_transport_diag_matrix))

print(traffic_accident_stat_per_billion_kms_pandas_matrix)

traffic_accident_stat_per_billion_kms_numpy_matrix = traffic_accident_stat_per_billion_kms_pandas_matrix.to_numpy()
traffic_accident_stat_per_billion_kms_numpy_matrix = traffic_accident_stat_per_billion_kms_numpy_matrix.round(decimals=2)

major_culprit_series = traffic_accident_stat_pandas_matrix.columns.to_series(index=np.arange(0, \
    len(traffic_accident_stat_pandas_matrix.columns.to_series())), name="major_culprit_series")
minor_culprit_series = traffic_accident_stat_pandas_matrix.index.to_series(index=np.arange(0,   \
    len(traffic_accident_stat_pandas_matrix.index.to_series())), name="minor_culprit_series")

for index, value in major_culprit_series.items():
   for text, symbols in text_to_symbols_dictionary.items():
       major_culprit_series[index] = major_culprit_series[index].replace(text, symbols)

   major_culprit_series[index] = major_culprit_series[index].replace(" ", "")

for index, value in minor_culprit_series.items():
   for text, symbols in text_to_symbols_dictionary.items():
       minor_culprit_series[index] = minor_culprit_series[index].replace(text, symbols)

   minor_culprit_series[index] = minor_culprit_series[index].replace(" ", "")

major_culprit = major_culprit_series.to_numpy()
minor_culprit = minor_culprit_series.to_numpy()

for index, value in major_culprit_series.items():
    major_culprit_series[index] = textwrap.fill(major_culprit[index], width=1)

fig, ax = plt.subplots(constrained_layout=True)
# cmap: Wistia, jet, brw, turbo

YlOrRdCmap = copy.deepcopy(cm.get_cmap('YlOrRd'))
YlOrRdCmap.set_bad((1,1,1))

im = ax.imshow(traffic_accident_stat_per_billion_kms_numpy_matrix, cmap=YlOrRdCmap, aspect='equal', \
              norm=colors.LogNorm(vmin=traffic_accident_stat_per_billion_kms_numpy_matrix.min()+0.1, \
                                  vmax=traffic_accident_stat_per_billion_kms_numpy_matrix.max()))
#              norm=colors.PowerNorm(gamma=0.3))

fig.suptitle("Anzahl der Verkehrs-Unfälle in Deutschland mit mehreren Beteiligten \n" + \
             traffic_accident_stat_stat_type + \
             "\n pro (Milliarden zurückgelegte Kilometer)^2", fontsize=12)
ax.set_title("laut Statistischem Bundesamt (Destatis), Fachserie 8 Reihe 7, \n" +
             "Kapitel 3. \"Beteiligte an Straßenverkehrsunfällen\" > \n" +
             "Kapitel 3.1 \"Alleinunfälle und Unfälle mit zwei Beteiligten nach Ortslage\" > \n" +
             "Kapitel 3.1.1 \"Nach Unfallverursacher und Unfallgegner\" \n", fontsize=9)
ax.set_xticks(np.arange(len(major_culprit)))
ax.set_yticks(np.arange(len(minor_culprit)))

ax.set_xticklabels(major_culprit, \
                   fontsize=24, \
                   fontproperties=means_of_transport_font, \
                   ha="center",
#                   va="bottom",
                   color="red",
                   wrap=True)
ax.set_yticklabels(minor_culprit, \
                   fontsize=24, \
                   fontproperties=means_of_transport_font, \
                   va="center",
                   ha="right",
                   color="blue")
ax.set_xlabel("Fortbewegungsmittel des Hauptverursachers/Täters", color="red")
ax.set_ylabel("Fortbewegungsmittel des Nebenverursachers/Opfers", color="blue")

ax.tick_params(axis='x', which='major', pad=3)
ax.tick_params(axis='y', which='major', pad=3)

ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

for i in range(len(major_culprit)):
    for j in range(len(minor_culprit)):
        text = ax.text(j, i, traffic_accident_stat_per_billion_kms_numpy_matrix[i, j], ha="center", va="center", \
                       color="black", fontsize=8)

ax.grid(axis="x", which="minor", color="grey", alpha=.5, linewidth=3, linestyle=":")
ax.grid(axis="y", which="minor", color="grey", alpha=.5, linewidth=3, linestyle=":")

plt.show()
plt.tight_layout()
