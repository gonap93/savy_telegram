import requests
import json
import pandas as pd

categories_to_value_map = {
    1: "Salud y Bienestar",
    2: "Gastronomía",
    3: " Entretenimiento",
    4: "Supermercados",
    5: "Hogar",
    6: "Viajes",
    7: "Indumentaria",
    8: "Educación",
    9: "Librerías",
    10: "Juguetes",
    11: "Vehículos",
    12: "Electrónica"
}

cards_to_column_map = {
    'visa_credito': 'tarjeta visa_credito_exists',
    'master_credito': 'tarjeta mastercard_credito_exists',
    'amex_credito': 'tarjeta american express_credito_exists',
    'debito': 'tarjeta galicia débito_debito_exists'
}

def make_general_request(promo_id: int, page: int = 1, size: int = 100):
    
    url = f"https://loyalty.bff.bancogalicia.com.ar/api/portal/personalizacion/v1/promociones/list/carrusel/{promo_id}?page={page}&pageSize={size}&cardEspecial=true"
    
    payload = json.dumps({
      "idHost": "11388939",
      "nombre": "GONZALO AGUSTIN",
      "clienteInscripto": True,
      "localidad": "CIUDAD AUTONOMA BUENOS AIRES",
      "provincia": "CAPITAL FEDERAL",
      "idMiembro": 1838461,
      "requiereTour": False,
      "esEmpleado": False,
      "latitud": -34.59401,
      "longitud": -58.506954,
      "mediosDePago": [
        {
          "code": "TD",
          "description": "Tarjeta Galicia Débito",
          "modifierCode": "COM"
        },
        {
          "code": "TC",
          "description": "Tarjeta Visa",
          "modifierCode": "SIG"
        },
        {
          "code": "TD",
          "description": "Tarjeta Galicia Débito",
          "modifierCode": "GEN"
        },
        {
          "code": "TC",
          "description": "Tarjeta Visa",
          "modifierCode": "SIG"
        },
        {
          "code": "TC",
          "description": "Tarjeta Mastercard",
          "modifierCode": "BLK"
        },
        {
          "code": "TC",
          "description": "Tarjeta Mastercard",
          "modifierCode": "BLK"
        },
        {
          "code": "TC",
          "description": "Tarjeta Mastercard",
          "modifierCode": "BLK"
        }
      ],
      "modeloAtencion": "EMINENT",
      "iDsCategoria": [
        80,
        87,
        54,
        12,
        108
      ],
      "valorCliente": "Medio",
      "idAudiencia": 1,
      "cuitHaberes": [
        "30717059936"
      ]
    })
    headers = {
      'Content-Type': 'application/json',
      #'Cookie': '2fc044ee01a62af6f8bb6eda277c47b3=2f6adfd19c61aa601620ee30bdd87067; 9968fd69d4ba3e8459cf106b95f7ee71=cdf18767e1a30370906d68de40821856; TS0119cb3b=019d4f32552aac9abac536b57fb7ef72ae1c05b2959810af6c613b95f17fb6689b1677db35c143a70d7352e43789f985563f0cd94b'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response

def make_request(promotion_id):
    # The URL to make the request to
    url = f'https://loyalty.bff.bancogalicia.com.ar/api/portal/catalogo/v1/promociones/idPromocion/{promotion_id}'

    # Headers as specified in the curl command
    headers = {
        'Accept': 'application/vnd.iman.v1+json, application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,es-MX;q=0.8,es;q=0.7,pt-BR;q=0.6,pt;q=0.5,es-AR;q=0.4',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI5NzUwOGVmMC02NWZkLTRmMzMtOWJkNy1mM2ZjZjQ1NTQ1OWYiLCJpYXQiOjE3MTE5NDU1MDUsImlzcyI6IlBPQ0EiLCJzdWIiOiIxMDQ4NDg4IiwiYXVkIjoib25saW5lYmFua2luZyIsImJyYW5jaC1pZCI6bnVsbCwiY2FwLXNjb3BlIjoiaWRlbnRpdHkiLCJjYXNoYm94LWlkIjpudWxsLCJjbGllbnQtYXR0ZW50aW9uLWlkIjpudWxsLCJjbGllbnQtZGV2aWNlLWlkIjpudWxsLCJjbGllbnQtaWQiOiJPQkFXIiwiY2xpZW50LWlwIjpudWxsLCJjbGllbnQtc2Vzc2lvbi1pZCI6bnVsbCwiZGV2aWNlLXByaW50IjpudWxsLCJlbXBsb3llZS1pZCI6bnVsbCwiZW1wbG95ZWUtc3VwZXJ2aXNvci1pZCI6bnVsbCwiZnVuY2lvbmFsaXR5LWlkIjoiY2FwX2ltcGVyc29uYWxfbG9naW4',
        'Cache-Control': 'no-store, no-cache, must-revalidate',
        'Connection': 'keep-alive',
        'Origin': 'https://onlinebanking.bancogalicia.com.ar',
        'Pragma': 'no-cache',
        'Referer': 'https://onlinebanking.bancogalicia.com.ar/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'id_canal': 'Quiero',
        'id_channel': 'onlinebanking',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    # Make the GET request
    response = requests.get(url, headers=headers)
    
    return response

def get_data():
    segments = {}

    for i in range(0, 58):
        response = make_general_request(i, 1, 250)
        # print(json.loads(response.text))
        if response:
            if json.loads(response.text)['data']['promociones']['totalSize'] > 0:
                segments[i] = {
                    "titulo": json.loads(response.text)['data']['titulo'],
                    "total_size": json.loads(response.text)['data']['promociones']['totalSize'],
                    "data": json.loads(response.text)['data']['promociones']['list']
                }
            else:
                pass
    
    # NOS QUEDAMOS SOLAMENTE CON LOS MISMOS SEGMENTOS PERO QUE MÁS REGISTROS TIENE

    # Initialize a new dictionary to store the results
    max_dict = {}

    # Iterate through the original dictionary
    for key, value in segments.items():
        titulo = value['titulo'].lower().strip()  # Remove any leading/trailing whitespaces
        total_size = value['total_size']
        data = value['data']
        
        # Check if we already have an entry for this 'titulo'
        if titulo in max_dict:
            # If yes, compare the 'total_size' values
            if total_size > max_dict[titulo]['total_size']:
                # If the current entry has a larger 'total_size', replace the stored entry
                max_dict[titulo] = {'id': key, 'titulo': titulo, 'total_size': total_size, 'data': data}
        else:
            # If no, add this entry to the result dictionary
            max_dict[titulo] = {'id': key, 'titulo': titulo, 'total_size': total_size, 'data': data}

    big_list = [item for value in max_dict.values() for item in value['data']]

    # Assuming 'big_list' is your list of dictionaries
    big_dataframe = pd.DataFrame(big_list)
    big_dataframe = big_dataframe.drop_duplicates(subset=['id'])


    # Step 1: Find all unique combinations of 'tarjeta' and 'tipoTarjeta'
    unique_combinations = set()
    for row in big_dataframe['mediosDePago']:
        if row:  # Check if the entry is not empty or NaN
            unique_combinations.update(
                (d['tarjeta'].strip().lower(), d['tipoTarjeta'].strip().lower()) for d in row if 'tarjeta' in d and 'tipoTarjeta' in d
            )

    # Step 2: Create new boolean columns for each unique combination
    for tarjeta, tipo in unique_combinations:
        col_name = f'{tarjeta}_{tipo}_exists'
        big_dataframe[col_name] = False

    # Step 3: Update the boolean columns based on the 'mediosDePago' entries
    for index, row in big_dataframe.iterrows():
        if row['mediosDePago']:  # Check if the entry is not empty or NaN
            for d in row['mediosDePago']:
                # Check if both 'tarjeta' and 'tipoTarjeta' are present in the dict
                if 'tarjeta' in d and 'tipoTarjeta' in d:
                    col_name = f"{d['tarjeta'].strip().lower()}_{d['tipoTarjeta'].strip().lower()}_exists"
                    big_dataframe.at[index, col_name] = True

    return big_dataframe


async def filter_dataframe_based_on_selections(df, selected_cards, selected_category):
    category = categories_to_value_map.get(selected_category)
    category_filtered_df = df[df['subtitulo'] == category]
    
    # Start with a mask that selects nothing, we'll add to this as we go
    cards_mask = pd.Series([False] * len(df), index=df.index)
    
    # Update the mask for each selected option
    for option in selected_cards: 
        column_name = cards_to_column_map.get(option)
        if column_name:
            # Update the mask to include rows where the relevant column is True
            cards_mask = cards_mask | category_filtered_df[column_name].fillna(False)  # Using fillna(False) in case of NaN values
    
    # Return the filtered DataFrame, but only the columns we care about
    cards_filtered_df = category_filtered_df[cards_mask]

    # Get the ids of the promotions
    promotion_ids = list(cards_filtered_df.id)

    promotions = await get_single_promotion_data(promotion_ids)

    return promotions


async def get_single_promotion_data(promotion_ids: list):
  results = []
  for promotion_id in promotion_ids:
    response = make_request(promotion_id)
    if response:
      data = json.loads(response.text)
      results.append(data)
  return results


def get_dias_aplicacion(dias: str):
    dias_aplicacion = {
        "Lu": "Lunes",
        "Ma": "Martes",
        "Mi": "Miércoles",
        "Ju": "Jueves",
        "Vi": "Viernes",
        "Sa": "Sábado",
        "Do": "Domingo"
    }

    # Split the 'dias' string into individual day abbreviations
    dias_abbr = dias.split(';')

    # Map each abbreviation to its full day name
    dias_full = [dias_aplicacion[abbr] for abbr in dias_abbr]

    # Join the full day names into a single string, separated by commas
    dias_str = ', '.join(dias_full)

    return dias_str
