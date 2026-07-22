from agents.resume_agent import resume_agent
from agents.job_agent import job_agent
from agents.skill_gap_agent import skill_gap_agent
from agents.learning_agent import learning_agent
# from agents.application_agent import application_agent
# from agents.resume_improvement_agent import resume_improvement_agent
# from agents.interview_agent import interview_agent


def resume_analysis(state):
    return resume_agent(state)


def job_requirements(state):
    return job_agent(state)


def skill_gap(state):
    return skill_gap_agent(state)


def learning_planner(state):
    return learning_agent(state)


# def application_ready(state):
#     return application_agent(state)


# def resume_improvement(state):
#     return resume_improvement_agent(state)


# def interview_preparation(state):
#     return interview_agent(state)