import openai
from openai import OpenAI
import os
import psycopg2
import pgvector
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
import numpy as np

# question= 'what is the significance of german sailors to the hamburger'

def call_embedding(client, text):
    embedding = client.embeddings.create(model="text-embedding-ada-002",input = [text.replace("\n"," ")]).data[0].embedding
    return embedding

def query_db(client, question):
    # prepare question
    embedding = call_embedding(client, question)


    #connect to db
    con_str= os.environ['pg_conn_str']
    conn = psycopg2.connect(con_str)
    cur = conn.cursor()

    # Get top 3 docs by cosign simantic sim
    sql = """SELECT 
                vec.content
                ,doc.url 
                ,doc.content
            FROM 
                vector_store vec
            INNER JOIN doc_store doc
                on vec.doc_id=doc.doc_id
            ORDER BY vec.embedding <=> %s 
            LIMIT 3"""
    cur.execute(sql, (str(embedding),))
    docs = cur.fetchall()
    return docs

def generate_rep(client, docs, question):
    #print(f'url: {docs[0][1]} \n {docs[1][1]} {docs[2][1]}')
    context = """You are a chatbot, highly skilled in foods, cooking and resturants. 
                You provide consice, accurate responses to questions from users. 
                The information provided as "relevant information" superseeds that from your training.
                If you do not know the answer to a question, you say that you do not know, you do not make up an answer."""
    
    delimiter = "```"

    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": f"{delimiter}{question}{delimiter}"},
        {"role": "assistant", "content": f"Relevant information: \n {docs[0][0]} \n {docs[1][0]} {docs[2][0]}"}   
    ]
    print(f'question: {question}')

    # OpenAI Call
    response = client.chat.completions.create(model="gpt-4",messages=messages,temperature=0, max_tokens=1000)
    # print(response)
    return response.choices[0].message.content

def get_answer(question):
    print(question)
    client = OpenAI()
    docs = query_db(client, question)
    answer = generate_rep(client, docs, question)
    urls = [set([x[1] for x in docs])]
    contexts = [set([x[0] for x in docs])]
    texts = [set([x[2] for x in docs])]
    return {'content':answer, 'context':contexts[0], 'urls': urls, 'full_text':texts[0]}

#print(get_answer(question))