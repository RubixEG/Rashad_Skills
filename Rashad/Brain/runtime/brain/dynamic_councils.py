from __future__ import annotations
from .expert_router import route_experts

def compose_dynamic_council(task):
    r=route_experts(task)
    return {
      "status":r.get("status"),"council_type":"DYNAMIC_EXECUTABLE_EXPERT_COUNCIL",
      "purpose":r.get("matched_domains") or ["GENERAL_PURSUIT"],
      "actors":r.get("selected_experts",[]),"actor_count":r.get("selected_count",0),
      "max_actors":r.get("max_active_experts"),"constitutional_councils_replaced":False,
      "execution_required_for_active_claim":True,"selection_reasons":r.get("selection_reasons",{})
    }
