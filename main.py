from qna.src.analysis import Analysis

qna_data_path = "./qna/data/kg"
question_template_path = "./qna/data/question_templates.csv"
    question = "Designing Destiny was written by?"
# question = "Babuji Lalaji books"
analysis = Analysis(qna_data_path, question_template_path)
#annotations = analysis._annotate_entities(question)
#annotated_question = analysis._substitute_entities(question, annotations)
#print(annotated_question)
ret_str = analysis._execute(question)
print('returned string ->', ret_str)
