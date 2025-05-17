import json 
import random 
import os



class DataManipulator:
    def __init__(self):
        pass
        
    ####### Private Functions #######
    def __get_ground_truth_from_question(self, question):
        ground_truth_info = {
            'qid': question['qid'],
            'question': question['question'],
            'ground_truth_documents_pid': question['ground_truth_documents_pid'],
            'ground_truth_snippets': question['ground_truth_snippets']
        }

        return ground_truth_info

    def __load_file(self, file_path):
        with open(file=file_path, mode='r') as file:
            data = json.load(file)

        return data['data']
    

    def __get_file_paths_from_folder(self, folder_path):
        json_files = []
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                file_path = os.path.join(folder_path, file)
                json_files.append(file_path)

        return json_files



    ####### Public Functions #######
    def get_all_articles(self, all_articles_file_path):
        '''
        This function loads all articles
        File path is provided when initializing the object of the class under `all_articles_file_path`

        Returns
            - List of dictionaries with article data (qid, title, abstract)
        '''
        with open(file=all_articles_file_path, mode='r') as file:
            all_articles = json.load(file)

        return all_articles
    
    def get_ground_truth_one_file(self, file_path):
        '''
        Get test ground truth data for FOR ONE FILE
        All data from test file dataset should be in 'data' array
        It can be either train dataset or test datasets json files

        Ground truth data object(dict) consists of:
            - qid -> question id
            - question -> question text
            - ground_truth_documents_pid: list of ground truth documents IDs 
            - ground_truth_snippets: list of ground truth snippets

        Returns 
            - List of ground_truth_data objects
        '''

        data = self.__load_file(file_path=file_path)

        ground_truth_data = []
        
        for question in data:
            ground_truth_data.append(self.__get_ground_truth_from_question(question=question))

        return ground_truth_data



    def get_ground_truth_from_all_files(self, folder_path):
        '''
        This function READS ALL JSON FILES FROM `folder_path` and COMBINE ALL GROUND TRUTH DATA FROM THEM
        Folder path has to be passed through 
        
        If we have 4 files, it will extract and combine all ground truth data from all 4 files
    
        Returns 
            - List of ground_truth_data objects
        '''

        all_ground_truth_data = []

        for file in self.__get_file_paths_from_folder(folder_path=folder_path):
            data = self.__load_file(file)
            
            for question in data:
                ground_truth_info = self.__get_ground_truth_from_question(question=question)
                all_ground_truth_data.append(ground_truth_info)


        return all_ground_truth_data
        
        
