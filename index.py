# Si quieres correr el cod. debes ir en la terminal a la ubicacion del archivo (Carpeta contenedora)
# Y luego debes poner python proy.py

#Selector post
from facebook_scraper import get_posts
#Flask importacion
from flask import Flask, render_template, request
#Necesario para analisis de sentimiento e importar el modelo
import pickle
import string
import emoji

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('principal.html')


@app.route('/selector', methods=['GET', 'POST'])
def about():
    pagina = request.args.get('pagina')

    L = [post for post in get_posts(
        pagina, pages=3, options={"comments": True})]
        
    global post1
    global post2
    global post3
    global post4

    post1, post2, post3, post4 = L[0], L[1], L[2], L[3]

    return render_template('selector.html',post1=post1, post2=post2 ,post3=post3 ,post4=post4  )

@app.route("/final", methods=['GET', 'POST'])
def final():

    '''
    en final.html seria:
    i[0] -> nombre
    i[1] -> texto
    i[2] -> hora
    i[3] -> analisis de sentimiento

    '''

    if request.method == 'POST':

            if request.form.get('boton') == 'VALUE1':
                #SE PUEDE SIMPLIFICAR EN UNA FUNCION:
                
                analisis = tarea_repetitiva(post1)

                return render_template('final.html', post = analisis)

            elif  request.form.get('boton') == 'VALUE2':
                
                analisis = tarea_repetitiva(post2)
                
                return render_template('final.html', post = analisis)
  
            elif  request.form.get('boton') == 'VALUE3':

                analisis = tarea_repetitiva(post3)

                return render_template('final.html', post = analisis)

            elif  request.form.get('boton') == 'VALUE4':

                analisis = tarea_repetitiva(post4)
                
                return render_template('final.html', post = analisis)
    

def tarea_repetitiva(post):
    analisis = []
    for i in post["comments_full"]:
        comentInfo = []
        comentInfo.append(i["commenter_name"])
        comentInfo.append(i["comment_text"])
        comentInfo.append(i["comment_time"])

        comentInfo.append(analisis_sentimiento(i["comment_text"]))

        analisis.append(comentInfo)
    return analisis

def analisis_sentimiento(comentario):
    file = open('vector', 'rb')
    vector = pickle.load(file)

    file = open('model_SVM.h5', 'rb')
    model = pickle.load(file)

    limpieza(comentario)

    fv = vector.transform([comentario])
    sentiment = model.predict(fv)

    if(sentiment[0] == 0):
        return "negative"
    elif (sentiment[0] == 1):
        return "positive"

def limpieza(texto):
    alfa = string.ascii_lowercase + ' '
    textoLimpio = ''.join([c for c in texto.lower() if c in alfa])
    textoLimpio = ' '.join(textoLimpio.split())
    for character in texto.lower():
        if character in emoji.UNICODE_EMOJI_SPANISH:           
            textoLimpio = emoji.demojize(character)
    return textoLimpio

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')  # Esta linea hace que se actualice cada que cambie algo
