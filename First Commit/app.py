

from flask import Flask, request, jsonify
import requests
import psycopg2
import os
from groq import Groq

app = Flask(__name__)

DB_HOST = "localhost"
DB_NAME = "country"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
TABLE_NAME = "country_data"

client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))
api_url = 'https://api.api-ninjas.com/v1/country?name='
headers = {'X-Api-Key': 'D4br28qLwwVqBEsWj83V5A==wFx7pwiY06LK74y0'}

def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def insert_country_data(conn, name, gdp, population, exports, surface_area, tourists):
    try:
        cur = conn.cursor()
        insert_query = f"""
        INSERT INTO {TABLE_NAME} (name, gdp, population, exports, surface_area, tourists)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (name, gdp, population, exports, surface_area, tourists))
        conn.commit()
        cur.close()
        print(f"Data for {name} inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

def fetch_and_store_country_data(country_name):
    conn = connect_db()
    if not conn:
        print("Failed to connect to database.")
        return {"error": "Database connection failed."}, 500

    response = requests.get(api_url + country_name, headers=headers)
    if response.status_code == requests.codes.ok:
        country_data = response.json()
        
        if len(country_data) > 0:
            country = country_data[0]  
            name = country.get("name", "")
            gdp = country.get("gdp", None)
            population = country.get("population", None)
            exports = country.get("exports", None)
            surface_area = country.get("surface_area", None)
            tourists = country.get("tourists", None)

            insert_country_data(conn, name, gdp, population, exports, surface_area, tourists)
            conn.close()
            return {"message": f"Data for {name} inserted successfully!"}, 200
        else:
            conn.close()
            return {"error": f"No data found for country: {country_name}"}, 404
    else:
        conn.close()
        return {"error": "Error fetching data from API"}, 500

@app.route('/fetch-country-data', methods=['GET'])
def fetch_country_data():
    country_name = request.args.get('country_name', None)
    
    if not country_name:
        return {"error": "Country name is required"}, 400

    result, status_code = fetch_and_store_country_data(country_name)
    return jsonify(result), status_code

@app.route('/fetch-multiple-countries', methods=['GET'])
def fetch_multiple_countries():
    country_names = request.args.getlist('country_name')

    if not country_names or not isinstance(country_names, list):
        return {"error": "At least one country name is required"}, 400

    results = []
    for country_name in country_names:
        result, status_code = fetch_and_store_country_data(country_name)
        results.append({"country": country_name, "result": result, "status_code": status_code})
    
    return jsonify(results), 200

def generate_groq_summary(country_data):
    prompt = f"""
    Summarize the following data about the country:

    Country: {country_data['name']}
    GDP: {country_data['gdp']}
    Population: {country_data['population']}
    Exports: {country_data['exports']}
    Surface Area: {country_data['surface_area']}
    Tourists: {country_data['tourists']}
    Generate a brief and informative summary of this country highlighting its economy, population, and tourism.
    """

    try:     
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"  
        )

        summary = chat_completion.choices[0].message.content
        return summary

    except Exception as e:
        print(f"Error generating Groq summary: {e}")
        return f"Error generating summary: {e}"

@app.route('/summary', methods=['GET'])
def summary():
    country_name = request.args.get('country_name', None)

    if not country_name:
        return {"error": "Country name is required"}, 400

    conn = connect_db()
    if not conn:
        return {"error": "Database connection failed"}, 500

    try:
        cur = conn.cursor()
        query = f"SELECT name, gdp, population, exports, surface_area, tourists FROM {TABLE_NAME} WHERE name = %s"
        cur.execute(query, (country_name,))
        country_data = cur.fetchone()
        cur.close()
        conn.close()

        if country_data:
            country_summary = {
                "name": country_data[0],
                "gdp": country_data[1],
                "population": country_data[2],
                "exports": country_data[3],
                "surface_area": country_data[4],
                "tourists": country_data[5]
            }
            
            groq_summary = generate_groq_summary(country_summary)

            return groq_summary, 200
        else:
            return jsonify({"error": f"Country {country_name} not found in the database"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error querying database: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
