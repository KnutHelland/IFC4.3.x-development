import os
import re
import sys
import operator
import itertools

import tabulate

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import express_parser
import nodes

fn1, fn2, output = sys.argv[1:]

print("Running difference", *sys.argv[1:])

schema_name_re = re.compile(r"ifc4x3_rc\d")

def eq(a, b):
    if (type(a) != type(b)):
        return False
    elif isinstance(a, (nodes.StringType, nodes.AggregationType, nodes.BinaryType, str, nodes.ExplicitAttribute, nodes.InverseAttribute, nodes.SimpleType)):
        return str(a) == str(b)
    elif isinstance(a, (nodes.SelectType, nodes.EnumerationType)):
        return set(map(str, a.values)) == set(map(str, b.values))
    else:
        # @todo
        import pdb; pdb.set_trace()
        
def format(a):
    if isinstance(a, (nodes.SelectType, nodes.EnumerationType)):
        return ", ".join(sorted(map(str, a.values)))
    else:
        return str(a)

def compare(fn1, fn2, m1, m2):
    s1, s2 = m1.schema, m2.schema
    
    for nm in sorted(set(s1.keys) - set(s2.keys)):
        yield "MISSING", (nm, "", "not in '%s'" % os.path.basename(fn2))
        
    for nm in sorted(set(s2.keys) - set(s1.keys)):
        yield "MISSING", (nm, "not in '%s'" % os.path.basename(fn1), "")
        
    for x in 'simpletypes', 'selects', 'enumerations':
        d1, d2 = map(operator.attrgetter(x), (s1, s2))
        for nm in sorted(d1.keys() & d2.keys()):
            if not eq(d1[nm], d2[nm]):
                yield "TYPE", (nm, d1[nm], d2[nm])
            if x == 'simpletypes':
                d1_wns = [a[0] for a in s1.types[nm].where]
                d2_wns = [a[0] for a in s2.types[nm].where]
                if d1_wns != d2_wns:
                    yield "WHERE", (nm + " where rules", d1_wns, d2_wns)
                for wnm in (set(d1_wns) & set(d2_wns)):
                    w1 = dict(s1.types[nm].where)[wnm]
                    w2 = dict(s2.types[nm].where)[wnm]
                    if w1 != w2:
                        yield "WHERE", (nm + "." + wnm, w1, w2)
            
    for e in sorted(s1.entities.keys() & s2.entities.keys()):
        e1, e2 = s1.entities[e], s2.entities[e]
        if e1.abstract != e2.abstract:
            yield "ENTITY", (e, ["not abstract", "abstract"][e1.abstract], ["not abstract", "abstract"][e2.abstract])
        if e1.supertypes != e2.supertypes:
            yield "ENTITY", (e + " supertype", e1.supertypes, e2.supertypes)
            
        e1_anames = [attr.name for attr in e1.attributes]
        e2_anames = [attr.name for attr in e2.attributes]
        if e1_anames != e2_anames:
            yield "ENTITY", (e + " attributes", e1_anames, e2_anames)
        e1_anames = {attr.name:attr for attr in e1.attributes}
        e2_anames = {attr.name:attr for attr in e2.attributes}
        for nm in e1_anames.keys() & e2_anames.keys():
            if not eq(e1_anames[nm], e2_anames[nm]):
                yield "ENTITY", (e + "." + nm, e1_anames[nm], e2_anames[nm])
                
        e1_anames = [attr.name for attr in (e1.inverse or [])]
        e2_anames = [attr.name for attr in (e2.inverse or [])]
        if e1_anames != e2_anames:
            yield "ENTITY", (e + " inverses", e1_anames, e2_anames)
        e1_anames = {attr.name:attr for attr in (e1.inverse or [])}
        e2_anames = {attr.name:attr for attr in (e2.inverse or [])}
        for nm in e1_anames.keys() & e2_anames.keys():
            if not eq(e1_anames[nm], e2_anames[nm]):
                yield "ENTITY", (e + "." + nm, e1_anames[nm], e2_anames[nm])
        
        for constraint in ("where", "unique", "derive"):            
            cv1 = getattr(s1.entities[e], constraint)
            cv2 = getattr(s2.entities[e], constraint)
            d1_wns = [a[0] for a in cv1]
            d2_wns = [a[0] for a in cv2]
            if d1_wns != d2_wns:
                yield "WHERE", (e + " " + constraint +  " rules", d1_wns, d2_wns)
            for wnm in (set(d1_wns) & set(d2_wns)):
                w1 = dict(cv1)[wnm]
                w2 = dict(cv2)[wnm]
                                
                # replace schema names              
                w1 = schema_name_re.sub("ifc4x3_dev", w1)
                w2 = schema_name_re.sub("ifc4x3_dev", w2)
                
                if w1 != w2:
                    yield "WHERE", (e + "." + wnm, w1, w2)
        
with open(output, "w") as f:
    all_items = sorted(
        ((typ, [format(x) for x in tup]) for typ, tup in compare(fn1, fn2, *map(express_parser.parse, (fn1, fn2)))),
        key=operator.itemgetter(0)
    )
    print("# Express schema differences\n", file=f)
    print(len(all_items), "items\n", file=f)
    
    for key, key_items in itertools.groupby(all_items, operator.itemgetter(0)):
        items = list(map(operator.itemgetter(1), key_items))
        print("### %s\n" % (key[0]+key[1:].lower()), file=f)
        print(len(items), "items\n", file=f)
        print(tabulate.tabulate(items, headers=["Name", os.path.basename(fn1), os.path.basename(fn2)], tablefmt="github"), file=f)
