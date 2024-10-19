from flask import Flask, jsonify,request
import requests
app = Flask(__name__)


@app.route('/',methods =["POST"])
def get_pokemon():
    data = request.get_json()
    if request.method == "POST":
        if 'id' in data:
            received_id = data['id']
            url = f"https://pokeapi.co/api/v2/pokemon/{received_id}"
            url_form =  f"https://pokeapi.co/api/v2/pokemon-form/{received_id}/"
            get_stat = requests.get(url).json()["stats"]
            get_data = requests.get(url_form).json()
            get_name = get_data["pokemon"]["name"]
            get_sprite = get_data['sprites']
            stat = []
            for i in range(len(get_stat)):   #for loop เอาเฉพาะ hp และ attack
                if get_stat[i]["stat"]["name"] == "hp":
                    stat.append(get_stat[i]) 
                elif get_stat[i]["stat"]["name"] == "attack":
                    stat.append(get_stat[i])
            return jsonify({"stats":stat,"name":get_name,"sprites":get_sprite}), 200
        else:
            return jsonify({'msg': 'pokemon not found'}), 400



if __name__ == '__main__':
    app.run()