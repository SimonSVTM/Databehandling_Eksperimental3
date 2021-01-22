# Databehandling_Eksperimental3
22-01-2021

Author: Simon S. Villadsen

Collaborators: Erik Steenberg, Esben J. Porat & Kasper Larsen.


Pakke til databehandling i eksperimental kursus på Fysisk Institut, Aarhus.
Husk at sætte roden i den arbejdene dictionary.

Indeholder:
Pakken "Data_computing" hvori der er klasserne
 - Calibration.py, der hjælper med kalibrering af data.
 - Datarefactor.py, der henter og konverterer data.
 - Fitter.py, der har en metode "getFit", der returner fitparametre for en model for data.
 - Nodes.py, der implementerer en binær træstruktur. Særligt andvendelig til histogrammer og lagring af meget data.
 - PlotterLayout.py, der giver metoder for layout af plots.
 - PlotterTypes.py, der giver metoder for forskellige måder at plotte data på.
 - DPA.py, Data Processing Algorithms, der indholder gode algoritmer til datamanipulering.
 - Statistics.py, der indeholder statistiske modeller.
 
 Test-filer:
  - Fitter_Test_File.py, tester Fitter-klassen på tilfældigt genereret data.
  - Nodes_Test_File.py, tester Nodes-klassen på tilfældigt genereret data. 
 
 Data-analyse fil:
 
 Mn_Data_Analysis.py, bruger "Mn56_v3_ch000.npy" filen i "Data.7z" mappen, til at analysere spektrummet af Mn-56.
 
 


