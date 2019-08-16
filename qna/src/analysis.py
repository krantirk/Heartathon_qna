# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 17:23:29 2019

@author: Kranti Kumar
"""
from src.knowledge import KG

import pandas as pd

class Analysis(KG):
    
    def __init__(self, qna_data_path, question_template_path, ngram_cnt=10):
        self.ngram_cnt = ngram_cnt
        self.question_templates_path = question_template_path
        self.question_templates = {}
        self.post_init()
        super().__init__(qna_data_path)
    
    def post_init(self):
        qdf = pd.read_csv(self.question_templates_path)
        qdf = qdf.set_index('question')
        for idx, row in qdf.iterrows():
            self.question_templates[idx] = [row['Parse'], row['Answer']]

    
    def _annotate_entities(self, question):
        # lower and load all entities
        annotations = []
        question = question.split(' ')
        for i, word in enumerate(question):
            for j in range(self.ngram_cnt):
                if j > len(question): break
                candidate = ' '.join(question[i:j])
                # look for this candidate in our DB
                ret_id = self.get_name_to_id(candidate)
                if ret_id:
                    annotations.append((i, j, ret_id))
        return annotations
    
    def _substitute_entities(self, question, annotations, with_type=False):
        question = question.split(' ')
        annotated_question = []
        for annotation in annotations:
            for i in range(len(question)):
                if i >= annotation[0] and i < annotation[1]:
                    if i == annotation[0]:
                        if with_type:
                            annotated_question.append(self.get_id_to_type(annotation[2]))
                        annotated_question.append(annotation[2])
                else:
                    annotated_question.append(question[i])

        return ' '.join(annotated_question)
    
    def _execute(self, question):
        annotations = self._annotate_entities(question)
        parsed_question = self._substitute_entities(question, annotations, with_type=True)
        print(parsed_question)
        
        
        