# Evaluation and uncertainty

Report test subjects, sample count, accuracy, balanced accuracy, confusion matrix, and a majority-class baseline. Label confusion-matrix axes (rows true, columns predicted). Report per-subject scores; a pooled score can hide one poorly performing participant.

Leave-one-subject-out evaluation holds out each subject in turn. Summarize mean and sample standard deviation of subject accuracies; that standard deviation describes variation across held-out subjects and is not a confidence interval. A subject-level bootstrap can estimate uncertainty with enough independent subjects, but tiny synthetic cohorts do not establish clinical performance.

**Report:** task, split, features, model, baseline, metrics, errors, limitations. Explain why high synthetic accuracy is not permission to attach predictions to a controller.
