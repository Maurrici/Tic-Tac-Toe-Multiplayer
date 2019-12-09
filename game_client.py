import socket
import json


def game_request():
    client_socket.sendto(str(1).encode(), (host, port))
    client_socket.sendto(name.encode(), (host, port))
    print("Aguardando um adversário a sua altura...")
    opponent, address = client_socket.recvfrom(1024)
    opponent = opponent.decode()
    player, address = client_socket.recvfrom(1024)
    player = player.decode()

    while True:
        vez, address = client_socket.recvfrom(1024)
        vez = int(vez.decode())
        tabuleiro, address = client_socket.recvfrom(1024)
        tabuleiro = json.loads(tabuleiro.decode())

        show_board(tabuleiro, opponent, player)

        if (vez != 7) and (vez == 1):
            jogada = False
            while not jogada:
                print("Digite a linha em que deseja jogar:")
                playL = int(input())
                print("Digite a coluna em que deseja jogar:")
                playC = int(input())
                if tabuleiro[playL][playC] == "":
                    tabuleiro[playL][playC] = player
                    show_board(tabuleiro)
                    jogada = True
                    client_socket.sendto(json.dumps(tabuleiro).encode(), (host, 8001))
                else:
                    print("O local escolhido é inválido!!")
                    print("Tente Novamente\n")
                    show_board(tabuleiro)
        elif vez == 7:
            msg, address = client_socket.recvfrom(1024)
            print(msg.decode())
            break


def show_board(tabuleiro, opponent, player):
    if player == "X":
        player_opponent = "O"
    else:
        player_opponent = "X"
    print(name+"("+player+")\t\t\t\t\t\t\t\t\t\t"+opponent+"("+player_opponent+")\n\t\t\t\t\t", end="")
    for c in range(0, 3):
        print("  " + str(c) + " ", end="")
    print("\n\t\t\t\t\t ", end="")
    print(" ___" * 3)
    l = 0
    for linha in tabuleiro:
        print("\t\t\t\t\t"+str(l), end="")
        for coluna in linha:
            if coluna == "":
                print("|___", end="")
            else:
                print("|_" + coluna + "_", end="")
        print("|")
        l += 1


def instructions():
    print("----------------------------------------------------")
    print("|           The Epic Battle: X VS O                |")
    print("----------------------------------------------------")
    print("1- Neste jogo serão escolhidos dois jogadores aleátorios\n"
          "   Aquele que estiver esperando mais tempo na fila\n"
          "   será o Player 1(X) e o outro o Player 2(O).")
    print("2- As jogadas ocorrem de forma alternada, e em cada\n"
          "jogada deverá ser informado a linha e a coluna desejada.")
    print("3- Aquele que vencer ganhará pontos no ranking.")
    print("4- Caso empate nenhum jogador ganhará o ponto.")
    input()


def ranking():
    client_socket.sendto(str(3).encode(), (host, port))
    rank, address = client_socket.recvfrom(1024)
    rank = json.loads(rank.decode())
    rank_number = 1
    print("------------------------------------------------------")
    print("|  RANK  |             USER                 |  WINS  |")
    print("------------------------------------------------------")
    for user in rank:
        print("\t["+str(rank_number)+"] \t\t\t"+user["name"]+"                     "+str(user["wins"]))
        rank_number += 1
    input()


# Socket de Comunicação
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 8000
host = "127.0.0.1"
op = 0
while op != 1:
    print("-------------------------------")
    print("|   The Epic Battle: X VS O   |")
    print("-------------------------------")
    print("| Digite um nome de Usuário:  |")
    print("-------------------------------")
    name = input()
    client_socket.sendto(str(0).encode(), ('127.0.0.1', port))
    client_socket.sendto(name.encode(), (host, port))
    op, address = client_socket.recvfrom(1024)
    op = int(op.decode())


while True:
    print("\n\n\n\n")
    print("-------------------------------")
    print("|   The Epic Battle: X VS O   |")
    print("-------------------------------")
    print("| (1) - JOGAR                 |")
    print("| (2) - INSTRUÇÕES            |")
    print("| (3) - PLACARES              |")
    print("| (4) - SAIR                  |")
    print("-------------------------------")
    op = int(input())

    if op == 1:
        game_request()
    elif op == 2:
        instructions()
    elif op == 3:
        ranking()