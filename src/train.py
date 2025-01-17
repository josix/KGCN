from typing import List, DefaultDict, Dict
import pickle as pkl
from collections import defaultdict

import tensorflow as tf
import numpy as np
from model import KGCN


def train(args, data, show_loss, show_topk):
    n_user, n_item, n_entity, n_relation = data[0], data[1], data[2], data[3]
    train_data, eval_data, test_data = data[4], data[5], data[6]
    adj_entity, adj_relation = data[7], data[8]

    model = KGCN(args, n_user, n_entity, n_relation, adj_entity, adj_relation)
    K_LIST=[1, 10, 100]
    # top-K evaluation settings
    user_list, train_record, test_record, item_set = topk_settings(
        show_topk,
        train_data,
        test_data,
        n_item,
        user_num=10000,
        )
    group_to_amount = defaultdict(int)
    user_to_group = defaultdict(int)
    user_with_degree = []
    group_to_ratings = defaultdict(list)
    # Export train_record
    # with open('./train_record.pkl', 'wb') as fout:
    #     pkl.dump(train_record, fout)
    for user, records in test_record.items():
        user_with_degree.append((len(records), user))
    total_user = len(user_with_degree)
    user_with_degree.sort()
    lower_bound = 1
    upper_bound = total_user
    groups_num = 10
    interval = int((upper_bound - lower_bound + 1) / groups_num)
    print('min: {} max: {} intaerval: {}'.format(lower_bound, upper_bound, interval))
    group_count = 1
    for i in range(lower_bound, upper_bound, interval):
        if i+interval-1 < len(user_with_degree):
            print("Group {}: degree {} - degree {}".format(group_count, user_with_degree[i-1][0], user_with_degree[i+interval-1][0]))
        else:
            print("Group {}: degree {} - degree {}".format(group_count, user_with_degree[i-1][0], user_with_degree[-1][0]))
        group_count += 1
    def map_group(num):
        group = (num - lower_bound + 1) // interval
        if group < 0:
            return 0
        elif group > groups_num:
            return 99999
        else:
            return group
    for idx, (_, user) in enumerate(user_with_degree):
        group_to_amount[map_group(idx+1)] += 1
        user_to_group[user] = map_group(idx+1)
        group_to_ratings[map_group(idx+1)] += test_record[user]
    with open('../data/{}/group_to_rating.pkl'.format(args.dataset), 'wb') as fout:
        pkl.dump(group_to_ratings, fout)
    with open('../data/{}/group_to_amount_user.pkl'.format(args.dataset), 'wb') as fout:
        pkl.dump(group_to_amount, fout)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for step in range(args.n_epochs):
            # training
            np.random.shuffle(train_data)
            start = 0
            # skip the last incomplete minibatch if its size < batch size
            while start + args.batch_size <= train_data.shape[0]:
                _, loss = model.train(sess, get_feed_dict(model, train_data, start, start + args.batch_size))
                start += args.batch_size
                if show_loss:
                    print(start, loss)

            # CTR evaluation
            train_auc, train_f1 = ctr_eval(sess, model, train_data, args.batch_size)
            eval_auc, eval_f1 = ctr_eval(sess, model, eval_data, args.batch_size)
            test_auc, test_f1 = ctr_eval(sess, model, test_data, args.batch_size)

            print('epoch %d    train auc: %.4f  f1: %.4f    eval auc: %.4f  f1: %.4f    test auc: %.4f  f1: %.4f'
                  % (step, train_auc, train_f1, eval_auc, eval_f1, test_auc, test_f1))
            # top-K evaluation
            if show_topk:
                precision, recall, map_, k_to_f1 = topk_eval(
                    sess, model, user_list, train_record, test_record, item_set, K_LIST, args.batch_size, user_to_group)
                print('precision: ', end='')
                for i in precision:
                    print('%.4f\t' % i, end='')
                print()
                print('recall: ', end='')
                for i in recall:
                    print('%.4f\t' % i, end='')
                print()
                print('MAP: ', end='')
                for i in map_:
                    print('%.4f\t' % i, end='')
                print('\n')
                if step == args.n_epochs - 1:
                    # Export pikle file so as to draw it at laptop
                    with open('../data/{}/k_to_f1_list_user.pkl'.format(args.dataset), 'wb') as fout:
                        pkl.dump(k_to_f1, fout)



def topk_settings(show_topk, train_data, test_data, n_item, user_num=100):
    if show_topk:
        train_record = get_user_record(train_data, True)
        test_record = get_user_record(test_data, False)
        user_list = list(set(train_record.keys()) & set(test_record.keys()))
        if len(user_list) > user_num:
            user_list = np.random.choice(user_list, size=user_num, replace=False)
        item_set = set(list(range(n_item)))
        return user_list, train_record, test_record, item_set
    else:
        return [None] * 5


def get_feed_dict(model, data, start, end):
    feed_dict = {model.user_indices: data[start:end, 0],
                 model.item_indices: data[start:end, 1],
                 model.labels: data[start:end, 2]}
    return feed_dict


def ctr_eval(sess, model, data, batch_size):
    start = 0
    auc_list = []
    f1_list = []
    while start + batch_size <= data.shape[0]:
        auc, f1 = model.eval(sess, get_feed_dict(model, data, start, start + batch_size))
        auc_list.append(auc)
        f1_list.append(f1)
        start += batch_size
    return float(np.mean(auc_list)), float(np.mean(f1_list))

def count_average_precision(predict:List, label:set):
    match = [rec in set(label) for rec in predict]
    average_precision = 0.0
    match_count = 0
    for i, is_matching in enumerate(match):
        if is_matching:
            match_count += 1
            average_precision += match_count / (i + 1)
    return average_precision / len(predict)

count_f1 = lambda p, r: 2 * (p * r / (p + r)) if p + r != 0 else 0

def topk_eval(sess, model, user_list, train_record, test_record, item_set, k_list:list, batch_size, user_to_group):
    precision_list: Dict[int, list] = {k: [] for k in k_list}
    recall_list: Dict[int, list] = {k: [] for k in k_list}
    average_precision_list: Dict[int, list] = {k: [] for k in k_list}
    k_to_group_to_f1: Dict[int, DefaultDict[int, list]] = {k: defaultdict(list) for k in k_list}

    for user in user_list:
        test_item_list = list(item_set - train_record[user])
        item_score_map = dict()
        start = 0
        while start + batch_size <= len(test_item_list):
            items, scores = model.get_scores(sess, {model.user_indices: [user] * batch_size,
                                                    model.item_indices: test_item_list[start:start + batch_size]})
            for item, score in zip(items, scores):
                item_score_map[item] = score
            start += batch_size

        # padding the last incomplete minibatch if exists
        if start < len(test_item_list):
            items, scores = model.get_scores(
                sess, {model.user_indices: [user] * batch_size,
                       model.item_indices: test_item_list[start:] + [test_item_list[-1]] * (
                               batch_size - len(test_item_list) + start)})
            for item, score in zip(items, scores):
                item_score_map[item] = score

        item_score_pair_sorted = sorted(item_score_map.items(), key=lambda x: x[1], reverse=True)
        item_sorted = [i[0] for i in item_score_pair_sorted]

        for k in k_list:
            hit_num = len(set(item_sorted[:k]) & test_record[user])
            precision_list[k].append(hit_num / k)
            recall_list[k].append(hit_num / len(test_record[user]))
            average_precision_list[k].append(count_average_precision(item_sorted[:k], test_record[user]))
            if user_to_group[user] >= 0 and user_to_group[user] != 99999:
                k_to_group_to_f1[k][user_to_group[user]].append(count_f1(precision_list[k][-1], recall_list[k][-1]))

    precision = [np.mean(precision_list[k]) for k in k_list]
    recall = [np.mean(recall_list[k]) for k in k_list]
    map_ = [np.mean(average_precision_list[k]) for k in k_list]
    k_to_f1: Dict[int, list] = {}
    for k in k_list:
        k_to_f1[k] = []
        for group in k_to_group_to_f1[k]:
            k_to_f1[k].append((group, np.mean(k_to_group_to_f1[k][group])))
        k_to_f1[k] = [i[1] for i in sorted(k_to_f1[k])]
    return precision, recall, map_, k_to_f1


def get_user_record(data, is_train):
    user_history_dict = dict()
    for interaction in data:
        user = interaction[0]
        item = interaction[1]
        label = interaction[2]
        if is_train or label == 1:
            if user not in user_history_dict:
                user_history_dict[user] = set()
            user_history_dict[user].add(item)
    return user_history_dict
