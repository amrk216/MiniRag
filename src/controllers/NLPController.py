import logging
from typing import List
import json
from fastapi import UploadFile
from stores.llm.LLMEnums import DocumentType
from models.db_schemes import Project,DataChunk
from .BaseController import BaseController
from .ProjectController import ProjectController

class NLPController(BaseController):
    def __init__(self,vectordb_client,generation_client,embedding_client,templateparser):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_clien = generation_client
        self.embedding_client = embedding_client
        self.templateparser = templateparser

    def create_collection_name(self,project_id:str): 
        return f"collection {project_id}".strip()
    
    def reset_vector_db_collection(self,project:Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vector_db_collection_info(self,project:Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)
        return json.loads(
            json.dumps(collection_info,default=lambda x:x.__dict__)
        )
            
    
    def index_into_vector_db(self,project:Project,chunks: List[DataChunk],
                             chunks_ids :List[int],
                             do_reset: bool = False):
        
        #step 1 get collecton name
        collection_name = self.create_collection_name(project_id=project.project_id)

        #step2 mange items

        texts = [
            c.chunk_text
            for c in chunks
        ]

        metadata = [
            c.chunk_metadata
            for c in chunks
        ]

        vectors = [
            self.embedding_client.embed_text(text= text,document_type=DocumentType.DOCUMENT.value)
            for text in texts
        ]

        
        #step3 create collection if not existits
        _ = self.vectordb_client.create_collection(
            collection_name = collection_name,
            embedding_size= self.embedding_client.embedding_size,
            do_reset = do_reset,

        )

        #step 4 insert into vector db

        _ = self.vectordb_client.insert_many(
            collection_name = collection_name,
            texts = texts,
            metadata = metadata,
            vectors= vectors,
            record_ids = chunks_ids

        )


        return True
    

    def search_vector_db_collection(self,project:Project,text:str,limit:int=5):

        #step 1 get collecton name
        collection_name = self.create_collection_name(project_id=project.project_id)

        #step2 get text embedding vector

        vector = self.embedding_client.embed_text(
            text= text,document_type=DocumentType.QUERY.value)
        logging.debug(f"Generated vector: {vector}")
        
        
        if not vector or len(vector) ==0:
            return False
        
        #step 3 search in vector db

        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )
        logging.debug(f"Search results: {results}")
        
        if not results:
            return False 
        
        return results
    

    def answer_rag_guestion(self,project:Project,query:str,limit:int=10):
        answer,full_prompt,chat_history = None,None,None

        retrieved_documents = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit
        )

        if not retrieved_documents or len(retrieved_documents) == 0 :
            return answer,full_prompt,chat_history

        
        system_prompt = self.templateparser.get(
            'rag',
            'system_prompt',

        )
   

        documents_prompts ="\n".join( [
            self.templateparser.get(
                     "rag",
                     'document_prompt',
                     {
                         "doc_num":idx +1,
                        "chunk_text":doc.text
                    })

            for idx,doc in enumerate(retrieved_documents)

        ])
        

        footer_prompt = self.templateparser.get(
            'rag',
            'footer_prompt',
            
        )

        chat_history = [
            self.generation_clien.construct_prompt(
                prompt = system_prompt,
                role = self.generation_clien.enums.SYSTEM.value
            )
        ]

        full_prompt = "\n\n".join([
            documents_prompts,
            footer_prompt
        ])

        answer = self.generation_clien.generate_text(
            prompt = full_prompt,
            chat_history= chat_history,
        )

        return answer,full_prompt,chat_history




            

        

        






        