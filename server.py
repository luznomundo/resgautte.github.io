#!/usr/bin/env python3
"""
Servidor Local de Doações - Resgautte
Gateway: MisticPay (PIX Dinâmico)
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os
import sys

PORT = 3000

# Credenciais MisticPay
CLIENT_ID = "pk_fd2d53baae9d0ac0b6600a0b4271b14b"
CLIENT_SECRET = "sk_7ac314f61204cebbe642f9c8f2025777e897611cf2f2367b2130ed799f7d6fb8"
AUTH_HEADER = "Basic cGtfZmQyZDUzYmFhZTlkMGFjMGI2NjAwYTBiNDI3MWIxNGI6c2tfN2FjMzE0ZjYxMjA0Y2ViYmU2NDJmOWM4ZjIwMjU3NzllODk3NjExY2YyZjIzNjdiMjEzMGVkNzk5ZjdkNmZiOA=="

MISTICPAY_CREATE_URL = "https://api.misticpay.com/api/transactions/create"
MISTICPAY_CHECK_URL = "https://api.misticpay.com/api/transactions/check"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Habilitar CORS e headers de segurança
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/create-pix':
            self.handle_create_pix()
        elif self.path == '/api/check-pix':
            self.handle_check_pix()
        else:
            self.send_error(404, "Endpoint não encontrado")

    def handle_create_pix(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            amount = float(data.get('amount', 5.0))
            payer_name = str(data.get('payerName', 'Doador Anonimo')).strip()
            payer_doc = str(data.get('payerDocument', '')).strip().replace('.', '').replace('-', '').replace('/', '')
            description = str(data.get('description', 'Doacao Canil Resgautte')).strip()

            payload = {
                "amount": amount,
                "payerName": payer_name,
                "payerDocument": payer_doc,
                "description": description
            }

            req = urllib.request.Request(
                MISTICPAY_CREATE_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Authorization': AUTH_HEADER,
                    'Content-Type': 'application/json',
                    'User-Agent': 'ResgautteApp/1.0'
                },
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=15) as response:
                res_body = response.read().decode('utf-8')
                self.send_response(response.status)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(res_body.encode('utf-8'))

        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(err_body.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            err_res = json.dumps({"error": str(e), "message": "Falha interna ao criar PIX"})
            self.wfile.write(err_res.encode('utf-8'))

    def handle_check_pix(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            transaction_id = str(data.get('transactionId', '')).strip()

            if not transaction_id:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "transactionId obrigatorio"}).encode('utf-8'))
                return

            payload = {
                "transactionId": transaction_id
            }

            req = urllib.request.Request(
                MISTICPAY_CHECK_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Authorization': AUTH_HEADER,
                    'Content-Type': 'application/json',
                    'User-Agent': 'ResgautteApp/1.0'
                },
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=15) as response:
                res_body = response.read().decode('utf-8')
                self.send_response(response.status)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(res_body.encode('utf-8'))

        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(err_body.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            err_res = json.dumps({"error": str(e), "message": "Falha interna ao consultar PIX"})
            self.wfile.write(err_res.encode('utf-8'))

if __name__ == '__main__':
    # Define diretório raiz como o diretório do script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    server_address = ('', PORT)
    httpd = socketserver.TCPServer(server_address, CustomHandler)
    httpd.allow_reuse_address = True
    print("=" * 60)
    print(f" Servidor Resgautte iniciado com sucesso!")
    print(f" Gateway MisticPay conectada (Client ID: {CLIENT_ID})")
    print(f" Acesse seu site em: http://localhost:{PORT}")
    print(" Pressione Ctrl+C para encerrar.")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        sys.exit(0)
