#!/usr/bin/python3

# This file contains the 'script' function to evaluate the performance
# of a file outputted by the parser against manual gold annotation.

NEW_KEYS = [
    'lemmaft_correct',
    'lemmaft_missed',
    'lemmaft_total',
    'nlp_5',
    'nlp_5_correct',
    'nlp_4',
    'nlp_4_correct',
    'nlp_3',
    'nlp_3_correct',
    'nlp_2',
    'nlp_2_correct',
    'nlp_1',
    'nlp_1_correct',
    'nlp_0',
    'nlp_0_correct',
    'obj_acc_correct',
    'obj_acc_missed',
    'obj_acc_total',
    'obj_acc_parser_correct',
    'obj_acc_parser_missed',
    'obj_acc_parser_total',
    'loc_correct',
    'loc_missed',
    'loc_total',
    'loc_parser_correct',
    'loc_parser_missed',
    'loc_parser_total',
    'reflexive_parser_correct',
    'reflexive_parser_missed',
    'reflexive_parser_total',
    'en_clitic_parser_correct',
    'en_clitic_parser_missed',
    'en_clitic_parser_total',
    'hit_correct'
]

def script(annotator, target_lemma=''):
    
    d = annotator.summary # Shortcut...
    hit = annotator.hit
    
    ###################################################################
    # PART 0: Add keys with count 0
    ###################################################################
    
    for key in NEW_KEYS:
        if not key in d:
            d[key] = 0
            
    is_parsed = True if 'loc_parser' in hit.tags else False
    ###################################################################
    # PART 1: Accuracy of lemmatization combined with nlp_score.
    # (Evaluation only)
    ###################################################################
    
    nlp_score = hit.tags.get('nlp_score', '')
    try:
        is_lemma = True if hit.tags['lemma_check'] == 'v' else False
    except:
        print(str(hit.uuid))
        raise
    if target_lemma == hit.tags['lemma_ft']:
        d['lemmaft_total'] += 1
        if is_lemma:
            d['lemmaft_correct'] += 1
    elif is_lemma:
        d['lemmaft_missed'] += 1
    #if is_parsed and target_lemma == hit.tags['lemma_parser']:
    #    d['lemma_parser_total'] += 1
    #    if is_lemma:
    #        d['lemma_parser_correct'] += 1
    #elif is_lemma:
    #    d['lemma_parser_missed'] += 1
        
    if is_lemma: d['hit_correct'] += 1
    
    for i in range(0, 6):
        stri = str(i)
        if stri == str(nlp_score):
            d[f'nlp_{stri}'] += 1
            if is_lemma: d[f'nlp_{stri}_correct'] += 1
    
    hit.tags['lemma'] = target_lemma if is_lemma else '--'
    hit.tags['lemma_variant'] = '1'
    hit.tags['_lemma'] = 'gold'
    hit.tags['_lemma_variant'] = 'auto'
    
    # If the lemma isn't correct, don't do anything further.
    if not is_lemma: 
        for key in ['_obj_acc', '_loc', 'obj_acc_parser_autocheck', 'loc_parser_autocheck']:
            hit.tags[key] = '--'
        return hit
            
    ###################################################################
    # PART 2: Check the direct object and update hit.tags
    ###################################################################
    
    is_obj = True if hit.tags['obj_acc_check'] == 'v' else False
    if hit.tags['obj_acc']:
        d['obj_acc_total'] +=1
        if is_obj:
            d['obj_acc_correct'] += 1
        else:
            hit.tags['obj_acc'] = ''
    elif 'obj_acc_add' in hit.tags and hit.tags['obj_acc_add']:
        d['obj_acc_missed'] += 1
        hit.tags['obj_acc'] = hit.tags['obj_acc_add']
        hit.tags['_obj_acc'] = 'gold'
    
    hit.tags['_obj_acc'] = 'gold'
    
    if is_parsed:
        if hit.tags['obj_acc_parser']:
            d['obj_acc_parser_total'] += 1
            if is_obj or ('obj_acc_add' in hit.tags and hit.tags['obj_acc_add']):
                d['obj_acc_parser_correct'] += 1
                hit.tags['obj_acc_parser_autocheck'] = 'v'
            else:
                hit.tags['obj_acc_parser_autocheck'] = 'x'
        elif is_obj or ('obj_acc_add' in hit.tags and hit.tags['obj_acc_add']):
            d['obj_acc_parser_missed'] += 1
            hit.tags['obj_acc_parser_autocheck'] = 'x'
        else:
            hit.tags['obj_acc_parser_autocheck'] = 'v'
    
    ###################################################################
    # PART 3: Check the loc arguments
    ###################################################################
    
    loc_lemmas = hit.tags['loc_lemma'].split(' | ') if hit.tags['loc_lemma'] else []
    add_lemmas = hit.tags['loc_lemma_add'].split('#') if hit.tags['loc_lemma_add'] not in ['#', ''] else []
    try:
        is_loc_lemma = True if hit.tags['loc_lemma_check'] == 'v' else False
    except:
        print(str(hit.uuid))
        raise
    
    d['loc_total'] += len(loc_lemmas)
    # Case 1. loc_lemma is correct
    if is_loc_lemma:
        d['loc_correct'] += len(loc_lemmas)
        if add_lemmas:
            d['loc_missed'] += len(add_lemmas)
    # Case 2. Nothing found. (NB: nothing cannot be right or wrong)
    elif len(loc_lemmas) == 0:
        d['loc_missed'] += len(add_lemmas)
        if add_lemmas: hit.tags['loc_type'] = 'RECHECK'
    # Case 3. Something found but it's wrong
    elif len(loc_lemmas) == 1:
        loc_lemmas = []
        if add_lemmas:
            d['loc_missed'] += len(add_lemmas)
            hit.tags['loc_type'] = 'RECHECK'
        else:
            hit.tags['loc_type'] = ''
    # Case 4: Multiple things found but at least one is wrong
    else:
        # loc_lemmas > 1, not correct
        hit.tags['loc_type'] = 'RECHECK'
        l = [True] * len(loc_lemmas)
        for add_lemma in add_lemmas[:]:
            if add_lemma.isdigit():
                add_lemmas.remove(add_lemma)
                if int(add_lemma) <= len(l):
                    # Remember to subtract 1 to get an index (digits count 1, 2, etc.)
                    l[int(add_lemma) - 1] = False
            else:
                d['loc_missed'] += 1
        for keep, loc_lemma in zip(l, loc_lemmas[:]):
            if keep:
                d['loc_correct'] += 1
            else:
                loc_lemmas.remove(loc_lemma)
    l = loc_lemmas + add_lemmas
    l.sort()
    hit.tags['loc_lemma'] = ' | '.join(l)
    hit.tags['_loc'] = 'gold'
    
    #################################################################
    # Check parser loc output. Not perfect, won't detect two
    # identical heads, but this is pretty rare.
    #################################################################
    if is_parsed:
        real_locs = set(l)
        s = hit.tags['loc_lemma_parser']
        parser_locs = set(s.split(' | ') if s else [])
        d['loc_parser_total'] += len(parser_locs)
        d['loc_parser_correct'] += len(real_locs.intersection(parser_locs))
        d['loc_parser_missed'] += len(real_locs.difference(parser_locs))
        if real_locs == parser_locs:
            hit.tags['loc_parser_autocheck'] = 'v'
        elif real_locs or parser_locs:
            hit.tags['loc_parser_autocheck'] = 'x'
        else:
            hit.tags['loc_parser_autocheck'] = l.extend(s)
            
    ##################################################################
    # PART 4: Reflexives and en clitics (parser output only)
    ##################################################################
    
    if is_parsed:
        if hit.tags['reflexive_parser'] == 'yes':
            d['reflexive_parser_total'] += 1
            if hit.tags['reflexive'] == 'yes':
                d['reflexive_parser_correct'] += 1
        elif hit.tags['reflexive'] == 'yes':
            d['reflexive_parser_missed'] += 1
            
        if hit.tags['en_clitic_parser'] == 'yes':
            d['en_clitic_parser_total'] += 1
            if hit.tags['en_clitic'] == 'yes':
                d['en_clitic_parser_correct'] += 1
        elif hit.tags['en_clitic'] == 'yes':
            d['en_clitic_parser_missed'] += 1
                    
 
