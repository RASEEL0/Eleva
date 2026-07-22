from langgraph.graph import StateGraph, START, END

from .state import CareerState

from .nodes import (
    resume_analysis,
    job_requirements,
    skill_gap,
    application_ready,
    learning_planner
)


builder = StateGraph(CareerState)


# Nodes

builder.add_node(
    "resume_analysis",
    resume_analysis
)

builder.add_node(
    "job_requirements",
    job_requirements
)

builder.add_node(
    "skill_gap",
    skill_gap
)

builder.add_node(
    "application_ready",
    application_ready
)

builder.add_node(
    "learning_planner",
    learning_planner
)


# Main flow

builder.add_edge(
    START,
    "resume_analysis"
)

builder.add_edge(
    "resume_analysis",
    "job_requirements"
)

builder.add_edge(
    "job_requirements",
    "skill_gap"
)
def decide_next_step(state: CareerState):

    if state["next_action"] == "APPLICATION_READY":
        return "application_ready"

    return "learning_planner"

builder.add_conditional_edges(
    "skill_gap",
    decide_next_step,
    {
        "application_ready": "application_ready",
        "learning_planner": "learning_planner"
    }
)
builder.add_edge(
    "application_ready",
    END
)


builder.add_edge(
    "learning_planner",
    END
)


graph = builder.compile()
