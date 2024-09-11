import json, csv
from flask import Flask, jsonify, request, render_template
from homeharvest import scrape_property
from datetime import datetime

