# Window and cycle features

RMS is `sqrt(mean(x**2))`; it includes a DC component. Population standard deviation uses `ddof=0`. Peak-to-peak range is `max(x)-min(x)`. Compute these on fixed windows or event-defined cycles and preserve provenance.

Overlapping windows are correlated. Carry subject, session, and time bounds into the feature table so ML can split groups before evaluation. Never impute or standardize from the full dataset before a split.

**Review:** compute features for `[1,-1,1,-1]` by hand. Explain how an offset changes RMS and mean while leaving standard deviation unchanged.
