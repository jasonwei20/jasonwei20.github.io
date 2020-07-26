---
title: "Addendum on EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification"
permalink: /addendum_eda/
author_profile: true
---

{% include base_path %}

Written by Jason Wei on June 11, 2020. 

I did this paper from start to finish in about five weeks.
I was only 20 at the time&mdash;not even old enough to have a beer in the US&mdash;and frankly, I had not a clue how a transformer worked.

But by most metrics, this paper is pretty good. 
It was accepted to EMNLP with three positive reviews, and at the time that I write this addendum, it has more than 50 citations and 600+ stars on Github.
Moreover, in the highlight of my career so far, an admitted student I met at the MLT Open House at CMU this spring asked if I wrote "the EDA paper" and if I went to "Brown (or was it UPenn?)," and then proceeded to call my work "kind-of a famous paper."

I have talked to scores of people about these techniques at conferences, interviews, and open house days, and yet I still do not know why no one tried them before me (the closest I know of is "[Robust Training under Linguistic Adversity](https://www.aclweb.org/anthology/E17-2004.pdf)" by Li et al., though they do not use the word "augment" in their paper).
(If anyone knows, please send me a message.)
Hopefully they can be useful for your research.
If not, I hope this paper can at least be helpful to the aspiring researcher in a different way, perhaps best explained by Stephen King in his bestseller on creative writing, *On Writing* (apologies for his crudeness).

 > "Most writers can remember the first book he/she put down thinking: *I can do better than this. Hell, I am doing better than this.* What could be more encouraging to the struggling writer than to realize his/her work is unquestionably better than that of someone who actually got paid for his/her stuff?"