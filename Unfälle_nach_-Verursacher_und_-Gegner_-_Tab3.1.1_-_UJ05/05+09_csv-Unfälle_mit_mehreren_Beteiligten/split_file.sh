#/usr/bin/bash

FILE=$(realpath "$1")

DIR_NAME=$(dirname "$FILE")
STAT_TYPE=$(basename -s .csv "$FILE") 
YEAR=$(echo $STAT_TYPE | grep -o -E "[0-9]{4}")

FILEPART01="${DIR_NAME}/mit_Getöteten/mit_Getöteten,_innerorts,_${YEAR}.csv" 
FILEPART02="${DIR_NAME}/mit_Getöteten/mit_Getöteten,_außerorts,_${YEAR}.csv" 
FILEPART03="${DIR_NAME}/mit_Getöteten/mit_Getöteten,_inner-_und_außerorts,_${YEAR}.csv" 
FILEPART04="${DIR_NAME}/mit_Personenschaden/mit_Personenschaden,_innerorts,_${YEAR}.csv" 
FILEPART05="${DIR_NAME}/mit_Personenschaden/mit_Personenschaden,_außerorts,_${YEAR}.csv" 
FILEPART06="${DIR_NAME}/mit_Personenschaden/mit_Personenschaden,_inner-_und_außerorts,_${YEAR}.csv" 
FILEPART07="${DIR_NAME}/schwerwiegend_und_mit_Sachschaden/schwerwiegend_und_mit_Sachschaden,_innerorts,_${YEAR}.csv" 
FILEPART08="${DIR_NAME}/schwerwiegend_und_mit_Sachschaden/schwerwiegend_und_mit_Sachschaden,_außerorts,_${YEAR}.csv" 
FILEPART09="${DIR_NAME}/schwerwiegend_und_mit_Sachschaden/schwerwiegend_und_mit_Sachschaden,_inner-_und_außerorts,_${YEAR}.csv" 
FILEPART10="${DIR_NAME}/mit_Getöteten/mit_Getöteten,_auf_Autobahnen,_${YEAR}.csv" 
FILEPART11="${DIR_NAME}/mit_Personenschaden/mit_Personenschaden,_auf_Autobahnen,_${YEAR}.csv" 
FILEPART12="${DIR_NAME}/schwerwiegend_und_mit_Sachschaden/schwerwiegend_und_mit_Sachschaden,_auf_Autobahnen,_${YEAR}.csv" 

echo "$FILEPART01" 
echo "$FILEPART02" 
echo "$FILEPART03" 
echo "$FILEPART04" 
echo "$FILEPART05" 
echo "$FILEPART06" 
echo "$FILEPART07" 
echo "$FILEPART08" 
echo "$FILEPART09" 
echo "$FILEPART10" 
echo "$FILEPART11" 
echo "$FILEPART12" 


sed -n '1,15p'    "$FILE" > $FILEPART01
sed -n '16,30p'   "$FILE" > $FILEPART02
sed -n '31,45p'   "$FILE" > $FILEPART03
sed -n '46,60p'   "$FILE" > $FILEPART04
sed -n '61,75p'   "$FILE" > $FILEPART05
sed -n '76,90p'   "$FILE" > $FILEPART06
sed -n '91,105p'  "$FILE" > $FILEPART07
sed -n '106,120p' "$FILE" > $FILEPART08
sed -n '121,135p' "$FILE" > $FILEPART09
sed -n '136,150p' "$FILE" > $FILEPART10
sed -n '151,165p' "$FILE" > $FILEPART11
sed -n '166,180p' "$FILE" > $FILEPART12

