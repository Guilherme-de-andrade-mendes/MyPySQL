
try:
    numero = int(input("igite um número: "))
    print(numero)
    print(x)
    10/0
except ZeroDivisionError:
    print("Divisão por zero não é possivel.")
except ValueError:
    print("Digite um valor valido.")
except:
    print("Erro inesperado.")
finally:
    print("Sempre executa.")