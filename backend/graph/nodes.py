from agents.resume_agent import resume_agent
from agents.job_agent import job_agent
from agents.skill_gap_agent import skill_gap_agent
from agents.learning_agent import learning_agent
from agents.application_agent import application_agent


def resume_node(state):
    return resume_agent(state)


def job_node(state):
    return job_agent(state)


def skill_gap_node(state):
    return skill_gap_agent(state)


def learning_node(state):
    return learning_agent(state)


def application_node(state):
    return application_agent(state)