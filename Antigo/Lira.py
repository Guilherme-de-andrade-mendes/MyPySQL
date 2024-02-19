import mysql.connector
from mysql.connector import errorcode

try:
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='As45Wd678Ty@',
        database='prmns'
    )
    print("Conexão criada com sucesso!")
except mysql.connector.Error as error:
    if error.errno == errorcode.ER_BAD_DB_ERROR:
        print("Essa base de dados não existe. Tente novamente.")
    elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("O usuário ou senha informado não está correto.")
    else:
        print(f"Erro inesperado: {error}.")

cursor = conexao.cursor()  # Cria a conexão com o banco

# CREATE
'''
codDisp = "INF-106"
disStatus = "Ativo"
dispSO = "Windows 11 Professional"
chaveAtiv = "TGYRN-FV3JH-H4D95-DX7QW-4VV26"
espaco = []

y = True
while y:
    particao = input("Espaço de armazenamento da partição: ").upper()
    espaco.append(particao)
    pgt = input("Deseja inserir uma nova partição (s/n): ").lower()
    if pgt == "n":
        y = False

# Inserir na tabela dispositivo
sql_dispositivo = f'INSERT INTO dispositivo (codDisp, dispStatus, dispSO, chaveAtiv) VALUES ("{codDisp}","{disStatus}","{dispSO}","{chaveAtiv}");'
cursor.execute(sql_dispositivo)

# Inserir na tabela armazenamento
sql_armazenamento = f'INSERT INTO armazenamento (codDisp, espaco) VALUES '
sql_armazenamento += ', '.join([f'("{codDisp}", "{particao}")' for particao in espaco])
cursor.execute(sql_armazenamento)
conexao.commit()  # Confirmar as operações no banco de dados
'''

# READ
'''
sql_mostrar = f'SELECT d.codDisp, d.dispStatus, d.dispSO, d.chaveAtiv, a.espaco FROM dispositivo d INNER JOIN armazenamento a on d.codDisp = a.codDisp;'
cursor.execute(sql_mostrar)
resultado = cursor.fetchall() # Ler banco de dados
print(resultado)
'''

# UPDATE
'''
codDisp = "INF-106"
dispSO = "Windows 10 Professional"
sql_update = f'UPDATE dispositivo SET dispSO = "{dispSO};" WHERE codDisp  = "{codDisp}";'
cursor.execute(sql_update)
conexao.commit()
'''

# DELETE
'''
codDisp = "INF-106"
sql_delete_armazenamento = f'DELETE FROM armazenamento WHERE codDisp = "{codDisp}";'
sql_delete_dispositivo = f'DELETE FROM dispositivo WHERE codDisp = "{codDisp}";'
cursor.execute(sql_delete_armazenamento)
cursor.execute(sql_delete_dispositivo)
conexao.commit()
'''

cursor.close()
conexao.close()
