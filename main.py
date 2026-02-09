from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
import pytz  
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_ID = 'rafael.cavalcanti69@gmail.com'  

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=creds)


BR_TZ = pytz.timezone('America/Sao_Paulo')

user_data = {}

@app.route('/')
def index():
    return 'Assistente Virtual'

@app.route("/bot", methods=["POST"])
def bot():
    from_number = request.form.get("From")
    incoming_msg = request.form.get("Body").strip().lower()
    resp = MessagingResponse()


    if from_number not in user_data:
        user_data[from_number] = {"state": None, "choices": []}


    state = user_data[from_number]["state"]
    choices = user_data[from_number]["choices"]

    if state is None:
        # resp.message("Seja muito bem vindo(a) ☺️ Como eu posso te ajudar?\n"
        #              )
        resp.message("Seja muito bem vindo(a) ☺️ Como eu posso te ajudar?\n"
                        "1️⃣ - Agendar uma Consulta \n"
                        "2️⃣ - Tirar Dúvida \n"
                        "3️⃣ - Débitos \n \n"
                         
                        'É só responder com o número da opção que eu já te ajudo!'
                    )

        choices.append({ "choice": "Entrou em contato", "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                      })
        user_data[from_number]["state"] = "escolha_1"

    elif state == 'escolha_1':
        if incoming_msg == '1':
            resp.message("Em qual dos casos abaixo voce se encaixa?\n\n"

                         "1️⃣ - Primeira Consulta \n"
                         "2️⃣ - Agendar Retorno \n \n"
                        )
            # resp.message("🍃 A consulta com o *_Plano_* *_Básico_* inclui:\n\n"
            #              "📸 Fotografias intra e extrabucais\n"
            #              "🦷 Exame clínico bucal e extrabucal\n"
            #              "🩺 Avaliação da saúde geral\n"
            #              "📋 Elaboração de plano de tratamento personalizado clínico e estético\n"
            #              "\n O investimento é de R$ 250,00.")
            # resp.message("🍃 A consulta com o *_Plano_* *_Essencial_* inclui o plano básico +\n\n "
            #              "✨ Limpeza dental completa com:\n"
            #              "🔹 Raspagem profissional\n"
            #              "🔹 Polimento de restaurações\n"
            #              "🔹 Aplicação de flúor protetor\n\n"
            #              "O investimento é de R$ 400,00.")
            choices.append({ "choice": "Quer agendar consulta", "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                      })
            user_data[from_number]["state"] = "escolha_2"


        elif incoming_msg == '2':
            resp.message("Oi, estou aqui pra te ajudar! Entao caso voce queria, posso te responder sobre os itens abaixo:\n \n"
                            "1️⃣ 👉🏻 itam A \n"
                            "2️⃣ 👉🏻 Item B \n"
                            "3️⃣ 👉🏻 Item C \n"
                            "4️⃣ 👉🏻 Item D \n"
                            "5️⃣ 👉🏻 Item E \n"
                        )
            resp.message("Ou se voce quiser me dispensar e falar com um humano é só digitar 0 😔")
            choices.append({ "choice": "Quer tirar dúvidas", "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                      })
            user_data[from_number]["state"] = "escolha_3"

        elif incoming_msg == '3':
            resp.message("No link abaixo voce encontra os horários disponiveis:")
            resp.message("👉🏻 https://algumlinkaqui \n \n")
            resp.message("Se nao tiver horário imediato para te atender, clica no link abaixo que falaremos diretamente com voce pra te ajudar.")
            resp.message("https://wa.me/5511986000611?text=Eu%20tenho%20uma%20urgencia! \n \n")
            choices.append({ "choice": "Urgencia", "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                      })
            user_data[from_number]["state"] = None

        else:
            resp.message("Desculpa, nao te entendi 🥲\n\n"
                        "Digita um dos itens acima que eu te ajudo!")

    elif state == 'escolha_2':
        if incoming_msg == '1':
            resp.message(
                "Eu mesmo posso agendar sua consulta rapidinho! ☺️\n"
                "Se quiser, é só digitar *sim*"
            )
            resp.message(
                "Se preferir fazer o agendamento manualmente, clique no link abaixo e preencha seus dados para nós te conhecermos antes 💛\n\n"
                "👉🏻 https://algumlinkaqui\n\n"
                "📍 Nordeste - Brasil"
            )
            user_data[from_number]["state"] = 'euquero_1'

        elif incoming_msg == '2':
            resp.message(
                "Eu mesmo posso agendar sua consulta rapidinho! ☺️\n"
                "Se quiser, é só digitar *sim*"
            )
            resp.message(
                "Se preferir fazer o agendamento manualmente, clique no link abaixo e preencha seus dados para nós te conhecermos antes 💛\n\n"
                "👉🏻 https://algumlinkaqui\n\n"
                "📍 Nordeste - Brasil"
            )
            choices.append({ "choice": "Retorno", "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            })
            user_data[from_number]["state"] = 'euquero_2'

        elif incoming_msg in ['sair']:
            resp.message("Até mais! Caso precise de mim novamente, manda um oi que eu apareco. ✋🏼")
            user_data[from_number]["state"] = None
        else:
            resp.message("Desculpa, nao te entendi 🥲\n\n"
                         "Digita *sim* que eu te ajudo!")
            resp.message("Se quiser deixar esta conversa, digita *_sair_*")

            user_data[from_number]["state"] = "escolha_2"

    elif state == 'euquero_1':
        if incoming_msg in ['sim', 'simm', 'siim']:
            resp.message("Estamos quase lá! Diz pra mim qual dia tens preferência de agendar a consulta:\n\n"
                            "1️⃣ - Hoje \n"
                            "2️⃣ - Amanhã \n"
                            "3️⃣ - Próximos cinco dias \n"
                        )
            resp.message("Se preferir, voce mesmo pode procura uma data mais conveniente conosco no link:\n"
                         "👉🏻 https://app.simplesdental.com/simples/agendamento/dragiulianasueyoshi \n \n"
                        )
            user_data[from_number]["state"] = "euquero_1_1"
        elif incoming_msg in ['sair']:
            resp.message("Até mais! Caso precise de mim novamente, manda um oi que eu apareco. ✋🏼")
            user_data[from_number]["state"] = None

        else:
            resp.message("Desculpa, nao te entendi 🥲\n\n"
                         "Digita 1️⃣,  2️⃣ ou 3️⃣ que eu te ajudo!")
            resp.message("Se quiser deixar esta conversa, digita *_sair_*")

            user_data[from_number]["state"] = "euquero_1"

    elif state == 'euquero_2':
        if incoming_msg in ['sim', 'simm', 'siim']:
            resp.message("Estamos quase lá! Diz pra mim qual dia tens preferência de agendar a consulta:\n\n"
                            "1️⃣ - Hoje \n"
                            "2️⃣ - Amanhã \n"
                            "3️⃣ - Próximos cinco dias \n"
                        )
            resp.message("Se preferir, voce pode procura uma data mais conveniente conosco no link:\n"
                         "👉🏻 https://app.simplesdental.com/simples/agendamento/dragiulianasueyoshi \n \n")
            user_data[from_number]["state"] = "euquero_2_1"

        elif incoming_msg in ['sair']:
            resp.message("Até mais! Caso precise de mim novamente, manda um oi que eu apareco. ✋🏼")
            user_data[from_number]["state"] = None

        else:
            resp.message("Desculpa, nao te entendi 🥲\n\n"
                         "Digita 1️⃣,  2️⃣ ou 3️⃣ que eu te ajudo!")
            resp.message("Se quiser deixar esta conversa, digita *_sair_*")

            user_data[from_number]["state"] = "euquero_2"

    elif state == 'euquero_1_1':
        try:
            # Always get Google Calendar busy times once
            now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
            end_utc = now_utc + timedelta(days=7)

            body = {
                "timeMin": now_utc.isoformat(),
                "timeMax": end_utc.isoformat(),
                "timeZone": "America/Sao_Paulo",
                "items": [{"id": CALENDAR_ID}]
            }

            freebusy = service.freebusy().query(body=body).execute()
            busy_times = freebusy["calendars"][CALENDAR_ID]["busy"]

            available_slots = []
            now_local = now_utc.astimezone(BR_TZ)

            # Round to next full hour
            if now_local.minute > 0 or now_local.second > 0 or now_local.microsecond > 0:
                next_hour = now_local.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            else:
                next_hour = now_local

            # ---------- HOJE ----------
            if incoming_msg in ['hoje', '1']:
                current = max(next_hour, now_local.replace(hour=9, minute=0, second=0, microsecond=0))
                end_local = now_local.replace(hour=18, minute=0, second=0, microsecond=0)
                title = "✨ Horários disponíveis:\n\n"

            # ---------- AMANHÃ ----------
            elif incoming_msg in ['amanha', 'amanhã', '2']:
                tomorrow = now_local + timedelta(days=1)
                current = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
                end_local = tomorrow.replace(hour=18, minute=0, second=0, microsecond=0)
                title = "✨ Horários disponíveis para amanhã:\n\n"

            # ---------- PRÓXIMOS 5 DIAS ----------
            elif any(word in incoming_msg for word in ['3', 'proximos dias', 'próximos dias', 'proximos cinco dias']):
                current = max(next_hour, now_local.replace(hour=9, minute=0, second=0, microsecond=0))
                end_local = now_local + timedelta(days=5)
                title = "✨ Horários disponíveis nos próximos 5 dias:\n\n"

            elif incoming_msg == 'sair':
                user_data[from_number]["state"] = None

            else:
                resp.message("❌ Opção inválida. Digite 'hoje', 'amanhã' ou 'próximos dias'.\n \n"
                             "Se quiser sair basta digitar _*sair*_")
                user_data[from_number]["state"] = 'euquero_1_1'
                return str(resp)

            # ---------- LOOP DE HORÁRIOS ----------
            while current < end_local:
                slot_start = current
                slot_end = current + timedelta(hours=1)

                # Check if slot overlaps busy time
                is_free = True
                for busy in busy_times:
                    busy_start = datetime.fromisoformat(busy["start"]).astimezone(BR_TZ)
                    busy_end = datetime.fromisoformat(busy["end"]).astimezone(BR_TZ)
                    if not (slot_end <= busy_start or slot_start >= busy_end):
                        is_free = False
                        break

                if is_free and 9 <= slot_start.hour < 18:  # working hours
                    available_slots.append({ "start": slot_start,  # datetime object
                                             "end": slot_end,      # datetime object
                                             "label": f"📅 {slot_start.strftime('%A, %d/%m')} \n🕒 {slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
                                                
                                            })
                current += timedelta(hours=1)

            user_data[from_number]["available_slots"] = available_slots


            if available_slots:
                message_text = title
                for i, slot in enumerate(available_slots[:10], start=1):
                    message_text += f"\n{i}️⃣ - {slot['label']}"
                resp.message(message_text)
                resp.message("\nDigite o número do horário que deseja agendar.")

                user_data[from_number]["state"] = "escolha_horario_1"

            else:
                resp.message("❌ Não há horários disponíveis nesse período.")

        except Exception as e:
            print("❌ Erro:", e)
            resp.message(f"Ocorreu um erro: {e}")

    elif state == 'euquero_2_1':
        try:
            # Always get Google Calendar busy times once
            now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
            end_utc = now_utc + timedelta(days=7)

            body = {
                "timeMin": now_utc.isoformat(),
                "timeMax": end_utc.isoformat(),
                "timeZone": "America/Sao_Paulo",
                "items": [{"id": CALENDAR_ID}]
            }

            freebusy = service.freebusy().query(body=body).execute()
            busy_times = freebusy["calendars"][CALENDAR_ID]["busy"]

            available_slots = []
            now_local = now_utc.astimezone(BR_TZ)

            # Round to next full hour
            if now_local.minute > 0 or now_local.second > 0 or now_local.microsecond > 0:
                next_hour = now_local.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            else:
                next_hour = now_local

            # ---------- HOJE ----------
            if incoming_msg in ['hoje', '1']:
                current = max(next_hour, now_local.replace(hour=9, minute=0, second=0, microsecond=0))
                end_local = now_local.replace(hour=18, minute=0, second=0, microsecond=0)
                title = "✨ Horários disponíveis:\n\n"

            # ---------- AMANHÃ ----------
            elif incoming_msg in ['amanha', 'amanhã', '2']:
                tomorrow = now_local + timedelta(days=1)
                current = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
                end_local = tomorrow.replace(hour=18, minute=0, second=0, microsecond=0)
                title = "✨ Horários disponíveis para amanhã:\n\n"

            # ---------- PRÓXIMOS 5 DIAS ----------
            elif any(word in incoming_msg for word in ['3', 'proximos dias', 'próximos dias', 'proximos cinco dias']):
                current = max(next_hour, now_local.replace(hour=9, minute=0, second=0, microsecond=0))
                end_local = now_local + timedelta(days=5)
                title = "✨ Horários disponíveis nos próximos 5 dias:\n\n"

            elif incoming_msg == 'sair':
                user_data[from_number]["state"] = None

            else:
                resp.message("❌ Opção inválida. Digite 'hoje', 'amanhã' ou 'próximos dias'.\n \n"
                             "Se quiser sair basta digitar _*sair*_")
                user_data[from_number]["state"] = 'euquero_2_1'
                return str(resp)

            # ---------- LOOP DE HORÁRIOS ----------
            while current < end_local:
                slot_start = current
                slot_end = current + timedelta(hours=1)

                # Check if slot overlaps busy time
                is_free = True
                for busy in busy_times:
                    busy_start = datetime.fromisoformat(busy["start"]).astimezone(BR_TZ)
                    busy_end = datetime.fromisoformat(busy["end"]).astimezone(BR_TZ)
                    if not (slot_end <= busy_start or slot_start >= busy_end):
                        is_free = False
                        break

                if is_free and 9 <= slot_start.hour < 18:  # working hours
                    available_slots.append({ "start": slot_start,  # datetime object
                                             "end": slot_end,      # datetime object
                                             "label": f"📅 {slot_start.strftime('%A, %d/%m')} \n🕒 {slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
                                                
                                            })
                current += timedelta(hours=1)

            user_data[from_number]["available_slots"] = available_slots


            if available_slots:
                message_text = title
                for i, slot in enumerate(available_slots[:10], start=1):
                    message_text += f"\n{i}️⃣ - {slot['label']}"
                resp.message(message_text)
                resp.message("\nDigite o número do horário que deseja agendar.")

                user_data[from_number]["state"] = "escolha_horario_1"

            else:
                resp.message("❌ Não há horários disponíveis nesse período.")

        except Exception as e:
            print("❌ Erro:", e)
            resp.message(f"Ocorreu um erro: {e}")

    elif state == "escolha_horario_1":
        try:
            choice_index = int(incoming_msg) - 1
            slots = user_data[from_number].get("available_slots", [])
            if 0 <= choice_index < len(slots):
                chosen_slot = slots[choice_index]
                user_data[from_number]["slot"] = chosen_slot
                resp.message(f"✅ Ótimo! Você escolheu: {chosen_slot['label']}")
                resp.message("Agora me diz seu nome completo para finalizar o agendamento:")
                user_data[from_number]["state"] = "aguardando_nome"
            elif incoming_msg in ['voltar']:
                user_data[from_number]["state"] = "euquero_1"
            else:
                resp.message("❌ Número inválido. Digite novamente o número do horário que deseja.\n\n"
                             "Se quiser voltar digite *voltar*, e escolha outro dia.")
        except ValueError:
            resp.message("❌ Por favor, digite apenas o número do horário escolhido.\n\n"
                         "Se quiser voltar digite *voltar*, e escolha outro dia.")

    elif state == "aguardando_nome":
        try:
            patient_name = incoming_msg.title()  
            
            selected_slot = user_data[from_number]["slot"]
            slot_label = selected_slot["label"]
            slot_start = selected_slot["start"]  # datetime object
            slot_end = selected_slot["end"]      # datetime object

            # Make sure they're timezone-aware (optional if already done)
            slot_start = slot_start.astimezone(BR_TZ)
            slot_end = slot_end.astimezone(BR_TZ)


            event = {
                "summary": f"Consulta com Dra. Giuliana - {patient_name}",
                "location": "Av. Paulista, 2202 - São Paulo",
                "description": f"Agendamento feito via WhatsApp bot para {patient_name}",
                "start": {"dateTime": slot_start.isoformat(), "timeZone": "America/Sao_Paulo"},
                "end": {"dateTime": slot_end.isoformat(), "timeZone": "America/Sao_Paulo"},
            }

            event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

            resp.message(f"✅ Oi, {patient_name}, seu agendamento tá confirmado no horário {slot_label}.")


            user_data[from_number]["state"] = None
            user_data[from_number].pop("slot", None)
            
        except Exception as e:
            print("❌ Erro:", e)
            resp.message(f"Ocorreu um erro: {e}")

    elif state == 'escolha_3':

        if incoming_msg.lower() in ['Item A', 'item a', '1' 'Item a']:
            resp.message( "Escolhe um dos números acima que te envio a resposta ☺️\n \n"
                "1️⃣ Procedimento e material usado"
                "2️⃣ Tempo de tratamento"
                "3️⃣ Valores"
            )
            resp.message("Se voce tem uma dúvida mais especifica, vou te convidar a conversar diretamente conosco através do link do whatsapp abaixo:\n\n"
                         "https://wa.me/5511986000611")
            resp.message("Detalha bem tua dúvida que ela vai te responder da melhor forma! 😁")
            user_data[from_number]["state"] = "item_a"

        elif incoming_msg.lower() in ['Item B', 'item b', '2' 'Item b']:
            resp.message( "Escolhe um dos números acima que te envio a resposta ☺️\n \n"
                "1️⃣ Procedimento e material usado"
                "2️⃣ Tempo de tratamento"
                "3️⃣ Valores"
            )
            resp.message("Se voce tem uma dúvida mais especifica, vou te convidar a conversar diretamente conosco através do link do whatsapp abaixo:\n\n"
                         "https://wa.me/5581996882421")
            resp.message("Detalha bem tua dúvida que ela vai te responder da melhor forma! 😁")
            user_data[from_number]["state"] = "item_b"

        elif incoming_msg.lower() in ['Item C', 'item c', '3' 'Item c']:
            resp.message( "Escolhe um dos números acima que te envio a resposta ☺️\n \n"
                "1️⃣ Procedimento e material usado"
                "2️⃣ Tempo de tratamento"
                "3️⃣ Valores"
            )
            resp.message("Se voce tem uma dúvida mais especifica, vou te convidar a conversar diretamente conosco através do link do whatsapp abaixo:\n\n"
                         "https://wa.me/5581996882421")
            resp.message("Detalha bem tua dúvida que ela vai te responder da melhor forma! 😁")
            user_data[from_number]["state"] = "item_c"

        elif incoming_msg.lower() in ['Item D', 'item d', '4' 'Item d']:
            resp.message( "Escolhe um dos números acima que te envio a resposta ☺️\n \n"
                "1️⃣ Procedimento e material usado"
                "2️⃣ Tempo de tratamento"
                "3️⃣ Valores"
            )
            resp.message("Se voce tem uma dúvida mais especifica, vou te convidar a conversar diretamente conosco através do link do whatsapp abaixo:\n\n"
                         "https://wa.me/5581996882421")
            resp.message("Detalha bem tua dúvida que ela vai te responder da melhor forma! 😁")
            user_data[from_number]["state"] = "item_d"

        elif incoming_msg.lower() in ['Item E', 'item e', '5' 'Item e']:
            resp.message( "Escolhe um dos números acima que te envio a resposta ☺️\n \n"
                "1️⃣ Procedimento e material usado"
                "2️⃣ Tempo de tratamento"
                "3️⃣ Valores"
            )
            resp.message("Se voce tem uma dúvida mais especifica, vou te convidar a conversar diretamente com a Dra. Giuliana através do link do whatsapp abaixo:\n\n"
                         "https://wa.me/5581996882421")
            resp.message("Detalha bem tua dúvida que ela vai te responder da melhor forma! 😁")

            user_data[from_number]["state"] = "item_e"

        else:
            resp.message("Se voce tem uma dúvida mais especifica, vou te convidar a conversar diretamente com a Dra. Giuliana através do link do whatsapp abaixo:\n\n"
                        "https://wa.me/5581996882421")
            resp.message("Detalha bem tua dúvida que ela vai te responder da melhor forma! 😁")

    elif state == 'item_a':
        if incoming_msg == '1':
            resp.message("A Dra. Giuliana resolve estes tipos de problemas: \n \n"
                         "1️⃣ Manchinhas brancas ou marrons(tipo de mancha dental)\n"
                         "2️⃣ Dente escurecido por trauma ou canal\n"
                         "3️⃣ Dentes amarelados\n \n" 
                         
                         "Qual das opcoes te interessa mais?"
                         )

            user_data[from_number]["state"] = "item_a_1"

        elif incoming_msg == '2':
            resp.message("O ideal é fazermos pelo menos 4 sessoes, que pode ser uma por semana. O valor pago pelo tratamento inclui todos os gastos, inclusive se houver a necessidade de uma sessao extra.")

        elif incoming_msg == '3':
            resp.message("Os valores variam entre R$1500,00 e R$4000,00, dependendo da técnica indicada (clareamento convencional, interno ou associado à microabrasão)")

    elif state == "item_a_1":
        if incoming_msg == '1':
            resp.message("*Microabrasão* + *clareamento*: trata manchas brancas, marrons ou opacas (_fluorose_, _hipoplasia_, _desmineralização_). Remove a camada superficial e uniformiza a cor dos dentes.")

        elif incoming_msg == '2':
            resp.message("*Clareamento* *interno*: o gel é colocanto na parte interna do dente agindo de dentro para fora, devolvendo a cor natural sem restauração ou faceta.")

        elif incoming_msg == '3':
            resp.message("*Clareamento* *tradicional*: Usamos  gel clareador (no consultório ou com moldeiras em casa) paraclarear todos os dentes de forma uniforme, deixando o sorriso mais claro, natural e harmônico."
                        )

    elif state == 'item_b':
        if incoming_msg == '1':
            resp.message("Ainda em construcao")

        elif incoming_msg == '2':
            resp.message("Ainda em construcao")

        elif incoming_msg == '3':
            resp.message("Ainda em construcao")

    elif state == 'item_c':
        if incoming_msg == '1':
            resp.message("Ainda em construcao")

        elif incoming_msg == '2':
            resp.message("Ainda em construcao")

        elif incoming_msg == '3':
            resp.message("Ainda em construcao")

    elif state == 'item_d':
        if incoming_msg == '1':
            resp.message("Ainda em construcao")

        elif incoming_msg == '2':
            resp.message("Ainda em construcao")

        elif incoming_msg == '3':
            resp.message("Ainda em construcao")

    elif state == 'item_e':
        if incoming_msg == '1':
            resp.message("Ainda em construcao")

        elif incoming_msg == '2':
            resp.message("Ainda em construcao")

        elif incoming_msg == '3':
            resp.message("Ainda em construcao")


    print(user_data)

    return str(resp)


@app.route("/debug", methods=["GET"])
def debug():
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(port=5001)
