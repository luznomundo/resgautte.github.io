# Guia de Integração - MisticPay Gateway

A sua gateway de pagamentos **MisticPay** foi integrada com sucesso ao site de doações **Resgautte**!

---

## 🚀 Como testar no seu computador (Local)

1. Vá até a pasta do projeto:
   `c:\Users\Pichau\Downloads\saveweb2zip-com-resgaute-github-io`
2. Dê **dois cliques** no arquivo:
   👉 **`iniciar_servidor.bat`**
3. O servidor web local será iniciado na porta **3000** e abrirá automaticamente o navegador no endereço:
   👉 **`http://localhost:3000`**

*(Alternativamente, você pode abrir o terminal na pasta e executar: `python server.py`)*

---

## ✨ O que foi implementado

1. **Checkout Dinâmico com PIX Oficial**:
   - Seleção de valores pré-definidos (R$ 5, R$ 10, R$ 25, R$ 50) ou campo para digitação de qualquer valor customizado.
   - Campos com validação para **Nome Completo** e **CPF** (com formatação e máscara automática `000.000.000-00`), exigidos pela rede Pix e pela MisticPay.
   - Emissão dinâmica da cobrança em tempo real via endpoint oficial `POST /api/transactions/create`.

2. **Exibição do QR Code e Pix Copia e Cola**:
   - Geração automática da imagem do QR Code retornada pela MisticPay.
   - Botão interativo **"Copiar Código PIX"** com feedback visual imediato.

3. **Confirmação Automática de Pagamento (Tempo Real)**:
   - O site consulta automaticamente o status da transação na MisticPay a cada 3,5 segundos (`/api/transactions/check`).
   - Quando o doador paga no aplicativo do banco, o site detecta o status `COMPLETO` e exibe instantaneamente a tela de confirmação e agradecimento 🎉!

4. **Arquitetura Segura & Flexível**:
   - **`server.py`**: Servidor em Python (sem precisar instalar nenhuma biblioteca externa) que protege seu `Client Secret` e evita problemas de CORS no navegador.
   - **`api/create-pix.js` e `api/check-pix.js`**: Funções serverless prontas caso você queira publicar o site na **Vercel** ou **Netlify**.
   - **Modo Direto (Fallback)**: Caso o site seja executado sem servidor (por exemplo, diretamente como arquivo ou em hospedagem puramente estática), ele tenta a conexão direta via cabeçalho HTTP Basic.

---

## 🔒 Suas Credenciais Configuradas

- **Client ID**: `pk_2d2d53baae9d0ac0b6600a0b4271b14b`
- **Client Secret**: `sk_7ac314f61204cebbe642f9c8f2025777e897611cf2f2367b2130ed799f7d6fb8`
- **Header Basic Auth**: `Basic cGtfMm...`

*(As credenciais já estão configuradas no `server.py`, nas funções da pasta `api/` e no `index.html`)*.

---

## 🌐 Publicação na Internet (Produção)

- **Opção 1: Vercel (Recomendado)**
  Basta subir os arquivos para um repositório no GitHub e importar na [Vercel](https://vercel.com). As funções na pasta `api/` e o arquivo `vercel.json` já estão 100% configurados para funcionar lá gratuitamente.

- **Opção 2: Servidor VPS / Hospedagem com Python**
  Basta rodar `python server.py` no servidor para manter a aplicação online.
