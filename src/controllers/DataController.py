from fastapi import UploadFile
from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ResponseSignal
import re
import os
class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTNSIONS:
            return False, ResponseSignal.FILE_TYPE_NOT_ALLOWED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * 1024 * 1024:
            return False , ResponseSignal.FILE_SIZE_EXCEEDED.value
        return True , ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value
        
    

    def get_clean_filename(self,orig_filename:str):

        cleaned_filename = re.sub(r'[^\w.]' , '',orig_filename.strip())

        # replace spaces with underscores

        cleaned_filename = cleaned_filename.replace(' ','_')

        return cleaned_filename
    
    
    def generate_unique_filepath(self,orig_filename:str,project_id:str):

        random_key = self.genrate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_filename = self.get_clean_filename(orig_filename=orig_filename)

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_filename
        )
        while os.path.exists(new_file_path):
            random_key = self.genrate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_filename
            )
        
        return new_file_path, random_key + "_" + cleaned_filename