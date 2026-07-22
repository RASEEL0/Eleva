from langgraph.graph import StateGraph, START, END

from .state import CareerState

from .nodes import (
    resume_analysis,
    job_requirements,
    skill_gap,
    match_evaluation,
    application_ready,
    learning_planner
)

builder = StateGraph(CareerState)

builder.add_node("resume_analysis", resume_analysis)
builder.add_node("job_requirements", job_requirements)
builder.add_node("skill_gap", skill_gap)
builder.add_node("match_evaluation", match_evaluation)

builder.add_edge(START, "resume_analysis")
builder.add_edge("resume_analysis", "job_requirements")
builder.add_edge("job_requirements", "skill_gap")
builder.add_edge("skill_gap", "match_evaluation")
builder.add_edge("match_evaluation", END)

graph = builder.compile()




from langgraph.graph import StateGraph, START, END

from graph.state import CareerState

from agents.resume_agent import resume_agent
from agents.job_agent import job_agent
from agents.skill_gap_agent import skill_gap_agent
from agents.learning_agent import learning_agent


def route_after_skill_gap(state: CareerState):

    if state["next_action"] == "APPLICATION_READY":
        return "application_ready"

    return "learning"


def build_graph():

    workflow = StateGraph(CareerState)


    # Add nodes

    workflow.add_node(
        "resume",
        resume_agent
    )

    workflow.add_node(
        "job",
        job_agent
    )

    workflow.add_node(
        "skill_gap",
        skill_gap_agent
    )

    workflow.add_node(
        "learning",
        learning_agent
    )


    # Connect nodes

    workflow.add_edge(
        START,
        "resume"
    )

    workflow.add_edge(
        "resume",
        "job"
    )

    workflow.add_edge(
        "job",
        "skill_gap"
    )


    # Conditional routing

    workflow.add_conditional_edges(
        "skill_gap",
        route_after_skill_gap,
        {
            "learning": "learning",
            "application_ready": END
        }
    )


    workflow.add_edge(
        "learning",
        END
    )


    return workflow.compile()