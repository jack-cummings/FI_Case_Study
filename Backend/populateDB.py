# Script to scrape corpus from Wikipidea, Chunk, embed and store in PgVector

import pandas as pd 
import wikipediaapi
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
import openai
from openai import OpenAI
import os
import psycopg2
import pgvector
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
import numpy as np


def preprocess_corpus_list():
    """Corpus will consist of wikipidia pages on various dishes pipular in the US.
    ChatGPT was used to populate a list of 100 such dishes, this list requires pre-processing prior
    to being used in wikipidia scraping to populate the text corpus"""
    with open('Backend/raw_list.txt') as f:
        content = f.read()
    foods_list  = [x.strip() for x in content.split(',')]
    foods_list = [{foods_list}]
    print(foods_list)

    return foods_list

def extract_text(input_list):
    """Input list of terms
       Output: dataframe of wiki articles containing the term, article text and article URL"""
    
    # Initialize connection to WIKI API
    wiki_wiki = wikipediaapi.Wikipedia('jc_personal', 'en')
    
    # df = pd.DataFrame(input_list,columns=['ID'])
    corpus = []
    for item in input_list:
            try:
                print(item)
                page = wiki_wiki.page(item)
                item_url = page.text
                item_text = page.fullurl
                corpus.append([item,item_text,item_url])
                print('success')
            except:
                 # as we are simply populating corpus, missing wikis can be ignored
                 print('failed')
                 
    
    df = pd.DataFrame(corpus,columns=['ID','Url','Text'])
    return df

def chunk_texts(df):
    # Use Langchain text splitters to create windowed doc chunks of length 1000
    # text_splitter = CharacterTextSplitter(separator = "\n", chunk_size = 1000, chunk_overlap  = 200, length_function = len, is_separator_regex = False)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7000, chunk_overlap=200, separators=[" ", ",", "\n"])

    chunks_corpus= []
    for i in range(len(df)):
        name = df.values[i][1]
        text = df.values[i][3]
        url = df.values[i][2]
        chunks = text_splitter.split_text(text)
        for chunk in chunks:
            pos = chunks.index(chunk)
            chunks_corpus.append([f'{name}_{pos}',chunk,url])
    
    chunks_df = pd.DataFrame(chunks_corpus, columns=['ID','Text','Url'])
    return chunks_df

def call_embedding(text):
    embedding = client.embeddings.create(model="text-embedding-ada-002",input = [text.replace("\n"," ")]).data[0].embedding
    return embedding

def get_embeddings(df):
    df['Embedding'] = df['Text'].apply(lambda x: call_embedding(x))
    return df

def populatePGV(vdf):

    # Conenct to DB
    con_str= os.environ['pg_conn_str']
    conn = psycopg2.connect(con_str)
    cur = conn.cursor()

    #install pgvector
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()
    register_vector(conn)

    # init table
    #  , 
    init_table = """
    DROP TABLE IF EXISTS vector_store;
    CREATE TABLE vector_store (
                id text primary key, 
                url text,
                content text,
                embedding vector(1536)
                );
                """

    cur.execute(init_table)


    print('db con and init complete')
    print(type(np.array(vdf.values[0][4])))
    batch_data = [(x[1],x[3],x[2], np.array(x[4])) for x in vdf.values]
    execute_values(cur, "INSERT INTO vector_store (id, url, content, embedding) VALUES %s", batch_data)
    # Commit changes
    conn.commit()

    # Validate
    cur.execute("SELECT COUNT(*) as cnt FROM vector_store;")
    cnt = cur.fetchone()[0]
    print(f'{cnt} records in vector_store db')

    cur.close()
    conn.commit()


#client = OpenAI()
# corpusDF = extract_text(preprocess_corpus_list())
# corpusDF.to_csv('./corpus.csv')
# corpusDF = pd.read_csv('./corpus.csv')
# chunkDF = chunk_texts(corpusDF)
# print(len(chunkDF))
# cost = ((len(chunkDF)*7000)/1000)*.0004
# print(cost)
# vectorDF = get_embeddings(chunkDF)
# vectorDF.to_csv('./vectorDF.csv')

vdf = pd.read_csv('./vectorDF.csv')
vdf['Embedding'] = vdf['Embedding'].apply(lambda x: [float(i) for i in x[1:-1].split(',')])
vdf= vdf[vdf['ID']!= 'Beef Wellington_0']
populatePGV(vdf)


print('done')



