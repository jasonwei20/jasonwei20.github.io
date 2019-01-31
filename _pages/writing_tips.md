---
layout: archive
title: "Writing Tips"
permalink: /writing_tips/
author_profile: true
---

{% include base_path %}

Below are some tips, mostly from other people, that I've compiled over my limited experience in writing research papers. I like Andrej Karpathy and Tom Cormen's writing.

General tips:

- Read some top papers in the conference/journal before you begin.
- The first sentence in a paragraph should tell me what the point of the paragraph is.
- Include math equations if relevant.
- You should make your code and data available, if possible.
- After you finish your first draft, go through the entire paper and delete any unncessary words. Also check all the prepositions to make sure they're correct.
- It's almost always good to have some sort of baseline approach for comparison, even if the point of your paper isn't the methods. This came up a lot in reviewer comments for me when I didn't include it.
- For methods papers, you should have a table comparing your results to other papers for a given benchmark task. You should also validate on multiple datasets.
- If you haven't done an extensive literature review, reviewers will likely notice. If you miss a related paper that the reviewer happens to personally know of, your credibility immediately drops and you'll likely get rejected.
- If your testing set is small, are you overfitting?
- If you're presenting a new application of deep learning, do some error analysis. What is your model doing well and what isn't it?
- What's the training time and runtime of your model?

Conferences: 

- Please, please use LaTeX. It is important that the look and feel of your paper is correct.
- Try a creative title. I should not get tired when I read it. Tom Cormen suggests titles like 'Algol 68 with Fewer Tears', 'ViC*: Running out-of-memory instead of running out of memory", '50 shades of grey codes'.
- Make sure your paper is exactly the page limit and not a single line less. Some tricks: delete spacing between figures and their captions, make the font in tables smaller. 
- If your paper isn't at the page limit, this could be an indicator that you should do more experiments. 

Figures:

- Include a pull figure on the first page to give the reader an idea of what the paper will be about.
- It's often nice to have a table that summarizes the dataset(s) you are using. This is a must if you're using a novel dataset. 
- For vision applications, it's always nice to have some LIME/CAM visualization to see what your model is looking at.
- For multi-class precision/recall/f1 tables, try a plot like in Figure 3B <a href="https://www.nature.com/articles/s41386-018-0247-x" style="color:navy" target="_blank">here</a>.
- Include ROC and AUC if applicable, and show the point on the curve that the model is performing at.
- You can display a confusion matrix as a heatmap.
- For a multivariate function *z = f(x, y)*, try using a heatmap.

Some phrases that I like:

- "We propose/present a deep learning model that xyz." -Andrej Karpathy
- "Of note, we are the first to xyz." -Saeed Hassanpour
- "In closing, we xyz."
- "Board-certified" radiologist/pathologist sounds good for asserting dominance.
- Transition words I like: in addition, furthermore, moreover.

Need more inspiration?:

- Tom Cormen's <a href="https://www.cs.dartmouth.edu/~thc/Cormen-rules.pdf" style="color:navy" target="_blank">usage rules</a>.
- Andrej Karpathy's <a href="http://karpathy.github.io/2016/09/07/phd/" style="color:navy" target="_blank">post</a> on PhD tips.
- <a href="https://greydanus.github.io/about.html" style="color:navy" target="_blank">Sam Greydanus</a>.
- Read <a href="http://yosinski.com/" style="color:navy" target="_blank">Jason Yosinki</a>.
- Read Steven King in your free time.