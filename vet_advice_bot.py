################################################################################################
#                                           ВНИМАНИЕ!                                          #
# Во избежания блокировки аккаунта OpenAI код телеграм бота реализован в ноутбуке Google Colab #
# см. файл
################################################################################################


# # Инсталяция библиотек
# # !pip install faiss-cpu langchain openai==0.28 tiktoken python-docx telebot
#
# # Импортируем необходимые библиотеки
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import FAISS
# import os
# import getpass
# import docx
# import openai
# from langchain.docstore.document import Document
# import logging
# from textwrap import fill
# logging.getLogger("langchain.text_splitter").setLevel(logging.ERROR)
# logging.getLogger("chromadb").setLevel(logging.ERROR)
# import telebot
#
# # Получение ключа API от пользователя и установка его как переменной окружения
# openai_key = getpass.getpass("OpenAI API Key:")
# os.environ["OPENAI_API_KEY"] = openai_key
# openai.api_key = openai_key
#
#
# # функция для загрузки документа по ссылке из гугл драйв
# def load_document_text(file_name: str) -> str:
#     doc = docx.Document(file_name)
#     text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
#     return text
#
# # Инструкция для GPT, которая будет подаваться в system
# system = '''Ты опытный Ветеринарный врач, проводящий консультации в ветеринарной клинике «ДАР».
# Твоя задача - помогать пользователям на основе подробного Руководства.
# Пользователь обращается к Тебе с вопросом. Твоя цель - подробно объяснить ,
# как решить его вопрос полагаясь исключительно на информацию из Руководства.
# 1. Если вопрос пользователя неоднозначен, предложите несколько вариантов уточняющих вопросов.
# иначе
# 1. Дай пользователю подробные инструкции для всех шагов, которые необходимы для решения его вопроса.
# 2. Отвечай максимально точно и не добавляй ничего от себя.
# 3. Последовательность шагов для разных действий может быть уникальна, пожалуйста, не предполагай,
# что она применима к тем действиям, для которых нет описания в Руководстве.
# 4. Если в Руководстве нет точного ответа, пожалуйста, ответь, что Тебе требуестся дополнительная информация для полноценного ответа.
# 5. Если в Руководстве есть информация для ответа, включи ее в ответ.
# 6. Если Ты можешь предложить альтернативное решение задачи пользователя - обязательно сделай это.
# 7. В ответе категорически нельзя упоминать предоставленные тебе Руководства и Отрывки из Руководства.
# 9. К каждому отрывку Руководства задай по одному вопросу близкому по смыслу к вопросу Пользователя. В Твоих вопросах должно обязательно содержаться то же действие, что и в вопросе пользователя.
# 10. Если в ответе ты хочешь сослаться на Руководство или Отрывок из Руководства переформулируй ответ без таких ссылок.
#
# Ответ дай в формате:
# Ветврач: текст ответа.
# Близкие вопросы:
# 1. Вопрос1
# 2. Вопрос2
# 3. Вопрос3
# '''
#
# # База знаний, которая будет подаваться в langChain
# database= load_document_text('df.docx')
#
# # Делим текст на чанки и создаем индексную базу
# source_chunks = []
# splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=0)
#
# for chunk in splitter.split_text(database):
#     source_chunks.append(Document(page_content=chunk, metadata={}))
#
# # Инициализирум модель эмбеддингов
# embeddings = OpenAIEmbeddings()
#
# # Создадим индексную базу из разделенных фрагментов текста
# db = FAISS.from_documents(source_chunks, embeddings)
#
# # Выбор модели, значение температуры и функции
# #MODEL_TURBO_16K = "gpt-3.5-turbo-16k"
# MODEL_TURBO_0613 = "gpt-3.5-turbo-0613"
# temperature= 0
#
# def create_completion(model, system, content, temperature):
#     messages = [
#         {"role": "system", "content": system},
#         {"role": "user", "content": content}
#     ]
#
#     completion = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=temperature
#
#     )
#     return completion.choices[0].message.content
#
# def answer_index(system, topic, search_index, temperature=0, verbose=0):
#     docs = search_index.similarity_search(topic, k=4)
#     message_content = ' '.join([f'\nОтрывок документа №{i+1}\n=====================' + doc.page_content + '\n' for i, doc in enumerate(docs)])
#     question_content = f"Документ с информацией для ответа клиенту: {message_content}\n\nВопрос клиента: \n{topic}"
#     return fill(create_completion(MODEL_TURBO_0613, system, question_content, temperature))
#
# def summarize_questions(dialog):
#     content = "Суммаризируй следующий диалог ассистента отдела обслуживания клиентов и клиента: " + " ".join(dialog)
#     return create_completion(MODEL_TURBO_0613, "Ты - ассистент, который умеет профессионально суммаризировать присланные тебе диалоги. Твоя задача - суммаризировать диалог, который тебе пришел. Отражай имя клиента в саммаризации", content, 0)
#
# def answer_user_question_dialog(system: str, db: str, user_question: str, question_history: list) -> str:
#     summarized_history = ""
#     if question_history:
#         summarized_history = "Вот краткий обзор предыдущего диалога: " + summarize_questions([f'{q} {a or ""}' for q, a in question_history])
#     input_text = f"{summarized_history}\n\nТекущий вопрос: {user_question}"
#     answer_text = answer_index(system, input_text, db)
#     question_history.append((user_question, answer_text or ''))
#     return fill(answer_text)
#
# def run_dialog(user_question, system=system, db=db):
#     question_history = []
#     dialog = ""
#     answer = answer_user_question_dialog(system, db, user_question, question_history)
#     dialog += f'\nЯ: {user_question} \n Ветврач: {answer}'
#     #print('\nВетврач: ', answer, '\n')
#     return answer
#
#
# # Токен для телеграм
# TOKEN = '6691485723:AAFHHB3OEYcFEvsLvs7icK4-ia6WYGWKX5g'
#
# # Инициализация бота
# bot = telebot.TeleBot(TOKEN)
#
# # Функция для команды /start
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.reply_to(message, "Привет! Я бот. Чем могу помочь?")
#
# # Функция для команды /help
# @bot.message_handler(commands=['help'])
# def help_command(message):
#     bot.reply_to(message, "Это пример телеграм бота. Он может преобразовывать введенный текст в заглавные буквы.")
#
# # Функция вопрос/ответ
# @bot.message_handler(content_types=['text'])
# def dialog_text(message):
#     text = run_dialog(message.text)
#     bot.reply_to(message, text)
#
# # Старт бота
# bot.polling()