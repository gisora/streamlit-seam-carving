# PTU8 Užduoties Nr. 1 atlikimo rezultatas

## Nuotraukos sutraukimas panaikinant mažiausios svarbos siūles
## Seam Carving for Content-Aware Image Risizing 

### Algoritmo įdėjos ir pavyzdžiai:
- [Shai Avidan, Ariel Shamir, Seam carving for content-aware image resizing, (2007-07-29)](https://dl.acm.org/doi/10.1145/1275808.1276390)
- [Alan Edelman, David P. Sanders & Charles E. Leiserson, Introduction to Computational Thinking, MIT](https://computationalthinking.mit.edu/Fall22/images_abstractions/seamcarving/)


### Naudotos priemonės:
- python
- scikit-image [ https://scikit-image.org/ ]
- streamlit [ https://streamlit.io/ ]

### Papildomos priemonės naudotos tyrimui:
- Jupyter Notebook [ https://jupyter.org/ ]
- Matplotlib [ https://matplotlib.org/ ]

### Paleidimo instrukcija:
1. Sukriam virtualią aplinką: ```python -m venv .env```
2. Aktyvuojam virtualią aplinką:
    - Linux: ```source .env/bin/activate```
    - Windows: ```.env\Scripts\activate```

3. Įdiegiam reikiamus python modulius: ```pip install -r requirements.txt```
    - Windows naudotojai scikit-image diegia iš sukompiliuoto paketo. Siunčiamės iš čia [Windows scikit-image binaties](https://www.lfd.uci.edu/~gohlke/pythonlibs/#scikit-image)
    - Suompiliuoto scikit-image paketo diegimas: ```pip install "package_name".whl```

- Jupyter notebook failui diegiame python modulius iš requirements_jupyter.txt

4. Paleidžiam Streamlit prgramą: ```streamlit run main.py```



