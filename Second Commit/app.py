from flask import Flask, request, jsonify
import os
from groq import Groq
import summary_functions, data_functions, database
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
TABLE_NAME = os.environ.get("TABLE_NAME")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/fetch-country-data', methods=['GET'])
def fetch_country_data():
    country_name = request.args.get('country_name', None)
    
    if not country_name:
        return {"error": "Country name is required"}, 400

    result, status_code = data_functions.store_country_data(country_name)
    return jsonify(result), status_code

@app.route('/fetch-multiple-countries', methods=['GET'])
def fetch_multiple_countries():
    country_names = request.args.getlist('country_name')

    if not country_names or not isinstance(country_names, list):
        return {"error": "At least one country name is required"}, 400

    results = []
    for country_name in country_names:
        result, status_code = data_functions.fetch_and_store_country_data(country_name)
        results.append({"country": country_name, "result": result, "status_code": status_code})
    
    return jsonify(results), 200

@app.route('/summary', methods=['GET'])
def summary():
    country_name = request.args.get('country_name', None)
    parameter = request.args.get('parameter',None)

    if not country_name:
        return {"error": "Country name is required"}, 400
    if not parameter:
        return {"error": "Paramter is required"}, 400
    
    conn = database.connect_db_()
    if not conn:
        return {"error": "Database connection failed"}, 500

    try:
        cur = conn.cursor()
        query = f"SELECT * FROM {TABLE_NAME} WHERE name = %s"
        cur.execute(query, (country_name,))
        country_data = cur.fetchone()
        cur.close()
        conn.close()

        if country_data:
            match parameter:
                case 'population_density':
                    groq_summary = summary_functions.pop_density_summary(country_data)
                case 'trade':
                    groq_summary = summary_functions.trade_summary(country_data)
                case 'import_export':
                    groq_summary = summary_functions.import_export_summary(country_data)
                case _:
                    groq_summary = summary_functions.default_summary(country_data)

            return groq_summary, 200
        else:
            return jsonify({"error": f"Country {country_name} not found in the database"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error querying database: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
