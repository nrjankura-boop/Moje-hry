import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="slniecko",
  database = "energia"
)

mycursor = mydb.cursor()

sql = "INSERT INTO potraviny (nazov, tuky, bielkoviny, sacharidy) VALUES (%s, %s, %s, %s)"


with open('Potraviny2.csv', encoding='utf8') as f:
    row_count = 1
    for line in f:
        if row_count != 1:
            values = line.strip().split(',')
            values[1] = values[1].strip('g').strip()
            values[2] = values[2].strip('g').strip()
            values[3] = values[3].strip('g').strip()
            values = tuple(values)
            mycursor.execute(sql, values)
            mydb.commit()
        row_count += 1
