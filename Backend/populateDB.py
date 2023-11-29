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
    foods_list = list(set(foods_list))
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
            corpus.append([item.replace(' ','_'),item_text,item_url])
            print('success')
        except:
            print('failed: {item}')
            # as we are simply populating corpus, missing wikis can be ignored

        # page = wiki_wiki.page(item)
        # item_text = page.text
        # item_url = page.fullurl
        # corpus.append([item.replace(' ','_'),item_text,item_url])
        # print('success')
                 
    
    df = pd.DataFrame(corpus,columns=['ID','Url','Text'])
    print(f' corpus df len: {len(df)}')
    return df

def write_corpus_df(df):
    # Conenct to DB
    con_str= os.environ['pg_conn_str']
    conn = psycopg2.connect(con_str)
    cur = conn.cursor()

    # init table
    #  , 
    init_table = """
    DROP TABLE IF EXISTS doc_store;
    CREATE TABLE doc_store (
                doc_id text primary key,
                url text,
                content text
                );
                """

    cur.execute(init_table)

    print('db con and doc store init complete')
    batch_data = [(x[0],x[1],x[2]) for x in df.values]
    execute_values(cur, "INSERT INTO doc_store (doc_id, url, content) VALUES %s", batch_data)
    # Commit changes
    conn.commit()

    # Validate
    cur.execute("SELECT COUNT(*) as cnt FROM doc_store;")
    cnt = cur.fetchone()[0]
    print(f'{cnt} records in doc_store db')

    cur.close()
    conn.commit()

def chunk_texts(df):
    """Chunk texts using token length of 1k with 200 token overlap.
    This is high resolution, optimized for accuracy over efficiency"""
    # Use Langchain text splitters to create windowed doc chunks of length 1000
    # text_splitter = CharacterTextSplitter(separator = "\n", chunk_size = 1000, chunk_overlap  = 200, length_function = len, is_separator_regex = False)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50, separators=[" ", ",", "\n"])

    chunks_corpus= []
    for i in range(len(df)):
        name = df.values[i][1]
        text = df.values[i][3]
        url = df.values[i][2]
        chunks = text_splitter.split_text(text)
        for chunk in chunks:
            pos = chunks.index(chunk)
            chunks_corpus.append([f'{name}_{pos}',chunk,url,name])
    
    chunks_df = pd.DataFrame(chunks_corpus, columns=['chunk_id','Text','Url','doc_id'])
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

    print('writing vector table and indexing')
    # init table
    #  , 
    init_table = """
    DROP TABLE IF EXISTS vector_store;
    CREATE TABLE vector_store (
                chunk_id text primary key,
                doc_id text, 
                url text,
                content text,
                embedding vector(1536)
                );
    CREATE INDEX ON vector_store USING hnsw (embedding vector_cosine_ops);
                """

    cur.execute(init_table)

    print('db con and init complete')
    print(type(np.array(vdf.values[0][4])))
    batch_data = [(x[0],x[3],x[2],x[1], np.array(x[4])) for x in vdf.values]
    execute_values(cur, "INSERT INTO vector_store (chunk_id, doc_id, url, content, embedding) VALUES %s", batch_data)
    # Commit changes
    conn.commit()

    # Validate
    cur.execute("SELECT COUNT(*) as cnt FROM vector_store;")
    cnt = cur.fetchone()[0]
    print(f'{cnt} records in vector_store db')

    cur.close()
    conn.commit()


client = OpenAI()
corpusDF = extract_text(preprocess_corpus_list())
write_corpus_df(corpusDF)
corpusDF.to_csv('./corpus.csv')
corpusDF = pd.read_csv('./corpus.csv')
chunkDF = chunk_texts(corpusDF)
print(f'chunk df len: {len(chunkDF)}')
print(chunkDF.head())
cost = ((len(chunkDF)*400)/1000)*.0004
print(cost)
vectorDF = get_embeddings(chunkDF)
vectorDF.to_csv('./vectorDF.csv')
populatePGV(vectorDF)
print('done')

# if using csv
# vdf = pd.read_csv('./vectorDF.csv')
# vdf['Embedding'] = vdf['Embedding'].apply(lambda x: [float(i) for i in x[1:-1].split(',')])
# vdf= vdf[vdf['ID']!= 'Beef Wellington_0']




