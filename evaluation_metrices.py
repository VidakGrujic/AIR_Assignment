import json
import math 
from tqdm import tqdm

class Accuracy:
    def __init__(self):
        pass 

    # this computes MRR for single quesion
    def compute_mrr(self, predicted_pids, ground_truth_pids):
        for i, pid in enumerate(predicted_pids):
            if pid in ground_truth_pids:
                return 1.0 / (i + 1)
        return 0.0
        

    # this computes average precision for single question
    def compute_average_precision(self, predicted_pids, ground_truth_pids):
        """
        Computes Average Precision based on:
        AP = sum(P@i * rel_i) / |relevant documents|
        """
        hits = 0
        score = 0.0
        for i, pid in enumerate(predicted_pids):
            if pid in ground_truth_pids:
                hits += 1
                score += hits / (i + 1)  # Precision at rank i
        return score / len(ground_truth_pids) if hits > 0 else 0.0
    


    # This computes nDCG for single question
    def compute_ndcg(self, predicted_pids, ground_truth_pids, k=10):
        """
        nDCG with binary relevance (1 if in ground truth, 0 otherwise)
        """
        dcg = 0.0
        for i, pid in enumerate(predicted_pids[:k]):
            if pid in ground_truth_pids:
                dcg += 1 / math.log2(i + 2)  # i+2 because ranks are 1-based

        ideal_dcg = sum(1 / math.log2(i + 2) for i in range(min(len(ground_truth_pids), k)))
        return dcg / ideal_dcg if ideal_dcg > 0 else 0.0
    

class Evaluator():
    def __init__(self, ground_truth_data, predicted_data):
        '''
        Input: 
            - ground_truth_data: data from the parsed_data_final (for training) 
              or parsed_data_final_test_batch_{1,2,3,4}.json
            - predicted_data: loaded json file with top 10 predicted articles and top 10 snippets
                format of result jsons
                {
                    'data': [
                        {
                            'id': {question id},
                            'question': {question text},
                            'top_10_articles': [
                                {
                                    'pid': article id (URL format),
                                    'title': article title, 
                                    'abstract': article abstract, 
                                    'score': score of bm25 // not mandatory
                                }, 
                                ...
                            ], 
                            "snippets": [
                                {
                                    "beginSection": "title",
                                    "endSection": "title",
                                    "text": "RankMHC",
                                    "document": "http://www.ncbi.nlm.nih.gov/pubmed/39555889",
                                    "offsetInBeginSection": 0,
                                    "offsetInEndSection": 7
                                }, 
                                ...
                            ]
                        },
                    ...
                    ]
                } 
        '''
        self.accuracy = Accuracy()
        self.ground_truth_data = ground_truth_data['data']
        self.predicted_data = predicted_data['data']


    def __get_ground_truth_articles_for_question(self, question):
        return question.get('ground_truth_documents_pid', [])

    def __get_ground_truth_snippets_for_question(self, question):
        return question.get('ground_truth_snippets', [])

    def __get_top_10_articles(self, question):
        return question.get('top_10_articles', [])

    def __get_top_10_snippets(self, question):
        return question.get('snippets', [])
    

    def evaluate_metrics_for_articles(self, k=10):
        mrr_total = 0.0
        map_total = 0.0
        ndcg_total = 0.0
        count = 0


        for gt_question, pred_question in tqdm(zip(self.ground_truth_data, self.predicted_data), desc="Processing questions..."):
            gt_pids = set(self.__get_ground_truth_articles_for_question(gt_question))
            pred_pids = [val['pid'] for val in self.__get_top_10_articles(pred_question)]

            if not gt_pids:
                continue

            mrr_total += self.accuracy.compute_mrr(pred_pids, gt_pids)
            map_total += self.accuracy.compute_average_precision(pred_pids, gt_pids)
            ndcg_total += self.accuracy.compute_ndcg(pred_pids, gt_pids, k=k)
            count += 1

            if count == 0:
                return {'MRR': 0.0, 'MAP': 0.0, f"nDCG@{k}": 0.0}
            
        return {
            "MRR": mrr_total / count,
            "MAP": map_total / count,
            f"nDCG@{k}": ndcg_total / count,
            "count": count
        }