import uvicorn
from decouple import config


if __name__ == "__main__":
    if config("MODE") == "DEVELOPMENT":
        print("il Server si avvia in modalità DEVELOPMENT")
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

    if config("MODE") == "PRODUCTION":
        print("il Server si avvia in modalità PRODUCTION")
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)

    else:
        print(
            "ERROR: nessuna modalità di run (PROD/DEV) è stata definita nella variabili d'ambiente"
        )
