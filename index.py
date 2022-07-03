# Si quieres correr el cod. debes ir en la terminal a la ubicacion del archivo (Carpeta contenedora)
# Y luego debes poner python proy.py

#Selector post
from facebook_scraper import get_posts
#Flask importacion
from flask import Flask, render_template, request
#Necesario para analisis de sentimiento e importar el modelo
import joblib
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.keras.models import load_model

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
                analisis = []
                for i in post1["comments_full"]:
                    comentInfo = []
                    comentInfo.append(i["commenter_name"])
                    comentInfo.append(i["comment_text"])
                    comentInfo.append(i["comment_time"])

                    comentInfo.append(analisis_sentimiento(i["comment_text"]))

                    analisis.append(comentInfo)
                
                return render_template('final.html', post = analisis)

            elif  request.form.get('boton') == 'VALUE2':
                analisis = []
                for i in post2["comments_full"]:
                    comentInfo = []
                    comentInfo.append(i["commenter_name"])
                    comentInfo.append(i["comment_text"])
                    comentInfo.append(i["comment_time"])

                    comentInfo.append(analisis_sentimiento(i["comment_text"]))

                    analisis.append(comentInfo)
                
                return render_template('final.html', post = analisis)
  
            elif  request.form.get('boton') == 'VALUE3':
                analisis = []
                for i in post3["comments_full"]:
                    comentInfo = []
                    comentInfo.append(i["commenter_name"])
                    comentInfo.append(i["comment_text"])
                    comentInfo.append(i["comment_time"])

                    comentInfo.append(analisis_sentimiento(i["comment_text"]))

                    analisis.append(comentInfo)
                
                return render_template('final.html', post = analisis)

            elif  request.form.get('boton') == 'VALUE4':

                analisis = []
                for i in post4["comments_full"]:
                    comentInfo = []
                    comentInfo.append(i["commenter_name"])
                    comentInfo.append(i["comment_text"])
                    comentInfo.append(i["comment_time"])

                    comentInfo.append(analisis_sentimiento(i["comment_text"]))

                    analisis.append(comentInfo)
                
                return render_template('final.html', post = analisis)
    

def analisis_sentimiento(comentario):
    tokenizer = joblib.load('tokenizer')
    comentario = tokenizer.texts_to_sequences(comentario)
    comentario = pad_sequences(comentario, maxlen=65, dtype='int32', value=0)
    model3 = load_model('model3.h5', compile = False)
    sentiment = model3.predict(comentario,batch_size=2,verbose = 2)[0]

    if(np.argmax(sentiment) == 0):
        return "negative"
    elif (np.argmax(sentiment) == 1):
        return "positive"

if __name__ == '__main__':
    app.run(debug=True)  # Esta linea hace que se actualice cada que cambie algo
