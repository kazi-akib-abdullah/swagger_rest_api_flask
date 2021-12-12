import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="parsingData"
)


def queryData(location, name, bedroom, bathroom, price, sleeps):
  jsonData = []
  mycursor = mydb.cursor()
  query = "SELECT * FROM Villa WHERE "
  # for map in mapping:
  if location!=None:
    if query == "SELECT * FROM Villa WHERE ":
      query = query + ("Location ="+f"'{location}' " )
    else:
      query = query + ("AND Location ="+f"'{location}'")
  if name!=None:
    if query == "SELECT * FROM Villa WHERE ":
      query = query + ("Name ="+f"'{name}' " )
    else:
      query = query + ("AND Name ="+f"'{name}'")
  if bedroom != None:
    if query == "SELECT * FROM Villa WHERE ":
      query = query + ("Bedroom ="+f"'{bedroom} Bedrooms' " )
    else:
      query = query + ("AND Bedroom ="+f"'{bedroom} Bedrooms'")
  if bathroom != None:
    if query == "SELECT * FROM Villa WHERE ":
      query = query + ("Bathroom ="+f"'{bathroom} Bathrooms' " )
    else:
      query = query + ("AND Bathroom ="+f"'{bathroom} Bathrooms'")
  if sleeps != None:
    if query == "SELECT * FROM Villa WHERE ":
      query = query + ("Sleeps ="+f"'Sleeps {sleeps}' " )
    else:
      query = query + ("AND Sleeps ="+f"'{sleeps}'")
  if price != None:
    if query == "SELECT * FROM Villa WHERE ":
      query = query + ("Price ="+f"'${price}' " )
    else:
      query = query + ("AND Price ="+f"'${price}'")
  print(query)
  mycursor.execute(query)
  myresult = mycursor.fetchall()

  for x in myresult:
    data = {
      "Title": x[0],
      "Sleeps": x[1],
      "Bedrooms": x[2],
      "Bathrooms": x[3],
      "Price": x[4],
      "Pictures": {
        "Picture_1": x[5][1:-1],
        "Picture_2": x[6][1:-1],
        "Picture_3": x[7][1:-1],
      },
      "Location": x[8],
    }
    jsonData.append(data)
  jsonData.sort(key=lambda x: x['Price'], reverse=True)
  json_object = json.dumps(jsonData, indent = 4)
  print(json_object)
  return json_object