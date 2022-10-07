import matplotlib.pyplot as plt
import sys
import math
import time
import itertools
import tkinter as tk
from tkinter import ttk

def Header():
    print()
    print('00=================00')
    print('||                 ||')
    print('|| ARE YOU THE ONE ||')
    print('||                 ||')
    print('00=================00')
    print('\nLösungsskript')
    print('Made by Alex/Pheagan \n')

def TeilnehmerA():      # Kleinere Gruppe!
    with open('GruppeA.txt', 'r') as datei:
        text = datei.read().split("\n") #Text direkt splitten

    teilnehmer = [""] * len(text)
    for i in range(0,len(text)):
        teilnehmer[i] = text[i]

    return teilnehmer

def TeilnehmerB():      # Größere Gruppe! 
    with open('GruppeB.txt', 'r') as datei:
        text = datei.read().split("\n") #Text direkt splitten

    teilnehmer = [""] * len(text)
    for i in range(0,len(text)):
        teilnehmer[i] = text[i]  
    return teilnehmer

def BekannteMatches():
    with open('BekannteMatches.txt', 'r') as datei:
        text = datei.read().split("\n") #Text direkt splitten

    matches = [0] * len(text)
    for i in range(0,len(text)):
        clearedText = text[i].split('%')[0]
        splittedText = clearedText.split(',')
        matches[i] = [int(splittedText[0]),int(splittedText[1])]
    return matches

def BekannteNoMatches():
    with open('BekannteNoMatches.txt', 'r') as datei:
        text = datei.read().split("\n") #Text direkt splitten

    nomatches = [0] * len(text)
    for i in range(0,len(text)):
        clearedText = text[i].split('%')[0]
        splittedText = clearedText.split(',')
        nomatches[i] = [int(splittedText[0]),int(splittedText[1])]
    return nomatches

def MatchingNights():           # Aus sicht von Gruppe A, wen sie aus Gruppe B gewählt haben!
    with open('MatchingNights.txt', 'r') as datei:
        text = datei.read().split("\n") #Text direkt splitten

    paare = [0] * len(text)
    paareStr = [""] * len(text)
    for i in range(0,len(text)):
        clearedText = text[i].split('%')[0]
        paareStr[i] = clearedText.split('//')[0].split(',')
        paare[i] = [0]*len(paareStr[i])
        for k in range(0,len(paareStr[0])):
            paare[i][k] = int(paareStr[i][k])

    return paare

def CorrectMatches():           # Wie viele korrekte Matches gab es in der jeweiligen Nacht
    with open('MatchingNights.txt', 'r') as datei:
        text = datei.read().split("\n") #Text direkt splitten

    matches = [0] * len(text)
    for i in range(0,len(text)):
        clearedText = text[i].split('%')[0].replace('\n','')
        matches[i] = int(clearedText.split('//')[1])
    return matches

def printProgress (iteration, total, decimals = 1):
    percent =("{0:." + str(decimals) + "f}").format(100 * (iteration / total))
    printEnd = "\r"
    print(f'\rFortschritt: {percent}%', end = printEnd)
    if iteration == n_combination: 
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
    print("Button", str(index[0]), ',', str(index[1]), "clicked")

    if index in manualMatches:
        manualMatches.remove(index)
        print("Index entfernt")
    else:
        manualMatches.append(index)
        print("Index hinzugefügt")

    # reducedCombination = Liste mit Berücksichtigung der manuellen Matches
    reducedCombinations = []
    for combination in allCombinations:
        isCombinationValid = True
        for match in manualMatches: # durch alle manuellen Matches durchgehen und schauen ob alle dabei sind
            if combination[match[0]] != match[1]:
                isCombinationValid = False
        if isCombinationValid: # nur die Kombinationen hinzufügen, die alle manuellen Matches enthalten
            reducedCombinations.append(combination)

    print( 'Nach Festlegung Match noch '+str(len(reducedCombinations)) + ' mögliche Kombinationen')
    label_count.config( text = 'Noch ' + str(len(reducedCombinations)) + ' Kombinationen')

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

gruppeA = TeilnehmerA()
gruppeB = TeilnehmerB()

lenA = len(gruppeA)
lenB = len(gruppeB)
n_combination = math.factorial(10)*10

# Es findet (fast) keine Überprüfung statt, dass Daten richtig eingetragen sind
# - alle Textdateien müssen vorliegen
# - Daten in den Textdateien müssen korrekt eingetragen sein
if lenA!=10 or lenB!=11:
    print('Länge der Teilnehmerlisten ist nicht korrekt')
    print('Gruppe A muss 10 Einträge enthalten und Gruppe B 11')
    input('\nDas Skript wird jetzt beendet. Press Enter to continue...')
    sys.exit(0)


print('Teilnehmer eingelesen')
print('Gruppe A: ' + str(gruppeA))
print('Gruppe B: '+ str(gruppeB))
print('Insgesammt mögliche Kombinationen: ' + str(n_combination))
print()

bekannteMatches = BekannteMatches()
bekannteNoMatches = BekannteNoMatches()
matchingNights = MatchingNights()
correctMatches = CorrectMatches();

print('Weitere Daten eingelesen:')
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
permutations_object = itertools.permutations(listA)                                        
permutations_list = list(permutations_object)


# VORGEHEN
# An 10x10 Matrix direkt Matches und NoMatches 10 testen, da kleinere Gruppe 
# Anschließend gekürzte Liste um Kombinationen für +1 Person erweitern und nochmal alle Bedingungen testen
print('Check 10x10 (' + str(len(permutations_list)) + ' combinations) for Perfect Matches and NoMatches')
permutations_list_10x10 = []
l = len(permutations_list)
for idx, combination in enumerate(permutations_list):
    if (CheckMatches(combination,bekannteMatches, True) and 
        CheckNoMatches(combination,bekannteNoMatches, True)):
        permutations_list_10x10.append(combination)
    #printProgress(idx, l, 1) #printProgress wird jede Iteration aktualisiert => macht Berechnung VIEL langsamer

endtime = time.time()
print('Elapsed Time: {:5.3f}s'.format(endtime-starttime), end='  ')
print('\nNoch mögliche Kombinationen: ' + str(len(permutations_list_10x10)))
print()


# 10x11 erstellen und alle Bedingungen testen
print('Check 10x11 (' + str(10*len(permutations_list_10x10)) + ' combinations) for MatchingNights, Perfect Matches and NoMatches')
possibleMatchcombinations = []
for b in range(0,lenA):
    l = len(permutations_list_10x10)
    for i in range(0, l):
        matchCombination = permutations_list_10x10[i] + (b,)
        # Überprüfen ob Kombination möglich ist
        if (CheckMatchingNights(matchCombination, matchingNights, correctMatches) and
            CheckMatches(matchCombination, bekannteMatches, False) and 
            CheckNoMatches(matchCombination, bekannteNoMatches, False)):
            possibleMatchcombinations.append(matchCombination);
        #printProgress(b*l+i, l*lenA, 1) #printProgress wird jede Iteration aktualisiert => macht Berechnung VIEL langsamer

endtime = time.time()
print('Elapsed Time: {:5.3f}s'.format(endtime-starttime), end='  ')
print()


# Alle Kombinationen in eine Tabelle zusammenfassen
print( '\nRelative Tabelle berechnen')
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
endtime = time.time()
print('Elapsed Time: {:5.3f}s'.format(endtime-starttime), end='  ')
print()

print("\n\nPrint interactive Table?")
userInput = input( "Press y/Y for interactive Table, else only static Table: ")
if userInput == 'y' or userInput == 'Y':
    printOnlyTable = False
else:
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
    plt.xlabel("Noch " + str(len(possibleMatchcombinations)) + " mögliche Kombinationen", fontsize=12)

    # Removing ticks and spines enables you to get the figure only with table
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    for pos in ['right','top','bottom','left']:
        plt.gca().spines[pos].set_visible(False)

    plt.show()
else:
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

    # Label für Kombinationen
    label_frame_count = tk.Frame(fenster,width=1090,height=40 )
    label_frame_count.config(bg="lightgrey")
    label_frame_count.pack_propagate(0)
    label_frame_count.place(x=10,y=610)
    label_count = tk.Label( label_frame_count,
                                         bg="lightgrey",
                                         fg="black",
                                         text='Noch ' + str(len(possibleMatchcombinations)) + ' Kombinationen',
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