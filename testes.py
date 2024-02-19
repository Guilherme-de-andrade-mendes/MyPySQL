import mysql.connector
from time import sleep
from mysql.connector import errorcode

def conectar_banco_de_dados():
    print("="*32 + " Gerenciador de dispositivos locais - Prominas " + "="*32)
    try:
        banco = mysql.connector.connect(
        host='localhost',
        user='root',
        password='As45Wd678Ty@',
        database='prmns_testes'
        )
        print("Conexão criada com sucesso!")
        return banco
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Essa base de dados não existe. Tente novamente.")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("O usuário ou senha informado não está correto.")
        else:
            print(f"Erro inesperado: {error}.")

def desligandoSistema():
    for x in range(1,4):
        print(f"Desligando{'.'*x}", end='\r')
        sleep(0.5)

def menu():
    print("="*32 + " Gerenciador de dispositivos locais - Prominas " + "="*32)
    print("1. Nova máquina.\n2. Mostrar todos.\n3. Mostrar uma máquina.\n4. Alterar especificações de uma máquina.\n5. Excluir.\n6. Excluir todos.\n7. Gerar PDF.\n8. Sair")
    print("="*80)
    opcao = input("Entre com o dígito da função desejada: ")
    return opcao

def valida_identificador(cursor):
    while True:
        nome = input("Nome da máquina: ").upper()
        sql = f'SELECT codDisp FROM dispositivo WHERE codDisp = ("{nome}");'
        cursor.execute(sql)
        resultado = cursor.fetchone()
        if resultado:
            print("Essa máquina já existe. Tente novamente.")
        else:
            return nome

def incluir_maquina(conexao, cursor):
    print("="*32 + "Cadastrando dispositivo" + "="*32)
    try:
        valida = valida_identificador(cursor)
        nome = valida
        exiSta = False
        while not exiSta:
            x = input("Status da máquina (Ativo/Inativo): ").lower().capitalize()
            if x in ["Ativo", "Inativo"]:
                exiSta = True
                status = x
        sistemaOperacional = input("Sistema Operacional: ").lower().capitalize()
        chaveDeAtivacao = input("Chave de ativação: ").upper()
        particoes = []
        y = True
        while y:
            particao = input("Espaço de armazenamento da partição: ").upper()
            sql_particao = f'SELECT codEspaco '
            particoes.append(particao)
            pgt = input("Deseja inserir uma nova partição (s/n): ").lower()
            if pgt == "n":
                y = False
        print("Dispositivo inserido com sucesso!")
        sql_dispositivo = f'INSERT INTO dispositivo (codDisp, dispStatus, dispSO, chaveAtiv) VALUES ("{nome}","{status}","{sistemaOperacional}","{chaveDeAtivacao}")'
        cursor.execute(sql_dispositivo)
        sql_armazenamento = f'INSERT INTO armazenamento (codDisp, espaco) VALUES '
        sql_armazenamento += ', '.join([f'("{nome}", "{particao}")' for particao in particoes])
        cursor.execute(sql_armazenamento)
        conexao.commit()
        print("Dispositivo inserido com sucesso!")
    except mysql.connector.Error as error:
        print(error)

def mostrar_todos(cursor):
    sql = f'SELECT d.codDisp, d.dispStatus, d.dispSO, d.chaveAtiv, a.espaco FROM dispositivo d INNER JOIN armazenamento a on d.codDisp = a.codDisp ORDER BY d.codDisp asc;'
    cursor.execute(sql)
    busca = cursor.fetchall() # Ler banco de dados
    if busca:
        print(f"Nome | Status | Sistema Operacional | Chave de ativação | Armazenamento")
        for dispositivos in busca:
            print(dispositivos)
    else:
        print("Não existem dispositivos cadastrados no sistema. Inclua dispositivos para poder visualiza-los.")
    
def imprimir_maquina_especifica(cursor):
    print("="*32 + "Mostrando dispositivo específico" + "="*32)
    nome = input("Nome da máquina: ").upper()
    sql = f'SELECT d.codDisp, d.dispStatus, d.dispSO, d.chaveAtiv, a.espaco FROM dispositivo d INNER JOIN armazenamento a on d.codDisp = a.codDisp WHERE d.codDisp = ("{nome}");'
    cursor.execute(sql)
    busca = cursor.fetchall()
    
    if busca:
        print(busca)
    else:
        print("O dispositivo indicado não pode ser encontrado. Verifique se o mesmo consta na base de dados atual.")

def buscar_dispositivo(cursor):
    nome = input("Nome da máquina: ").upper()
    sql = f'SELECT codDisp FROM dispositivo WHERE codDisp = ("{nome}");'
    cursor.execute(sql)
    resultado = cursor.fetchone()
    if resultado:
        return nome
    else:
        return False

def alterar_especificacao(conexao, cursor):
    identificador = buscar_dispositivo(cursor)
    if identificador:
        opcao = input("="*32 + "Alterando especificações do dispositivo" + "="*32 + "\n1. Status.\n2. Sistema Operacional.\n3. Chave de ativação.\n4. Partições\nEntre com o dígito da opção que deseja alterar no dispostivo: ")
        if opcao == "1":
            print("Alterando Status do dispositivo\n")
            exiSta = False
            while not exiSta:
                x = input("Status da máquina (Ativo/Inativo): ").lower().capitalize()
                if x in ["Ativo", "Inativo"]:
                    exiSta = True
                    status = x
                    sql_status = f'UPDATE dis'
    else:
        print("O dispositivo indicado não pode ser encontrado. Verifique se o mesmo consta na base de dados atual.")


def main():
    banco = conectar_banco_de_dados()
    cursor = banco.cursor()
    opcao = menu()
    while opcao != "8":
        if opcao == "1":
            incluir_maquina(banco, cursor)
        elif opcao == "2":
            mostrar_todos(cursor)
        elif opcao == "3":
            imprimir_maquina_especifica(cursor)
        elif opcao == "4":
            alterar_especificacao(banco, cursor)
        else:
            print("Opção inválida. Tente novamente com uma das opções disponíveis no menu.")
        opcao = menu()
        banco.commit()
    desligandoSistema()
    cursor.close()
    banco.close()

if __name__ == "__main__":
    main()