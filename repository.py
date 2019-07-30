#!/usr/bin/env python3

import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_database = mongo_client["checker"]
collection = mongo_database["git_repos"]


def get_all():
    return collection.find()


def branch_exists(repo, branch_name):
    result = bool(collection.count_documents({"repo": repo, "branch": branch_name}))
    return result


def delete_by_repo(repo_name):
    query = {"repo": repo_name}
    collection.delete_many(query)
    return


def update_record(repo_name, branch_name, test_suite, passed):
    query = {"repo": repo_name, "branch": branch_name}
    collection.update_one(query, {"$set": {test_suite: passed}})
    return


def delete_by_branch(branch_name):
    query = {"branch": branch_name}
    collection.delete_many(query)
    return


def add(repo_name, branch_name):
    record = {'repo': repo_name, "branch": branch_name, 'local_tested': False, 'bas_it_tested': False, 'ui_tested': False,
              'perf_tested': False}
    collection.insert_one(record)
    return
