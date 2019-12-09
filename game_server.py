import socket
import json
import threading
import copy


def login():
    aux = 1
    name, address = server_socket.recvfrom(1024)
    name = name.decode()

    # Verificando se o nickname ja existe
    with open("users.json", "r") as f:
        users = json.load(f)
        f.close()
    if not users:
        pass
    else:
        for user in users:
            if user["name"] == name:
                server_socket.sendto(str(1).encode(), address)
                aux = 0
                break

    # Verificando se é necessário cadastrar o user
    if aux == 1:
        # Criando novo user
        new_user = {}
        new_user["name"] = name
        new_user["wins"] = 0

        # Adicionando ao arquivo
        users.append(new_user)
        with open("users.json", "w") as f:
            json.dump(users, f)
            f.close()
            server_socket.sendto(str(1).encode(), address)


def match_request(endereco, name):
    if user1["address"] == "":
        user1["address"] = endereco
        user1["name"] = name
    else:
        user2["address"] = endereco
        user2["name"] = name

        player1 = copy.deepcopy(user1)
        player2 = copy.deepcopy(user2)
        new_playroom = threading.Thread(target=playroom, args=(player1, player2))
        new_playroom.start()
        # Resetando users
        user1["address"] = ""
        user1["name"] = ""
        user2["address"] = ""
        user2["name"] = ""


def playroom(player1, player2):
    playroom_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = ""
    port = 8001
    playroom_socket.bind((host, port))

    # Tabuleiro Inicial
    tabuleiro = board()
    # Enviando dados do Player 1
    playroom_socket.sendto(player2["name"], player1["address"])
    playroom_socket.sendto("X".encode(), player1["address"])
    playroom_socket.sendto(str(1).encode(), player1["address"])
    playroom_socket.sendto(tabuleiro, player1["address"])

    # Enviando dados do Player 2
    playroom_socket.sendto(player1["name"], player2["address"])
    playroom_socket.sendto("O".encode(), player2["address"])
    playroom_socket.sendto(str(0).encode(), player2["address"])
    playroom_socket.sendto(tabuleiro, player2["address"])

    winner = False
    while not winner:
        # Verificando tabuleiro
        # Resultados:
        # X -> Player1 Win
        # O -> Player2 Win
        # - -> Empate
        # N -> O jogo continua
        tabuleiro = json.loads(tabuleiro.decode())
        resul = verification(tabuleiro)
        print(resul)
        tabuleiro = json.dumps(tabuleiro).encode()
        if resul == "N":
            # Esperando Jogada do Player1
            tabuleiro, address = playroom_socket.recvfrom(1024)
            if verification(json.loads(tabuleiro.decode())) == "N":
                playroom_socket.sendto(str(1).encode(), player2["address"])
                playroom_socket.sendto(tabuleiro, player2["address"])
        elif resul == "X":
            playroom_socket.sendto(str(7).encode(), player1["address"])
            playroom_socket.sendto(str(7).encode(), player2["address"])
            playroom_socket.sendto(tabuleiro, player1["address"])
            playroom_socket.sendto(tabuleiro, player2["address"])
            msg = "O vencedor é " + player1["name"].decode() + "(" + resul + ")"
            playroom_socket.sendto(msg.encode(), player1["address"])
            playroom_socket.sendto(msg.encode(), player2["address"])
            add_win(player1["name"].decode())
            break
        elif resul == "O":
            playroom_socket.sendto(str(7).encode(), player1["address"])
            playroom_socket.sendto(str(7).encode(), player2["address"])
            playroom_socket.sendto(tabuleiro, player1["address"])
            playroom_socket.sendto(tabuleiro, player2["address"])
            msg = "O vencedor é " + player2["name"].decode() + "(" + resul + ")"
            playroom_socket.sendto(msg.encode(), player1["address"])
            playroom_socket.sendto(msg.encode(), player2["address"])
            add_win(player2["name"].decode())
            break
        elif resul == "-":
            playroom_socket.sendto(str(7).encode(), player1["address"])
            playroom_socket.sendto(str(7).encode(), player2["address"])
            playroom_socket.sendto(tabuleiro, player1["address"])
            playroom_socket.sendto(tabuleiro, player2["address"])
            msg = "Ótima partida " + player1["name"].decode() + " e " + player2["name"].decode() + ". Vocês empataram!"

            playroom_socket.sendto(msg.encode(), player1["address"])
            playroom_socket.sendto(msg.encode(), player2["address"])
            break

        # Verificando tabuleiro
        # Resultados:
        # X -> Player1 Win
        # O -> Player2 Win
        # - -> Empate
        # N -> O jogo continua
        tabuleiro = json.loads(tabuleiro.decode())
        resul = verification(tabuleiro)
        print(resul)
        tabuleiro = json.dumps(tabuleiro).encode()
        if resul == "N":
            # Esperando Jogada do Player2
            tabuleiro, address = playroom_socket.recvfrom(1024)
            if verification(json.loads(tabuleiro.decode())) == "N":
                playroom_socket.sendto(str(1).encode(), player1["address"])
                playroom_socket.sendto(tabuleiro, player1["address"])
        elif resul == "X":
            playroom_socket.sendto(str(7).encode(), player1["address"])
            playroom_socket.sendto(str(7).encode(), player2["address"])
            playroom_socket.sendto(tabuleiro, player1["address"])
            playroom_socket.sendto(tabuleiro, player2["address"])
            msg = "O vencedor é "+player1["name"].decode()+"("+resul+")"
            playroom_socket.sendto(msg.encode(), player1["address"])
            playroom_socket.sendto(msg.encode(), player2["address"])
            add_win(player1["name"].decode())
            break
        elif resul == "O":
            playroom_socket.sendto(str(7).encode(), player1["address"])
            playroom_socket.sendto(str(7).encode(), player2["address"])
            playroom_socket.sendto(tabuleiro, player1["address"])
            playroom_socket.sendto(tabuleiro, player2["address"])
            msg = "O vencedor é "+player2["name"].decode()+"("+resul+")"
            playroom_socket.sendto(msg.encode(), player1["address"])
            playroom_socket.sendto(msg.encode(), player2["address"])
            add_win(player2["name"].decode())
            break
        elif resul == "-":
            playroom_socket.sendto(str(7).encode(), player1["address"])
            playroom_socket.sendto(str(7).encode(), player2["address"])
            playroom_socket.sendto(tabuleiro, player1["address"])
            playroom_socket.sendto(tabuleiro, player2["address"])
            msg = "Ótima partida "+player1["name"].decode()+" e "+player2["name"].decode()+". Vocês empataram!"
            playroom_socket.sendto(msg.encode(), player1["address"])
            playroom_socket.sendto(msg.encode(), player2["address"])
            break
    playroom_socket.close()


def board():
    tabuleiro = [["", "", ""], ["", "", ""], ["", "", ""]]
    return json.dumps(tabuleiro).encode()


def verification(tabuleiro):
    # Verificando Linhas
    i = ""
    for linha in tabuleiro:
        if all(i == "X" for i in linha):
            return "X"
        elif all(i == "O" for i in linha):
            return "O"

    # Verificando Colunas
    for c in range(0,3):
        if tabuleiro[0][c] == "X" and tabuleiro[1][c] == "X" and tabuleiro[2][c] == "X":
            return "X"
        elif tabuleiro[0][c] == "O" and tabuleiro[1][c] == "O" and tabuleiro[2][c] == "O":
            return "O"

    # Verificando empate
    for linha in tabuleiro:
        if any(i == "" for i in linha):
            return "N"

    # Ao fim de todos os teste é declarado o empate
    return "-"


def add_win(name):
    with open("users.json", "r") as f:
        users = json.load(f)
        f.close()
    for user in users:
        if user["name"] == name:
            user["wins"] += 1
    with open("users.json", "w") as f:
        json.dump(users, f)
        f.close()


def ranking(address):
    with open("users.json", "r") as f:
        users = json.load(f)
        f.close()
    users = sorted(users, key=lambda user: user["wins"], reverse=True)
    server_socket.sendto(json.dumps(users).encode(), address)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "127.0.0.1"
port = 8000

user1 = {"name": "", "address": ""}

user2 = {"name": "", "address": ""}

server_socket.bind(('127.0.0.1', port))
print("Server Status: Running...")

while True:
    op, address = server_socket.recvfrom(1024)
    print("Server connected by {}".format(address))
    op = int(op.decode())
    # Funções
    # 0 -> Login
    # 1 -> Requisição de Jogar
    # 2-> Requisição de instruções
    # 3 -> Requisição de Placares
    print(op)
    if op == 0:
        login()

    elif op == 1:
        name, address = server_socket.recvfrom(1024)
        match_request(address, name)

    elif op == 3:
        ranking(address)