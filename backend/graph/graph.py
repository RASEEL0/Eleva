from langgraph.graph import StateGraph, START, END

from .state import CareerState

from .nodes import (
    resume_analysis,
    job_requirements,
    skill_gap,
    match_evaluation,
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