# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 17:23:29 2019

@author: Kranti Kumar
"""
from qna.src.knowledge import KG

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
        qdf = qdf.set_index('Question')

        # replace ? -> lower question -> replace
        for idx, row in qdf.iterrows():
            idx = idx.replace('?', '')
            self.question_templates[idx.lower()] = [idx, row['Parse'], row['Answer']]

    def _preprocess_question(self, question):
        return question.lower().replace('?', '')


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
        entity_types = []
        for annotation in annotations:
            for i in range(len(question)):
                if i >= annotation[0] and i < annotation[1]:
                    if i == annotation[0]:
                        if with_type:
                            entity_type = '_'+self.get_id_to_type(annotation[2])
                            annotated_question.append(entity_type)
                            entity_types.append(entity_type)
                        else:
                            annotated_question.append(annotation[2])
                else:
                    annotated_question.append(question[i])

        return ' '.join(annotated_question), entity_types

    def _match_template_question(self, question):
        return self.question_templates.get(question)

    def _parse_question(self, annotation, parse):
        # assuming we have one annotation to subsitute
        # return Answer
        parse = parse.split('|')
        print(self.id_to_predicate)
        if parse[0].startswith('predicate'):
            print(annotation[2], parse[2])
            predicate = parse[2]+'_'+parse[3]
            print(predicate)
            print(annotation[2])
            output = self.get_id_to_predicate(annotation[2], predicate)

            # so output should be a list of attributes of typoe parse[3]
            # lets perform type checking
            for item in output:
                assert self.get_id_to_type(item) == parse[3]
            output = ', '.join([self.get_id_to_name(item) for item in output])

            return '_'+parse[3], output

    def _fill_answer_template(self, io, answer_template):
        for item in io:
            answer_template = answer_template.replace(item[0], item[1])
        return answer_template


    def _execute(self, question):
        preprocessed_question = self._preprocess_question(question) # question mark removal can make problem in future
        annotations = self._annotate_entities(question)
        parsed_question, entity_types = self._substitute_entities(preprocessed_question, annotations, with_type=True)

        question_template, parse, answer_template = self._match_template_question(parsed_question.lower())

        outputs = self._parse_question(annotations[0], parse) # output -> tuple

        inputs = [(entity_type, ''.join(self.get_id_to_name(annotation[2]))) for annotation, entity_type in zip(annotations, entity_types)]
        print("inputs")
        print(inputs)
        print("outputs")
        print(outputs)

        # io = inputs.extend(outputs)
        inputs.append(outputs)
        print(inputs)
        answer = self._fill_answer_template(inputs, answer_template)
        print(answer)
        # print(parsed_question)
        # print(question_template, parse, answer_template)


        
        
if __name__ == '__main__':
    qna_data_path = "../../data/kg"
    question_template_path = "../../data/question_templates.csv"
    question = "Who is the author of Reality at Dawn"
    analysis = Analysis(qna_data_path, question_template_path)
    #annotations = analysis._annotate_entities(question)
    #annotated_question = analysis._substitute_entities(question, annotations)
    #print(annotated_question)
    analysis._execute(question)
