from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.form.get("Body").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg.lower() in ['hi', 'hello', 'oi']:
        msg.body(
            "Olá! Bem-vindo ao Rafael Chat! 👋\n\n"
            "Escolha uma opção:\n"
            "1️⃣ - Ver preço do cuscuz\n"
            "2️⃣ - Ver preço do macarrão\n"
            "3️⃣ - Saber horário de funcionamento\n"
            "4️⃣ - Falar com um atendente"
        )
    elif incoming_msg == '1':
        msg.body("O cuscuz custa R$ 10,00.")
    elif incoming_msg == '2':
        msg.body("O macarrão custa R$ 20,00.")
    elif incoming_msg == '3':
        msg.body("Nosso horário de funcionamento é das 08h às 18h, de segunda a sexta.")
    elif incoming_msg == '4':
        msg.body("Um atendente falará com você em breve. Aguarde! 🙋‍♂️")
    else:
        msg.body("Desculpe, não entendi. Envie 'Oi' ou 'Hello' para começar.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
