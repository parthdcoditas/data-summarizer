import requests,os
from database import connect_db_
api_url = 'https://api.api-ninjas.com/v1/country?name='
headers = {'X-Api-Key': os.environ.get("X-Api-Key")}
TABLE_NAME = os.environ.get("TABLE_NAME")


def insert_country_data(conn, data):
    try:
        cur = conn.cursor()
        insert_query = f"""
        INSERT INTO {TABLE_NAME} (name, gdp, population, surface_area, imports, exports, tourists, gdp_growth, pop_density, pop_growth, currency, sex_ratio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11]))
        conn.commit()
        cur.close()
        print(f"Data for {data[0]} inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

def store_country_data(country_name):
    conn = connect_db_()
    if not conn:
        print("Failed to connect to database.")
        return {"error": "Database connection failed."}, 500

    response = requests.get(api_url + country_name, headers=headers)
    if response.status_code == requests.codes.ok:
        country_data = response.json()
        country = country_data[0]
        if len(country_data) > 0:
            data = [
                country.get("name", ""),
                country.get("population", None),
                country.get("gdp", None),
                country.get("surface_area", None),
                country.get("imports", None),
                country.get("exports", None),
                country.get("tourists", None),
                country.get("gdp_growth", None),
                country.get("pop_density", None),
                country.get("pop_growth", None),
                country.get("currency").get("name",None),
                country.get("sex_ratio", None),
            ]

            insert_country_data(conn, data)
            conn.close()
            return {"message": f"Data for {data[0]} inserted successfully!"}, 200
        else:
            conn.close()
            return {"error": f"No data found for country: {country_name}"}, 404
    else:
        conn.close()
        return {"error": "Error fetching data from API"}, 500

