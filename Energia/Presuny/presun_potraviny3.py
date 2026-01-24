import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="slniecko",
  database = "energia"
)

mycursor = mydb.cursor()

sql = "INSERT INTO potraviny (nazov, bielkoviny, sacharidy, tuky) VALUES (%s, %s, %s, %s)"


with open('Potraviny3.csv', encoding='utf8') as f:
    row_count = 1
    for line in f:
        if row_count != 1:
            values = tuple(line.strip().split(','))
            mycursor.execute(sql, values)
            mydb.commit()
        row_count += 1
