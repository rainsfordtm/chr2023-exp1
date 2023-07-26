#!/usr/bin/python3

# This file contains the 'script' function to generate the data
# required for the MVIC from FRANTEXT data re-parsed with a parser.

import re, sys

LOCTS = {
    # Particles
    'ens': 'en[sz]', # REVISED FT
    'fors': '[fh]ors', # REVISED FT
    'sus': 's(us|uz|os)', # REVISED FT
    'jus': 'ju[sz]', # REVISED FT
    'avant': 'ad?[uv]ant', # REVISED FT
    'arrière': 'arr?i[eéè]re?s?', # REVISED FT
    'amont': 'amont', # REVISED FT
    'aval': 'aval', # REVISED FT
    'contremont': 'contre-?mont', # REVISED FT
    'contreval': 'contre-?val', # REVISED FT
    # Ps
    'contre3': r"contr['e]?", # REVISED FT
    'deçà': 'd[ée][çc][aà]', # NEW FT
    'delà': 'd[eé]l[aà]', # NEW FT
    'delez': 'del[eé][sz]', # REVISED FT
    'dedans': r'd[eé]d[ae]n[sz]', # REVISED FT
    'dehors': r'd[eé]hors', # NEW FT
    'devant': r'de[uv][ae]n(t|ts|s)', # REVISED FT
    'devers': 'd[eé][uv]ers', # REVISED FT
    'dessur': 'dess?[ou]r', # REVISED FT
    'dessus': 'dess?u[sz]', # REVISED FT
    'dessous': r'dess?ou?b?[sz]', # REVISED FT
    'derrière': r'derr?i[eéè]re?s?', # REVISED FT
    'en+jusque': "en[ij]osk['e]|enies=c'", #not definitive
    'entour': 'entou?rs?', # REVISED FT
    'entre': "entr[e']", # REVISED FT
    'encontre2': "encontr[e']", # REVISED FT
    'enmi': 'e[nm]m[iy]', # NEW FT
    'envers2': 'en[uv]ers', # REVISED FT
    'jouxte': '[ij]ouxte', # NEW FT
    'outre2': "oul?tr[e']", # REVISED FT
    'parmi': 'par-?m[iy]', # REVISED FT
    'par+deçà': 'par-?d[ée][çc][aà]', # REVISED FT
    'par+delà': 'par-?d[eé]l[aà]', # REVISED FT
    'par+dessus': 'par-?dessus', # REVISED FT, tagged as a noun when 1 word
    'par+dessous': 'par-?dessoub?[sz]', # NEW FT, tagged as a noun when 1 word
    'par+derrière': 'par-?derri[eè]re', # NEW FT
    'par+devant': 'par-?de[uv]ant', # NEW FT
    'par+devers': 'par-?de[vu]ers', # NEW FT
    'travers': 'tra[uv]ers' # NEW FT
}

LOCIS = {
    # ADVERBS
    'à+dedans': 'au-?d[eé]d[ae]n[sz]', # REVISED FT
    'à+dehors': 'au-?d[eé]hors', # REVISED FT
    'à+deçà': 'au-?d[ée][çc][aà]', # REVISED FT
    'à+delà': 'au-?d[eé]l[aà]', # REVISED FT
    'à+dessous': 'au-?dess?ou?b?[sz]', # REVISED FT
    'à+dessus': 'au-?dess?u[sz]', # REVISED FT
    'à+devant': 'au-?de[uv][ae]n(t|ts|s)', # REVISED FT
    'auprès': 'aupr[eèêé]s', # NEW FT
    'ailleurs': 'ai?l[lhi]eurs', # NEW FT
    'alentour': 'alentour', # NEW FT
    'autour': 'aul?tours?', # ADDED FT
    'bas': 'bas', # NEW FT
    'en+deçà': '[ae]n-?d[ée][çc][aà]', #REVISED FT
    'en+dedans': '[ae]n-?d[eé]d[ae]n[sz]', #REVISED FT
    'en+dehors': '[ae]n-?d[eé]hors', #REVISED FT
    'en+dessous': '[ae]n-?dess?ou?b?[sz]', #REVISED FT
    'en+dessus': '[ae]n-?dess?u[sz]', #REVISED FT    
    'çà': '[çc][aà]', #REVISED FT
    'ci': '-?[cç][iy]', # REVISED FT
    'ci+dessous': 'c[iy]-?dess?ou?b?[sz]', # REVISED FT
    'ci+dessus': 'c[iy]-?dess?u[sz]', # REVISED FT
    'ci+devant': 'c[iy]-?de[uv][ae]n(t|ts|s)', # NEW FT
    'céans': 'ch?[eé]ans', # REVISED FT
    'haut': 'haul?t', # NEW FT
    'ici': '[iy]c[iy]', # REVISED FT
    'ici+bas': '[iy]c[iy]-?bas', # NEW FT
    'illuec': r'illu?e(c|c?que[sz]?)', # REVISED FT
    'iqui': 'iqui', # REVISED FT
    'jusque+là': "[ij]usqu(e|'|es)-?l[aà]", # NEW FT
    'là+sus': 'lai?ss?us', # REVISED FT
    'là': '-?l[aà]', # REVISED FT
    'là+bas': 'l[aà]-?bas', # REVISED FT
    'là+dedans': 'l[aà]-?d[eé]d[ae]n[sz]', # REVISED FT
    'là+dessous': 'l[aà]-?dess?ou?b?[sz]', # REVISED FT
    'là+dessus': 'l[aà]-?dess?u[sz]', # REVISED FT
    'là+haut': 'l[aà]-?haul?t', # REVISED FT
    'léans': 'l[eé][ae]ns', # REVISED FT
    'loin': r'loing?', # REVISED FT
    'par+ci': 'par-?c[iy]', # NEW FT
    'par+là': 'par-?l[aà]', # NEW FT
    'près': 'pr[eéèê][sz]', # NEW FT
}

# Always transitive (Ps of interest)
PS = {
    'à': '[aà]|au|aul?x|au[sz]|al',
    'en': 'en',
    'chez': 'chi?[ée][sz]', # REVISED FT
    'dans': r'd(a|e|ei)n[sz]',
    'jusque': "[ij]usqu(e|'|es)", 
    'par': 'par', 
    'lez': 'l(ez|és|ès)',
    'sur': r'sur',
    'sous': r'sou?b?[sz]',
    'vers2': r'v[eé]r[sz]'
}

# Always transitive, may be relators within NP
RELS = {
    'de': "de|d'|des|du"
}

# 1st and 2nd person SJpros, because the pos tagger sucks at 
# capitalization and they are often the first word in the sentence
# 3rd person pronouns added to help calculate reflexive *unknown*.
SJPROS = {
    'je': "j[ée']",
    'tu': "tu",
    'nous': 'nou[sz]',
    'vous': 'vou[sz]',
    'il': '-?il',
    'elle': '-?ell?e',
    'ils': '-?il[sz]',
    'elles': '-?ell?e[sz]',
    'ce': "[çc][e']",
    'ça': "(ça|ca|ç')"
}

LOCRELS = {
    'où': 'o[uù]',
    'dont': 'dont'
}

# Nouns which (almost) always indicate a temporal adjunct. The
# lemmatization is trusted here (not so critical)

FILTERED = [
    'abord', 'automne', 'an', 'année', 'après-midi', 'avantage', 'cas', 
    'coup', 'conséquence', 'dérobée', 'espoir', 'été', 'excéption', 'exemple',
    'façon', 'fois', 'force', 'fortune', 'fin', 'gage', 'guise',
    'hasard',  'heure', 'hiver', 'instant', 'intervalle',
    'jour', 'lendemain', 'manière', 'matin', 'midi', 'minuit', 'moitié',
    'moment', 'mot', 'nuit', 
    'parole', 'printemps', 'propos', 'rechief', 'regard', 'reste', 'semblance', 
    'signe', 'silence',
    'soir', 'sorte', 'temps',
    'veille', 'voix'
]

QS = [
    'assez', 'beaucoup', 'moins', 'plus', 'point', 'tant', 'trop'
]

############################
# Relevant Conll deprel tags
############################

SUBJECTS = ['nsubj', 'nsubj:pass', 'expl:subj', 'csubj']
OBJECTS = ['obj', 'obj:agent'] 

def script(annotator, lemma='', transitive=True):
    
    def am_i_locative(parent, children):
        
        def not_locative():
            return None, None, None
        
        the_type = ''
        # Pre-treatment
        ########################
        # Find parent_lemma
        ########################
        parent_lemma = get_lemma(parent, {**LOCTS, **LOCIS, **LOCRELS})
        # There are a couple of minor issues if parent is a
        # locative, principally to check whether the following word is
        # a preposition of some kind and tagged as such.
        parent_next_tok = None
        if parent_lemma:
            next_toks = hit.get_following_tokens(parent)
            # Check 1: next token is tagged as a adposition
            if next_toks: parent_next_tok = next_toks[0]
            if next_toks and parent_next_tok.tags.get('conll_CPOSTAG', '') == 'ADP':
                parent1_lemma = get_lemma(parent_next_tok, RELS)
                # Check 2: it's an adposition of interest to us
                if parent1_lemma:
                    # Check 3: it's descended from parent (i.e. part of
                    # the same constituent)
                    descendents = annotator.get_descendents(parent)
                    for descendent in descendents:
                        if parent_next_tok is descendent:
                            parent_lemma += '+' + parent1_lemma
                            print(parent_lemma)
                            the_type = 'transitive'
        ###################
        # Process children
        ###################
        # 0. Get rid of initial coordinating conjunctions
        while children and children[0].tags['conll_CPOSTAG'] == 'CCONJ':
            children.pop(0)
        # 1. Find child0, which must precede the parent, or treat this
        # multi-word thing as though only the parent is important.
        if children and int(children[0].tags['conll_ID']) < int(parent.tags['conll_ID']):
            child0 = children[0]
        elif parent_lemma:
            return parent_lemma, annotator.get_string(parent), the_type or 'intransitive'
        else:
            return not_locative()
        #########################################
        # Process child0 ... parent combinations
        #########################################
        # 1. Find out if the parent is a time noun
        if not parent_lemma and (parent.tags['lemma'] in FILTERED or parent.tags['conll_LEMMA'] in FILTERED):
            return not_locative()
        # 2. Get the lemma of the first child using the adpositions list,
        c0_lemma = get_lemma(child0, {**LOCTS, **PS, **RELS})
        ################################################
        # OK, so now four scenarios:
        # 1. parent is a locative and c0 is a locative
        # 2. c0 is a locative and parent isn't
        # 3. parent is a locative and c0 isn't
        # 4. neither c0 not parent are locatives
        ################################################
        # At this point, if there is a c0 lemma, we need to check that
        # the element which follows it should not also be treated as
        # part of c0_lemma.
        if c0_lemma:
            next_toks = hit.get_following_tokens(child0)
            # Need to check the parser has tagged the next token as
            # marking case, otherwise we'll get *de* determiners being
            # swept up :-(
            # HOWEVER, prep + det combinations can be tagged as 
            # determiners.
            # So if it's not with de, then we should include it anyway
            # despite the fact it's not tagged as a case marked.
            # If with *de*, we need to check the preceding lemma.
            # At present, after *fors*, de will consistently be assumed
            # to be a preposition.
            # *********************************************************#
            # BASIC QUERY: rely on 'case' annotation
            # *********************************************************
            if next_toks and not next_toks[0] == parent:
                c1_lemma = get_lemma(next_toks[0], {**LOCTS, **PS, **RELS})
                if c1_lemma and next_toks[0].tags['conll_DEPREL'] == 'case':
                    c0_lemma += '+' + c1_lemma

        # OK, now we process the four scenarios.
        # Scenario 4 is easy: it's not locative
        if not c0_lemma and not parent_lemma: return not_locative()
        # Scenario 2 is locative as long as parent is a nominal
        if c0_lemma and not parent_lemma:
            if not parent.tags['conll_CPOSTAG'] in ['PRON', 'PROPN', 'NOUN']:
                return not_locative()
            # Don't want indirect objects
            if c0_lemma == 'à' and child0.tags['conll_DEPREL'] == 'iobj':
                return not_locative()
            # What if the c0_lemma is de but it's tagged as a determiner?
            if c0_lemma == 'de' and child0.tags['conll_CPOSTAG'] == 'DET':
                return not_locative()
            # What if the parent_lemma is followed by a subordinating conjunction?
            if parent_next_tok and \
            parent_next_tok.tags.get('conll_CPOSTAG', 'SCONJ') == 'SCONJ':
                return not_locative()
            # Filtering out at an end, now we can return it
            return c0_lemma, annotator.get_string(parent), the_type or 'transitive'
            
        # Scenario 1 is definitely a locative, but there are some tweaks
        # as to what we return.
        if c0_lemma and parent_lemma:
            # If parent is a relative pronoun, just return c0.
            if parent_lemma in LOCRELS:
                s = c0_lemma
                the_type = 'transitive'
            # If parent and c0 are not continguous, just return c0
            # (e.g. vers l'arrière)
            elif int(child0.tags['conll_ID']) + 1 != int(parent.tags['conll_ID']):
                s = c0_lemma
                the_type = 'transitive'
            # Otherwise, we concatenate c0 lemma and parent lemma, which is 
            # then intransitive.
            else:
                s = c0_lemma + '+' + parent_lemma
                the_type = 'intransitive'
            return s, annotator.get_string(parent), the_type
        # Scenario 3 is... mysterious. Let's keep it and see what we get.
        if not c0_lemma and parent_lemma:
            return parent_lemma, annotator.get_string(parent), 'scenario3'
    
    def get_lemma(tok, var):
        """
        Returns the lemma matching the form of token from the key: regex
        dictionary in var.
        """
        for lemma, pattern in var.items():
            if re.fullmatch(pattern, str(tok).lower()):
                return lemma
        return ''
        
    def object_allowed(args):
        # If the verb allows transitive structures: return True
        if transitive: return True
        # If the verb doesn't allow transitive structures, only
        # return True:
        # (i) if there is a expressed, personal subject that
        # isn't "il";
        # (ii) if the thing that's tagged as an obj isn't a noun,
        # unless it's *le*, *la* or *les*.
        # If not, whatever's tagged as "obj" is probably
        # a mistagged extraposed subject or a misinterpreted segment.
        subject = False
        for arg in args:
            if arg.tags['conll_DEPREL'] == 'obj':
                # if the argument is "le/l'/les", probably an object.
                if re.fullmatch(r"l(a|e|'|es)", str(arg).lower()): return True
                if arg.tags['conll_CPOSTAG'] not in ['NOUN', 'PROPN']: return False
        for arg in args:
            if str(arg).lower() == 'il': return False
            # Sequoia uses expl:subj; SRCMF-UD just uses expl, but also for
            # complements. So the following only works for SEQUOIA.
            if arg.tags['conll_DEPREL'] == 'expl:subj': return False
            # If a subject has been found, less likely that an object argument
            # is also a subject (although this is still possible)
            if arg.tags['conll_DEPREL'] in SUBJECTS: return True
        # No suitable subject found: return False
        return False
            
    # Set up
    annotator.reset_ids()
    hit = annotator.hit

    # Main procedure
    kw = hit.kws[0]
    # 1. Find arguments dependent on kw
    args = annotator.get_children(kw)
    #print(kw)
    
    ###########################################################################
    # SCRIPT PART 1                                                           #
    # -------------                                                           #
    # Are these even tokens of the right lemma?                               #
    ###########################################################################
    
    # 1. Promote the POS and LEMMA tags from the parser to hit level
    # for the user to check easily
    hit.tags['pos_parser'] = kw.tags['conll_CPOSTAG']
    # Only enable if the parser has re-lemmatized; not the case with HOPS.
    # hit.tags['lemma_parser'] = kw.tags['conll_LEMMA']
    
    # 2. Score the likelihood of this being an instance of the lexical item
    # we're looking for:
    # - 1 point for each tool that thinks it's a verb
    # - 1 point if FRANTEXT thinks it's the right lemma
    # - 1 point if the hopsparser has found verb-specific arguments, like
    # a subject or an object.
    score = 0
    if hit.tags['pos_ft'].startswith('V'): score +=1
    if hit.tags['pos_parser'] == 'VERB': score +=1
    if lemma and hit.tags['lemma_ft'] == lemma: score +=1
    #if lemma and hit.tags['lemma_parser'] == lemma: score += 1
    for arg in args:
        if arg.tags['conll_DEPREL'] in ['nsubj', 'obj'] or arg.tags['conll_DEPREL'].startswith('obl'):
            score +=1
            break
    hit.tags['nlp_score'] = str(score)

    #print(args)
    
    ###########################################################################
    # SCRIPT PART 2                                                           #
    # -------------                                                           #
    # What arguments did the parser find?                                     #
    ###########################################################################
    
    # 2. Locatives
    # BASIC QUERY:
    #   - SEQUOIA: must be annotated as "obl:arg", "obl:mod" or "advmod" to be considered.
    #   - SRCMF-UD: must be annotated as "obl" or "advmod" to be considered.
    
    loc_lemmas = []
    loc_strings = []
    loc_transitive = []
    for arg in args:
        # BASIC QUERY: "obl:arg", "obl:mod"
        if arg.tags['conll_DEPREL'] not in ['obl', 'obl:arg', 'obl:mod', 'advmod']: continue
        children = annotator.get_children(arg)
        # This routine deals with lone arguments. Otherwise, the more
        # complex am_i_locative() function is called.
        if not children:
            # Try lemmatizing it.
            # 1. First, start with the very particular case of relative
            # pronouns, which are complicated because 'où' and 'dont'
            # may be temporal
            lemma = get_lemma(arg, LOCRELS)
            if lemma:
                governor = annotator.get_parent(kw)
                if governor and not governor.tags.get('lemma', '') in FILTERED:
                    loc_lemmas.append(lemma)
                    loc_strings.append(str(arg))
                    loc_transitive.append('pronoun')
            # 2. Next, things other than relative pronouns.
            lemma = get_lemma(arg, {**LOCIS, **LOCTS})
            if lemma:
                # There are a couple of cases which still should be
                # filtered out here. First, it might be the first 
                # element of a complex conjunction like *avant que*
                next_toks = hit.get_following_tokens(arg)
                next_tok = next_toks[0] if next_toks else None
                # Complex conjunction: same parent and it's a *que*
                if next_tok and arg.tags['conll_HEAD'] == next_tok.tags.get('conll_HEAD', '') and \
                re.fullmatch(r"qu?['e]", str(next_tok).lower()):
                    continue
                loc_lemmas.append(lemma)
                loc_strings.append(str(arg))
                loc_transitive.append('intransitive')
            # Check also for 'Y' here
            elif re.fullmatch(r'[iy]', str(arg).lower()):
                loc_lemmas.append('y2')
                loc_strings.append(str(arg))
                loc_transitive.append('pronoun')
        else:
            # Any multi-word argument.
            x, y, z = am_i_locative(arg, children)
            if x:
                loc_lemmas.append(x)
                loc_strings.append(y)
                loc_transitive.append(z)
                
    hit.tags['loc_parser'] = ' | '.join(loc_strings)
    hit.tags['loc_lemma_parser'] = ' | '.join(loc_lemmas)
    hit.tags['loc_type_parser'] = ' | '.join(loc_transitive)
    
    # 3. Detect subject
    # Useful to have the subject argument, if expressed
    # However, this is not a structure we're so interested in and so
    # there's not a lot of extra checking involved.
    subjects = []
    subject_lemma = ''
    for arg in args:
        if arg.tags['conll_DEPREL'] in SUBJECTS:
            subjects.append(annotator.get_string(arg))
            subject_lemma = arg.tags['lemma']
    hit.tags['subject'] = ' | '.join(subjects)
    
    # 4. Detect reflexive
    # BASIC QUERY: rely on 'expl:comp' tag plus regex for the 
    # correct form.
    reflexive_tok = None
    for arg in args:
        # First, use expl(:comp) tag.
        if arg.tags['conll_DEPREL'].startswith('expl') and \
        re.match(r'-?[mts]|nou|vou', str(arg).lower()):
            reflexive_tok = arg
    hit.tags['reflexive_parser'] = 'yes' if reflexive_tok else 'no'
    
    
    # 5. Detect en clitic
    # BASIC QUERY: same as complex query, just look for an "en"
    # argument.
    # SEQUOIA: 'PRON'; SRCMF: 'ADV'
    en_tok = None
    for arg in args:
        if arg.tags['conll_CPOSTAG'] in ['PRON', 'ADV'] and \
        re.fullmatch(r'-?[ea][nm]$', str(arg)):
            en_tok = arg
    hit.tags['en_clitic_parser'] = 'yes' if en_tok else 'no'
    
    # 6. Detect direct object
    # BASIC QUERY: use direct object tag only.
    objects = []
    for arg in args:
        if arg.tags['conll_DEPREL'] == 'obj':
            objects.append(annotator.get_string(arg))
    hit.tags['obj_acc_parser'] = ' | '.join(objects)
    
    # 7. Predicate type
    # The parser *really* struggles with this because it can't
    # indicate the verb form.
    #simple, finite = True, True
    #for arg in args:
    #    if arg.tags['conll_CPOSTAG'] == 'AUX' and \
    #    arg.tags['conll_LEMMA'] in ['avoir', 'être']:
    #        simple = False
    
    # 5. Annotate TMA, basic version, uses pos_bfm
    # Currently not reliable, needs refining.
    #tma = 'simple'
    #for arg in args:
    #    if arg.tags['conll_DEPREL'] == 'aux':
    #        if kw.tags['pos_rnn'] == 'VERppe': tma = 'compound'
    #        if kw.tags['pos_rnn'] == 'VERinf': tma = 'modal'
    #    if kw.tags['pos_rnn'] == 'VERinf' and arg.tags['conll_DEPREL'] == 'mark':
    #        tma = 'non-finite'
    #if kw.tags['conll_DEPREL'] == 'xcomp' and tma == 'simple': tma = 'non-finite'
    #hit.tags['predicate_type'] = tma        
