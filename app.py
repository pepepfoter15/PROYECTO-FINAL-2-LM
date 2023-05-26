import requests,json
from flask import Flask, render_template, abort, redirect, request

app = Flask(__name__)

@app.route('/')
def inicio():
	return render_template("inicio.html")

@app.route('/jugadores', methods=["GET","POST"])
def jugadores():
    if request.method == "POST":
        codigo_jugador = request.form.get('nombre')
        
        url = f'https://api.clashofclans.com/v1/players/%23{codigo_jugador}'
        token = 'Bearer ["INTRODUCE TU TOKEN"]'

        headers = {'Authorization': token}

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            json = response.json()
            nombre = json['name']
            nivel_experiencia = json['expLevel']
            datos_jugador = {
                'nombre': nombre,
                'nivel_experiencia': nivel_experiencia
            }
            return render_template("jugadores.html", jugador=datos_jugador, codigo=codigo_jugador)
        else:
            error = f'Jugador no encontrado. Prueba con otro código :)'
            return render_template("jugadores.html", error=error)
    else:
        return render_template("jugadores.html")


@app.route('/jugadores/<codigo>')
def jugadores_detalles(codigo):
    url = f'https://api.clashofclans.com/v1/players/%23{codigo}'
    token = 'Bearer ["INTRODUCE TU TOKEN"]'
	
    headers = {'Authorization': token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json = response.json()
        nombre = json['name']
        codigo = json['tag']
        nivel_ayuntamiento_normal = json['townHallLevel']
        copas_aldea_normal = json['trophies']
        record_copas_aldea_normal = json['bestTrophies']
        nivel_ayuntamiento_nocturna = json['builderHallLevel']
        copas_aldea_nocturna = json['builderBaseTrophies']
        record_copas_aldea_nocturna = json['bestBuilderBaseTrophies']
        donaciones = json['donations']
        puntos_capital = json['clanCapitalContributions']
        nombre_clan = json['clan']['name']
        codigo_clan = json['clan']['tag']
        nivel_clan = json['clan']['clanLevel']
        rol_clan = json['role']

        detalles_del_jugador = {
            'nombre': nombre,
            'codigo_jugador': codigo,
            'nvl_ayun_nor': nivel_ayuntamiento_normal,
            'copas_nor': copas_aldea_normal,
            'record_copas_nor': record_copas_aldea_normal,
            'nvl_ayun_noc': nivel_ayuntamiento_nocturna,
            'copas_noc': copas_aldea_nocturna,
            'record_copas_noc': record_copas_aldea_nocturna,
            'donaciones': donaciones,
            'puntos_capital': puntos_capital,
            'nombre_clan': nombre_clan,
            'codigo_clan': codigo_clan,
            'nivel_clan': nivel_clan,
            'rol_clan': rol_clan
        }
        return render_template("detallejugador.html", jugador=detalles_del_jugador)
    else:
        return render_template("detallejugador.html")



@app.route('/clanes', methods=["GET","POST"])
def clanes():
    if request.method == "POST":
        nombre_clan_busqueda = request.form.get('clan')

        url = f'https://api.clashofclans.com/v1/clans?name={nombre_clan_busqueda}&limit=20'
        token = 'Bearer ["INTRODUCE TU TOKEN"]'      

        headers = {'Authorization': token}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            clanes = []
            for item in data['items']:
                nombre_clan = item['name']
                copas_clan_nor = item['clanPoints']
                copas_clan_noc = item['clanBuilderBasePoints']
                datos_clan = {
                    'nombre_clan': nombre_clan,
                    'copas_clan_nor': copas_clan_nor,
                    'copas_clan_noc': copas_clan_noc,
                }
                clanes.append(datos_clan)
            
            clanes_ordenados = sorted(clanes, key=lambda x: x['copas_clan_nor'], reverse=True)
            
            return render_template("clanes.html", clanes=clanes_ordenados, codigo_c=nombre_clan_busqueda)
        else:
            error = 'Clan no encontrado. Prueba con otro nombre válido :)'
            return render_template("clanes.html", error=error)
    else:
        return render_template("clanes.html")


@app.route('/clanes/<codigo_c>')
def clanes_detalles(codigo_c):
    url = f'https://api.clashofclans.com/v1/clans?name={codigo_c}&limit=20'
    token = 'Bearer ["INTRODUCE TU TOKEN"]'
	
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json = response.json()
        nombre_clan = json['items'][0]['name']
        codigo_clan = json['items'][0]['tag']
        estado_clan = json['items'][0]['type']
        copas_aldea_normal_clan = json['items'][0]['clanPoints']
        copas_aldea_nocturna_clan = json['items'][0]['clanBuilderBasePoints']
        pais_clan = json['items'][0]['location']['name']
        codigo_pais = json['items'][0]['location']['countryCode']
        liga_clanes = json['items'][0]['warLeague']['name']
        nivel_clan_clan = json['items'][0]['clanLevel']
        copas_minimas_nor = json['items'][0]['requiredTrophies']
        copas_minimas_noc = json['items'][0]['requiredBuilderBaseTrophies']
        
        detalles_del_jugador = {
            'nombre_clan': nombre_clan,
            'codigo_clan': codigo_clan,
            'estado_clan': estado_clan,
            'copas_nor': copas_aldea_normal_clan,
            'copas_noc': copas_aldea_nocturna_clan,
            'pais_clan': pais_clan,
            'codigo_pais': codigo_pais,
            'liga_clanes': liga_clanes,
            'nivel_clan': nivel_clan_clan,
            'copas_minimas_nor': copas_minimas_nor,
            'copas_minimas_noc': copas_minimas_noc
        }
        return render_template("detalleclan.html", jugador=detalles_del_jugador)
    else:
        return render_template("detalleclan.html")

app.run('0.0.0.0',5000, debug=True)
