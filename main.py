from flask import Flask, request,render_template,jsonify
import pandas as pd
import base64
from io import BytesIO
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def Home():
   iso_codes=['iso_code']
   df= pd.read_csv('owid-covid-data.csv',usecols=iso_codes)
   iso_codes_filt=df['iso_code'].drop_duplicates()
   lista_isos="<br>".join(iso_codes_filt.tolist())
   return f"Para ver todos os dados, utilizar /get_all_data <br><br> Para ver dados de unico pais, utilizar a ISO na barra de pesquisa, coloque /get_iso/'iso especifica' <br> <strong>ISO's:</strong> <br> {lista_isos}"



@app.route("/get_all_data", methods={'POST','GET'})
def get_all_data():
    deaths_data=['iso_code','continent','location','date','total_deaths']
    df= pd.read_csv('owid-covid-data.csv',usecols=deaths_data)
    data_json = df.to_json(orient='records')
    data_web = df.to_string(index=False)

    return  f"<pre>{data_web}</pre> {jsonify(data_json)}"

@app.route("/get_iso/<iso_code>", methods={'GET'})
def get_iso_code(iso_code):
    iso_data=['iso_code','continent','location','date','total_deaths']
    df=pd.read_csv('owid-covid-data.csv',usecols=iso_data)

    country_iso = escape(iso_code)

    if country_iso:
        df_filtered = df[df['iso_code']== country_iso]

        if not df_filtered.empty:
            data_json=df_filtered.to_json(orient='records')
            data_web = df_filtered.to_string(index=False)
            return f"<pre>{data_web}</pre> {jsonify(data_json)}"
        else:
            return "Páis não encontrado",404
    else:
        return "Digite o ISO Code",400


# response = requests.post(url, data=data_json, headers =headers)
# if response.status_code ==200:
#     print('Dados enviados com sucesso!')

# else:
#     print(f'Falha ao enviar dados. Status code:{response.status_code}')
#     print(response.text)

if __name__ == '__main__': 
    app.run(debug=True)