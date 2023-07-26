# Direct objects for *jeter*

## Common sources of errors

+ Non-standard spelling, which occasionally causes the verb to be
  tagged as something other than a verb, or (presumably) causes the
  parser not to have any reference for what its argument structure
  should be. Typically DOs missed.
+ Some partitives, e.g.
	+ *de leur bien*
+ Postverbal subjects, preverbal objects

## Errors which are fixable with better filtering

+ The clitic *en* can be recognized as a direct object by the model.
  This is something that the MVIC analysis doesn't want.
    + FIXED 14.7.23
+ Some cases of *se* tagged as a DO, e.g. `8dae3b76-4c70-4191-82b8-5726deed6f19`
	+ this is not necessarily wrong, e.g. *se jeter à ses pieds*,#
	  but it's not the analysis we want for the MVIC.
    + FIXED 14.7.23
+ Some cases of *le, les* tagged as a subject.
    + FIXED 14.7.23 to recognize them as objects
+ Quantified DOs are not picked up, e.g. *trop de*, *plus de*, 
	+ `05f4dea7-86f9-464e-b0d3-ab638e951edc`
+ Some cases of reflexive plus direct object; OK for some verbs,
  unlikely for others.
	+ could this arg. structure be flagged for checking??
+ preverbal clitic + postverbal subject: the parser tends to miss the
  clitic DO in this case.
+ couple of cases of *c'* as DO (can't be right)
    + FIXED 14.7.23
  
## Notes on manual annotation

+ Coordination, e.g. *et les arracha et jeta*. Best analysis is as
  a null object, because *les* is the object of *arracher*
  (`de3a8bcb-c83f-4211-911a-915e9d624a8c`).
  
# Locative complements for *jeter*

## Common sources of errors

+ Parser identifies too many complements (also a problem in MCVF):
    + many PPs are not always locatives, particularly if far from the verb
    + *par* complements are always ambiguous
    + temporals are also collected
+ Bad hierarchy
    + e.g. *jeter les yeux dessus* -> *dessus* as locative
    + *de X à l'autre* as a single argument, e.g. `a944fbc9-93c0-4e9f-ba02-c042ecf0895e`
    + particularly bad with *sur* PPs, which this model seems to want to 
      attach to the NP, e.g. `d1d4bb84-30dd-4449-9384-3668cb4010a8`
+ Parser is not good at quantifiers; *tant de X* analysed as two args with
  the *de* often as a PP.
    
## Things which are genuinely ambiguous
    
+ Differences of interpretation for indirect objects (*à qui*?)
+ Mesure phrases
    + *jeter dans le Mississippi à trente-cinq lieues des natchez*
+ Double references 
    + *au port de Rutupine en l' isle de Bretaigne* (`f273644c-c703-450f-9874-cfdab2e9af58`)
+ Any *l'un ... l'autre* construction, e.g. *jeter l'un contre l'autre*:
  do we want to analyse *contre* here as a argument of *jeter*?
  (`36b0466f-36de-410e-ad43-62354cca3933`)
    
## Errors which are fixable with better filtering

+ Fixed expressions:
    + *à ... mots*, *à ... paroles* never locative (blocked)
    + *jeter à corps perdu*, also never locative
    + *en silence* (blocked)
    + *à l'exemple de...* (blocked)
    + *à la dérobée* (blocked)
    + *à la fin* (blocked)
    + *en signe de...* (blocked)
    + *à la semblance...* (blocked)
    + *à moitié* (blocked)
    + anything with *coup* in it (blocked)
    + *à un instant* (blocked)
    + *au hasard* (blocked)
    + *au lieu que/de*
    + *instant* (blocked)
    + *au moins*
    + *au reste* (blocked)
    + *au retour*
    + *en guise de* (blocked)
    + *jusqu'à ce que* (fixed by SCONJ?)
    + *de peur que* 
    + *d'avantage* (blocked)
    + *de rechief* (blocked)
    + *d'une voix*, *d'une regard* (blocked)
    + *à corps perdu*
    + *dans l'espoir de* (blocked)
    + *de telle façon* (blocked)
    + *en gage de* (blocked)
    + *de ce que...* (fixed by SCONJ?)
    + *de dépit*
    + *en ce cas* (blocked)
    + *en ceste façon* (blocked)
    + *en ceste sorte* (blocked)
    + *en conséquence* (blocked)
    + *en fin* (blocked)
    + *en présence* (blocked)
    + *en manière* (blocked)
    + *en abondance*
    + *à l'exception de* (blocked)
    + *par force* (blocked)
    + *par fortune* (blocked)
    + *par hasard* (blocked)
    + *par instant* (blocked)
    + *par intervalle* (blocked)
    + *par l'esprit* 
    + *sur ce*
    + *à propos de* (blocked)

+ PPs which are "far" from the predicate, separated by commas, are
  not so likely to be locatives
+ PPs which serves as part of complementizers not likely to be locatives,
  e.g. *à mesure que...*
    * FIXED 19.7.23: these nouns now filtered out if followed by SCONJ
+ The first element of a complex conjunction depends on the governed
  verb, e.g. *avant qu'il jette* (`f692e930-fe3f-4b58-80d2-a02b27abba63`)
    + FIXED 14.7.23
+ Discursive use of *la-dessus*, e.g. `7e26c646-8192-4807-ae4a-9602084b4f26`
+ Temporal uses of *où*, typically after *moment où*, e.g. 
    `8595cb08-2efe-4154-9586-acdb3ff9ef6b`
    + FIXED 19.7.23
+ *force* is a form of *fors* (*jeter fors qqc*)
  
## Bugs

+ *à travers* not correctly recognized in output
    + `6f14b5d0-e4aa-487a-ba76-892a6844e2dc`
    + FIXED 14.7.23 with c1_lemma
+ *loin de* not correctly recognized, also:
    + *hors+de*
        + FIXED 14.7.23 with c1_lemma
    + *par+dessus*, e.g. `a622263d-648b-4913-89a2-fc7d72a4a830`
        + FIXED 14.7.23 with c1_lemma
    
+ Inconsistency as to whether or not *de* is considered part of the
  head in the lemmatization 
    + it is in the MCVF annotation.
    + probably best if it is; TODO update parser annotation script
    and check on:
	+ `51070d80-1cb7-4b11-8efd-1126ff539209`
	+ `a7b7f804-4ea9-4d5e-a3ef-317069b19dec`
	+ `6a66a183-b55e-4ffc-bb23-1efdafd74b12`
    + FIXED 18.7.23, except for some cases of *hors de*
+ Script didn't correctly identify proper nouns as nominals
    + NOW FIXED (4.7.23)
+ `loc_lemma_add` not being parsed correctly when there are numbers.
    + FIXED 18.7.23
+ Coordination with two different heads is one constituent
    + *au visage et en la bouche*
+ Annotation of *d'où*, e.g. `dbda067e-b40a-4d2d-9481-e8a61390282b`
    + FIXED 18.7.23
+ *haut* with a definite article analysed as a head, not sure we want this.
+ Ordering of heads in *là+dessus*, e.g `10912a66-b9fe-4545-84d9-e9331d34ee57`
+ *vers l'arrière* tagged as `vers+arriere` (`15a5a6b9-b6f3-4757-9161-a9aef421f3fc`)
    + FIXED 18.7.23
+ Preposition *voire* matched
    + `080bc2e1-3a2b-4a76-b048-0c3416a8254d`
    
## Specific constructions

+ *jeter à bas de* identified as a single constituent by the parser.

# Direct objects for *entrer*

*There generally aren't any DOs for entrer, but the parser still finds
quite a few*

## Common parser errors

*SCRIPT MODIFIED 14.7.23 to make it more cautious about accepting obj
arguments if it's told that the verb isn't usually transitive.*

+ Postverbal subjects, e.g. `f49d7cee-7ad1-40d6-8e08-e38351537872`
+ Extraposition structure with postverbal subjects, e.g. `2ff7f183-2c03-4b57-a2b6-15d7bf4e0eee`
+ Mis-read locatives in older constructions, e.g. transitive *dedans*
    + `a2ed6c07-182b-41ee-9aaf-b86d3a56debc`
+ Split subjects *nous... tous deux*

# Locative complements for *entrer*

## Errors which are are fixable with better filtering

+ *céans* not recognized as a locative, e.g. `346507c9-21a4-4fb2-9ef6-5f31ed4505d6`
+ *comme ça* recognized as locative, e.g. `c4965f7f-0f0b-4443-b379-6457c237eaf4`

## Bugs

+ Annotation of *par où* as, e.g. `9b4c543f-81f7-45cf-8316-2086c57c5368`
    + FIXED 14.7.23
+ Annotation of *à travers*, e.g. `540c5a58-ed8d-42b4-9b90-4b247ee00434`
    + FIXED 14.7.23 with c1_lemma
+ Annotation of *jusque à*, e.g. `6052a7b8-da2f-4908-9126-a6962c69469f`
    + FIXED 14.7.23 with c1_lemma
    
