# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 21:56:04 2019

@author: Kranti Kumar
"""
from qna.src.analysis import Analysis

qna_data_path = "./qna/data/kg"
question_template_path = "./qna/data/question_templates.csv"
question = "Who is the author of Reality at Dawn"
analysis = Analysis(qna_data_path, question_template_path)
#annotations = analysis._annotate_entities(question)
#annotated_question = analysis._substitute_entities(question, annotations)
#print(annotated_question)
analysis._execute(question)
