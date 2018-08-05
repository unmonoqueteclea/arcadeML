# -*- coding: utf-8 -*-
'''
title           :ML_engines.py
description     :Methods for applying Machine Learning algorithms to games
author          :Pablo Gonzalez Carrizo (unmonoqueteclea)
date            :20180803
notes           :
python_version  :3.6
''' 

from bigml.api import BigML
from bigml.deepnet import Deepnet
import config
from config import util


def createPongDataset(type=util.ML_BIGML):
    if type == util.ML_BIGML:
        api = BigML(config.BIGML_USER, config.BIGML_API_KEY)
        # Initialize BigML
        print("Creating source...")
        source = api.create_source('train_pong.csv', args={"name": "Pong Data"})
        api.ok(source)
        # Change "movement" field type to Categorical
        changes = {"fields": {"000004": {"optype": "categorical"}}}
        api.update_source(source, changes)
        api.ok(source)
        print("Creating dataset...")
        dataset = api.create_dataset(source, args={"name": "Pong Data"})
        api.ok(dataset)
    return dataset


def createRacingDataset(type=util.ML_BIGML):
    if type == util.ML_BIGML:
        api = BigML(config.BIGML_USER, config.BIGML_API_KEY)
        # Initialize BigML
        print("Creating source...")
        source = api.create_source(
            'train_racing.csv',
            args={"name": "Racing Data"})
        api.ok(source)
        # Changes "movement" field type to categorical
        changes = {"fields": {"000005": {"optype": "categorical"}}}
        api.update_source(source, changes)
        api.ok(source)
        print("Creating dataset...")
        dataset = api.create_dataset(source, args={"name": "Racing Data"})
        api.ok(dataset)
    return dataset


def createPongModel(dataset, type=util.ML_BIGML):
    if type == util.ML_BIGML:
        api = BigML(config.BIGML_USER, config.BIGML_API_KEY)
        print("Creating model...")
        args = {"name": "Pong Model", "objective_field": "Movement"}
        model = api.create_deepnet(dataset, args)
        api.ok(model)
        resource = model["resource"]
        # Saves model id to a file
        file = open("saved_models.txt", "a+")
        file.write(f"\npong-{resource}")
        file.close()
        # Creates LOCAL model
        model = Deepnet(resource, api)
    return model


def createRacingModel(dataset, type=util.ML_BIGML):
    if type == util.ML_BIGML:
        api = BigML(config.BIGML_USER, config.BIGML_API_KEY)
        print("Creating model...")
        args = {"name": "Racing Model", "objective_field": "Movement"}
        model = api.create_deepnet(dataset, args)
        api.ok(model)
        resource = model["resource"]
        # Saves model id to a file
        file = open("saved_models.txt", "a+")
        file.write(f"\nracing-{resource}")
        file.close()
        # Creates LOCAL model
        model = Deepnet(resource, api)
    return model


def predict(model, data, type):
    # Makes a prediction based on current data
    if type == util.ML_BIGML:
        movement = model.predict(data, full=True)
        return movement["prediction"]


def modelFromID(resource, type=util.ML_BIGML):
    # Creates a local model based on a model id
    if type == util.ML_BIGML:
        api = BigML(config.BIGML_USER, config.BIGML_API_KEY)
        model = Deepnet(resource, api)
    return model


def get_model(game):
    # Returns a LOCAL model from a model ID in a text file
    model = None
    try:
        with open("saved_models.txt") as f:
            data = f.readlines()
            models = [
                item.split("-")[1] 
                for item in data if item.split("-")[0] == game]
            model = models[-1]
            model = modelFromID(model, config.ENGINE)
    except:
        print(f"No saved {game} models")
    return model
