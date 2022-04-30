import jsonlines
import pandas as pd
from matplotlib import pyplot as plt

from trends import trends
from terms import terms
import seaborn as sn


gov = []
with jsonlines.open('data.jl') as reader:
    for obj in reader:
        gov.append(obj)

normalized = {}
for entry in terms:
    normalized["asylum " + entry['language'] + " " + entry['nationality']] = \
        trends(gov, 'asylum', entry['language'], entry['asylum'], entry['code'], entry['nationality'])
    normalized["war " + entry['language'] + " " + entry['nationality']] = \
        trends(gov, 'war', entry['language'], entry['war'], entry['code'], entry['nationality'])

print(normalized, sep = "\n")