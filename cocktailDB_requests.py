import requests

def main():

	while True:
		print("\nWhat would like to do?\n\n 1. Get instructions for a cocktail\n 2. List all cocktails that start with a given letter\n 3. Quit \n")
		choice = input(f"Enter the number corresponding to your chosen action: ")

		if choice == "1":
			get_drinks()
		elif choice == "2":
			list_cocktails()
		elif choice == "3":
			return False
		else:
			print("Invalid option. Please try again :)\n")


def list_cocktails():
	
	while True:
		letter = input("\nPlease enter a letter: ")
		if letter.isalpha():
			break
		else:
			print("Invalid character. Please enter a letter.\n")

	g = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}")

	print(f"\nCocktails that start with the letter {letter}:\n")
	for d in g.json()["drinks"]:
		print(d.get("strDrink"))
	print("\n")


def get_drinks():

	while True:
		drink = input("\nPlease enter a cocktail name: ")
		g = requests.get(f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}")
		
		if g.json()["drinks"] is None:
			print("Invalid cocktail name. Please try again :)\n")
		else:
			break
	
	ingredients  = []

	for k,v in g.json()["drinks"][0].items():
		if "strIngredient" in k:
			if v is not None:
				ingredients.append(v)

	gd = [d.get("strInstructions") for d in g.json()["drinks"]]

	print(f"\nIngredients for {drink}:\n")

	for item in ingredients:
		print(item)

	print(f"\nHow to make a {drink}:\n")
	print(gd[0])

# END OF PROGRAM FUNCTIONALITY DECLARATIONS
# PROGRAM EXECUTION STARTS BELOW THIS LINE

main()