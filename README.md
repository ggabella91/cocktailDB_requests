This program makes calls to TheCocktailDB's free JSON API to fetch data about cocktails and ingredients in that database, and then serves it to the user.

The program first queries a local MySQL database, which stores data from previous API calls if the data wasn't already present in the database.

If a match is found in the database, it serves the desired data to the user. If no match is found in the database, the program makes a new call to TheCocktailDB's API.