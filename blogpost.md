# Open source Logic-LLM

### Authors

---

*Abstract very short*
---

## Introduction
Logic-LM is a novel framework, proposed by Pan et al. (2023) \[1\], that combines Large Language Models (LLMs) and Symbolic Solvers for reasoning tasks . Leveraging the translative power of LLMs, they counterbalance potential inaccuracies in reasoning by employing Symbolic Solvers (Shanan, 2022) \[2\].

<!--Logic-LM, proposed by Pan et al. (2023) [1], introduces a novel framework that merges Large Language Models (LLMs) with Symbolic Solvers for reasoning tasks. Leveraging the translative power of LLMs, they counterbalance potential inaccuracies in reasoning by employing Symbolic Solvers [2]. Recent advancements in adapting LLMs for logical reasoning tasks have seen approaches like fine-tuning and in-context learning, which optimize LLMs' reasoning ability through specialized training modules or prompt-based step-by-step reasoning. While these methods operate directly over natural language, the Logic-LM framework stands out by utilizing symbolic language for reasoning, transferring complex tasks to external symbolic solvers while leveraging LLMs for problem formulation. Unlike prior neuro-symbolic methods, which often require specialized modules and suffer from optimization challenges, Logic-LM seamlessly integrates modern LLMs with symbolic logic, offering a more generalizable solution. Additionally, this work explores tool-augmented LLMs, extending their capabilities beyond language comprehension by integrating external tools for improved performance on logical reasoning tasks. Auto-formalization, widely applied in mathematical reasoning, finds a pioneering extension in Logic-LM to a broader range of logical reasoning tasks, bridging the gap between natural language understanding and formal logic with modern LLMs.-->

### Related work
<!-- Nog niet goed -->
Recent advancements in adapting Large Language Models (LLMs) for logical reasoning tasks can be categorized into two main approaches: fine-tuning and in-context learning. Fine-tuning methods optimize LLMs' reasoning ability through specialized training modules (Clark et al., 2020; Tafjord et al., 2022; Yang et al., 2022), while in-context learning designs prompts to elicit step-by-step reasoning. Chain-of-Thought prompting (Wei et al., 2022b; Wang et al., 2023) is an example of in-context learning, in which explanaitions are generated before the final answer. While these methods operate directly over natural language, the Logic-LM framework stands out by utilizing symbolic language for reasoning, transferring complex tasks to external symbolic solvers while leveraging LLMs for problem formulation. Unlike prior neuro-symbolic methods (Mao et al., 2019; Gupta et al., 2020; Manhaeve et al., 2021; Cai et al., 2021; Tian et al., 2022; Pryor et al., 2023), which often require specialized modules and suffer from optimization challenges, the Logic-LM framework integrates modern LLMs with symbolic logic without the need for complex module designs, offering a more generalizable solution. Additionally, this work explores tool-augmented LLMs, extending their capabilities beyond language comprehension by integrating external tools for improved performance on logical reasoning tasks. While auto-formalization has been widely applied in mathematical reasoning (Wu et al., 2022; Drori et al., 2022; He-Yueya et al., 2023; Jiang et al., 2023), Pan et al. (2023) pioneer its extension to a broader range of logical reasoning tasks, bridging the gap between natural language understanding and formal logic with modern LLMs.

### Logic-LM framework
<!--The Problem Formulation stage prompts an LLM to translate the problem into symbolic language, leveraging the model's few-shot generalization ability. We use four symbolic formulations to cover different types of logical reasoning problems. Then, in the Symbolic Reasoning stage, we call external solvers based on the problem type, such as Pyke for deductive reasoning or Z3 for SAT problems. Finally, the Result Interpreter translates the solver's output back into natural language. Additionally, a Self-Refiner module adjusts inaccurate logical formulations based on solver feedback. This framework reduces the burden on LLMs by focusing on symbolic representation rather than step-by-step reasoning.-->

The Logic-LM decomposes a logical reasoning problem into three stages: stages: *Problem Formulation*,
*Symbolic Reasoning*, and *Result Interpretation*. The *Problem Formulation* prompts an LLM to translate a natural language problem into symbolic language, utilizing the few-shot generalization ability of LLMs. The LLM is provided with instructions about the grammar of the symbolic language alongside in-context examples. Specifically, four different symbolic formulations are used to cover four common types of logical reasoning problems: deductive reasoning, firstorder logic reasoning, constraint satisfaction problem, and analytical reasoning. Afterwards, in the *Symbolic Reasoning* stage, external solvers perform inference on the symbolic representation. Based on the problem type a different solver is used, such as Pyke (Frederiksen, 2008) for deductive reasoning or Z3 (de Moura and Bjørner, 2008) for SAT problems. The *Result Interpreter* explains the output of the solver and maps it to the correct answer. Moreover, a self-refinement module is introduced which improves accuracy by iteratively revising symbolic formulations using error messages from the solvers. This module instructs the LLM to refine incorrect logical forms by promptinh it with the erroneous logic form, the solver’s error message, and a set of demonstrations showing common error cases and remedies.

### Experiments
The performance of three GPT models serving as underlying models for the Problem Formulator of Logic-LM (ChatGPT, GPT-3.5, and GPT-4) is evaluated against two baselines: 1) Standard LLMs, which leverage incontext learning to directly answer the question; and 2) Chain-of-Thought (CoT) (Wei et al., 2022b), which adopts a step-by-step problem-solving approach. The performance is evaluated across five logical reasoning datasets. *PrOntoQA* (Saparov and He, 2023)offers synthetic challenges for deductive reasoning, with the hardest 5-hop subset tested. *ProofWriter* (Tafjord et al., 2021) presents problems in a more natural language form under the open-world assumption, focusing on different levels of reasoning depth, with the depth-5 subset chosen for evaluation. *FOLIO* (Han et al., 2022), a challenging expert-written dataset, demands complex first-order logic reasoning. *LogicalDeduction* (Srivastava et al.,2022) from BigBench and *AR-LSAT* (Zhong et al., 2022) present real-world scenarios and analytical logic reasoning questions, respectively, adding diversity to the evaluation. 

<!--The performance of three GPT models serving as underlying models for the Problem Formulator of Logic-LM (ChatGPT, GPT-3.5, and GPT-4) is evaluated against two baselines: 1) Standard LLMs, which use in-context learning to answer questions directly; and 2) Chain-of-Thought (CoT), adopting a step-by-step problem-solving approach. The evaluation spans five logical reasoning datasets: PrOntoQA, ProofWriter, FOLIO, LogicalDeduction, and AR-LSAT, each offering distinct challenges. PrOntoQA provides synthetic challenges for deductive reasoning, while ProofWriter presents problems in a more natural language form. FOLIO demands complex first-order logic reasoning, while LogicalDeduction and AR-LSAT present real-world scenarios and analytical logic reasoning questions, respectively, adding diversity to the evaluation.-->

### Main results
Pan et al. (2023) present three main results. First, LOGIC-LM notably outperforms standard LLMs and Chain-of-Thought (CoT) across various datasets, showcasing the advantage of integrating LLMs with external symbolic solvers for logical reasoning. Second, GPT-4 exhibits superior performance compared to GPT-3.5, especially in standard prompting. Logic-LM further improves GPT-4 24.98% and 10.44% for standard
prompting and CoT prompting, respectively. Third, while CoT generally enhances LLM performance, its benefits vary across datasets, with less substantial or negative effects seen in certain scenarios. Additionally, the effectiveness of problem formulation, the robustness of reasoning, and the impact of self-refinement, highlight both the successes and challenges encountered in these areas.

<!--Pan et al. (2023) report three main results. First, LOGIC-LM notably outperforms standard LLMs and Chain-of-Thought (CoT) across various datasets, highlighting the advantage of integrating LLMs with external symbolic solvers for logical reasoning. Second, GPT-4 exhibits superior performance compared to GPT-3.5, especially in standard prompting. Logic-LM further improves GPT-4 by 24.98% and 10.44% for standard prompting and CoT prompting, respectively. Third, while CoT generally enhances LLM performance, its benefits vary across datasets, with less substantial or negative effects seen in certain scenarios. Additionally, the effectiveness of problem formulation, the robustness of reasoning, and the impact of self-refinement highlight both the successes and challenges encountered in these areas.-->

## <a name="reasons">Reasons for extension</a>
*Exposition of its weaknesses/strengths/potential which triggered your group to come up with a response.*
As outlined in the introduction, the Logic-LM framework relies on three LLMs: ChatGPT, GPT-3.5, and GPT-4. However, due to their closed-source nature, these models suffer from limited transparency, customization options, and opportunities for collaboration. Therefore,  integrating open-source LLMs into the Logic-LM framework would be beneficial, as it increases accessibility, usability and flexibility. 

The authors of Logic-LM pointed out a crucial constraint, stating that “the model’s applicability is inherently bounded by the expressiveness of the symbolic solver”. Currently, only four distinct symbolic solvers are employed, limiting the framework's scope to four specific types of logical reasoning problems. Despite this, the authors proposed a solution, emphasizing that “this limitation can be mitigated by integrating a more diverse set of symbolic solvers”. Therefore, incorporating an additional solver type expands the framework’s capabilities, which is facilitated by the inherent flexibility of its design. Moreover, this addition encourages the development of a versatile logic-solving model. 

## <a name="contribution">Novel contribution</a>
*Describe your novel contribution.*


## <a name="results">Results</a>
*Results of your work (link that part with the code in the jupyter notebook)*



## <a name="conclusion">Conclusion</a>



## Authors' Contributions
*example*
- Jonathan: Initial setup of codebase & implementation of architecture ablation studies, implementation of transformer architectures, implementation of FID metric, training of ablation models, wrote novel model architecture. Loss plots
- Ana: did ablation study for activation functions and normalization, bias research, model architecture diagram, wrote Image Editing with Diffusion Models (partly), Discovering Semantic Latent Space (training loss part), Model Architecture, Evaluating Diffusion Models and Concluding Remarks.
- Luc: did DM vs LDM research and notebook; wrote header, Image Editing Using Diffusion Models (partly), Recap on Diffusion Models, the Discovering Semantic Latent Space, Bias in Editing Directions (partly), Ablation Study, and Further Research: Latent Diffusion Models. 
- Eric: Structure of the repository, implementations, reproducibility experiment configurations, executions, visualizations, and analysis for "Reproduction of the Experiments", collaboration on the initial implementation of the transformer-based architecture, help as needed with run executions, figures, and tables for other sections.

## Bibliography

[1] Pan, L., Albalak, A., Wang, X., & Wang, W. Y. (2023). Logic-lm: Empowering large language models with symbolic solvers for faithful logical reasoning. arXiv preprint arXiv:2305.12295.

[2] Murray Shanahan. 2022. Talking about large language models. CoRR, abs/2212.03551.
