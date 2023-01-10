import matplotlib.pyplot as plt
import sys
import math
import time
import itertools
import tkinter as tk
from tkinter import ttk
import pandas
import warnings

def Header():
    print()
    print('00=================00')
    print('||                 ||')
    print('|| ARE YOU THE ONE ||')
    print('||                 ||')
    print('00=================00')
    print('\nLösungsskript')
    print('Made by Alex/Pheagan \n')

def ImportExcelData(fileName):
    candidatesXL = pandas.read_excel(fileName, sheet_name="TeilnehmerInnen")
    matchBoxesXl = pandas.read_excel(fileName, sheet_name="Matchboxen")
    matchingNightsXL = pandas.read_excel(fileName, sheet_name="MatchingNights")

    # Evaluate Candidates
    groupA = []
    for i in range(0,10):
        groupA.append( candidatesXL.values[i+1, 2] )
    groupB = []
    for i in range(0,11):
        groupB.append( candidatesXL.values[i+1, 5] )

    if candidatesXL.values[13,4] == "ja":
        bonusPersonKnown = True
    else:
        bonusPersonKnown = False

    # Evaluate Matchboxes
    YesMatches = []
    NoMatches = []
    for i in range(0,20):
        matchResult = matchBoxesXl.values[2+i, 4]
        if matchResult == 'ja':
            matchA = matchBoxesXl.values[2+i, 2] # Name
            matchB = matchBoxesXl.values[2+i, 3] # Name
            matchA_ID = groupA.index(matchA) # ID
            matchB_ID = groupB.index(matchB) # ID
            yesMatchIDs = [ matchA_ID, matchB_ID ] # ID von PersonA/PersonB
            YesMatches.append( yesMatchIDs )

            # Überprüfen ob einzigartiges Match
            # Wenn ja, dann hat PersonA automatisch alle anderen PersonenB als NoMatch
            uniqueMatch = matchBoxesXl.values[2+i, 6];
            if uniqueMatch == 'ja':
                for b in range(0, len(groupB) ):
                    if b != matchB_ID:
                        NoMatches.append([ matchA_ID, b ])

        elif matchResult == 'nein':
            noMatch = [ matchBoxesXl.values[2+i, 2], matchBoxesXl.values[2+i, 3] ]
            NoMatches.append( [ groupA.index(noMatch[0]), groupB.index(noMatch[1]) ] )

    matchingNights = []
    correctMatches = []
    # Evaluate MatchingNights
    for i in range(0,10):
        matchValueTmp = matchingNightsXL.values[ 5*i+4 ,14]
        if math.isnan(matchValueTmp):
            continue
        correctMatches.append(matchValueTmp)
        combination = []
        for k in range(0,10):
            partner = matchingNightsXL.values[ 5*i+4 ,3+k]
            combination.append( groupB.index(partner) )
        matchingNights.append(combination)

    return [groupA, groupB, YesMatches, NoMatches, matchingNights, correctMatches, bonusPersonKnown]

def printProgress (iteration, total, decimals = 1):
    percent =("{0:." + str(decimals) + "f}").format(100 * (iteration / total))
    printEnd = "\r"
    print(f'\rFortschritt: {percent}%', end = printEnd)
    if iteration == total: 
        print()

def CheckMatches(matchCombination, bekannteMatches, ignoreExtraPerson):
    # Für jedes Match wird überprüft, ob in der Kombination der Eintrag von Person-B ihr Match Person-A ist
    # Ist ein Match nicht enthalten => Kombination nicht möglich
    for [match_a,match_b] in bekannteMatches:
        if ignoreExtraPerson and match_b == 10: # Bei erstem 10x10 Test Infos bezüglich der Zusatzperson ignorieren
            continue
        elif matchCombination[match_b] != match_a:
            return False
    return True # Kein Ausschlusskriterium zutreffend => Kombination möglich

def CheckNoMatches(matchCombination, bekannteNoMatches, ignoreExtraPerson):
    # Für jedes No-Match wird überprüft, ob in der Kombination der Eintrag von Person-B ein No-Match Person-A ist
    # Ist ein No-Match enthalten => Kombination nicht möglich
    for [match_a,match_b] in bekannteNoMatches:
        if ignoreExtraPerson and match_b == 10: # Bei erstem 10x10 Test Infos bezüglich der Zusatzperson ignorieren
            continue
        elif matchCombination[match_b] == match_a: 
            return False
    return True # Kein Ausschlusskriterium zutreffend => Kombination möglich

def CheckMatchingNights(matchCombination, matchingNights, correctMatches):
    # Übereinstimmungen zwischen Kombination und Matchingnight zählen
    # Schauen, ob Übereinstimmungen = korrekte Matches in der Nacht
    # sonst ist Kombination nicht möglich
    for night in range(0,len(matchingNights)):
        uebereinstimmungen = 0
        for a in range(0,len(matchingNights[night])):
            match_a = a;
            match_b = matchingNights[night][a];
            
            if matchCombination[match_b] == match_a:
                uebereinstimmungen += 1

        if uebereinstimmungen != correctMatches[night]:
            return False
    return True # Kein Ausschlusskriterium zutreffend => Kombination möglich

def ClickBtn(allCombinations, button_frame, manualMatches, label_count, index):
    # Knopf gedrückt, Zeile = Person aus Gruppe B, Spalte = Person aus Gruppe A
    if index in manualMatches:
        manualMatches.remove(index)
    else:
        manualMatches.append(index)

    # reducedCombination = Liste mit Berücksichtigung der manuellen Matches
    reducedCombinations = []
    for combination in allCombinations:
        isCombinationValid = True
        for match in manualMatches: # durch alle manuellen Matches durchgehen und schauen ob alle dabei sind
            if combination[match[0]] != match[1]:
                isCombinationValid = False
        if isCombinationValid: # nur die Kombinationen hinzufügen, die alle manuellen Matches enthalten
            reducedCombinations.append(combination)

    # Labelcount für Kombinationen
    if extraPerson_isKnown:
        labelCount = len(reducedCombinations)
    else:
        labelCount = int( len(reducedCombinations)/2 )
    label_count.config( text = 'Nacht ' + str(len(matchingNights)) + ', noch ' + str(labelCount) + ' Kombinationen')

    # Matchmatrix neu berechnen basierend aus Ausgewähltem Match
    newMatchMatrix = [[0 for _ in range(10)] for _ in range(11)] # leere 11x10 Matrix
    for combination in reducedCombinations:
        for i in range (0, len(combination)):
            newMatchMatrix[i][combination[i]] += 1


    combinations_left = len(reducedCombinations)
    if combinations_left == 0:
        combinations_left = 1

    for row in range(0,len(newMatchMatrix)):
        for col in range(0,len(newMatchMatrix[0])):
            newMatchMatrix[row][col] = round(newMatchMatrix[row][col]*100/combinations_left,1)

    UpdateMatrix(newMatchMatrix, button_frame, manualMatches)

def UpdateMatrix(matchMatrix, button_frame, manualMatches):     
    for row in range (0, len(button_frame)):
        for column in range (0, len(button_frame[0])):
            # Durch alle Durchgehen und aktivieren / deaktivieren und Farbe anpassen

            value = matchMatrix[row][column]
            button_frame[row][column].config(text=str(value))
            BtnColor = "lightyellow"
            BtnState = "normal"
            if(value == 0):
                BtnColor = "white"
                BtnState = "disabled"                
            elif(value == 100):
                if [row, column] in manualMatches:
                    BtnColor = "lawngreen"
                else:
                    BtnColor = "lightgreen"
                    BtnState = "disabled"  

            elif(value >= 50):
                BtnColor = "bisque"
            
            button_frame[row][column].config(bg=BtnColor)
            button_frame[row][column]["state"] = BtnState

# Programmstart
starttime = time.time()
Header()

# The Excel file contains Data Validations for only allowing Names of the participant for Macht-Boxes or -nights
# These can not be processed by openpyxl (which is not needed here), so the warning will be ignored to not show up in the console
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
excelData = ImportExcelData("AYTO_Data.xlsx")

gruppeA = excelData[0]
gruppeB = excelData[1]
bekannteMatches = excelData[2]
bekannteNoMatches = excelData[3]
matchingNights = excelData[4]
correctMatches = excelData[5]
extraPerson_isKnown = excelData[6]

lenA = len(gruppeA)
lenB = len(gruppeB)
n_combination = math.factorial( lenA )* lenA
if not extraPerson_isKnown:
    n_combination = n_combination*lenB # eigentlich lenB/2 da durch doppelte Person zwei Kombinationen identisch sind, ich prüfe aber aktuell noch alle

print('Teilnehmer:')
print('Gruppe A: ' + str(gruppeA))
print('Gruppe B: '+ str(gruppeB))
print('Insgesammt mögliche Kombinationen: ' + str(n_combination))
print()

print('Weitere Daten:')
print('Bekannte Matches: ' + str(len(bekannteMatches)))
print('Bekannte No-Matches: ' + str(len(bekannteNoMatches)))
print('Matching-Nights: ' + str(len(matchingNights)))
print('Nacht-Ergebnisse: ' + str(len(correctMatches)))
print()


# MatchMatrix erstellen 10x10
# MatchMatrix aus Sicht der größeren Gruppe, weil da nur exakt Eintrag (eine Person aus der Kleinen Gruppe hat zwei Einträge)
listA = []
for b in range(0,lenA): 
    listA.append(b);
permutations_list_10x10 = list( itertools.permutations(listA) )

possibleBonusIDs = []
if extraPerson_isKnown:
    possibleBonusIDs.append( lenB-1 ) # letzter Eintrag in Gruppe B ist BonusPerson
else:
    for b in range(0,lenB): 
        possibleBonusIDs.append(b); # Jeder Eintrag in Gruppe B kann BonusPerson sein


# ------------------------------------------
# || Zeitoptimierung an 10x10 Permutation ||
# ------------------------------------------
if extraPerson_isKnown:
    # An 10x10 Matrix direkt Matches und NoMatches 10 testen, da kleinere Gruppe 
    # Anschließend gekürzte Liste um Kombinationen für +1 Person erweitern und nochmal alle Bedingungen testen
    # Geht nur wenn bekannt ist, dass Person 11 aus Gruppe B die Bonusperson ist
    print('Check 10x10 (' + str(len(permutations_list_10x10)) + ' combinations) for Perfect Matches and NoMatches')
    permutations_list_reduced = []
    for idx, combination in enumerate(permutations_list_10x10):
        if (CheckMatches(combination,bekannteMatches, True) and 
            CheckNoMatches(combination,bekannteNoMatches, True)):
            permutations_list_reduced.append(combination)
        #printProgress(idx, len(permutations_list_10x10), 1) #printProgress wird jede Iteration aktualisiert => macht Berechnung VIEL langsamer

    permutations_list_10x10 = permutations_list_reduced
    endtime = time.time()
    print('Elapsed Time: {:5.3f}s'.format(endtime-starttime), end='  ')
    print('\nNoch mögliche Kombinationen: ' + str(len(permutations_list_10x10)))
    print()


# -------------------------------------------------
# || 10x11 erstellen und alle Bedingungen testen ||
# -------------------------------------------------
counterBonusPerson = [0 for _ in range(lenB)]
possibleMatchcombinations = []
print('Check all combinations for MatchingNights, Perfect Matches and NoMatches')
for iBonusPerson in possibleBonusIDs: # Zusatzperson in Liste B durchgehen
    for iBonusMatch in range(0, lenA): # Match der Zusatzperson in Liste A durchgehen      
        for combination in permutations_list_10x10: # Alle Kombinationen durchgehen
            matchCombination = list(combination)
            matchCombination.insert(iBonusPerson, iBonusMatch)
            if (CheckMatchingNights(matchCombination, matchingNights, correctMatches) and
                CheckMatches(matchCombination, bekannteMatches, False) and 
                CheckNoMatches(matchCombination, bekannteNoMatches, False)):
                possibleMatchcombinations.append(matchCombination)
                counterBonusPerson[iBonusPerson] = counterBonusPerson[iBonusPerson] + 1
        # Fortschritt über äußere 2 Schleifen laufen lassen (in innerer Schleife jede Iteration viel zu Langsam, so nur 110 Aktualisierungen)
        progress = iBonusPerson*lenA + iBonusMatch + 1
        printProgress(int(progress), int(lenB*lenA), 1)


# Alle Kombinationen in eine Tabelle zusammenfassen
matchMatrix = [[0 for _ in range(lenA)] for _ in range(lenB)] # leere 11x10 Matrix
for combination in possibleMatchcombinations:
    for i in range (0, len(combination)):
        matchMatrix[i][combination[i]] += 1

combinations_left = len(possibleMatchcombinations)
if combinations_left == 0:
    combinations_left = 1

for row in range(0,len(matchMatrix)):
    for col in range(0,len(matchMatrix[0])):
        matchMatrix[row][col] = round(matchMatrix[row][col]*100/combinations_left,1)

if not extraPerson_isKnown:
    combinations_left = int(combinations_left/2)

# Berechnung und Text für Bonusperson:
textBonusPerson = ""
for i in range (0, lenB):
    if (counterBonusPerson[i] != 0):
        percent =("{0:." + str(1) + "f}").format(100 * (counterBonusPerson[i] / combinations_left))
        textBonusPerson = textBonusPerson + gruppeB[i] + ": " + str(percent) + "%, "


endtime = time.time()
print('Elapsed Time: {:5.3f}s'.format(endtime-starttime), end='  ')
print('\nNoch mögliche Kombinationen: ' + str(combinations_left))
print()

if not extraPerson_isKnown:
    print("Bonusperson: ")
    if (textBonusPerson == ""):
        print("Anhand der Daten keine Bonuspersön möglich")
    else:
        print(textBonusPerson) 
    print() # Zusatztext ausgeben

print('\n__________________________________________________________')

#print("Print interactive Table?")
#userInput = input( "Press y/Y for interactive Table, else only static Table: ")
#if userInput == 'y' or userInput == 'Y':
#    printOnlyTable = False
#else:
#    printOnlyTable = True

printOnlyTable = True

if printOnlyTable:
    # PLOTTEN der relativen Tabelle
    fig = plt.figure(figsize=(14,6), dpi = 100)
    col_labels = gruppeA
    row_labels = gruppeB
    # Set colors
    colors = [["w" for a in range(lenA)] for b in range(lenB)]
    for row in range (0,lenB):
        for col in range (0,lenA):
            if(matchMatrix[row][col] == 0):
                colors[row][col] = "w"
            elif(matchMatrix[row][col] == 100):
                colors[row][col] = "lightgreen"
            elif(matchMatrix[row][col] >= 50):
                colors[row][col] = "bisque"
            else:
                colors[row][col] = "lightyellow"

    # Draw table
    the_table = plt.table(cellText=matchMatrix,
                          colWidths=[0.1] * 11,
                          cellColours=colors,
                          rowLabels=row_labels,
                          colLabels=col_labels,
                          rowColours =["lightgrey"] * lenB,  
                          colColours =["lightgrey"] * lenA,
                          loc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(14)
    the_table.scale(1, 2)
    plt.title("Matchingnight " + str(len(matchingNights)), fontsize=18)
    
    label = "Noch " + str(combinations_left) + " mögliche Kombinationen"
    if not extraPerson_isKnown:
        label = label + "\nDoppelt: " + textBonusPerson
    plt.xlabel(label, fontsize=12)

    # Removing ticks and spines enables you to get the figure only with table
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    for pos in ['right','top','bottom','left']:
        plt.gca().spines[pos].set_visible(False)

    plt.show()
#else:
    # Interaktive Tabelle erstellen
    manualMatches = [] # Liste mit x/y Koordinaten von Matches, die manuell gesetzt werden (können)

    # Fenster erstellen
    fenster = tk.Tk() # tkinter Fenster
    fenster.title("AYTO Lösungstabelle by Pheagan")

    style = ttk.Style()
    style.theme_use('clam')

    fenster.geometry("1110x660")
    fenster.resizable(width=False, height=False)


    # Erst Frame erstellen, in dem dann Variablen eingefügt werden
    label_frame = []
    for row in range(0,12):
        label_frame.append([])
        for column in range(0,11):
            label_frame[row].append( tk.Frame(fenster,width=90,height=40 ))
            label_frame[row][column].config(bg="lightgrey")
            label_frame[row][column].pack_propagate(0)
            if(row==0 or column==0):
                label_frame[row][column].config(bg="grey")
            pos_x = column*100 + 10
            pos_y = row*50 + 10
            label_frame[row][column].place(x=pos_x,y=pos_y)


    # Namen der TeilnehmerInnen eintragen
    label_names_A = [tk.Label]*10 # kleine Gruppe in Spalten
    label_names_B = [tk.Label]*11 # große Gruppe in Zeilen
    for column in range(0,10):
        row = 0
        label_names_A[column] = tk.Label( label_frame[row][column+1],
                                         bg="grey",
                                         fg="black",
                                         text=gruppeA[column],
                                         font=("Arial",12)).place(relx=0.5, rely=0.5, anchor='center')

    for row in range(0,11):
        column = 0
        label_names_A[column] = tk.Label( label_frame[row+1][column],
                                         bg="grey",
                                         fg="black",
                                         text=gruppeB[row],
                                         font=("Arial",12))
        label_names_A[column].place(relx=0.5, rely=0.5, anchor='center')

    # Labelcount für Kombinationen
    if extraPerson_isKnown:
        labelCount = len(possibleMatchcombinations)
    else:
        labelCount = int( len(possibleMatchcombinations)/2 )


    label_frame_count = tk.Frame(fenster,width=1090,height=40 )
    label_frame_count.config(bg="lightgrey")
    label_frame_count.pack_propagate(0)
    label_frame_count.place(x=10,y=610)
    label_count = tk.Label( label_frame_count,
                                         bg="lightgrey",
                                         fg="black",
                                         text = 'Nacht ' + str(len(matchingNights)) + ', noch ' + str(labelCount) + ' Kombinationen',
                                         font=("Arial",12))
    label_count.place(relx=0.5, rely=0.5, anchor='center')

    # Buttons einfügen mit Wahrscheinlichkeiten
    button_frame = []
    for row in range(0,11):
        button_frame.append([])
        for column in range(0,10):
            button_frame[row].append( tk.Button(label_frame[row+1][column+1],
                                               command = lambda index=[row,column]: ClickBtn(possibleMatchcombinations, button_frame, manualMatches, label_count, index)))
            button_frame[row][column].config(bg="lightgrey")
            button_frame[row][column].config(text="0")
            button_frame[row][column].config(font=("Arial",12))        
            button_frame[row][column].config(height=10, width=10)
            button_frame[row][column].place(relx=0.5, rely=0.5, anchor='center')

    UpdateMatrix(matchMatrix, button_frame, manualMatches)

    fenster.mainloop()