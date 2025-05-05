# AIR_Assignment

Po mom misljenju, za training i test vam trebaju sledeci datasetovi. BTW, ja cu ove datasetove koristiti za moj BM25 i metrics evaluation.
Training -> parsed_data_final.json
Test -> parsed_data_final_test_batch_1.json, parsed_data_final_test_batch_2.json, parsed_data_final_test_batch_3.json
10.5.2025 ce izaci i test batch 4 sa golden asnwers, pa cu i taj dataset da ubacim. 

Link do svih fajlova: https://www.transfernow.net/dl/20250505038iHHsk

Easter egg: https://www.youtube.com/watch?v=iu_Z_d1lyeg

Ako hocete da znate kako sam ih dobio, procitajte dole. Sve ovo sto dole pisem napisacu u reportu. 

Ovako, u globalu imamo training i test datasetove. Training dataset koji smo skinuli sa BioASQ sajta je training13b.json. Tu imamo oko 5300 pitanja sa golden article (golden article je ground truth article, tj. relevantan artikal). Medjutim, mi mora da izvucemo top 10 articles i snippeta. Zbog toga smo napravili Training_&_Gold_Test_Question_API_retreival.ipynb. On ucitava ove datasetove, prolazi kroz pitanja, pravi izmedju 10-20 querija i salje API request da se vrate relevantni artciles za svaki query. U totalu to bude puno njih (> 10 000 articles). Medjutim mi ne mozemo tolko da sacuvamo pa sta radimo? Vidimo dal smo uspeli da dobavimo ground truth artikle. Ako jesmo, uzmemo njih i plus 150 random artikala. U totalu, po pitanju mi imamo 150 + n articles, gde je n broj ground truth articles. Sve to se cuva u retrieved_articles_sampled.json (training) i u retreived_articles_sampled_test_batch_{i} gde je i broj batcha (ima ih 4). Tu cuvamo puno potrebnih i nepotrebnih informacija. Potom, postoji notebook Additiona_Training_&_Gold_Test_Data_Parsing.json koji iz navedenih datasetova izvlaci informacije: question, ground_truth_documents_pid, ground_truth_snippets, all_relevant_articles. To su fajlovi koji su navedeni u prvom paragrafu ovog teksta. Inace, test golden answers su dobijeni od test datasets iz faze B, posto test datasets za fazu A su samo tekst pitanja, id pitanja i tip pitanja. Da bi njih dobili sa BioASQ API-ja, napravljena je skripta Test_Question_API_Retreival.ipynb, koja uzima random 150 aritkala po pitanju. Ovo se koristi samo da bismo nesto predali na BioASQ sajtu. Videcu dal cu ovo za report da stavim. Za sam predmet i projekat predmeta, 4 fajla (posle 10.5. 5 fajla) gore navedena su vazna.