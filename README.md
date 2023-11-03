# Parser evaluation for experiment 1 in CHR2023 poster (Rainsford and
Regnault 2023)

## 1. Introduction

The parser evaluation in experiment 1 of Rainsford and Regnault (2023)
took place in several stages and made use of the Concordance Manager
(Rainsford 2023) to combine and query annotations. This README
file summarizes the procedure adopted and the principal files in this
repository but does not provide comprehensive documentation of 
an experimental process which will be further developed in the framework
of an ongoing project.

## 2. Objective

The objective was to produced concordances of two French verbs 
(*jeter* "to throw" and *entrer* "to enter") containing correct annotation
of the following features of argument structure:
+ **reflexive**: (y or n) presence or absence of a reflexive pronoun
+ **en_clitic**: (y or n) presence or absence of a *en* clitic pronoun
+ **obj_acc**: (string) the direct object, if present
+ **loc**: (string) locative arguments and adjuncts, if present
+ **loc_lemma**: (string) head of locative arguments and adjuncts
+ **loc_type**: (string) whether the head of the locative is transitive
(i.e. takes an NP complement) or intransitive
+ **predicate_type**: (string) nature of the verb form

The data was extracted from a corpus containing only automatic
lemmatization and part-of-speech tags. The objective was to automatically
generate the features of argument structure listed above using a 
combination of parsers trained on pre-existing models and "expert queries",
whose purpose was to enrich and correct the annotation produced by the
parser.

## 3. Procedure

1. Extraction of all the occurrences of the verbs *jeter* and *entrer*
found in the public domain texts of FRANTEXT in the form of a concordance.
1. ConMan (first pass)
    + create initial annotation of the relevant features of argument
    structure using part-of-speech tags only.
        + Annotation script [parser-eval/py/frantext-cqp-annotate.py](parser-eval/py/frantext-cqp-annotate.py)
        + Results in [parser-eval/csv/00extracted](parser-eval/csv/00extracted)
    + create a CONLL-U file from the concordance ready to be parsed
        + Results in [parser-eval/conllu/00extracted](parser-eval/conllu/00extracted)
1. Manual correction of initial annotation to produce "gold" annotation
    + Results in [parser-eval/csv/eval-gold](parser-eval/csv/eval-gold)
1. Parsing of the CONLL-U file with three different parser-model combinations:
    + HOPS parser, Sequoia-Flaubert model [parser-eval/conllu/01parsed-hops-sequoia-flaubert](parser-eval/conllu/01parsed-hops-sequoia-flaubert)
    + HOPS parser, SRCMF UD (Old French) model [parser-eval/conllu/01parsed-hops-srcmfud-29-bertrade-base-8192-32e-only](parser-eval/conllu/01parsed-hops-srcmfud-29-bertrade-base-8192-32e-only)
    + UD Pipe parser, GSD model [parser-eval/conllu/01parsed-udpipe-gsd](parser-eval/conllu/01parsed-udpipe-gsd)
1. ConMan (second pass)
    + recombine the parsed CONLL-U file with the original concordance
    + annotate the concordance for the relevant aspects of argument
    structure using only the parser annotation and save the output.
        + Annotation script: [parser-eval/py/frantext-parser-annotate-basic.py](parser-eval/py/frantext-parser-annotate-basic.py)
        + Results for HOPS parser, Sequoia-Flaubert model [parser-eval/csv/01parsed-hops-sequoia-flaubert-basic](parser-eval/csv/01parsed-hops-sequoia-flaubert-basic)
        + Results for HOPS parser, SRCMF-UD model [parser-eval/csv/01parsed-hops-srcmfud-29-basic](parser-eval/csv/01parsed-hops-srcmfud-29-basic)
        + Results for UD pipe parser, GSD model [parser-eval/csv/01parsed-udpipe-gsd-basic](parser-eval/csv/01parsed-udpipe-gsd-basic)
1. ConMan (third pass)
    + combine the annotated concordance with the gold annotation
    + print a table showing the accuracy of the parser-based annotation
        + Annotation script: [parser-eval/py/frantext-parsed-eval.py](parser-eval/py/frantext-parsed-eval.py)
        + Results for HOPS parser, Sequoia-Flaubert model [parser-eval/csv/02evaluation-hops-sequoia-flaubert-basic/](parser-eval/csv/02evaluation-hops-sequoia-flaubert-basic/)
        + Results for HOPS parser, SRCMF-UD model [parser-eval/csv/02evaluation-hops-srcmfud-29-basic](parser-eval/csv/02evaluation-hops-srcmfud-29-basic)
        + Results for UD Pipe parser, GSD model [parser-eval/csv/01parsed-udpipe-gsd-basic](parser-eval/csv/01parsed-udpipe-gsd-basic)
1. Optimize the query script to correct common errors from the best parser / model combination
(HOPS/Sequoia) and improve annotation of the targeted phenomena ("expert queries")
1. ConMan (fourth pass)
    + recombine the parsed CONLL-U file with the original concordance
    + annotate the concordance for the relevant aspects of argument
    structure using the expert query and save the output.
        + Annotation script: [parser-eval/py/frantext-parser-annotate.py](parser-eval/py/frantext-parser-annotate.py)
        + Results [parser-eval/csv/01parsed-hops-sequoia-flaubert-expert](parser-eval/csv/01parsed-hops-sequoia-flaubert-expert)
1. ConMan (fifth pass)
    + combine the annotated concordance with the gold annotation
    + print a table showing the accuracy of the "expert query" based annotation
        + Annotation script: [parser-eval/py/frantext-parsed-eval.py](parser-eval/py/frantext-parsed-eval.py)
        + Results [parser-eval/csv/02evaluation-hops-sequoia-flaubert-expert/](parser-eval/csv/02evaluation-hops-sequoia-flaubert-expert/)
        
## 4. Running the annotation scripts

The annotation scripts are integrated into the Conman software, a 
version of which is included in the repository. Here's how to use
the scripts on the data provided in this repository (examples for
running queries on *entrer* using HOPS Sequoia):

**Pass 2**. First, update the path in [parser-eval/cfg/wf_pass2_entrer.cfg](parser-eval/cfg/wf_pass2_entrer.cfg)
so that it points to [parser-eval/py/frantext-parser-annotate-basic.py](parser-eval/py/frantext-parser-annotate-basic.py)
(Conman requires absolute paths to annotation scripts). Then run
```
conman-1.0.0/conman.py -s -z -w parser-eval/cfg/wf_pass2_entrer.cfg -m parser-eval/conllu/01parsed-hops-sequoia-flaubert/entrer.conllu parser-eval/cnc/00extracted/entrer.cnc.gz <OUTPUT_FILE>
```

**Pass 3**. First, update the path in [parser-eval/cfg/wf_pass3_pass5_eval_entrer.cfg](parser-eval/cfg/wf_pass3_pass5_eval_entrer.cfg)
so that it points to [parser-eval/py/frantext-checked-eval.py](parser-eval/py/frantext-checked-eval.py)
(Conman requires absolute paths to annotation scripts). Then run
```
conman-1.0.0/conman.py -w parser-eval/cfg/wf_pass3_pass5_entrer.cfg -m parser-eval/csv/eval-gold/entrer.csv parser-eval/cnc/01parsed-hops-sequoia-flaubert-basic/entrer.cnc.gz <OUTPUT_FILE>
```

**Pass 4** First, update the path in [parser-eval/cfg/wf_pass4_entrer.cfg](parser-eval/cfg/wf_pass4_entrer.cfg)
so that it points to [parser-eval/py/frantext-parser-annotate.py](parser-eval/py/frantext-parser-annotate.py)
(Conman requires absolute paths to annotation scripts). Then run
```
conman-1.0.0/conman.py -s -z -w parser-eval/cfg/wf_pass4_entrer.cfg -m parser-eval/conllu/01parsed-hops-sequoia-flaubert/entrer.conllu parser-eval/cnc/00extracted/entrer.cnc.gz <OUTPUT_FILE>
```

**Pass 5**. First, update the path in [parser-eval/cfg/wf_pass3_pass5_eval_entrer.cfg](parser-eval/cfg/wf_pass3_pass5_eval_entrer.cfg)
so that it points to [parser-eval/py/frantext-checked-eval.py](parser-eval/py/frantext-checked-eval.py)
(Conman requires absolute paths to annotation scripts). Then run
```
conman-1.0.0/conman.py -w parser-eval/cfg/wf_pass3_pass5_entrer.cfg -m parser-eval/csv/eval-gold/entrer.csv parser-eval/cnc/01parsed-hops-sequoia-flaubert-expert/entrer.cnc.gz <OUTPUT_FILE>
```
