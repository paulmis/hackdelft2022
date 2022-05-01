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

normalized = []
for entry in terms:
    normalized.append([["asylum " + entry['language'] + " " + entry['nationality']],
                       trends(gov, 'asylum', entry['language'], entry['asylum'], entry['code'], entry['nationality'])])
    normalized.append([["war " + entry['language'] + " " + entry['nationality']],
                       trends(gov, 'war', entry['language'], entry['war'], entry['code'], entry['nationality'])])
    if 'netherlands' in entry:
        normalized.append([["netherlands " + entry['language'] + " " + entry['nationality']],
                           trends(gov, 'netherlands', entry['language'], entry['netherlands'], entry['code'],
                                  entry['nationality'])])
    if 'taliban' in entry:
        normalized.append([["taliban " + entry['language'] + " " + entry['nationality']],
                           trends(gov, 'taliban', entry['language'], entry['taliban'], entry['code'],
                                  entry['nationality'])])

normalized.sort(key=lambda e: e[1])
[print(entry) for entry in normalized]
