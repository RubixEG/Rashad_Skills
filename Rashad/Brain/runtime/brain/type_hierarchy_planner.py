from __future__ import annotations

def resolve_type_hierarchy(language='AR',dense=False):
    fam='Montserrat Arabic' if str(language).upper().startswith('AR') else 'Montserrat'
    return {'font_family':fam,'levels':[{'role':'TITLE','px':44 if dense else 48},{'role':'THESIS','px':28 if dense else 32},{'role':'BODY','px':19 if dense else 21},{'role':'SOURCE','px':12 if dense else 13}],'min_distinct_levels':3}
