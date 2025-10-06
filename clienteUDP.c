#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

#define PORTA 8080
#define TAMANHO_BUFFER 1024

int main() {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2,2), &wsa);

    SOCKET socket_cliente;
    struct sockaddr_in endereco_servidor;
    char buffer[TAMANHO_BUFFER];

    socket_cliente = socket(AF_INET, SOCK_DGRAM, 0);

    endereco_servidor.sin_family = AF_INET;
    endereco_servidor.sin_port = htons(PORTA);
    endereco_servidor.sin_addr.s_addr = inet_addr("127.0.0.1");

    while(1) {
        double valor;
        char moeda[20];

        printf("Digite o valor em R$: ");
        scanf("%lf", &valor);
        printf("Digite a moeda: ");
        scanf("%s", moeda);

        snprintf(buffer, TAMANHO_BUFFER, "%lf %s", valor, moeda);
        sendto(socket_cliente, buffer, strlen(buffer), 0, (struct sockaddr*)&endereco_servidor, sizeof(endereco_servidor));

        int bytes_recebidos = recvfrom(socket_cliente, buffer, TAMANHO_BUFFER, 0, NULL, NULL);
        buffer[bytes_recebidos] = '\0';
        printf("Resultado: %s\n\n", buffer);
    }

    closesocket(socket_cliente);
    WSACleanup();
    return 0;
}
