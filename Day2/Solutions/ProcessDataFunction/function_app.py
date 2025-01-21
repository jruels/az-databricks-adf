import azure.functions as func
import logging
import json
import psycopg2

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="ProcessData")
def ProcessData(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    data = req.get_json()

    # PostgreSQL connection details
    host = 'adfpostgres.postgres.database.azure.com'
    dbname = 'analytics'
    user = 'adfadmin'
    password = 'adf@min2025'
    port = 5432

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port,
            sslmode='require'
        )
        cursor = conn.cursor()
        logging.info("Connected to PostgreSQL successfully")
    except Exception as e:
        logging.error(f"Failed to connect to PostgreSQL: {e}")
        return func.HttpResponse(f"Failed to connect to PostgreSQL: {e}", status_code=500)

    # Create table if it does not exist
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS public.happiness_population (
        Region VARCHAR(255),
        Country VARCHAR(255),
        Happiness_Score FLOAT,
        Population INT
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()

    if data:
        run_output = data["runOutput"]
        parsed_data = [json.loads(record) for record in run_output]
        for row in parsed_data:
            if row["Region"] == "Europe":
                cursor.execute(
                    "INSERT INTO public.happiness_population (Region, Country, Happiness_Score, Population) VALUES (%s, %s, %s, %s)",
                    (row['Region'], row['Country'], row['Happiness_Score'], row['Population'])
                )
                conn.commit()
        return func.HttpResponse(f"Data processed successfully: {parsed_data}")
    
    
    cursor.close()
    conn.close()