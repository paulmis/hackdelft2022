# About

This repository contains a robust statistical model for predicting asylum application trends with social media, in particular using Google Trends. Built in 24 hours, it won the HackDelft 2022 hackathon challenge from the Dutch ministry of justice and service's IND (Immigratie en Naturalisatiedienst). 

## Explanation
IND has asked us to design a system that could help predict short-term changes in the quantity of asylum applications. At the time the asylum application processing team would often be either understaffed or overstaffed due to sharp changes in demand, leading to high costs and frequent delays. 

Our system uses localized search data to determine the sentiment of potential asylum seekers. We take advantage of the following propositions:
1. Indication of interest in applying for an aslym preceeds the actual application, usually on the order of weeks
2. Asylum applications are made predominantly due to major geopolitical events (e.g. wars, regime changes, food supply instabilities)
3. Each shelter country has a unique distribution (profile) of application sources determined by its geography, culture, and complex socioeconomic factors
4. The application trendline will often have a significant seasonal variability

To understand how our solutions works we will explain each of the propositions and put them together to picture the final system.
