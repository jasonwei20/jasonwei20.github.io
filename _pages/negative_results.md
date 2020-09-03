---
title: "Negative Results"
permalink: /failures/
author_profile: true
---

{% include base_path %}

Experiments that I tried seriously but did not produce substantial results.

## Machine Learning for NLP
1. **Augmentation classification as an auxiliary task for multi-task learning (Jul '20).** The idea here is to apply data augmentation for text in a multi-task learning setup where the primary task is the standard text classification task of interest and the auxiliary task is to classify what type of augmentation was applied to a sentence. The intuition is that the nuance needed to detect augmentation type can act as regularization and also allow the model to escape types of augmentation that don't work well. For BERT-avgpool and BERT-finetune on small dataset sizes, this doesn't seem to help. Experimentally, however, augmentation doesn't help too much for BERT-finetune and the auxiliary task just seems to be fighting the original training loss, leading to substantially worse performance. One explanation is that BERT pre-training already encodes a lot of the information that would have been learned here.
1. **Gradient comparisons as text classification (Jul '20).** The gradients between two correctly-labeled examples should be more similar than the gradients of a correctly-labeled example and an incorrectly labeled example. Comparing the gradient of a test example, computed by assigning labels, with gradients of correctly-labeled known examples does the same thing as just running the example through a classifier trained with the training set. [[Blog post]](https://medium.com/@jason.20/classification-by-per-example-gradient-similarities-looks-at-the-same-thing-as-output-confidences-1b13c2be60bd)
1. **Noising-based curriculum learning for text classification (Jun '20).** Classifying noisy data is harder than original data. So one idea is to first train on original data and then do a second fine-tuning stage on original plus noisy data. For BERT-avgpool (average the hidden state outputs of BERT encoder and then classify with MLP), this does not improve over vanilla data augmentation.
1. **Weighted gradient aggregation for reducing label noise in sentence classification (Jun '20).** My [undergraduate thesis](https://www.cs.dartmouth.edu/~trdata/reports/TR2020-899.pdf) showed a minimally invasive way to reduce label noise by looking at gradient similarities. I tried applying this method to text classification, but when the text classification is only for few classes (e.g., two) then incorrect examples will agree with each other.
1. **Noising prediction as self-supervised learning (Mar '20).** I hypothesized a task for self-supervised learning where a model would predict which type of task was applied text, and ran experiments with CNNs for small datasets. Models with this pre-training didn't do better than vanilla training. *Learnings*: don't do pre-training with CNNs or small datasets. Also, the pre-training task should also be similar to the downstream task (?)

## CV 
1. **Confidence-based curriculum learning for medical images (Jun '20).** Classifying colorectal polyp histopathology images that are ordered based on the confidence of a pre-trained classifier doesn't improve much over vanilla training.
2. **Confidence-based curriculum learning for pre-text CV tasks (Feb-Apr '20).** Applying curriculum learning to a self-supervised task based on confidence of the model should improve perform on downstream classification tasks. Curriculum learning only improved pre-text task performance marginally, and this did not translate to better performance on downstream tasks, although coding issues with the fair benchmark repo could have a role in the evaluation here.
