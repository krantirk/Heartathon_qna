# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 11:39:51 2019

@author: Kranti Kumar
"""

import pandas as pd
import sys
import os
import logging

   
class KG:
      def __init__(self, qna_data_path):

          self.qna_data_path = qna_data_path
          self.name_to_id = {}
          self.id_to_name = {}
          self.type_to_id ={}
          self.id_to_type = {}
          self.id_to_attribute ={}
          self.id_to_predicate ={}
          self.init_kg()

      def ingest_names_and_types(self, root, files, entities):
          
          if 'names.txt' in files:
              for ent in entities:
                  if ent in root:
                      entity = ent
                      break
              df_names = pd.read_csv(os.path.join(root, 'names.txt'), sep=',', names=['id', 'name'])
              df_names = df_names.set_index(['id'])
              names_conv_to_list = lambda x: x.split('|')
              df_names['name'] = df_names['name'].apply(names_conv_to_list)
              
              self.type_to_id[entity] = []  
              for idx, row in df_names.iterrows():                          
                  self.id_to_name[idx] = row['name']
                  self.type_to_id[entity].append(idx)
                  self.id_to_type[idx] = entity
                  
                  for name in row['name']:
                      self.name_to_id[name] = idx
                      
      def ingest_attributes(self, root, attribute_files):
          
          for attribute_file in attribute_files:
              attribute = attribute_file[10:-4]
              df_attribute = pd.read_csv(os.path.join(root, attribute_file), sep=',', names=['id', 'attribute'])
              df_attribute = df_attribute.set_index('id')
              for idx, row in df_attribute.iterrows():
                  if not self.id_to_attribute.get(idx): self.id_to_attribute[idx] = {}
                  self.id_to_attribute[idx][attribute] = row["attribute"]
                  
      def ingest_predicates(self, root, predicate_files):
         
          for predicate_file in predicate_files:
                  predicate = predicate_file[10:-4]
                  df_predicate = pd.read_csv(os.path.join(root, predicate_file), sep=',', names=['id', 'predicate'])
                  df_predicate = df_predicate.set_index('id')
                  for idx, row in df_predicate.iterrows():
                      if not self.id_to_predicate.get(idx): self.id_to_predicate[idx] = {}
                      self.id_to_predicate[idx][predicate] = row["predicate"]

      def init_kg(self):
          
          for root, dirs, files in os.walk(self.qna_data_path):
              if files == []:
                  entities = dirs 
              if dirs == []:
                  self.ingest_names_and_types(root, files, entities)
                  attribute_files = [file for file in files if file.startswith('attribute')]
                  predicate_files = [file for file in files if file.startswith('predicate')]
                  self.ingest_attributes(root, attribute_files)
                  self.ingest_predicates(root, predicate_files)
            
      def show_output(self):          
          print()
          print(self.type_to_id, self.id_to_type)
          print("\n\nAttributes Ingested\n\n")
          print(self.id_to_attribute)
          print("\n\nPredicates Ingested\n\n")
          print(self.id_to_predicate)
##########Initialised the Knowledge Graph  ###################################################################
                    
      def get_id_to_name(self, idx):
          return self.id_to_name.get(idx)
               
      def get_name_to_id(self,name):
          return self.name_to_id.get(name)
      
      def get_id_to_type(self,idx):
          return self.id_to_type.get(idx)
      
      def get_type_to_id(self,entity):
          return self.type_to_id.get(entity)
      
      def get_id_to_attribute(self,attribute):
          return self.id_to_attribute.get(attribute)
          
      def get_id_to_predicate(self,predicate):
          return self.id_to_predicate.get(predicate)


                          
if __name__ == '__main__':
    qna_data_path = "C:/Users/Kranti Kumar/heartathon/qna/data/kg"
    KG = KG(qna_data_path)
    KG.show_output()
