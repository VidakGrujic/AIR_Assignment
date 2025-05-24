import json
import math 
from tqdm import tqdm
import re

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
    
    def compute_gmap(self, average_precisions, epsilon=1e-6):
            """
            GMAP = geometric mean of (AP + ε)
            """
            if not average_precisions:
                return 0.0
            log_sum = sum(math.log(ap + epsilon) for ap in average_precisions)
            return math.exp(log_sum / len(average_precisions))

    def compute_precision_recall_f1(self, predicted_pids, ground_truth_pids):
        """
        Computes unordered Precision, Recall, and F1 for articles
        """
        pred_set = set(predicted_pids)
        gold_set = set(ground_truth_pids)

        tp = len(pred_set & gold_set)
        fp = len(pred_set - gold_set)
        fn = len(gold_set - pred_set)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        return precision, recall, f1



######### Snippets Metrices #############
    
    def normalize_text(self, text):
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces
        return text

    def get_snippet_texts(self, snippets):
        return set(self.normalize_text(snip['text']) for snip in snippets)


    def compute_snippet_overlap_metrics(self, predicted_snippets, ground_truth_snippets):
        """
        Computes P_snip, R_snip, F1_snip using exact normalized snippet text match
        """
        S = self.get_snippet_texts(predicted_snippets)
        G = self.get_snippet_texts(ground_truth_snippets)

        if not S or not G:
            return 0.0, 0.0, 0.0

        intersection = S & G
        precision = len(intersection) / len(S)
        recall = len(intersection) / len(G)
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        return precision, recall, f1

    def compute_snippet_average_precision(self, predicted_snippets, ground_truth_snippets):
        """
        Computes Average Precision (AP) for snippets using exact text match
        """
        G = self.get_snippet_texts(ground_truth_snippets)
        if not G:
            return 0.0

        hits = 0
        score = 0.0
        seen = set()

        for i, snip in enumerate(predicted_snippets):
            snip_text = self.normalize_text(snip['text'])
            if snip_text in G and snip_text not in seen:
                hits += 1
                score += hits / (i + 1)
                seen.add(snip_text)

        return score / min(len(G), 10) if hits > 0 else 0.0



    def compute_snippet_gmap(self, average_precisions, epsilon=1e-6):
        """
        GMAP = geometric mean of (AP + epsilon)
        """
        if not average_precisions:
            return 0.0

        log_sum = sum(math.log(ap + epsilon) for ap in average_precisions)
        return math.exp(log_sum / len(average_precisions))


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
        precision_total = 0.0
        recall_total = 0.0
        f1_total = 0.0    
        count = 0
        ap_list = []

        for gt_question, pred_question in tqdm(zip(self.ground_truth_data, self.predicted_data), desc="Processing questions..."):
            gt_pids = set(self.__get_ground_truth_articles_for_question(gt_question))
            pred_pids = [val['pid'] for val in self.__get_top_10_articles(pred_question)]

            if not gt_pids:
                continue


            mrr_total += self.accuracy.compute_mrr(pred_pids, gt_pids)
            ap = self.accuracy.compute_average_precision(pred_pids, gt_pids)
            map_total += ap
            ap_list.append(ap)
            ndcg_total += self.accuracy.compute_ndcg(pred_pids, gt_pids, k=k)
            precision, recall, f1 = self.accuracy.compute_precision_recall_f1(pred_pids, gt_pids)
            precision_total += precision
            recall_total += recall
            f1_total += f1


            count += 1

            if count == 0:
                return {
                    "MRR": 0.0,
                    "MAP": 0.0,
                    f"nDCG@{k}": 0.0,
                    "P_article": 0.0,
                    "R_article": 0.0,
                    "F1_article": 0.0,
                    "GMAP": 0.0,
                    "count": 0
                }

        return {
            "MRR": mrr_total / count,
            "MAP": map_total / count,
            f"nDCG@{k}": ndcg_total / count,
            "P_article": precision_total / count,
            "R_article": recall_total / count,
            "F1_article": f1_total / count,
            "GMAP": self.accuracy.compute_gmap(ap_list),
            "count": count
        }


    def evaluate_metrics_for_snippets(self):
        total_precision = 0.0
        total_recall = 0.0
        total_f1 = 0.0
        ap_list = []
        count = 0

        for gt_question, pred_question in tqdm(zip(self.ground_truth_data, self.predicted_data), desc="Evaluating snippets..."):
            gt_snippets = self.__get_ground_truth_snippets_for_question(gt_question)
            pred_snippets = self.__get_top_10_snippets(pred_question)

            if not gt_snippets:
                continue

            # Compute P, R, F1
            p, r, f1 = self.accuracy.compute_snippet_overlap_metrics(pred_snippets, gt_snippets)
            total_precision += p
            total_recall += r
            total_f1 += f1

            # Compute AP for MAP and GMAP
            ap = self.accuracy.compute_snippet_average_precision(pred_snippets, gt_snippets)
            ap_list.append(ap)

            count += 1

        if count == 0:
            return {
                'P_snip': 0.0,
                'R_snip': 0.0,
                'F1_snip': 0.0,
                'MAP_snip': 0.0,
                'GMAP_snip': 0.0,
                'count': 0
            }

        return {
            'P_snip': total_precision / count ,
            'R_snip': total_recall / count,
            'F1_snip': total_f1 / count,
            'MAP_snip': sum(ap_list) / count,
            'GMAP_snip': self.accuracy.compute_snippet_gmap(ap_list),
            'count': count
        }


    def print_results(self, results):
        for key, value in results.items():
            if key != 'count':
                print(f"{key}: {round(value * 100, 2)}")

    