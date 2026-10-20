# Targets and baselines

Start with a specific target, such as synthetic activity class (0=still, 1=walking). Features may summarize acceleration and rotation, but subject identifiers, labels, and future measurements must not be features. Keep provenance alongside the feature table.

Use a majority-class baseline and a classical model before increasing complexity. This training uses scikit-learn logistic regression; neural networks are an optional follow-up once there is enough real, independently labeled data. Synthetic success demonstrates the pipeline, not effectiveness on people.

**Try:** create an imbalanced label array with 90 zeros and 10 ones. A model predicting only zero has 90% accuracy. What does balanced accuracy reveal?
