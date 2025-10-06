#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <time.h>

#pragma comment(lib, "ws2_32.lib")

#define PORTA 8080
#define TAMANHO_BUFFER 1024

int main() {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2,2), &wsa); // Inicializa Winsock

    SOCKET socket_servidor;
    char buffer[TAMANHO_BUFFER];
    struct sockaddr_in endereco_servidor, endereco_cliente;
    int tamanho_cliente = sizeof(endereco_cliente);

    // Cria socket UDP
    socket_servidor = socket(AF_INET, SOCK_DGRAM, 0);

    // Configura endereço do servidor
    endereco_servidor.sin_family = AF_INET;
    endereco_servidor.sin_addr.s_addr = INADDR_ANY;
    endereco_servidor.sin_port = htons(PORTA);

    bind(socket_servidor, (struct sockaddr*)&endereco_servidor, sizeof(endereco_servidor));

    printf("Servidor UDP rodando na porta %d...\n", PORTA);

    while(1) {
        int bytes_recebidos = recvfrom(socket_servidor, buffer, TAMANHO_BUFFER, 0,
                                       (struct sockaddr*)&endereco_cliente, &tamanho_cliente);
        buffer[bytes_recebidos] = '\0';

        double valor;
        char moeda[20];
        sscanf(buffer, "%lf %s", &valor, moeda);

        // Gera cotação aleatória
        srand((unsigned int)time(NULL));
        double cotacao = 4.5 + ((double)rand() / RAND_MAX);

        double resultado = valor / cotacao;

        snprintf(buffer, TAMANHO_BUFFER, "%.2lf R$ = %.2lf %s (cotação %.2lf)", valor, resultado, moeda, cotacao);
        sendto(socket_servidor, buffer, strlen(buffer), 0, (struct sockaddr*)&endereco_cliente, tamanho_cliente);
    }

    closesocket(socket_servidor);
    WSACleanup();
    return 0;
}
