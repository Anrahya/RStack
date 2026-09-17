# Data analysis

Define the question, unit of observation, population, time window, source version
and metric before calculating. Check freshness, missingness, duplicate keys,
units, category meanings and the denominator. Do not silently replace unknown
values with zero or omit failed attempts from an efficiency metric.

Inspect join cardinality and unmatched records before interpreting aggregates.
Reconcile totals against an independent simple calculation. Distinguish a
correlation from a causal result and an exploratory pattern from a held-out
confirmation. For model or workflow evaluation, keep grading information out of
candidate access and separate task diversity from repeated runs of one task.

Use reproducible queries or scripts tied to the actual input snapshot. Exercise
small known examples and adversarial cases that would expose a broken formula,
unit conversion or filter. Preserve enough provenance to rerun the result without
claiming access to unavailable data.

Report values with units and uncertainty appropriate to the sampling design.
Plot or summarize relevant distributions rather than only a favorable average.
If comparing variants, disclose missing pairs and changes in population, budget,
tooling or scoring. A fabricated demonstration dataset is not empirical evidence
about the user's actual system.
