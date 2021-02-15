import random
import mysql.connector
import cpuinfo
import time

mydb = mysql.connector.connect(
    host="mysql5044.site4now.net",
    user="a6f0a3_dacoinn",
    password="test12345",
    database="db_a6f0a3_dacoinn"
)

print(mydb)

mycursor = mydb.cursor(buffered=True)


def add_row(table, columns_values={}):
    sql_command = "INSERT INTO " + table + " ("
    columns_list_keys = list(columns_values.keys())
    columns_list_values = list(columns_values.values())

    for i in range(len(columns_list_keys)):
        sql_command += str(columns_list_keys[i])
        if i <= (len(columns_list_keys) - 2):
            sql_command += ", "
        else:
            sql_command += ")"

    sql_command += " VALUES ("

    for i in range(len(columns_list_values)):

        if type(columns_list_values[i]) == type("R"):
            sql_command += "\'"
            sql_command += columns_list_values[i]
            sql_command += "\'"
        else:
            sql_command += str(columns_list_values[i])

        if i <= (len(columns_list_values) - 2):
            sql_command += ", "
        else:
            sql_command += ");"
    mycursor.execute(sql_command)
    mydb.commit()


def delete_row(table, column, value):
    sql_command = "DELETE FROM " + str(table) + " WHERE " + str(column) + " = " + str(value)
    mycursor.execute(sql_command)
    mydb.commit()
    return sql_command


def add_array(table, column, n_array):
    sql_command = "INSERT INTO " + table + " (" + column + ")" + "VALUES (" + n_array + ");"
    mycursor.execute(sql_command)
    mydb.commit()


def change_element(table, change_column, column, og_value, value):
    sql_command = "UPDATE " + table + " SET " + change_column + " = " + value + " WHERE " + column + " = " + og_value
    mycursor.execute(sql_command)
    mydb.commit()


def read_element(table, column, return_column, value_at_column):
    sql_command = "SELECT " + return_column + " FROM " + table + " WHERE " + str(column) + " = " + value_at_column
    mycursor.execute(sql_command)
    mydb.commit()

    toreturn = mycursor.fetchall()

    for x in toreturn:
        toreturn = ''.join(x)

    return toreturn


def count_rows(table):
    sql_command = "SELECT COUNT(*) FROM " + table + ";"
    mycursor.execute(sql_command)
    mydb.commit()
    toreturn = mycursor.fetchall()

    toreturn = toreturn[0]
    toreturn = int(toreturn[0])

    return toreturn


def difficulty():
    blockTime = 0
    size = count_rows("mined")
    for x in ((size - 11), (size - 1)):
        blockTime += int(read_element("mined", "row_id", "block_time", str(x)))

    return (75 / (blockTime / 10)) * 250000000


def mald256(hash):
    prevBlock = read_element("blocks", "block_height", "block_hash",
                             read_element("variables", "var_name", "var_value", "smallest_unmined_block"))

    guess = ["" for x in range(32)]
    possibilites = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    guess[0] = prevBlock[28]
    guess[1] = prevBlock[29]
    guess[2] = prevBlock[30]
    guess[3] = prevBlock[31]

    for x in range(4, 32):
        for i in range(62):
            guess[x] = possibilites[i]
            if guess[x] == hash[x]: break

    return "".join(guess)


def interface():
    global mineAt
    global totalCoins
    global height

    mineAt = input("ENTER ADDRESS TO MINE AT: ")
    print("\n\nINITIALIZING - MINING AT ADDRESS " + mineAt)
    print("\nMINING ON " + cpuinfo.get_cpu_info()['brand_raw'])

    while True:
        hash = read_element("blocks", "block_height", "block_hash",
                            read_element("varibles", "var_name", "var_value", "smallest_unmined_block"))

        blockReward = read_element("blocks", "block_hash", "reward", hash)

        speedTest1 = time.time()

        diff = difficulty()
        print("\n\n-------------------------------------")
        print("MINING BLOCK: " + str(height) + " - DIFFICULTY: " + str(round(diff / 1000000, 1)) + " MH")
        print("-------------------------------------")

        for x in range(0, diff):
            if (x % 10000000 == 0 and x != 0):
                print("Hash " + str(round(x / 1000000)) + " million")

            map(mald256, hash)

        speedTest2 = time.time()

        print("\n\n\n\n\n\nBLOCK WORK COMPLETED; HASH: " + hash)

        blockTime = round(speedTest2 - speedTest1)

        hashSpeed = round((diff / 1000000) / blockTime, 3)

        change_element()

    print("\nSpeed: " + str(hashSpeed) + "MH/s")

    print("Block Time: " + str(blockTime) + " seconds")

    print("\nAccount " + mineAt + " recieved " + str(blockReward) + " MALDCOIN")


def getBlock():
    lowestBlock = read_element("variables", "var_name", "var_value", "smallest_unmined_block")[0]

    return read_element("blocks", "block_height", "block_hash", lowestBlock)


#HELLO THIS IS A COMMENT LMAO



