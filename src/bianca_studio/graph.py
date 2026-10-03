"""LangGraph skeleton. Phase 2 fills in nodes; keep this file the single source of flow truth."""
from langgraph.graph import END, StateGraph

from .nodes import approval, assemble, director, producer, qc, strategist, voice
from .state import JobState


def build_graph(checkpointer=None):
    g = StateGraph(JobState)
    g.add_node("strategist", strategist.run)
    g.add_node("pick_angles", approval.pick_angles)          # interrupt
    g.add_node("director", director.run)
    g.add_node("produce_shots", producer.run_all_shots)      # keyframe→video→qc loop per shot
    g.add_node("voice", voice.run)
    g.add_node("assemble", assemble.run)
    g.add_node("final_qc", qc.final)
    g.add_node("human_approval", approval.decide)            # interrupt
    g.add_node("route_rejection", approval.route)

    g.set_entry_point("strategist")
    g.add_edge("strategist", "pick_angles")
    g.add_edge("pick_angles", "director")
    g.add_edge("director", "produce_shots")
    g.add_edge("produce_shots", "voice")
    g.add_edge("voice", "assemble")
    g.add_edge("assemble", "final_qc")
    g.add_conditional_edges("final_qc", qc.final_router, {"pass": "human_approval", "fail": "produce_shots"})
    g.add_edge("human_approval", "route_rejection")
    g.add_conditional_edges("route_rejection", approval.router,
                            {"approved": END, "director": "director", "producer": "produce_shots"})
    return g.compile(checkpointer=checkpointer, interrupt_before=["pick_angles", "human_approval"])
