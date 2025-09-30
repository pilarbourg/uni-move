import os
from backend.Apartamentos import listar_apartamentos, buscar_precio, buscar_barrio_precio
from supabase import create_client, Client

SUPABASE_URL = "https://qtclucrcmrhaeqwllccn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0Y2x1Y3JjbXJoYWVxd2xsY2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg2Mjg1NjcsImV4cCI6MjA3NDIwNDU2N30.OvNzc5HNPV0cyVA965JstZ942kaua02lhYXcWEEeWq0"

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