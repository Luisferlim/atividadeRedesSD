#!/usr/bin/env python3

import socket
import random
import json
import threading
from datetime import datetime


class CurrencyConverterServer:
    def __init__(self, host="localhost", port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False

        self.exchange_rates = {
            "USD": 5.20,
            "EUR": 5.60,
            "GBP": 6.50,
            "JPY": 0.035,
            "CAD": 3.80,
            "AUD": 3.40,
            "CHF": 5.80,
            "CNY": 0.72,
        }

    def generate_random_rate(self, base_rate):
        variation = random.uniform(-0.1, 0.1)
        return base_rate * (1 + variation)

    def convert_currency(self, amount_brl, target_currency):
        if target_currency.upper() not in self.exchange_rates:
            return None, f"Moeda '{target_currency}' não suportada"

        base_rate = self.exchange_rates[target_currency.upper()]
        current_rate = self.generate_random_rate(base_rate)

        converted_amount = amount_brl / current_rate

        return {
            "original_amount": amount_brl,
            "original_currency": "BRL",
            "target_currency": target_currency.upper(),
            "exchange_rate": round(current_rate, 4),
            "converted_amount": round(converted_amount, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }, None

    def handle_client_request(self, data, client_address):
        try:
            request = json.loads(data.decode("utf-8"))

            amount = request.get("amount")
            currency = request.get("currency")

            if not amount or not currency:
                error_response = {
                    "error": 'Parâmetros inválidos. Use: {"amount": valor, "currency": "moeda"}'
                }
                self.socket.sendto(
                    json.dumps(error_response).encode("utf-8"), client_address
                )
                return

            result, error = self.convert_currency(amount, currency)

            if error:
                error_response = {"error": error}
                self.socket.sendto(
                    json.dumps(error_response).encode("utf-8"), client_address
                )
            else:
                self.socket.sendto(json.dumps(result).encode("utf-8"), client_address)

        except json.JSONDecodeError:
            error_response = {
                "error": 'Formato JSON inválido. Use: {"amount": valor, "currency": "moeda"}'
            }
            self.socket.sendto(
                json.dumps(error_response).encode("utf-8"), client_address
            )
        except Exception as e:
            error_response = {"error": f"Erro interno: {str(e)}"}
            self.socket.sendto(
                json.dumps(error_response).encode("utf-8"), client_address
            )

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.running = True

            print(
                f"Servidor UDP de Conversão de Moedas iniciado em {self.host}:{self.port}"
            )
            print("Moedas suportadas:", ", ".join(self.exchange_rates.keys()))
            print("Pressione Ctrl+C para parar o servidor\n")

            while self.running:
                try:
                    data, client_address = self.socket.recvfrom(1024)

                    print(f"Requisição recebida de {client_address}")

                    thread = threading.Thread(
                        target=self.handle_client_request, args=(data, client_address)
                    )
                    thread.daemon = True
                    thread.start()

                except socket.error as e:
                    if self.running:
                        print(f"Erro no socket: {e}")

        except KeyboardInterrupt:
            print("\nServidor interrompido pelo usuário")
        except Exception as e:
            print(f"Erro ao iniciar servidor: {e}")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()
        print("Servidor finalizado")


if __name__ == "__main__":
    server = CurrencyConverterServer()
    server.start()
