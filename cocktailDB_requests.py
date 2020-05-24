import requests
import queries
import time

def main():

	while True:
		print("\nWhat would you like to do?\n\n"
		"1. Get instructions for a cocktail\n" 
		"2. List all cocktails that start with a given letter\n" 
		"3. Learn about an ingredient\n"
		"4. Quit\n")

		choice = input(f"Enter the number corresponding to your chosen action: ")

		if choice == "1":
			get_drink_details()
		elif choice == "2":
			list_cocktails()
		elif choice == "3":
			get_ingredient_details()
		elif choice == "4":
			return False
		else:
			print("Invalid option. Please try again :)\n")



def list_cocktails():
	
	while True:
		letter = input("\nPlease enter a letter: ")
		if letter.isalpha() and len(letter) == 1:
			break
		else:
			print("\nInvalid input. Please enter a single letter.\n")

	g = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}")

	print(f"\nCocktails that start with the letter {letter}:\n")
	if g.json()["drinks"]:
		for d in g.json()["drinks"]:
			print(d.get("strDrink"))
		print("\n")
	else:
		print(f"No matches for the letter '{letter}.' Please try again.")


def get_drink_details():

	while True:
		drink = input("\nPlease enter a cocktail name: ")
		
		print("\nStarting query:\n")
		start_time = time.time()
		query = queries.query_cocktail(drink)

		if query:
			break
		else:
			print("No matching results from query. Starting API call.")
			g = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}")
		
			if g.json()["drinks"] is None:
				print("Invalid cocktail name. Please try again :)\n")
			else:
				break
		
	ingredients  = []
	measures = []
	if query:
		print("Query complete. Match found!\n")
		stop_time = time.time() - start_time
		print(f"Query duration: {round(stop_time, 5)} seconds.\n")
		print(f"About {query['name']}:\n")
		print(f"Category: {query['category']}\n")
		print(f"IBA Category: {query['IBA_category']}\n")
		alcoholic_int_map = {0 : "Non alcoholic", 1 : "Alcoholic", 2 : "Optional alcohol"}
		print(f"Alcoholic: {alcoholic_int_map[query['alcoholic']]}\n")
		print(f"Glass: {query['glass']}\n")
		print(f"Ingredients for {query['name']}:\n")
		for item in query["ingredient measures"]:
			print(f"{item}")
		print(f"\nHow to make a {query['name']}:\n")
		print(query["instructions"])
		##### GET INGREDIENTS FROM DATABASE ###########
	else:
		for k,v in g.json()["drinks"][0].items():
			if "strIngredient" in k:
				if v is not None:
					ingredients.append(v)
			elif "strMeasure" in k:
				if v is not None:
					measures.append(v)
			
		ingredient_measures = tuple(zip(measures, ingredients))

		drink_name = g.json()["drinks"][0].get("strDrink")
		foreign_drink_id = g.json()["drinks"][0].get("idDrink")
		category = g.json()["drinks"][0].get("strCategory")
		cat_IBA = g.json()["drinks"][0].get("strIBA")
		alc = g.json()["drinks"][0].get("strAlcoholic")
		alcoholic_map = {"Non alcoholic": 0, "Alcoholic": 1, "Optional alcohol": 2}
		is_alcoholic = alcoholic_map[alc]
		glass = g.json()["drinks"][0].get("strGlass")
		instructions = g.json()["drinks"][0].get("strInstructions")

		print("\nAPI call complete!\n")
		stop_time = time.time() - start_time
		print(f"API call duration: {round(stop_time,5)} seconds.\n")

		drink_details = {"name" : drink_name, "category" : category,
						"IBA_category" : cat_IBA, "alcoholic": is_alcoholic,
						"foreign_id" : foreign_drink_id, "glass" : glass,
						"instructions" : instructions, 
						"ingredient measures" : ingredient_measures}
		
		#### INSERT DATA INTO THE SQL DATABASE #######
		queries.insert_drink_details(drink_details)
		##############################################

		print(f"\nIngredients for {drink_name}:\n")

		for item in ingredient_measures:
			print(f"{item[0]} {item[1]}")

		print(f"\nHow to make a {drink_name}:\n")
		print(instructions)


def get_ingredient_details():
	
	while True:
		ingredient = input("\nPlease enter an ingredient name: ")

		query = queries.query_ingredient(ingredient)

		if query[0] != -10 and len(query) == 2:
			break
		else:
			g = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?i={ingredient}")

			if g.json()["ingredients"] is None:
				print("\nInvalid ingredient name. Please try again :)\n")
			else:
				break
	
	if len(query) == 2:
		print(f"\nAbout {ingredient}:\n")
		print(f"{query[1]}")
	else:
		ingredient_name = g.json()["ingredients"][0].get("strIngredient")
		ingred_desc = g.json()["ingredients"][0].get("strDescription")

		print(f"\nAbout {ingredient_name}:\n")
		
		if ingred_desc is None:
			print("No description available for this item. Sorry!")
		else:
			queries.insert_ingredient_description(ingredient_name, ingred_desc)
			print(f"\n{ingred_desc}")


# END OF PROGRAM FUNCTIONALITY DECLARATIONS
# PROGRAM EXECUTION STARTS BELOW THIS LINE
main()