import mysql.connector
from mysql.connector import errorcode
from time import sleep
import datetime as dt

def informacoes_banco_dados():
    print("="*32 + " Informações do banco de dados " + "="*32)
    ipv4 = input("Endereço de IPv4: ")
    usuario = input("Usuário da sessão: ")
    senha = input("Senha: ")
    base_dados = input("Banco de dados: ")
    return conectar_banco_de_dados(ipv4,usuario,senha,base_dados)

def conectar_banco_de_dados(ipv4,usuario,senha,base_dados):
    print("="*32 + " Gerenciador de dispositivos locais - Prominas " + "="*32)
    try:
        banco = mysql.connector.connect(
        host = ipv4,
        user = usuario,
        password = senha,
        database = base_dados
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
            informacoes_banco_dados()

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
    print("1. Inserir usuário.\n2. Listar usuários cadastrados.\n3. Apresentar usuário específico.\n4. Alterar dados de um usuários.\n5. Deletar usuários.\n6. Voltar ao menu")
    opcao = input("Entre com o dígito da função desejada: ")
    return opcao

def menu_dispositivos():
    print("="*32 + " Menu de Dispositivos " + "="*32)
    print("1. Inserir dispositivo.\n2. Listar dispositivos cadastrados.\n3. Apresentar dispositivo específico.\n4. Alterar dados de um dispositivos.\n5. Deletar dispositivos.\n6. Voltar ao menu")
    opcao = input("Entre com o dígito da função desejada: ")
    return opcao

def menu_componentes():
    print("="*32 + " Menu de Componentes " + "="*32)
    print("")
    opcao = input("Entre com o dígito da função desejada: ")
    return opcao

def verificar_usuario(cursor, id):
    sql_busca_usu = f'SELECT codUsu FROM usuario WHERE codUsu = ("{id}");'
    cursor.execute(sql_busca_usu)
    resultado = cursor.fetchone()
    if resultado:
        return False
    else:
        return True

def inserir_usuario(conexao, cursor):
    print("="*32 + "Cadastro de usuários" + "="*32)
    try:
        x = True
        while x:
            try:
                id = int(input("Identificador do usuário: "))
                validador = verificar_usuario(cursor, id)
                if validador == False:
                    print("Esse Identificador já está associado a um usuário. Tente novamente.")
                else:
                    nome = input("Nome do usuário: ").lower().capitalize()
                    departamento = input("Nome do Departamento: ").lower().capitalize()
                    existe_status = False
                    while not existe_status:
                        status = input("Status do usuário (Ativo/Inativo): ").lower().capitalize()
                        if status in ["Ativo", "Inativo"]:
                            existe_status = True
                            estado = status
                        else:
                            print("Status inválido. Tente novamente.")
                    sql_dep = f'INSERT INTO usuario (codUsu, nome, estado, departamento) VALUES ("{id}","{nome}","{estado}","{departamento}");'
                    cursor.execute(sql_dep)
                    conexao.commit()
                    print("usuario cadastrado com sucesso!")
                    x = False
            except ValueError:
                print("O identificador do usuário deve ser um numero inteiro. Tente novamente")
    except mysql.connector.Error as error:
        print(f"Erro: {error}.")

def listar_usuarios(cursor):
    print("="*32 + "Listando usuarios cadastrados" + "="*32)
    sql_listagem_dep = f'SELECT * FROM usuario ORDER BY nome;'
    cursor.execute(sql_listagem_dep)
    busca = cursor.fetchall()
    if busca:
        print("ID | NOME | STATUS | DEPARTAMENTO")
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
        print(f"ID | NOME | STATUS | DEPARTAMENTO\n{busca}")
    else:
        print("O usuario indicado não pode ser encontrado. Verifique se o mesmo consta na base de dados atual.")

def alteracao_usuario(conexao,cursor):
    print("="*32 + "Alterando dados de usuário" + "="*32)
    id = int(input("Identificador do usuário: "))
    validador = verificar_usuario(cursor, id)
    if validador == False:
        opcao = input("1. Alterar nome.\n2. Alterar Status.\n3. Alterar Departamento")
        if opcao == "1":
            nome = input(f"{'='*32}\nNome de usuário: ")
            sql_alter_nome = f'UPDATE usuario SET nome = ("{nome}") WHERE codUsu = ("{id}");'
            cursor.execute(sql_alter_nome)
            conexao.commit()
            print(f"O nome do usuário {id} foi alterado com sucesso!")
        if opcao == "2":
            existe_status = False
            while not existe_status:
                status = input(f"{'='*32}\nStatus do usuário (Ativo/Inativo): ").lower().capitalize()
                if status in ["Ativo", "Inativo"]:
                    existe_status = True
                    estado = status
                else:
                    print("Status inválido. Tente novamente.")
                sql_alter_sta = f'UPDATE usuario SET estado = ("{estado}") WHERE codUsu = ("{id}");'
                cursor.execute(sql_alter_sta)
                conexao.commit()
                print(f"O status do usuário {id} foi alterado com sucesso!")
        elif opcao == "3":
            departamento = input(f"{'='*32}\nDepartamento: ")
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
    validador = verificar_usuario(cursor, id)
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

def verifica_dispositivo(cursor, id):
    sql_busca_disp = f'SELECT codDisp FROM dispositivo WHERE codDisp = ("{id}");'
    cursor.execute(sql_busca_disp)
    resultado = cursor.fetchone()
    if resultado:
        return False
    else:
        return True

def inserir_dispositivo(conexao, cursor):
    print("="*32 + "Cadastro de dispositivos" + "="*32)
    try:
        x = True
        while x:
            id = input("Identificador do dispositivo: ").upper()
            validador_disp = verifica_dispositivo(cursor, id)
            if validador_disp == False:
                print("Esse Identificador já está associado a um dispositivo. Tente novamente.")
            else:
                z = True
                while z:
                    codUsu = int(input("Identificador do usuário: "))
                    sql_verifica_usu = f'SELECT * FROM usuario WHERE codUsu = {codUsu};'
                    cursor.execute(sql_verifica_usu)
                    busca_usu = cursor.fetchone()
                    if not busca_usu:
                        print(f"Usuário {codUsu} não existe. Tente novamente.")
                    else:
                        sql_verifica_usu_associado = f'SELECT * FROM dispositivo WHERE codUsu = {codUsu} AND estado = "Ativo";'
                        cursor.execute(sql_verifica_usu_associado)
                        busca_usu_associado = cursor.fetchone()
                        if busca_usu_associado:
                            print(f"Usuário {codUsu} já possui um dispositivo associado. Escolha outro usuário.")
                        else:
                            z = False
                    existe_status = False
                    while not existe_status:
                        status = input("Status do dispositivo (Ativo/Inativo): ").lower().capitalize()
                        if status in ["Ativo", "Inativo"]:
                            existe_status = True
                            estado = status
                        else:
                            print("Status inválido. Tente novamente.")
                    existe_alocacao = False
                    while not existe_alocacao:
                        aloc = input("Alocação do dispositivo (Perm/Plan/Temp): ").lower().capitalize()
                        if aloc in ["Perm", "Plan", "Temp"]:
                            existe_alocacao = True
                            alocacao = aloc
                        else:
                            print("Estado de alocação inválido. Tente novamente.")
                montagem = input("Montagem: ").lower().capitalize()
                nota_fiscal = input("Nota fiscal: ").lower().capitalize()
                sistema_operacional = input("Sistema Operacional: ").lower().capitalize()
                y = True
                while y:
                    try:
                        chave = input("Chave de ativação : ").upper()
                        chave_formatada = f'{chave[0:5]}-{chave[5:10]}-{chave[10:15]}-{chave[15:20]}-{chave[20:26]}'
                        if len(chave_formatada) == 29:
                            sql_busca_chav = f'SELECT * FROM dispositivo WHERE chave_ativacao = ("{chave_formatada}");'
                            cursor.execute(sql_busca_chav)
                            busca = cursor.fetchone()
                            if busca:
                                print("A chave de ativação informada já está associada a um dispositivo. Tente novamente com outra chave.")
                            else:
                                y = False
                    except IndexError:
                        print("A Chave de ativação não cumpre os requisitos de 25 (Vinte e Cinco) caracteres. Tente novamente.")
                    except mysql.connector.IntegrityError as integrity_error:
                        print(f"Erro de integridade: {integrity_error}.")
                existe_rede = False
                while not existe_rede:
                    conexao_rede = input("Conexão de rede (Cabeada/Wirelles): ").lower().capitalize()
                    if conexao_rede in ["Cabeada","Wirelles"]:
                        existe_rede = True
                        rede = conexao_rede
                    else:
                        print("Tipo de conexão de rede inválida. Tente novamente.")
                data_atualizacao = dt.date.today()
                sql_inserir_disp = f'INSERT INTO dispositivo (codDisp, codUsu, estado, alocacao, montagem, nota_fiscal, sistema_operacional, chave_ativacao, conexao_rede, data_atualizacao) VALUES ("{id}", "{codUsu}", "{estado}", "{alocacao}", "{montagem}", "{nota_fiscal}", "{sistema_operacional}", "{chave_formatada}", "{rede}", "{data_atualizacao}");'
                cursor.execute(sql_inserir_disp)
                conexao.commit()
                print("Dispositivo cadastrado com sucesso!")
                x = False
    except mysql.connector.Error as Error:
        print(f"Erro: {Error}.")

def listar_dispositivos(cursor):
    print("="*32 + "Listando dispositivos cadastrados" + "="*32)
    sql_listagem_disp = f'SELECT d.codDisp, u.nome, d.estado, d.alocacao, d.montagem, d.nota_fiscal , d.sistema_operacional , d.chave_ativacao , d.conexao_rede , d.data_atualizacao FROM dispositivo d INNER JOIN usuario u ON d.codUsu = u.codUsu ORDER BY d.codDisp;'
    cursor.execute(sql_listagem_disp)
    busca = cursor.fetchall()
    if busca:
        print("ID | USUÁRIO | STATUS | MONTAGEM | NOTA FISCAL | SISTEMA OPERACIONAL | CHAVE DE ATIVAÇÃO | CONEXÃO DE REDE | DATA DE INSERÇÃO ")
        for dispositivos in busca:
            print(dispositivos)
    else:
        print("Não existem dispositivos cadastrados no sistema. Inclua dispositivos para poder visualiza-los")

def imprimir_dispositivo_especifico(cursor):
    print("="*32 + "Apresentando dispositivo específico" + "="*32)
    dispositivo = input("Identificador do dispositivo: ").upper()
    sql_dep_espec = f'SELECT d.codDisp, u.nome, d.estado, d.alocacao, d.montagem, d.nota_fiscal , d.sistema_operacional , d.chave_ativacao , d.conexao_rede , d.data_atualizacao FROM dispositivo d INNER JOIN usuario u ON d.codDisp = u.codUsu WHERE codDisp = ("{dispositivo}") ORDER BY codDisp;'
    cursor.execute(sql_dep_espec)
    busca = cursor.fetchone()
    if busca:
        print(f"ID | USUÁRIO | STATUS | MONTAGEM | NOTA FISCAL | SISTEMA OPERACIONAL | CHAVE DE ATIVAÇÃO | CONEXÃO DE REDE | DATA DE INSERÇÃO\n{busca}")
    else:
        print("O dispositivo indicado não pode ser encontrado. Verifique se o mesmo consta na base de dados atual.")

def main():
    banco = informacoes_banco_dados()
    cursor = banco.cursor()
    opcao = menu_principal()
    while opcao != "6":
        if opcao == "1":
            op_usu = menu_usuario()
            while op_usu != "6":
                if op_usu == "1":
                    inserir_usuario(banco,cursor)
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
            while op_disp != "6":
                if op_disp == "1":
                    inserir_dispositivo(banco, cursor)
                elif op_disp == "2":
                    listar_dispositivos(cursor)
                elif op_disp == "3":
                    imprimir_dispositivo_especifico(cursor)
                op_disp = menu_dispositivos()
        elif opcao == "3":
            print("Em construção")
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