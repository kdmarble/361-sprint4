Instructions for running person-generator.py:

Required:
    - Dataset from https://www.kaggle.com/openaddresses/openaddresses-us-west downloaded and extracted
    - Dataset must be in a folder titled 'archive'
    - 'archive' folder must be in the same directory as person-generator.py
    - Ex:
        person-generator.py
        archive
            > ak.csv
            > az.csv
            > ca.csv
                .
                . 

    - If using a custom input file, the file must be titled 'input.csv'
    - Input file must be in the same directory as person-generator.py
    - Input file must match the format specified in the project requirements


To run: 
    - Without an input file: $ python person-generator.py
    - With an input file: $ python person-generator.py input.csv

Output:
    - A GUI to run the program if run with no input file
    - Output be stored as "output.csv", in the same directory as person-generator.py

Notes:
    - When running without a custom input file, the GUI can be used to run the program as many times as you'd like
    - With a custom input file, the program will only display and write to the output once