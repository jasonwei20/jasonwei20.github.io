---
layout: archive
title: "Writing Tips"
permalink: /writing_tips/
author_profile: true
---

{% include base_path %}

I like Andrej Karpathy's, Tom Cormen's, and Sam Greydanus's writing.
These are some guidelines that I compiled, mostly from other people.

Well-written papers:
- [Sam Greydanus](https://arxiv.org/pdf/1906.01563.pdf)
- [Ryan Cotterell](https://arxiv.org/abs/1705.01684.pdf)
- [Justine Zhang](https://tisjune.github.io/research/)


General writing tips:

- The first sentence in a paragraph should tell me what that paragraph is about.
- X, so Y. -> X, *and so* Y. 
- The worst place to use *however* is at the beginning of a sentence (Tom Cormen).
- Use active voice.
- You can use the word *shall* to sound fancy.
- Don't use *while* when you mean *although*.
- Use verbs instead of gerunds when possible (the inclusion of -> including)
- Feel free to be creative, even in academic writing (my own opinion).
- Calculate -> compute (unless you're using a calculator)



General paper tips:

- Take elements from top conference papers that you like and try to incorporate them into your own paper, if applicable.
- Absolutely do not overstate the novelty of your paper. Good reviewers will notice.
- Try a creative title. I should not get tired when I read it. Tom Cormen suggests titles like 'Algol 68 with Fewer Tears', 'ViC*: Running out-of-memory instead of running out of memory", '50 shades of grey codes'.
- Your literature review be comprehensive and include all relevant papers and well-known papers in the area. Don't get rejected because you were too lazy too do a good literature review.
- Include math equations if relevant.
- Make sure your paper is exactly the page limit and not a single line less. Some tricks: delete spacing between figures and their captions, make the font in tables smaller. 
- If your paper isn't at the page limit, this could be an indicator that you should do more experiments. 
- You should make your code and data available, if possible.
- All your references should have links.
- After you finish your first draft, go through the entire paper and delete any unncessary words. Also check all the prepositions to make sure they're correct.



Figures and tables:

- Include a pull figure on the first page to give the reader an idea of what the paper will be about.
- Your tables should not have more lines (e.g., borders), than necessary.
- Should some tables be represented as graphs?
- For a multivariate function *z = f(x, y)*, try using a heatmap. They look colorful.



Tips specific to applied ML/DL papers in medical journals:

- It is good to have some sort of baseline approach for comparison, even if the point of your paper isn't the methods. This came up a lot in reviewer comments for me when I didn't include it.
- For methods papers, you should have a table comparing your results to other papers for a given benchmark task. You should also validate on multiple datasets.
- If your testing set is small, are you overfitting?
- If you're presenting a new application of deep learning, do some error analysis. What is your model doing well and what isn't it?
- What's the training time and runtime of your model?
- Can you do a cute t-SNE visualization?
- It's often nice to have a table that summarizes the dataset(s) you are using. This is a must if you're using a novel dataset. Maybe try a violin plot.
- For vision applications, it's always nice to have some LIME/CAM visualization to see what your model is looking at.
- You can display a confusion matrix as a heatmap.
- For multi-class precision/recall/f1 tables, try a plot like in Figure 3B <a href="https://www.nature.com/articles/s41386-018-0247-x" style="color:navy" target="_blank">here</a>.
- Include ROC and AUC if applicable, and show the point on the curve that the model is performing at.



Easiest reasons for a reviewer to reject you:

- No literature review
- No methodological innovation



Need more inspiration?:
- Tom Cormen's <a href="https://www.cs.dartmouth.edu/~cs191/" style="color:navy" target="_blank">writing class</a>.
- Tom Cormen's <a href="https://www.cs.dartmouth.edu/~thc/Cormen-rules.pdf" style="color:navy" target="_blank">usage rules</a>.
- Andrej Karpathy's <a href="http://karpathy.github.io/2016/09/07/phd/" style="color:navy" target="_blank">post</a> on PhD tips.
- <a href="https://greydanus.github.io/about.html" style="color:navy" target="_blank">Sam Greydanus</a>.
- Read <a href="http://yosinski.com/" style="color:navy" target="_blank">Jason Yosinki</a>.
- Read Steven King in your free time.