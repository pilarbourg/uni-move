import os
from supabase import create_client, Client
from dotenv import load_dotenv
from backend.Apartamentos import listar_apartamentos, buscar_precio, buscar_barrio_precio, buscar_resultado_vacio


# Cargar variables de entorno
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "database.env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("No se pudo cargar SUPABASE_URL o SUPABASE_KEY del .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def principal():

    print("\n Listado de apartamentos:")
    data = listar_apartamentos()
    for apt in data:
        print(f"{apt['id']} | {apt['titulo']} | {apt['precio']}€")



    print("\n Buscador por presupuesto")
    try:
        presupuesto = float(input("\n -> Ingresa tu presupuesto máximo: "))
        resultados = buscar_precio(presupuesto)

        if resultados:
            for row in resultados:
                print(f"{row['id']} | {row['titulo']} | {row['barrio']} | {row['precio']}€")
        else:
            print("No se encontraron apartamentos en ese presupuesto.")
    except ValueError:
        print("Presupuesto inválido.")



    print("\n Buscador por barrio y presupuesto")
    barrio = input("-> Ingresa un barrio: ")
    try:
        presupuesto = float(input("-> Ingresa presupuesto máximo: "))
        resultados = buscar_barrio_precio(barrio, presupuesto)

        if resultados:
            for row in resultados:
                print(f"{row['id']} | {row['titulo']} | {row['barrio']} | {row['precio']}€")
        else:
            print("No se encontraron apartamentos en ese barrio con esos filtros.")
    except ValueError:
        print("Presupuesto inválido.")


if __name__ == "__main__":
    principal()

