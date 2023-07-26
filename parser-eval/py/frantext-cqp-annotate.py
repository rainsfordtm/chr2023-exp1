#!/usr/bin/python3

# This file contains the 'script' function to parse the CQP output
# from FRANTEXT and provide initial annotation of the MVIC categories.
# Regexes and lemmas are given for the 16th century onwards, not for
# medieval texts.

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
    'chez': 'ch?(e|é|eu|ie|ié|ieu|)(s|x|z)?',
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

ZEITS = [
    'abord', 'automne', 'an', 'année', 'après-midi', 'été', 'fois', 'heure', 'hiver',
    'jour', 'lendemain', 'matin', 'midi', 'minuit', 'moment', 'printemps', 'nuit',
    'soir', 'temps', 'veille'
]

QS = [
    'assez', 'beaucoup', 'moins', 'plus', 'point', 'tant', 'trop'
]

def script(annotator, target_lemma=''):
	
    ###################################################################
    # FUNCTIONS
    ###################################################################
    
    ###################################################################
    # STAGE 1. Parse the CQP output to generate the .tags dictionary
    # for each token.
    ###################################################################
    
    def stageone():
        ##################################
        # Old stage 1 (for FRANTEXTPUBDOM)
        ##################################
        # lemmas_with_spaces: these are cases where the space in the
        # lemma hardly ever corresponds to two tokens. These lemma
        # tags need to be fused.
        lemmas_with_spaces = [
            ('P+D', ['à', 'le']),
            ('P+D', ['de', 'le']),
            ('P+D', ['de', 'ledit'])
        ]
        # posless_lemmas: these are cases where the lemma and the
        # word contain a space but only have one pos. The pos tag
        # should be split
        posless_lemmas = [
            ('CS', ['parce', 'que']),
            ('CS', ['afin', 'que']),
            ('P', ['afin', 'de']),
            ('CS', ['tandis', 'que']),
            ('I', ['eh', 'bien']),
            ('I', ['eh', 'quoi']),
            ('P', ['quant', 'à']),
            ('CS', ['pour', 'ce', 'que']),
            ('P', ['à', 'partir', 'de']),
            ('P', ['y', 'compris']),
            ('ADV', ['à', 'vrai', 'dire']),
            ('ADV', ['à', 'tâtons']),
            ('ADV', ['a', 'priori']),
            ('ADV', ['au', 'fur', 'et', 'à', 'mesure']),
            ('CS', ['pourvu', 'que']),
            ('ADV', ['en', 'outre']),
            ('ADV', ['au', 'demeurant']),
            ('DET', ['cent', 'mille']),
            ('DET', ['dix', 'mille']),
            ('DET', ['deux', 'mille']),
            ('DET', ['trois', 'mille']),
            ('DET', ['vingt', 'mille']),
            ('DET', ['quatre', 'mille']),
            ('DET', ['six', 'mille']),
            ('DET', ['cinquante', 'mille']),
            ('DET', ['trente', 'mille']),
            ('DET', ['douze', 'mille']),
            ('DET', ['cinq', 'mille']),
            ('DET', ['soixante', 'mille']),
            ('DET', ['huit', 'mille']),
            ('DET', ['quinze', 'mille']),
            ('DET', ['vingt-cinq', 'mille']),
            ('DET', ['quatre-vingt', 'mille']),
            ('DET', ['deux', 'cents']),
            ('DET', ['trois', 'cents']),
            ('DET', ['quatre', 'cents']),
            ('DET', ['cinq', 'cents']),
            ('DET', ['six', 'cents']),
            ('DET', ['douze', 'cents']),
            ('DET', ['huit', 'cents']),
            ('DET', ['cent', 'cinquante']),
            ('DET', ['vingt', 'et', 'un']),
            ('DET', ['cent', 'vingt']),
            ('NC', ['un', 'million']),
            ('NC', ['deux', 'millions']),
            ('NC', ['trois', 'millions']),
            ('NC', ['compte', 'rendu']),
            ('NC', ['don', 'juan']),
            ('NC', ['garde', 'champêtre']),
            ('NP', ['Louis', 'XIV']),
            ('NP', ['Louis', 'XVI']),
            ('NP', ['Henri', 'IV']),
            ('NP', ['La', 'Rochefoucauld']),
            ('NP', ['La', 'Bruyère']),
            ('NP', ['Henri', 'III']),
            ('NP', ['Charles', 'XII']),
            ('NP', ['La', 'Rochelle']),
            ('NP', ['La', 'Valette']),
            ('NP', ['Philippe', 'II']),
            ('NP', ['Louis', 'XV']),
            ('NP', ['Charles', 'IX']),
            ('NP', ['Charles', 'VI']),
            ('NP', ['Charles', 'X']),
            ('NP', ['Henri', 'II']),
            ('NP', ['Henri', 'III']),
            ('NP', ['Napoléon', 'III']),
        ]
        toks = hit.get_tokens()
        poss = hit.tags['pos_all_ft'].split()
        lemmas = hit.tags['lemma_all_ft'].split()
        # Because FRANTEXT includes whitespace in words and lemmas
        # (ARGH!) remapping pos tags and lemmas to word is unfortunately
        # very tricky, since ConMan retokenizes on whitespace in the
        # edition.
        # The algorithm does the following:
        #   - first, map lemmas to pos
        #   - then, map the resulting list to words
        pos = ''
        assign_x = 0
        tok_poss, tok_lemmas = [], []
        # MAIN ITERATOR: GENERATES LIST OF LEMMAS AND POS TAGS
        for tok in toks:
            if not poss or not lemmas: break # Exit if pos or lemma lists exhausted
            # If no pos, take the first pos from the list
            if not pos: pos = poss.pop(0)
            # If we're assigning the pos tag X at the moment, do this
            # first
            if assign_x > 0:
                tok_poss.append('X')
                tok_lemmas.append(lemmas.pop(0))
                assign_x = assign_x - 1
                continue
            # Check for the 'quant' in 'quant à le':
            if pos == 'P+D' and len(lemmas) >= 3 and lemmas[:3] == \
            ['quant', 'à', 'le']:
                tok_poss.append('X')
                tok_lemmas.append('quant')
                lemmas = lemmas[1:]
                # Move on to next token without resetting the pos tag
                continue
            # Check for lemmas with spaces
            for check_pos, check_lemmas in lemmas_with_spaces:
                n = len(check_lemmas)
                if pos == check_pos and len(lemmas) >= n \
                and lemmas[:n] == check_lemmas:
                    tok_poss.append(pos)
                    tok_lemmas.append('.'.join(lemmas[:n]))
                    pos = ''
                    lemmas = lemmas[n:]
                    break
            # break out of loop if the first check has worked
            if not pos: continue
            for check_pos, check_lemmas in posless_lemmas:
                n = len(check_lemmas)
                if pos == check_pos and len(lemmas) >= n \
                and lemmas[:n] == check_lemmas:
                    tok_poss.append('X')
                    tok_lemmas.append(lemmas.pop(0))
                    assign_x = n - 2 # one X already assigned, last token gets pos tag
                    break
            else:
                # Triggered if this hasn't been found in posless lemmas
                # Just assign a pos and lemma normally
                tok_poss.append(pos)
                tok_lemmas.append(lemmas.pop(0))
                pos = ''
        # After the loop:
        if len(toks) == len(tok_poss) == len(tok_lemmas):
            for tok, pos, lemma in zip(toks, tok_poss, tok_lemmas):
                tok.tags['pos'] = pos
                tok.tags['lemma'] = lemma
            hit.tags['ft_aligned'] = 'yes'
        else:
            for tok in toks:
                tok.tags['pos'] = '--'
                tok.tags['lemma'] = '--'
            hit.tags['ft_aligned'] = 'no'
        hit.tags['pos_all_ft_corr'] = ' '.join(tok_poss)
        hit.tags['lemmas_all_ft_corr'] = ' '.join(tok_lemmas)
        
    def stageonert():
        ##############################################################
        # New stage 1 (PUBDOMRT)
        ##############################################################
        # 1. Get tokens
        toks = hit.get_tokens(hit.TOKENS)
        # 2. Get poss and lemmas
        poss = hit.tags['pos_all_ft'].split()
        lemmas = hit.tags['lemma_all_ft'].split()
        # 3. Zip 'em
        if len(toks) == len(poss) == len(lemmas):
            for tok, pos, lemma in zip(toks, poss, lemmas):
                tok.tags['pos'] = pos
                tok.tags['lemma'] = lemma
            hit.tags['ft_aligned'] = 'yes'
        else:
            for tok in toks:
                tok.tags['pos'] = '--'
                tok.tags['lemma'] = '--'
            hit.tags['ft_aligned'] = 'no'
        
    ###################################################################
    # STAGE 2. Calculate nlp_score and lemmatization accuracy
    ###################################################################
    
    def stagetwo():
        nlp_score = 0
        if hit.tags['lemma_ft'][0].isupper():
            # Set NLP score to 2 for all upper-case lemmas, which are
            # not lemmatized properly.
            nlp_score = 2
        elif hit.tags['pos_ft'].startswith('V'):
            # One point if FRANTEXT thinks it's a verb
            nlp_score += 1
            # Score the lemma, +2 if it matches, +1 if FRANTEXT thinks
            # it's a verb but can't attach it to a verb lemma
            if hit.tags['lemma_ft'] == target_lemma:
                nlp_score += 2
            if not hit.tags['lemma_ft'][-2:] in ['ir', 'er', 're']:
                nlp_score += 1
        hit.tags['nlp_score'] = nlp_score
       
    ###################################################################
    # STAGE 3. Produce the remaining MVIC annotation.
    ###################################################################
    
    def stagethree():
        
        ###############################################################
        # Functions
        ###############################################################

        def _get_clitics(base_tok, enclisis=False):
            clitics = []
            fnc = get_next_tok if enclisis else get_prev_tok
            tok = fnc(base_tok)
            apostrophe = False
            # Extra check for enclitics: token should start with a hyphen
            # It's a crap approximation, but it avoids catching proclitics
            # on the infinitive by accident.
            # Also, apostrophe flag is set if the previous token ends
            # with an apostrophe, because in sequences like "-m'y",
            # "y" doesn't start with a hyphen.
            while tok and is_clitic(tok) and \
            (enclisis == False or tok[0] == '-' or apostrophe == True):
                clitics.append(tok)
                apostrophe = True if tok[-1] == "'" else False
                tok = fnc(tok)
            return clitics
        
        def get_clitics():
            kw = get_kw()
            vcjg = get_vcjg()
            clitics = []
            # clitics before infinitives and present participles
            if kw.tags['pos'] in ['VINF', 'VPR']:
                clitics = _get_clitics(kw)
            if clitics: return clitics
            # Continue with the auxiliary. Also picks up clitic
            # climbing over modals (auxiliary is modal) 
            # Proclitics
            clitics = _get_clitics(vcjg)
            if clitics: return clitics
            # Enclitics
            clitics = _get_clitics(vcjg, enclisis=True)
            return clitics
            
        def get_complement(complement=None):
            # Tries to identify the post-verbal nominal constituent -
            # at least the beginning of it.
            # Words are divided into the following types:
            #   1. words that can be ignored (clitics, most adverbs)
            #      -> 
            #   2. words that unambiguously indicate a nominal complement
            #      or locative complement
            #       (determiner, adjective, noun, pronoun, locative Ps)
            #   3. words that unambiguously indicate we should give up
            #      looking for a nominal complement (punctuation, 
            #      a verb form, conjunctions or relative pronouns)
            #      -> tagged as "abort"
            #   4. grammaticalized prepositions like à or de, which may
            #      be relevant, or may not be, depending on what comes
            #      next.
            # If a complement is passed, tries to find the NEXT
            # complement.
            kw = get_kw()
            # Set the offset
            offset = 0
            rcx_toks = hit.get_tokens(hit.RCX)
            tag_string = ''
            # Adapt for presence of a complement
            if complement:
                if not 'type' in complement or not 'last_ix' in complement:
                    return {}
                offset = complement['last_ix']
                rcx_toks = rcx_toks[offset:]
            for rcx_tok in rcx_toks:
                tag_string += tag_for_chunker(rcx_tok)
            # Now, a hack. The string "QR" + nominal or adj normally
            # represents a So we're going to "prefilter" these as
            # DD, and turn any other "Q" strings back into "X"
            tag_string = re.sub(r'QR(?![PTID])', 'DD', tag_string)
            tag_string = re.sub(r'Q', 'X', tag_string)
            # 0. Anything where the first nominal is a temporal one
            m = re.match(r'[^NZ#]*Z', tag_string)
            if m:
                # Call self recursively...
                return get_complement({'type': 'Z', 'last_ix': offset + m.end()})
            # 2. Transitive PP, possibly locative
            m = re.match(r'X*([PR]+|[PR]*T+R*)X*D*X*(N+)X*(?![RW])', tag_string)
            if not m: m = re.match(r'X*([PR]+|[PR]*T+R*)X*D*X*(N+)X*([RW]+)', tag_string)
            if m:
                last_ix = m.end()
                start_ix = m.start(1)
                head_ixs = [m.start(1), m.end(1)]
                return {'type': 'T',
                        'heads': [tok.tags['lemma_mvic'] for tok in rcx_toks[head_ixs[0]:head_ixs[1]]],
                        'toks': rcx_toks[start_ix:last_ix],
                        'last_ix': last_ix + offset}
            # 3. Intransitive locative, no nominal follows
            m = re.match(r'X*([PR]*[IT]+)X*R?X*(?!N)', tag_string)
            if m:
                last_ix = m.end(1)
                start_ix = m.start(1)
                head_ixs = [m.start(1), m.end(1)]
                return {'type': 'I',
                        'heads': [tok.tags['lemma_mvic'] for tok in rcx_toks[head_ixs[0]:head_ixs[1]]],
                        'toks': rcx_toks[start_ix:last_ix],
                        'last_ix': last_ix + offset}
            # Exit at this point if complement passed.
            if complement: return {}
            # 1. Simple NP - but only if no complement passed
            m = re.match(r'X*(D+)X*(N+)X*(?![RW])', tag_string)
            if not m: m = re.match(r'X*(D+)X*(N+)X*([RW]+)', tag_string)
            if m:
                last_ix = m.end()
                start_ix = m.start(1)
                head_ix = m.end(2)
                return {'type': 'N', 
                        'toks': rcx_toks[start_ix:last_ix],
                        'last_ix': last_ix + offset}
                        
        def tag_for_chunker(tok):
            # Used by get_complement to classify each word.
            pos = tok.tags['pos']
            form = str(tok)
            # Part one. Filter based on pos.
            if re.fullmatch(r'(CC|CS|I|PONCT|V.*)\*?', pos):
                tok.tags['lemma_mvic'] = '--'
                return '#'
            if re.fullmatch(r'DET\*?', pos):
                tok.tags['lemma_mvic'] = '--'
                return 'D'
            if re.fullmatch(r'PRO(REL|WH)\*?', pos):
                tok.tags['lemma_mvic'] = '--'
                return 'W'
            # Part two. Identify Ps and ADVs. Also looks at NC and NP
            # tags, which are over-applied.
            if re.fullmatch(r'(P(\+D)?|ADV|NC|NP|PRO)\*?', pos):
                for lemma, regex in RELS.items():
                    if re.fullmatch(regex, str(tok).lower()):
                        tok.tags['lemma_mvic'] = lemma
                        return 'R'
                for lemma, regex in PS.items():
                    if re.fullmatch(regex, str(tok).lower()):
                        tok.tags['lemma_mvic'] = lemma
                        return 'P'
                for lemma, regex in LOCTS.items():
                    if re.fullmatch(regex, str(tok).lower()):
                        tok.tags['lemma_mvic'] = lemma
                        return 'T'
                for lemma, regex in LOCIS.items():
                    if re.fullmatch(regex, str(tok).lower()):
                        tok.tags['lemma_mvic'] = lemma
                        return 'I'
                if tok.tags['lemma'] in ZEITS: return 'Z'
                if tok.tags['lemma'] in QS: return 'Q'
                if re.fullmatch(r'(NC|NP|PRO)\*?', pos):
                    return 'N'
                if re.fullmatch(r'P\*?', pos):
                    # Prepositions which aren't of interest are tagged
                    # as '#' (stop looking)
                    return '#'
            # If all else fails, return 'X'
            return 'X'
        
        def get_vcjg():
            id_aux_cqp = int(hit.tags['id_aux_cqp'])
            id_cqp = int(hit.tags['id_cqp'])
            if id_aux_cqp == id_cqp:
                return get_kw()
            else:
                ix = get_ix_from_tok(get_kw())
                ix += id_aux_cqp - id_cqp
                return get_tok_by_ix(ix)
        
        def get_kw():
            return hit.get_tokens(hit.KEYWORDS)[0]
        
        def get_tok_by_ix(ix):
            nonlocal hit_tokens
            return hit_tokens[ix]
        
        def get_ix_from_tok(tok):
            nonlocal hit_tokens
            l = [x is tok for x in hit_tokens]
            return l.index(True)
        
        def get_next_tok(tok):
            nonlocal hit_tokens
            ix = get_ix_from_tok(tok)
            if ix < len(hit_tokens):
                return get_tok_by_ix(ix + 1)
            else:
                return None
        
        def get_prev_tok(tok):
            ix = get_ix_from_tok(tok)
            if ix > 0:
                return get_tok_by_ix(ix - 1)
            else:
                return None
                
        def _get_subject_pronoun(base_tok, enclisis=False):
            fnc = get_next_tok if enclisis else get_prev_tok
            tok = fnc(base_tok)
            while tok.tags['pos'] in ['CLO', 'ADV']:
                tok = fnc(tok)
            for lemma, regex in SJPROS.items():
                if re.fullmatch(regex, str(tok).lower()):
                    tok.tags['lemma_mvic'] = lemma
                    return tok
            return None
                
        def get_subject_pronoun():
            vcjg = get_vcjg()
            tok = _get_subject_pronoun(vcjg)
            if tok: return tok
            tok = _get_subject_pronoun(vcjg, enclisis=True)
            return tok
                
        def is_clitic(tok):
            return tok.tags['pos'] == 'CLO'
        
        hit_tokens = hit.get_tokens(hit.TOKENS)
        loc_toks = []
        loc_head_lemmas = []
        loc_types = []
        obj_acc_toks = []
        reflexive = 'no'
        en_clitic = False
        
        ###############################################################
        # PART 1. Fairly certain information from the clitic group
        ###############################################################
        
        clitics = get_clitics()
        for clitic in clitics:
            # Test number one. An 'y' clitic is a loc element and
            # should be added to loc_toks. Can just test on the form.
            if re.fullmatch(r'[IiYy]', str(clitic)) or re.search(r"[-'][IiYy]($|-)", str(clitic)):
                loc_toks.append([clitic])
                loc_head_lemmas.append(['y2'])
                loc_types.append('pronoun')
            # Test number two. An 'en' sets the "en_clitic" flag to True
            if re.fullmatch(r'[Ee]n', str(clitic)) or re.search(r"[-']en($|-)", str(clitic)):
                en_clitic = True
            # Test number three. A direct object pronoun should be added
            # to obj_acc_toks. Forms le la les l' are DEFINITELY obj_acc
            if re.fullmatch(r"[Ll](e|a|'|es)", str(clitic)) or \
            re.search(r"[-'][Ll](e|a|'|es)($|-)", str(clitic)):
                obj_acc_toks.append(clitic)
            # Test number four. A se pronoun marks a reflexive.
            if re.fullmatch(r"[Ss][e']", str(clitic)) or \
            re.search(r"[-']s('|e$|e-)", str(clitic)):
                reflexive = 'yes'
                
        ###############################################################
        # PART 2. Guessing if it's a reflexive from the subject
        ###############################################################
        
        sjpro = get_subject_pronoun()
        if sjpro and clitics and reflexive == 'no':
            if sjpro.tags['lemma_mvic'] == 'je':
                test = 'm'
            elif sjpro.tags['lemma_mvic'] == 'tu':
                test = 't'
            elif sjpro.tags['lemma_mvic'] == 'nous':
                test = 'nou'
            elif sjpro.tags['lemma_mvic'] == 'vous':
                test = 'vou'
            else:
                test = ''
            if test:
                for clitic in clitics:
                    if str(clitic).lower().startswith(test):
                        reflexive = 'yes'
        elif clitics and reflexive == 'no':
            # No subject pronoun but a clitic which might be reflexive.
            for clitic in clitics:
                if re.match(r'(m|t|nou|vou)', str(clitic).lower()):
                    reflexive = 'unk'
                    
        # could probably be improved to better handle imperatives.
                
        ###############################################################
        # PART 3. Locatives and objects from the first and second
        # constituents after the finite verb
        ###############################################################
        
        complement = get_complement()
        if complement and complement['type'] == 'N' and not obj_acc_toks:
            obj_acc_toks = complement['toks']
            complement = get_complement(complement)
        while complement and complement['type'] in ['T', 'I']:
            loc_toks.append(complement['toks'])
            loc_head_lemmas.append(complement['heads'])
            loc_types.append('transitive' if complement['type'] in 'T' else 'intransitive')
            # Loop back around for 'I' complements
            if complement['type'] == 'I':
                complement = get_complement(complement)
            else:
                complement = None
            
        ###############################################################
        # PART 4. Look for a preceding relative pronoun. Only checks
        # où and dont and doesn't do anything if a locative has
        # already been found (Maybe switch before complement?)
        ###############################################################
        
        vcjg = get_vcjg()
        tok = get_prev_tok(vcjg)
        while tok and not tok.tags['pos'] in ['V', 'VINF', 'CS', 'PROREL', 'PROWH']:
            tok = get_prev_tok(tok)
        for lemma, regex in LOCRELS.items():
            if re.fullmatch(regex, str(tok)):
                tok.tags['lemma_mvic'] = lemma
                loc_toks.append([tok])
                loc_head_lemmas.append([lemma])
                loc_types.append('pronoun')
                    
        ###############################################################
        # PART 5. Predicate type
        # Only être/avoir auxiliary counts as "compound"
        ###############################################################
        
        vcjg = get_vcjg()
        kw = get_kw()
        simple, finite = True, True
        if not vcjg == kw and vcjg.tags['lemma'] in ['être', 'avoir']:
            simple = False
        if vcjg.tags['pos'].startswith('V') and not vcjg.tags['pos'] == 'V':
            finite = False
                
        ###############################################################
        # Checking code: Dump attributes as TEST
        ###############################################################
        hit.tags['TEST_clitics'] = repr(clitics)
        hit.tags['TEST_loc_toks'] = repr(loc_toks)
        hit.tags['TEST_obj_acc_toks'] = repr(obj_acc_toks)
        hit.tags['reflexive'] = reflexive
        hit.tags['en_clitic'] = 'yes' if en_clitic else 'no'
        hit.tags['obj_acc'] = ' '.join([str(tok) + '_' + tag_for_chunker(tok) for tok in obj_acc_toks])
        loc_strings, loc_lemma_strings = [], []
        for l in loc_toks:
            loc_strings.append(' '.join([str(tok) + '_' + tag_for_chunker(tok) for tok in l]))
        for l in loc_head_lemmas:
            loc_lemma_strings.append('+'.join(l))
        hit.tags['loc'] = ' | '.join(loc_strings)
        hit.tags['loc_lemma'] = ' | '.join(loc_lemma_strings)
        hit.tags['loc_type'] = ' | '.join(loc_types)
        s = 'simple ' if simple else 'compound '
        s += 'finite' if finite else 'non-finite'
        hit.tags['predicate_type'] = s
        
    ###################################################################
    # SCRIPT
    # Runs the stages
    ###################################################################
    
    hit = annotator.hit
    stageonert()
    stagetwo()
    stagethree()
    
    
    
    

    
