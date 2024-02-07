"""
Este módulo calcula las ventas y muestra una factura de la compra.
"""

import json
import sys
import time


def load_json_file(filename):
    """
    Carga datos JSON desde un archivo.

    Args:
        filename (str): El nombre del archivo a cargar.

    Returns:
        dict or None: Los datos JSON cargados, o None si hubo un error.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Formato JSON inválido en el archivo '{filename}'.")
        return None


def compute_total_cost(price_catalogue, sales_record):
    """
    Calcula el precio total a partir del catálogo
    de precios y los registros de ventas.

    Args:
        price_catalogue (list): Una lista de diccionarios que
                                contiene los precios de los productos.
        sales_record (list): Una lista de diccionarios que
                                contiene los registros de ventas.

    Returns:
        tuple: Una tupla que contiene el costo total
            y una lista de artículos vendidos.
    """
    total_cost = 0
    items_list = []

    for sale in sales_record:
        product = sale.get("Product")
        quantity_sold = sale.get("Quantity")
        matching_products = [p for p in price_catalogue
                             if p.get("title") == product]
        if matching_products:
            price_per_unit = matching_products[0].get("price")
            subtotal = price_per_unit * quantity_sold
            total_cost += subtotal
            items_list.append((product, quantity_sold,
                               price_per_unit, subtotal))
        else:
            print(f"Advertencia: Producto '{product}\
                  ' no encontrado en el catálogo de precios.")

    return total_cost, items_list


def main():
    """
    Función principal para calcular las ventas totales
    y generar una factura.
    """
    if len(sys.argv) != 3:
        print("Uso: Revisar documentacion")
        return

    start_time = time.time()

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    price_catalogue = load_json_file(price_catalogue_file)
    sales_record = load_json_file(sales_record_file)

    if price_catalogue is None or sales_record is None:
        return

    total_cost, items_list = compute_total_cost(price_catalogue, sales_record)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("***************************** Factura ****************************")
    print("Producto                    Cantidad       Unit   Subtot")
    print("------------------------------------------------------------------")
    for item in items_list:
        product, quantity_sold, price_per_unit, subtotal = item
        print(f"{product:30}{quantity_sold:>10}\
              {price_per_unit:>15.2f}{' ':>11}{subtotal:.2f}")
    print("------------------------------------------------------------------")
    print(f"Total:                                                           \
          ${total_cost:.2f}")
    print("**************************************************************")

    with open("ResultadosVentas.txt", 'w', encoding='utf-8') as results_file:
        results_file.write("***************************** Factura \
                           *****************************\n")
        results_file.write("Producto                    Cantidad   \
                               Unit    Subtot\n")
        results_file.write("-----------------------------------------\n")
        for item in items_list:
            product, quantity_sold, price_per_unit, subtotal = item
            results_file.write(f"{product:30}{quantity_sold:>10}\
                               {price_per_unit:>15.2f}{' ':>11}\
                                {subtotal:.2f}\n")
        results_file.write("------------------------------------------\n")
        results_file.write(f"Total:                       \
                            ${total_cost:.2f}\n")
        results_file.write("****************************************\n\n")
        results_file.write(f"Tiempo transcurrido: {elapsed_time:.2f} seg\n")


if __name__ == "__main__":
    main()
