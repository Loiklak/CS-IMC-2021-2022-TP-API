import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    server = os.environ["TPBDD_SERVER"]
    database = os.environ["TPBDD_DB"]
    username = os.environ["TPBDD_USERNAME"]
    password = os.environ["TPBDD_PASSWORD"]
    driver= '{ODBC Driver 17 for SQL Server}'


    if len(server)==0 or len(database)==0 or len(username)==0 or len(password)==0:
        return func.HttpResponse("Au moins une des variables d'environnement n'a pas été initialisée.", status_code=500)

    return func.HttpResponse("All is good")

    errorMessage = ""
    dataString = ""
    try:
        logging.info("Test de connexion avec pyodbc...")
        with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT DISTINCT genre
FROM [dbo].[tPrincipals] principals1
INNER JOIN (
    SELECT nconst
    FROM [dbo].[tPrincipals] principals
    GROUP BY principals.nconst
    HAVING COUNT(DISTINCT category) > 1
) principals2
ON principals1.nconst = principals2.nconst
LEFT JOIN [dbo].[tTitles] titles
ON titles.tconst = principals1.tconst
LEFT JOIN [dbo].[tGenres] genres
ON genres.tconst = titles.tconst
WHERE genre IS NOT NULL
""")

            rows = cursor.fetchall()
            for row in rows:
                dataString += f"{row[0]}\n"


    except:
        errorMessage = "Erreur de connexion a la base SQL"
    
    if errorMessage != "":
        return func.HttpResponse(dataString + errorMessage, status_code=500)

    else:
        return func.HttpResponse(dataString)
