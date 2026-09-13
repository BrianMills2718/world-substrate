"""Read-only LC relation view for World Substrate semantic bindings."""
from __future__ import annotations
from world_substrate.semantic import SEMANTIC_BINDINGS, SemanticBinding

GRAMMAR_REF="linguistic-core@4801374bbe500d6e60baf34cf21fac3c4aaa4254:relation-schema.v1+relation-assertion-bundle.v1"
SPECS=(
("sense","lc:PredicateSense",1,1),
("participant_profile","ws:ParticipantRoleProfile",1,1),
("specialization","ws:SemanticSpecialization",0,1),
("causal_class","ws:CausalClass",1,1),
("causal_bearer","ws:CausalBearer",0,1),
("mechanic","ws:Mechanic",0,1),
("interpretation_limit","ws:InterpretationLimit",0,None),
)

def schema():
    roles=[]
    for i,(name,typ,lo,hi) in enumerate(SPECS):
        roles.append({"role_definition_id":f"ws.roledef.semantic_binding.{name}","relation_schema_id":"ws:semantic_binding","local_name":name,"grounded_role_id":None,"expected_filler_type":typ,"min_count":lo,"max_count":hi,"presentation_ordinal":i,"constraints":["consumer-owned consequence authority"] if name=="mechanic" else []})
    return {"schema_version":"relation-schema.v1","relation_schema_id":"ws:semantic_binding","owner_namespace":"ws","review_status":"candidate","roles":roles}

def rb(name,ref):
    return {"role_definition_id":f"ws.roledef.semantic_binding.{name}","filler":{"filler_kind":"reference","filler_id":ref}}

def project(binding:SemanticBinding):
    pid=f"ws.profile:{binding.binding_id}"; aid=f"assert:ws.semantic_binding:{binding.binding_id}"
    catalog={pid:{"kind":"participant_profile","roles":dict(binding.roles),"role_definition_ids":None if binding.role_definition_ids is None else dict(binding.role_definition_ids)}}
    bs=[rb("sense",binding.sense_id),rb("participant_profile",pid)]
    if binding.specialization:
        ref=f"ws.specialization:{binding.binding_id}"; catalog[ref]={"kind":"semantic_specialization","text":binding.specialization}; bs.append(rb("specialization",ref))
    ref=f"ws.causal_class:{binding.causal_class}"; catalog[ref]={"kind":"causal_class","value":binding.causal_class}; bs.append(rb("causal_class",ref))
    if binding.causal_bearer:
        ref=f"ws.binding_role:{binding.binding_id}:{binding.causal_bearer}"; catalog[ref]={"kind":"binding_role","role_name":binding.causal_bearer}; bs.append(rb("causal_bearer",ref))
    if binding.mechanic_id: bs.append(rb("mechanic",binding.mechanic_id))
    for i,value in enumerate(binding.interpretation_limits):
        ref=f"ws.interpretation_limit:{binding.binding_id}:{i}"; catalog[ref]={"kind":"interpretation_limit","text":value}; bs.append(rb("interpretation_limit",ref))
    bundle={"schema_version":"relation-assertion-bundle.v1","schemas":[schema()],"assertions":[{"assertion_id":aid,"relation_schema_id":"ws:semantic_binding","bindings":bs}],"top_assertion_id":aid}
    return {"schema_version":"ws-semantic-binding-relation-view.v1","grammar_ref":GRAMMAR_REF,"source_binding_id":binding.binding_id,"read_only":True,"relation_bundle":bundle,"reference_catalog":catalog}

def project_kind(kind:str):
    value=SEMANTIC_BINDINGS.get(kind)
    return None if value is None else project(value)
