import mysql.connector
from mysql.connector import errorcode
from time import sleep

def conectar_banco_de_dados():
    print("="*32 + " Gerenciador de dispositivos locais - Prominas " + "="*32)
    try:
        banco = mysql.connector.connect(
        host='localhost',
        user='root',
        password='As45Wd678Ty@',
        database='prmns'
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

def menu_principal():
    print("="*32 + " Gerenciador de dispositivos locais - Prominas " + "="*32)
    print("\n1. Submenu de Usuários.\n2. Submenu de Dispositivos.\n3. Submenu de Componentes.\n4. Gerar PDF.\n5. Gerar PDF.\n6. Sair")
    print("="*80)
    opcao = input("Entre com o dígito do submenu desejado: ")
    return opcao

def menu_usuario():
    print("="*32 + " Menu de Usuário " + "="*32)
    print("1. Inserir usuário.\n2. Listar usuários cadastrados.\n3. Apresentar usuário específico.\n4. Alterar dados de usuários.\n5. Deletar usuários.\n6. Voltar ao menu")
    opcao = input("Entre com o dígito da função desejada: ")
    return opcao

def menu_dispositivos():
    print("="*32 + " Menu de Dispositivos " + "="*32)
    print("")
    opcao = input("Entre com o dígito da função desejada: ")
    return opcao

def menu_componentes():
    print("="*32 + " Menu de Componentes " + "="*32)
    print("")
    opcao = input("Entre com o dígito da função desejada: ")
    return opcao

def verifica_usuario(cursor, id):
    sql = f'SELECT codUsu FROM usuario WHERE codUsu = ("{id}");'
    cursor.execute(sql)
    resultado = cursor.fetchone()
    if resultado:
        return False
    else:
        return True

def incluir_usuario(conexao, cursor):
    print("="*32 + "Cadastro de usuário" + "="*32)
    try:
        x = True
        while x:
            id = int(input("Identificador do usuário: "))
            validador = verifica_usuario(cursor, id)
            if validador == False:
                print("Esse Identificador já está em uso. Insira outro identificador para esse usuário.")
            else:
                nome = input("Nome do usuário: ")
                departamento = input("Nome do Departamento: ")
                exiSta = False
                while not exiSta:
                    status = input("Status do usuário (Ativo/Inativo): ").lower().capitalize()
                    if status in ["Ativo", "Inativo"]:
                        exiSta = True
                        estado = status
                    else:
                        print("Status inválido. Tente novamente.")
                sql_dep = f'INSERT INTO usuario (codUsu, nome, estado, departamento) VALUES ("{id}","{nome}","{estado}","{departamento}");'
                cursor.execute(sql_dep)
                conexao.commit()
                print("usuario cadastrado com sucesso!")
                x = False
    except mysql.connector.Error as error:
        print(f"Erro: {error}.")

def listar_usuarios(cursor):
    print("="*32 + "Listando usuarios cadastrados" + "="*32)
    sql_listagem_dep = f'SELECT * FROM usuario ORDER BY nome;'
    cursor.execute(sql_listagem_dep)
    busca = cursor.fetchall()
    if busca:
        print("ID | Nome | Status | Departamento")
        for usuarios in busca:
            print(usuarios)
    else:
        print("Não existem usuarios cadastrados no sistema. Inclua usuarios para poder visualiza-los")

def imprimir_usuario_especifico(cursor):
    print("="*32 + "Apresentando usuário específico" + "="*32)
    usuario = input("Identificador do usuário: ").lower().capitalize()
    sql_dep_espec = f'SELECT * FROM usuario WHERE codUsu = ("{usuario}");'
    cursor.execute(sql_dep_espec)
    busca = cursor.fetchone()
    if busca:
        print(f"ID | Nome | Status | Departamento\n{busca}")
    else:
        print("O usuario indicado não pode ser encontrado. Verifique se o mesmo consta na base de dados atual.")

def alteracao_usuario(conexao,cursor):
    print("="*32 + "Alterando dados de usuário" + "="*32)
    id = int(input("Identificador do usuário: "))
    validador = verifica_usuario(cursor, id)
    if validador == False:
        opcao = input("1. Alterar nome.\n2. Alterar Status.\n3. Alterar Departamento")
        if opcao == "1":
            nome = input("Nome de usuário\nNome: ")
            sql_alter_nome = f'UPDATE usuario SET nome = ("{nome}") WHERE codUsu = ("{id}");'
            cursor.execute(sql_alter_nome)
            conexao.commit()
            print(f"O nome do usuário {id} foi alterado com sucesso!")
        if opcao == "2":
            exiSta = False
            while not exiSta:
                status = input("Status do usuário (Ativo/Inativo): ").lower().capitalize()
                if status in ["Ativo", "Inativo"]:
                    exiSta = True
                    estado = status
                else:
                    print("Status inválido. Tente novamente.")
                sql_alter_sta = f'UPDATE usuario SET estado = ("{estado}") WHERE codUsu = ("{id}");'
                cursor.execute(sql_alter_sta)
                conexao.commit()
                print(f"O status do usuário {id} foi alterado com sucesso!")
        elif opcao == "3":
            departamento = input("Alterando nome do departamento\nDepartamento: ")
            sql_alter_dep = f'UPDATE usuario SET departamento = ("{departamento}") WHERE codUsu = ("{id}");'
            cursor.execute(sql_alter_dep)
            conexao.commit()
            print(f"O nome do departamento do usuário {id} foi alterado com sucesso!")
        else:
            print("Opção inválida. Tente novamente.")
    else:
        print("Não foi possível encontrar o usuário informado. Verifique se o mesmo consta na base de dados atual.")

def deletar_usuario(conexao, cursor):
    print("="*32 + "Deletando usuário" + "="*32)
    id = input("Identificador do usuário: ").lower().capitalize()
    validador = verifica_usuario(cursor, id)
    if validador == False:
        sql_verif_status = f'SELECT estado FROM usuario WHERE codUsu = ("{id}")'
        cursor.execute(sql_verif_status)
        status = cursor.fetchone()[0]
        if status == "Inativo":
            sql_delete_usu = f'DELETE FROM usuario WHERE codUsu = ("{id}")'
            cursor.execute(sql_delete_usu)
            conexao.commit()
            print(f"O Usuário {id} foi deletado com sucesso!")
        else:
            print(f"O usuário {id} está ativo, portanto não pode ser deletado.")
    else:
        print("Não foi possível encontrar o usuário informado. Verifique se o mesmo consta na base de dados atual.")

def main():
    banco = conectar_banco_de_dados()
    cursor = banco.cursor()
    opcao = menu_principal()
    while opcao != "6":
        if opcao == "1":
            op_usu = menu_usuario()
            while op_usu != "6":
                if op_usu == "1":
                    incluir_usuario(banco,cursor)
                elif op_usu == "2":
                    listar_usuarios(cursor)
                elif op_usu == "3":
                    imprimir_usuario_especifico(cursor)
                elif op_usu == "4":
                    alteracao_usuario(banco,cursor)
                elif op_usu == "5":
                    deletar_usuario(banco, cursor)
                op_usu = menu_usuario()
        elif opcao == "2":
            op_disp = menu_dispositivos()
            

        elif opcao == "3":
            op_comp = menu_componentes()
            

        elif opcao == "4":
            print("Em construção")
        else:
            print("Opção inválida. Tente novamente com uma das opções disponíveis no menu.")
        opcao = menu_principal()
        banco.commit()
    desligandoSistema()
    cursor.close()
    banco.close()

if __name__ == "__main__":
    main()