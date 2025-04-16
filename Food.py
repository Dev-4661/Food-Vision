import requests
from urllib.parse import unquote
import os
from dotenv import load_dotenv
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Force reload environment variables
load_dotenv(override=True)
api_key = os.getenv('alter_spoonacular_api')
logger.info(f"Loaded API key: {api_key[:5]}...")  # Log first 5 chars of API key for verification

if not api_key:
    raise ValueError("alter_spoonacular_api not found in environment variables")

# For testing API key validity
def test_api_key():
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {'apiKey': api_key, 'query': 'test', 'number': 1}
    response = requests.get(url, params=params)
    logger.info(f"API Key Test - Status Code: {response.status_code}")
    return response.status_code == 200

# Test API key on module load
if not test_api_key():
    logger.error("API key validation failed!")

# For getting recipe details
def search_recipe(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey':api_key,
        'query':query,
        'number':10,
        'instructionsRequired':True,
        'addRecipeInformation':True,
        'fillIngredients':True
    }

    # Sending GET request to api
    logger.info(f"\nSearching recipes for: {query}")
    response = requests.get(url, params=params)
    logger.info(f"API Response: {response.status_code}")
    
    # if the API call is successful
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        logger.info(f"Found {len(results)} recipes")
        return results
    else:
        logger.error(f"API Error: {response.text}")
        return []

def FoodInformation(class_name):
    logger.info(f"\nProcessing food: {class_name}")
    recipe = search_recipe(class_name)
    return recipe


# For getting the information of a specific food
def view_recipe(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': api_key,
    }

    logger.info(f"Retrieving recipe information for: {recipe_id}")
    response = requests.get(url, params=params)

    if response.status_code == 200:
        logger.info(f"Recipe information retrieved successfully")
        recipe = response.json()
        return recipe
    else:
        logger.error(f"API Error: {response.text}")
        return 'Recipe not found',404


# Getting nutritional information
def get_food_nutrition(product_id):
    url = f'https://api.spoonacular.com/food/products/{product_id}'
    params = {
        'apiKey': api_key
    }

    logger.info(f"Retrieving nutritional information for product: {product_id}")
    # Sending GET request to api
    response = requests.get(url, params=params)

    # if the API call is successful
    if response.status_code == 200:
        logger.info(f"Nutritional information retrieved successfully")
        # Parse the API response as JSON Data
        data = response.json()
        # Return the detailed nutritional information for the product
        nutrition_info = data.get('nutrition', {})
        return nutrition_info

    # If not successful
    logger.error(f"API Error: {response.text}")
    return {}

def search_food_nutrition(query):
    url = f'https://api.spoonacular.com/food/products/search'
    params = {
        'apiKey': api_key,
        'query': query,
        'number': 1
    }

    logger.info(f"Searching for food nutrition information: {query}")
    # Sending GET request to api
    response = requests.get(url, params=params)

    # if the API call is successful
    if response.status_code == 200:
        logger.info(f"Food nutrition information retrieved successfully")
        # Parse the API response as JSON Data
        data = response.json()
        
        # Check if products are found
        if data['totalProducts'] > 0:
            product_id = data['products'][0]['id']
            nutrition_info = get_food_nutrition(product_id)
            return nutrition_info

    # If not successful
    logger.error(f"API Error: {response.text}")
    return {}


# Function to get restaurant search response

# Function to get restaurant search response
def get_restaurant_search(query):
    url = 'https://api.spoonacular.com/food/restaurants/search'
    params = {
        'apiKey': api_key,
        'query': query,
        'lat': 19.2183,
        'lng': 72.9781,
        'distance': 5
    }

    logger.info(f"Searching for restaurants: {query}")
    # Sending GET request to the API
    response = requests.get(url, params=params)

    # Check if the API call is successful
    if response.status_code == 200:
        logger.info(f"Restaurant search results retrieved successfully")
        # Parse the API response as JSON data
        data = response.json()
        # Return the response data
        return data

    # If not successful
    logger.error(f"API Error: {response.text}")
    return None


# Nutritional Label
def get_nutrition_label_image(recipe_id, filename=None):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/nutritionLabel.png'
    params = {'apiKey': api_key}
    logger.info(f"Retrieving nutrition label image for recipe: {recipe_id}")
    response = requests.get(url, params=params)
    if response.status_code == 200:
        logger.info(f"Nutrition label image retrieved successfully")
        if filename is None:
            filename = f'static/neutritional_img/Neutritional.png'  # Changed filename to include folder path
        else:
            filename = f'static/neutritional_img/{filename}'  
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        logger.error(f"API Error: {response.text}")
        return f"Error: {response.status_code} - {response.text}"
