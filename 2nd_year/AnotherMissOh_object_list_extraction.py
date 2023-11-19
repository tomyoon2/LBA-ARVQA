import json
import argparse
import torch
import ipdb
import utils
import os
import pickle
import itertools
import copy
import numpy as np
import random
from tqdm import tqdm

import utils_sys
import utils

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer



def build_parser():
	parser = argparse.ArgumentParser(description='object extraction from dramaQA data annotation')

	parser.add_argument('--seed', type=int, default=42)

	parser.add_argument('--run_name', type=str, default='debugging')

	parser.add_argument('--output_dir', type=str, default='./saves/custom_dataset')
	parser.add_argument('--dataset_dir', type=str, default='./dataset')

	parser.add_argument('--world_size', default=1, type=int,
						help='number of distributed processes')
	parser.add_argument('--dist_url', default='env://', help='url used to set up distributed training')	   

	return parser

def main(args):
# ============================================= run name ======================================================
	if args.run_name == 'date':
		args = utils_sys.set_run_name(args)

# ============================================= gpu setting ======================================================
	args = utils_sys.set_gpu(args)

# ============================================= seed setting ======================================================
	if args.seed:
	 	utils_sys.set_seed(args, args.seed)

# ============================================= obejct extraction ======================================================
	
	detection_annotation = utils_sys.read_jsonl(os.path.join(args.dataset_dir, 'DramaQA/AnotherMissOh_Visual_Faster_RCNN_detected.json'))[0]
	scenes = list(detection_annotation.keys())

	train_questions = utils_sys.read_json(os.path.join(args.dataset_dir, 'DramaQA/AnotherMissOhQA_train_set.json'))
	val_questions = utils_sys.read_json(os.path.join(args.dataset_dir, 'DramaQA/AnotherMissOhQA_val_set.json'))
	test_questions = utils_sys.read_json(os.path.join(args.dataset_dir, 'DramaQA/AnotherMissOhQA_test_set.json'))
	questions = train_questions+val_questions+test_questions
	ipdb.set_trace()

	object_list_detected = []
	object_list_extracted = []

	exception_object = ['Haeyoung', 'Jinsang', 'Taejin', 'relationship', 'kind', 'something', 'communication', 'someone', 'everything', 'com', 'color']

	for idx, scene in enumerate(tqdm(scenes)):
		for frame in detection_annotation[scene]:
			objects = frame['objects']
			# ipdb.set_trace()
			for object_item in objects:
				object_ = object_item['object_id']

				if object_ not in object_list_detected:
					object_list_detected.append(object_)

	for idx, question in enumerate(tqdm(questions)):
		try:
			objects_temp = utils.object_extract(question['que'])
		except:
			continue
		for object_, object_idx in objects_temp:
			exception_list = [1 if exception in object_ else 0 for exception in exception_object]
			if sum(exception_list) > 0:
				continue
			if object_.lower().split(' ') not in object_list_extracted:
				object_list_extracted.append(object_.lower().split(' '))


		

	ipdb.set_trace()
	object_list_fname = 'AnotherMissOhQA_object_list.pkl'
	utils_sys.save_pkl(object_list_extracted, os.path.join(args.output_dir, object_list_fname))




	return







if __name__ == "__main__":

	if not torch.cuda.is_available(): #
		print("Need available GPU(s) to run this model...") #
		quit() #

	parser = build_parser()
	args = parser.parse_args()

	main(args)

	ipdb.set_trace()
