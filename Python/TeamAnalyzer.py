import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

connection = sqlite3.connect('pokemon.sqlite')
cursor = connection.cursor()

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):

    if i == 0:
        continue

    # query to find pokemon name from given index
    #print(str(arg))
    queryval = "SELECT name from pokemon WHERE pokedex_number = " + str(arg)
    pokemon = cursor.execute(queryval)
    pokemon = cursor.fetchone()
    pokemon = str(pokemon)
    pokemon = pokemon[2:-3]
    #print(pokemon)

    # query to find the first type
    typeval1 = "SELECT type.name FROM type JOIN pokemon_type JOIN pokemon ON pokemon.pokedex_number = pokemon_type.pokemon_id AND pokemon_type.type_id = type.id WHERE pokemon_type.which = 1 AND pokedex_number = " +str(arg)
    type1 = cursor.execute(typeval1)
    type1 = cursor.fetchone()
    type1 = str(type1)
    type1 = type1[2:-3]

    # query to find the id for the first type to be used in a later query
    typeval1 = "SELECT type.id FROM type JOIN pokemon_type JOIN pokemon ON pokemon.pokedex_number = pokemon_type.pokemon_id AND pokemon_type.type_id = type.id WHERE pokemon_type.which = 1 AND pokedex_number = " + str(arg)
    type1num = cursor.execute(typeval1)
    type1num = cursor.fetchone()
    type1num = str(type1num)
    type1num = type1num[1:-2]
    #print(type1)
    #print(type1num)

    # query to find the second type
    typeval2 = "SELECT type.name FROM type JOIN pokemon_type JOIN pokemon ON pokemon.pokedex_number = pokemon_type.pokemon_id AND pokemon_type.type_id = type.id WHERE pokemon_type.which = 2 AND pokedex_number = " +str(arg)
    type2 = cursor.execute(typeval2)
    type2 = cursor.fetchone()
    type2 = str(type2)
    type2 = type2[2:-3]

    # query to find the id for the second type to be used in a later query
    typeval2 = "SELECT type.id FROM type JOIN pokemon_type JOIN pokemon ON pokemon.pokedex_number = pokemon_type.pokemon_id AND pokemon_type.type_id = type.id WHERE pokemon_type.which = 2 AND pokedex_number = " + str(arg)
    type2num = cursor.execute(typeval2)
    type2num = cursor.fetchone()
    type2num = str(type2num)
    type2num = type2num[1:-2]
    #print(type2)
    #print(type2num)

    # declare lists for strong and weak
    strong = []
    weak = []

    # determines the strengths and weakness by looping over the list of types
    for name in types:

        valagainst = "SELECT against_" + name +" FROM against WHERE type_source_id1 = " + type1num + " AND type_source_id2 = " + type2num
        cursor.execute(valagainst)
        agianst = cursor.fetchone()
        agianst = str(agianst)
        agianst = agianst[1:-2]
        agianst = float(agianst)

        if agianst > 1.0:
            strong.append(name)
        if agianst < 1.0:
            weak.append(name)

    #builds and prints the final output to console + makes the team list
    sentence = ""
    if type2num == '19':
        sentence = pokemon + " (" + type1 + ") is strong against " + str(strong) + " but is weak against " + str(weak)
    else:
        sentence = pokemon + " (" + type1 + " " + type2 + ") is strong against " + str(strong) + " but is weak against " + str(weak)

    team.append(sentence)
    print("Analyzing " + str(arg))
    print(sentence)


cursor.close()
    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

