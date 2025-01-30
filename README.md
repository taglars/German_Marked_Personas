# German_Marked_Personas
Program Code and Resources for my Bachelor Thesis on "Marked Personas in German Context: Analyzing Demographic Stereotypes in Large Language Models and Their Implications for Integration"

Steps for Data Creation:
1. in generators.openai_gen select the right OpenAI Modell
2. run main.py -> Personas getting created
3. check file naming of each demographic
4. run analyze_demographics.py -> creation of raw data in json format (words + z-scores)
5. run toExcel.py -> creation of csv files in the export folder
6. open csv files in Excel and order by Demographic, z-score etc.
7. save files depending on the Model used
8. repeat steps again with different model

