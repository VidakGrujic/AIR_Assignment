# AIR_Assignment

Dataset folder struktura:

Link: https://www.transfernow.net/dl/20250517SMIHedCm

datasets
-> final_correct_datasets
    -> test
        -> `parsed_data_final_test_batch_1.json`
        -> `parsed_data_final_test_batch_2.json`
        -> `parsed_data_final_test_batch_3.json`
        -> `parsed_data_final_test_batch_4.json`
    -> training
        -> `parsed_data_final.json`
    -> `all_retreived_articles.json`
-> other_datasets
    ... ovo nije tolko vazno


Update:

Posto sam skontao da nije dobro da za svako pitanje imamo samo po 170 artikala, tj sistem da gleda u 170 artikala samo po pitanju, napravio sam mini bazu podataka pub meda. U prevodu, spojio sam sve artikle koje smo dobavili sa pubmed-a, znaci za svako pitanje uzimao sam sve arikle i spajao u jedan fajl. U njemu se u totalu nalaze 880327 aritkala. Svoj model trebate da trenirate i testirate na tim artiklima. Bukvalno kao da smo samplovali celokupnu pubmed bazu podataka. Fajl se zove `all_retrieved_articles.json`

Sto se tice ground_truth informacija, njih mozete izvuci za training dataset iz `parsed_data_final.json`. Sto se tice test ground_truth, njih mozete izvuci iz `parsed_data_final_test_batch_[1,2,3,4].json` 

Napravio sam klasu `DataManipulator` iz fajla `data_manipulation` koja pomaze da se izvuku svi artikli i ground truth infomacije iz gore navedenih fajlova

-> Import class: from data_manipulation import DataManipulator

U njemu postoje 3 glavne metode:
    -> `get_all_articles(all_articles_file_path)`: One izvlace sve artikle koje smo spojili u jedan fajl. (Objasnjenje gore)
    -> `get_ground_truth_one_file(file_path)`: izvlaci ground truth informacije iz jednog fajla. Primer: `get_ground_truth_one_file('datasets/final_correct_datasets/test/parsed_data_final_test_batch_1.json')`
    -> `get_ground_truth_all_files(folder_path)`: izvlaci ground truth informacije iz svih JSON fajlova koji se nalaze u `folder_path`. Prevashodno sam napravio ovo za test fajlove, da ne morate da citate jedan po jedan. Takodje mozete i training folder path da prosledite, on ce ucitati jedan training fajl. Primer: `get_ground_truth_one_file('datasets/final_correct_datasets/test')` -> Ovo ce ucitati sve test fajlove, spojice ground truth podate i vratice listu ground truth objekta koji ovako izgleda:
    
        Ground truth data object(dict) consists of:
            - qid -> question id
            - question -> question text
            - ground_truth_documents_pid: list of ground truth documents IDs 
            - ground_truth_snippets: list of ground truth snippets



Zakljucak:
    -> Za training i testiranje koristite nasu samplovanu pubmed bazu podata `all_retrieved_articles.json`
    -> Za dobijanje ground truth podataka koristite `DataManipulator` klasu. Ovo sam napravio da olaksa, ali vi mozete i sami rucno da ucitavate podatke.








