This program makes calls to TheCocktailDB's free JSON API to fetch data about cocktails and ingredients in that database, and then serve it to the user.

The program first queries a local MySQL database, which stores data from previous API calls if the data wasn't already present in the database. If no match is found in the database, the program makes a new call to TheCocktailDB's API.