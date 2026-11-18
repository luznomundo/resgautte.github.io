// Vercel Serverless Function: /api/create-pix
export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const AUTH_HEADER = "Basic cGtfZmQyZDUzYmFhZTlkMGFjMGI2NjAwYTBiNDI3MWIxNGI6c2tfN2FjMzE0ZjYxMjA0Y2ViYmU2NDJmOWM4ZjIwMjU3NzllODk3NjExY2YyZjIzNjdiMjEzMGVkNzk5ZjdkNmZiOA==";

  try {
    const { amount, payerName, payerDocument, description } = req.body || {};
    const docClean = String(payerDocument || '').replace(/\D/g, '');

    const response = await fetch('https://api.misticpay.com/api/transactions/create', {
      method: 'POST',
      headers: {
        'Authorization': AUTH_HEADER,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amount: Number(amount) || 5,
        payerName: String(payerName || 'Doador').trim(),
        payerDocument: docClean,
        description: String(description || 'Doacao Canil Resgautte').trim()
      })
    });

    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (error) {
    return res.status(500).json({ error: error.message, message: 'Falha ao conectar com MisticPay' });
  }
}
