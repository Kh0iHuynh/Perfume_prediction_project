# Perfume_prediction_project

-----
Data
-----
perfume_data.csv:
1. Name: contain perfume name from top 100 perfume on fragraneX website
2. Top: contain the comma separated list of top notes
3. Heart: contain the comma separated list of heart notes
4. Base: contain the comma separated list of Base notes
5. Gender : supposed gender for the perfume

-----
Data generation
-----
create_augmented_perfume_data.py:
1. generate random combination of Top,Heart,Base using notes in perfume_data.csv
2. generate random names for th those note combinations
3. label genreated perfume as Losing and label real perfume as Winning

-----
Convolutinal neural network training script and prediction script
-----
model_training.py: use the augmented data to train neural network model
load_and_predict2.py: load in new scent combination and make prediction on chance to win

-----
App package into standalone version
-----
load_and_predict_gui.py is a script used to package everything into a standalone window exe file.
full steps to generate exe can be read in window_app_make_guide.txt
App can make prediction if provided with combination of Top,Heart,Base notes using notes presented in winning_note_proportions.tsv
