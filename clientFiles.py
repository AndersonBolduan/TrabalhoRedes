import socket
import json

HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 50000        # Porta que o servidor está escutando

# Mensagem JSON de exemplo que o cliente vai enviar
# Comandos aceitos pelo servidor: 
# 'ADICIONAR_INFO' add um arquivo a lista. 
# 'LISTAR_INFO' lista os arquivos. 
# 'ALTERAR_ARQUIVO' altera um dado dentro do arquivo
""""ensagem = {
    "comando": "LISTAR_ARQUIVOS",
    "diretorio": "trabalho_redes-main",
    "arquivo": "dados.json",
    "chave": "arquivos",
    "dados": {"nome": "foto.jpg", "tamanho": 12}
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(json.dumps(mensagem).encode('utf-8'))  # Envia a mensagem para o servidor
    resposta = s.recv(1024)                          # Recebe a resposta do servidor
    print('Resposta do servidor:', resposta.decode('utf-8'))"""

def solicitar_lista_arquivos(s):
    mensagem = {
        "comando": "LISTAR_ARQUIVOS",
        "diretorio": "trabalho_redes-main",
        "arquivo": "dados.json",
        "chave": "arquivos"
        }
    s.sendall(json.dumps(mensagem).encode('utf-8'))
    resposta = s.recv(4096)
    resposta_json = json.loads(resposta.decode('utf-8'))
    return resposta_json

def solicitar_alteracao_arquivo(s, arquivo):
    mensagem = {
        "comando": "BAIXAR_ARQUIVO",
        "diretorio": "trabalho_redes-main",
        "arquivo": "dados.json",
        "chave": arquivo
    }
    s.sendall(json.dumps(mensagem).encode('utf-8'))
    resposta = s.recv(4096)
    resposta_json = json.loads(resposta.decode('utf-8'))
    return resposta_json

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Solicita a lista de arquivos
    resposta = solicitar_lista_arquivos(s)
    if resposta["status"] == "sucesso":
        print("Arquivos disponíveis:", resposta["arquivos"])
        
        # O cliente escolhe um arquivo (exemplo: "arquivo1")
        arquivo_escolhido = input("Digite o nome do arquivo que deseja baixar: ")
        if arquivo_escolhido in resposta["arquivos"]:
            resposta_alteracao = solicitar_alteracao_arquivo(s, arquivo_escolhido)
            print(resposta_alteracao["mensagem"])
        else:
            print("Arquivo não encontrado na lista.")
    else:
        print("Erro ao listar arquivos:", resposta["mensagem"])
