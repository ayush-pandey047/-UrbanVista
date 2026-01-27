This project motivates me to boost my Ml and AI learning.

So for this i start by installing all dependiencies and virtual environemet.
For ENV:-
        In backend i write python -m venv venv after running this i write source venv/bin/activate to activate the the environment.

Install dependencies:
            pip install pandas numpy scikit-learn fastapi uvicorn joblib
            then save them: pip freeze > requirements.txt

This is the solution of my problem:- 
I have use global python .drienv but o have to use my local .venv 
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % which python
        /Users/ayushpandey/.direnv/python-3.9/bin/python
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % source .venv/bin/activate
        which python
        /Users/ayushpandey/.direnv/python-3.9/bin/python
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % ls -a

        .                       .DS_Store               data                    requirements.txt
        ..                      .venv                   models                  src
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % ls .venv/bin/python

        .venv/bin/python
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % ./.venv/bin/python -c "import pandas; print('pandas OK')"

        zsh: no such file or directory: ./.venv/bin/python
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % /.venv/bin/python -c "import pandas; print('pandas OK')" 

        zsh: no such file or directory: /.venv/bin/python
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % rm -rf .venv

        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % ls -a

        .                       ..                      .DS_Store               data                    models                  requirements.txt        src
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % python3 -m venv .venv

        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % ls .venv/bin

        Activate.ps1    activate        activate.csh    activate.fish   pip             pip3            pip3.9          python          python3         python3.9
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % source .venv/bin/activate

        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % which python

        /Users/ayushpandey/Desktop/UrbanVista/backend/.venv/bin/python
        (.venv) ayushpandey@ayushs-MacBook-Pro-7 backend % 

SO the most probalmitc thing is path. Then after i take help from my friend Raman Pandey and he told me me to correct the path as i am using "../path/data_unde.py"  but i have to do "data/data_ude.py"

So in data set there is 0,1,9 in features apart from no.of bedroom ans those represents:
        1 means Yes (The house has this feature).
        0 means No (The house specifically does not have it).
        9 means Unknown (The data was missing during the collection).

For training the model i am using 80% to train it and 20% for testing the data.
after this i am using random forest regessor as it is little bit advance in comparision to linear regission.

{import os  # Standard library to handle folders}

SOone mew thing i learn is streamlit which help python to write long/ big lines of Javascript/Html/Css code in just one word i use dropdown so it makes dropdiwn function, i used sidebar it makes sidebar. Great functionality i truly like this streamlit I will learn more about this function. 

So run streamlit localy i have to run this code in terminal {(streamlit run src/app.py)}  for testing.