#!/usr/bin/env python3

import socket
import json
import sys


class CurrencyConverterTCPClient:
    def __init__(self, host="localhost", port=9999):
        self.host = host
        self.port = port
        self.socket = None

        self.supported_currencies = [
            "USD",
            "EUR",
            "GBP",
            "JPY",
            "CAD",
            "AUD",
            "CHF",
            "CNY",
        ]

    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.host, self.port))
            return True
        except socket.timeout:
            print("Timeout: Não foi possível conectar ao servidor")
            return False
        except ConnectionRefusedError:
            print("Conexão recusada: Servidor não está rodando")
            return False
        except Exception as e:
            print(f"Erro de conexão: {e}")
            return False

    def send_conversion_request(self, amount, currency):
        try:
            request = {"amount": amount, "currency": currency.upper()}

            message = json.dumps(request).encode("utf-8")
            self.socket.send(message)

            response_data = self.socket.recv(1024).decode("utf-8")
            response = json.loads(response_data)

            return response

        except socket.timeout:
            return {"error": "Timeout: Servidor não respondeu"}
        except json.JSONDecodeError:
            return {"error": "Resposta inválida do servidor"}
        except Exception as e:
            return {"error": f"Erro de comunicação: {str(e)}"}

    def display_result(self, result):
        if "error" in result:
            print(f"Erro: {result['error']}")
            return

        print("\n" + "=" * 50)
        print("RESULTADO DA CONVERSÃO")
        print("=" * 50)
        print(f"Valor original: R$ {result['original_amount']:.2f}")
        print(f"Moeda de destino: {result['target_currency']}")
        print(f"Cotação atual: {result['exchange_rate']}")
        print(
            f"Valor convertido: {result['target_currency']} {result['converted_amount']:.2f}"
        )
        print(f"Timestamp: {result['timestamp']}")
        print("=" * 50 + "\n")

    def get_user_input(self):
        print("\nCONVERSOR DE MOEDAS TCP")
        print("=" * 30)
        print("Moedas suportadas:", ", ".join(self.supported_currencies))
        print("=" * 30)

        try:
            amount_str = input("Digite o valor em reais (R$): ").strip()

            amount_str = (
                amount_str.replace("R$", "").replace("$", "").replace(",", ".").strip()
            )
            amount = float(amount_str)

            if amount <= 0:
                print("Valor deve ser maior que zero")
                return None, None

            currency = (
                input("Digite a moeda de destino (ex: USD, EUR): ").strip().upper()
            )

            if currency not in self.supported_currencies:
                print(f"Moeda '{currency}' não suportada")
                print(f"Moedas disponíveis: {', '.join(self.supported_currencies)}")
                return None, None

            return amount, currency

        except ValueError:
            print("Valor inválido. Digite um número válido.")
            return None, None
        except KeyboardInterrupt:
            print("\nSaindo...")
            return None, None

    def run(self):
        print("Cliente TCP de Conversão de Moedas")
        print("Conectando ao servidor...")

        if not self.connect_to_server():
            return

        print("Conectado ao servidor!")

        try:
            while True:
                amount, currency = self.get_user_input()

                if amount is None or currency is None:
                    continue

                print(f"\nConvertendo R$ {amount:.2f} para {currency}...")

                result = self.send_conversion_request(amount, currency)

                self.display_result(result)

                try:
                    continue_choice = (
                        input("Deseja fazer outra conversão? (s/n): ").strip().lower()
                    )
                    if continue_choice not in ["s", "sim", "y", "yes"]:
                        break
                except KeyboardInterrupt:
                    break

        except KeyboardInterrupt:
            print("\nCliente finalizado pelo usuário")
        except Exception as e:
            print(f"Erro no cliente: {e}")
        finally:
            if self.socket:
                self.socket.close()
            print("Conexão fechada")


if __name__ == "__main__":
    host = "localhost"
    port = 9999

    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    client = CurrencyConverterTCPClient(host, port)
    client.run()
