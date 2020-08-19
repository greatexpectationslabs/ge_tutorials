---
theme: superconductive
footer: '.'
marp: true
---

<style scoped>
	h1 {margin-top: 120px;}
	p {font-size: 0.8em; margin-top:2em;}
</style>

![bg right:40% 80%](img/generic_dickens_protagonist.png)

# Great Expectations 101: Getting Started

**Sam Bail, Superconductive**
**August 2020**

---

## Welcome!

- **Quick intro - who are we?** (5 minutes)
- **Getting started with Great Expectations** (40 minutes)
    - A data horror story
    - How to create and edit Expectation Suites
    - Validating your data
    - Additional features of Great Expectations
    - Wrap-up
- **Q&A session** (15 minutes)

---

## Communication modes

- This will mostly be a presentation style webinar
- Feel free to post questions in the Zoom chat
    - We'll stop after each section to answer them
- We might answer some more in-depth questions via Slack after the webinar!
- We're recording the webinar and content will be made available after
- Our community Code of Conduct also applies to our webinars
- **Please fill in the survey (posted in the Zoom chat) after the session**!

---

## Who are we?

- We're **Superconductive**, the company behind Great Expectations
- Today's team:
    - Sam Bail (@spbail): Technical Lead of the Partnerships team at Superconductive
    - Eugene Mandel (@eugmandel): Head of Product at Superconductive

---

## Let's get started - a Data Horror Story

Let's assume we have an analytics pipeline tracking NYC taxi data...

![width:900px](img/pipeline1.png)

---

## Example: Passenger stats in January

Based on our data, we expect between 1 and 6 passengers per ride

![width:500px](img/passengers1.png)

---

## Example: Passenger stats in Feburary

Something happened this month - we didn't expect 0 passengers?

![width:500px](img/passengers2.png)


---

## Could we prevent such issues?

How can we test the monthly update before it gets to the dashboard?

![width:1000px](img/pipeline2.png)

---

## Data validation with Great Expectations

![width:1100px](img/datadocs1.png)

---

## Data validation with Great Expectations (GE)

![width:1100px](img/datadocs2.png)

---

![bg right:30% 80%](img/generic_dickens_protagonist.png)


## Let's dive into Great Expectations

- How do we set up GE and connect our data?
- How do we create and edit expectations?
- How do we validate our staging data?


![width:450px](img/demotime.png)


---


## What does a typical GE workflow look like?
 
1. Create your expectation suites using the **knowledge** and **data** you have
    a. These are intended to be version controlled
    b. We're working on automatically *"scaffolding"* expectations
2. Whenever your data changes (new batch is ingested, pipelines are modified...), **validate** with the expectation suites
3. Make your pipelines **react** to validation results, e.g.
    a. Halt the pipeline execution and notify stakeholders
    b. Continue the pipeline execution and log results
    

---


## GE in a real-world pipeline
 
![width:1100px](img/ge_architecture.png)


---



![bg right:30% 80%](img/generic_dickens_protagonist.png)


## More powerful features!
 
- **Stores**: Allow you to store expectations in different backends, e.g. in S3, databases, etc.
    - Configurable in `great_expectations.yml`
- **Data docs sites**: Allows you to host data docs as a shared source of truth
    - Configurable in `great_expectations.yml`
- **Built-in profiling**: Automatically create expectations based on the data
    - Try out the `suite scaffold` command
    - We're working a lot on profiling this quarter!
    
    
---


![bg right:30% 80%](img/generic_dickens_protagonist.png)


## Recap and wrap-up
- We've showed you
    - How to create and edit Expectation Suites
    - How to validate your data
    - Additional features of Great Expectations
- Next up: Q&A - **please post your questions in the chat!**


---


## And finally...

- Great Expectations is an open source project - join our community!
    - Check out the docs: link on **greatexpectations.io**
    - Join our Slack channel: link on **greatexpectations.io**
    - Star us on GitHub: link on **greatexpectations.io**
- **Please fill in the survey (posted in the Zoom chat) after the session**!
- **We offer partnerships & consulting services: superconductive.com** 

![width:220px](img/generic_dickens_protagonist.png)
