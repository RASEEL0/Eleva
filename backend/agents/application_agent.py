from graph.state import CareerState


def application_agent(state: CareerState):

    return {
        "status": "Candidate is ready to apply",
        "next_action": "DONE"
    }