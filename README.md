# AIR_Assignment

We ahve 2 datasets, 
1) Whole retreived dataset (retrived_articles_sampled.json) 
2) Additionally processed dataset (parsed_data_final.json)
3) Training data downloaded from BioASQ (training13b.json)

From the training13b.json dataset, we iterated over questions and retreived between 150 and 200 relevant articles, with a lot of additionall data, which is stored in retreived_articles_sampled.json. After that, using notebook Additional_Parsing_Of_data.ipynb, we additionally processed data and extracted relevant information, which produced the file parsed_data_final.json
This file should contain all relevant information needed to create IR system for the training dataset. For test batches, we will discuss what is necessary to do. 

## Link to whole retreived dataset
https://www.transfernow.net/dl/20250428Yb0yaxs6
Expires on 5.5.2025.

## Link to the additionally processed dataset. Contains qid, questin, ground_truth_documents_pid, error_rate, ground_truth_snippets, all_retreived_articles

https://www.transfernow.net/dl/20250503y4w3gpDW
Expires on 10.5.2025.