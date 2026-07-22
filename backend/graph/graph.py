from langgraph.graph import StateGraph, START, END

from .state import CareerState

from .nodes import (
    resume_analysis,
    job_requirements,
    skill_gap,
    application_agent,
    learning_planner,
    resume_improvement_agent,
    interview_agent
)

builder = StateGraph(CareerState)

# Register Nodes
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
    "application_agent",
    application_agent
)
builder.add_node(
    "resume_improvement_agent",
    resume_improvement_agent
)
builder.add_node(
    "interview_agent",
    interview_agent
)
builder.add_node(
    "learning_planner",
    learning_planner
)

# Main Flow
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


# Decision
def decide_next_step(state: CareerState):
    if state.get("next_action") == "APPLICATION_READY":
        return "application_agent"
    return "learning_planner"


builder.add_conditional_edges(
    "skill_gap",
    decide_next_step,
    {
        "application_agent": "application_agent",
        "learning_planner": "learning_planner",
    },
)

# Application Path (candidate is ready now)
builder.add_edge(
    "application_agent",
    "resume_improvement_agent"
)

# Learning Path (candidate needs skill improvement first) —
# now also continues on to resume improvement + interview prep,
# instead of stopping at END. Every candidate gets these two
# steps regardless of which branch they took.
builder.add_edge(
    "learning_planner",
    "resume_improvement_agent"
)

# Shared tail for both paths
builder.add_edge(
    "resume_improvement_agent",
    "interview_agent"
)
builder.add_edge(
    "interview_agent",
    END
)

# Compile
graph = builder.compile()