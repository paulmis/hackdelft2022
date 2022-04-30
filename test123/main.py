import jsonlines
from trends import trends
from terms import translate


gov = []
with jsonlines.open('data.jl') as reader:
    for obj in reader:
        gov.append(obj)

translate()

trends(gov, "війни", "UA", "Ukrainian")