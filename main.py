"""There will be flask api for this app"""
import os
import configparser

from flask import Flask, jsonify, request, url_for, redirect, make_response, render_template

#########################################################
# The import can be changed regarding the implementation
#########################################################
from postgres.warehouse.warehouse import Warehouse
from postgres.warehouse.box import Box

app = Flask(__name__)
box_id_counter = 0
storage = Warehouse(1000)

"""This part is only an example that it is possible to do it for all classes."""


@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify({"status": 200})


@app.route("/barrel", methods=["GET", "POST"])
def index():
    return jsonify({"status": 200})


@app.route("/package", methods=["GET", "POST"])
def index():
    return jsonify({"status": 200})


"""This part shows possibility to create new Box by endpoint /box  
and then check that the warehouse capacity has been changed. It can be verified in endpoint /warehouse."""


@app.route("/box", methods=["GET", "POST"])
def index():
    global box_id_counter

    box = Box(box_id_counter, 1, 2, 3)
    box_id_counter += 1
    storage.put(box)
    return jsonify({"id": box.id,
                    "height": box.height,
                    "width": box.width,
                    "depth": box.depth,
                    "capacity": box.capacity()})


@app.route("/warehouse", methods=["GET", "POST"])
def index():
    return jsonify({"capacity": storage.get_current_capacity(), "number_of_items": storage.get_number_of_items_in_storage(), })
