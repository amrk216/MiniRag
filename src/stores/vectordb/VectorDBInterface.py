from abc import ABC, abstractmethod
from typing import List


class vectordbInterface(ABC):
    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_existed(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def create_collection(self,
                           collection_name: str,
                             embedding_size: int,
                             do_reset: bool = False
                             ):
        pass

    @abstractmethod
    def list_all_collection(self) ->List:
        pass

    @abstractmethod
    def get_collection_info(self ,collection_name:str):
        pass    

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass


    @abstractmethod
    def insert_one(self,
                   collection_name:str,
                   text:str,
                   vector:list,
                   metadate:dict=None,
                   record_id:str = None
                   ):
        pass

    @abstractmethod
    def insert_many(self,
                    collection_name:str,
                    vectors:list,
                    texts =list,
                    metadata:list=None,
                    record_ids:list=None,
                    batch_size:int=50,
                               ) -> List:
        pass

    @abstractmethod
    def search_by_vector(self,
                         collection_name:str,
                         vector:list,
                         limit:int=5,
                         ):
        pass
