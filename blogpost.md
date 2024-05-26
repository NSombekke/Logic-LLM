# Logic-LM integrated with Llama-3 and Linear Temporal Logic

### Authors
Niels Sombekke, AnneLouise de Boer, Roos Hutter, Rens Baas, Sacha Buijs
---

*Abstract*
*We still need to write the abstract*
---

## Introduction
Logic-LM is a novel framework, proposed by Pan et al. (2023) \[1\], that combines Large Language Models (LLMs) and Symbolic Solvers for reasoning tasks. Leveraging the translative power of LLMs, they counterbalance potential inaccuracies in reasoning by employing Symbolic Solvers (Shanan, 2022) \[2\].
Recent advancements in adapting Large Language Models (LLMs) for logical reasoning tasks can be categorized into two main approaches: fine-tuning and in-context learning. Fine-tuning methods optimize LLMs' reasoning ability through specialized training modules (Clark et al., 2020; Tafjord et al., 2022; Yang et al., 2022), while in-context learning designs prompts to elicit step-by-step reasoning. Chain-of-Thought prompting (Wei et al., 2022b; Wang et al., 2023) is an example of in-context learning, in which explanaitions are generated before the final answer. While these methods operate directly over natural language, the Logic-LM framework stands out by utilizing symbolic language for reasoning, transferring complex tasks to external symbolic solvers while leveraging LLMs for problem formulation. Unlike prior neuro-symbolic methods (Mao et al., 2019; Gupta et al., 2020; Manhaeve et al., 2021; Cai et al., 2021; Tian et al., 2022; Pryor et al., 2023), which often require specialized modules and suffer from optimization challenges, the Logic-LM framework integrates modern LLMs with symbolic logic without the need for complex module designs, offering a more generalizable solution. Additionally, this work explores tool-augmented LLMs, extending their capabilities beyond language comprehension by integrating external tools for improved performance on logical reasoning tasks. While auto-formalization has been widely applied in mathematical reasoning (Wu et al., 2022; Drori et al., 2022; He-Yueya et al., 2023; Jiang et al., 2023), Pan et al. (2023) pioneer its extension to a broader range of logical reasoning tasks, bridging the gap between natural language understanding and formal logic with modern LLMs.

<table align="center">
  <tr align="center">
      <td><img src="src/Logic_LM_framework.png" width=800></td>
  </tr>
  <tr align="left">
    <td colspan=2><b>Figure 1.</b>  Overview of the LOGIC-LM model, which consists of three modules: (1) Problem Formulator generates a symbolic representation for the input problem with LLMs via in-context learning (2) Symbolic Reasoner performs logical inference on the formulated problem, and (3) Result Interpreter interprets the symbolic answer. Figure by Pan et al. (2023) [1]</td>
  </tr>
</table>

<!--The Problem Formulation stage prompts an LLM to translate the problem into symbolic language, leveraging the model's few-shot generalization ability. We use four symbolic formulations to cover different types of logical reasoning problems. Then, in the Symbolic Reasoning stage, we call external solvers based on the problem type, such as Pyke for deductive reasoning or Z3 for SAT problems. Finally, the Result Interpreter translates the solver's output back into natural language. Additionally, a Self-Refiner module adjusts inaccurate logical formulations based on solver feedback. This framework reduces the burden on LLMs by focusing on symbolic representation rather than step-by-step reasoning.-->

The Logic-LM decomposes a logical reasoning problem into three stages: stages: *Problem Formulation*,
*Symbolic Reasoning*, and *Result Interpretation* (Figure 1). The *Problem Formulation* prompts an LLM to translate a natural language problem into symbolic language, utilizing the few-shot generalization ability of LLMs. The LLM is provided with instructions about the grammar of the symbolic language alongside in-context examples. Specifically, four different symbolic formulations are used to cover four common types of logical reasoning problems: deductive reasoning, firstorder logic reasoning, constraint satisfaction problem, and analytical reasoning (Table 1). Afterwards, in the *Symbolic Reasoning* stage, external solvers perform inference on the symbolic representation. Based on the problem type a different solver is used, such as Pyke (Frederiksen, 2008) for deductive reasoning or Z3 (de Moura and Bjørner, 2008) for SAT problems. The *Result Interpreter* explains the output of the solver and maps it to the correct answer. Moreover, a self-refinement module is introduced which improves accuracy by iteratively revising symbolic formulations using error messages from the solvers. This module instructs the LLM to refine incorrect logical forms by prompting it with the erroneous logic form, the solver’s error message, and a set of demonstrations showing common error cases and remedies.

| Problem                | Formulation | NL Sentence                                                                 |            Symbolic Formulation                                     |                Solver                  |      Dataset       |      
|------------------------|-------------|-----------------------------------------------------------------------------|---------------------------------------------------------|-----------------------------------------------------|-------------------|
| Deductive Reasoning    | LP          | If the circuit is complete and the circuit has the light bulb then the light bulb is glowing. | Complete(Circuit, True) ∧ Has(Circuit, LightBulb) → Glowing(LightBulb, True) | Pyke              | ProntoQA, ProofWriter |
| First-Order Logic      | FOL         | A Czech person wrote a book in 1946.                                        | ∃x₂∃x₁(Czech(x₁) ∧ Author(x₂, x₁) ∧ Book(x₂) ∧ Publish(x₂, 1946)) | Prover9           | FOLIO                 |
| Constraint Satisfaction| CSP         | On a shelf, there are five books. The blue book is to the right of the yellow book. | blue_book ∈ {1, 2, 3, 4, 5} yellow_book ∈ {1, 2, 3, 4, 5} blue_book > yellow_book | python-constraint | LogicalDeduction      |
| Analytical Reasoning   | SAT         | Xena and exactly three other technicians repair radios                      | repairs(Xena, radios) ∧ Count([t:technicians], t ≠ Xena ∧ repairs(t, radios)) == 3 | Z3                | AR-LSAT               |
| Temporal reasoning  | LTL         | Go through the red room to the second floor.                    |F(red_room ∧ F (second_floor)) | Buchi Automaton                | Drone Planning             |

**Table 1**: A summary of the symbolic formulations and symbolic solvers we use for cateogies of logical reasoning in our study.


The performance of three GPT models serving as underlying models for the Problem Formulator of Logic-LM (ChatGPT, GPT-3.5, and GPT-4) is evaluated against two baselines: 1) Standard LLMs, which leverage in-context learning to directly answer the question; and 2) Chain-of-Thought (CoT) (Wei et al., 2022b), which adopts a step-by-step problem-solving approach. The performance is evaluated across five logical reasoning datasets. *PrOntoQA* (Saparov and He, 2023) offers synthetic challenges for deductive reasoning, with the hardest 5-hop subset tested. *ProofWriter* (Tafjord et al., 2021) presents problems in a more natural language form under the open-world assumption, focusing on different levels of reasoning depth, with the depth-5 subset chosen for evaluation. *FOLIO* (Han et al., 2022), a challenging expert-written dataset, demands complex first-order logic reasoning. *LogicalDeduction* (Srivastava et al.,2022) from BigBench and *AR-LSAT* (Zhong et al., 2022) present real-world scenarios and analytical logic reasoning questions, respectively. Additionally, the effect of the refiner is researched by investigating the accuracy and the executable rates on the FOLIO dataset across different rounds of self refinement. 

<!--The performance of three GPT models serving as underlying models for the Problem Formulator of Logic-LM (ChatGPT, GPT-3.5, and GPT-4) is evaluated against two baselines: 1) Standard LLMs, which use in-context learning to answer questions directly; and 2) Chain-of-Thought (CoT), adopting a step-by-step problem-solving approach. The evaluation spans five logical reasoning datasets: PrOntoQA, ProofWriter, FOLIO, LogicalDeduction, and AR-LSAT, each offering distinct challenges. PrOntoQA provides synthetic challenges for deductive reasoning, while ProofWriter presents problems in a more natural language form. FOLIO demands complex first-order logic reasoning, while LogicalDeduction and AR-LSAT present real-world scenarios and analytical logic reasoning questions, respectively, adding diversity to the evaluation.-->

Pan et al. (2023) present three main results. First, LOGIC-LM notably outperforms standard LLMs and Chain-of-Thought (CoT) across various datasets, showcasing the advantage of integrating LLMs with external symbolic solvers for logical reasoning. Second, GPT-4 exhibits superior performance compared to GPT-3.5, especially in standard prompting. Logic-LM further improves GPT-4 24.98% and 10.44% for standard
prompting and CoT prompting, respectively. Third, while CoT generally enhances LLM performance, its benefits vary across datasets, with less substantial or negative effects seen in certain scenarios. Additionally, the effectiveness of problem formulation, the robustness of reasoning, and the impact of self-refinement, highlight both the successes and challenges encountered in these areas.

<!--Pan et al. (2023) report three main results. First, LOGIC-LM notably outperforms standard LLMs and Chain-of-Thought (CoT) across various datasets, highlighting the advantage of integrating LLMs with external symbolic solvers for logical reasoning. Second, GPT-4 exhibits superior performance compared to GPT-3.5, especially in standard prompting. Logic-LM further improves GPT-4 by 24.98% and 10.44% for standard prompting and CoT prompting, respectively. Third, while CoT generally enhances LLM performance, its benefits vary across datasets, with less substantial or negative effects seen in certain scenarios. Additionally, the effectiveness of problem formulation, the robustness of reasoning, and the impact of self-refinement highlight both the successes and challenges encountered in these areas.-->

## <a name="reasons">Reasons for extension</a>
As outlined in the introduction, the Logic-LM framework is tested on three LLMs: ChatGPT, GPT-3.5, and GPT-4. However, due to their closed-source nature, these models suffer from limited transparency, customization options, and opportunities for collaboration. Therefore, integrating open-source LLMs into the Logic-LM framework would be beneficial, as it increases accessibility, usability and flexibility. For this first extension, we included two versions of the state-of-the-art model Llama-3.

The authors of Logic-LM pointed out a crucial constraint, stating that “the model’s applicability is inherently bounded by the expressiveness of the symbolic solver” (Pan et al., 2023). Currently, the framework utilizes only four distinct symbolic solvers, restricting its scope to four specific types of logical reasoning problems. The current solvers in Logic-LM do not facilitate reasoning about temporal aspects, which limits the model's applicability in scenarios where time-based reasoning is essential. Therefore we opted to include Linear Temporal Logic into the framework. LTL allows for the encoding of formulas about the future of paths, enabling the framework to handle tasks that require an understanding of temporal sequences and future events. By integrating LTL into the Logic-LM framework, we can extend its functionality to encompass temporal logic reasoning, thus broadening its applicability and making it a more powerful tool for a variety of logical reasoning tasks.

Additionally, we will reproduce the results of the original paper to investigate its reproducibility. As the authors utilized closed-source models, we have opted to reproduce the results on a smaller scale using the web version of ChatGPT.

In summary, our contributions are threefold:

1. Making Logic-LM open-source to enhance accessibility.
2. Extending Logic-LM by integrating Linear Temporal Logic.
3. Reproducing the results of the original paper to investigate its reproducibility.


## <a name="open_source">Extension: Open-source models</a>
Our first extension is making Logic-LM work with open-source language models, instead of closed-source models like ChatGPT. To make the application as flexible as possible, this was applied by using models from the Huggingface library (https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct). Two versions of the current state-of-the-art open-source model Llama-3 have been utilized<!--(TODO add ref)-->. First, the smaller 8B version of the model is implemented and evaluated to see how well Logic-LM performs with a lower resource model. Additionally, the larger version of Llama-3 (70B) is utilized to extend Logic-LM, as it is significantly larger it is expected it outperforms the 8B variant. Both models are be compared with the GPT models used by the original author to see how SoTA open-source models compare to closed-source models. 

### Experiments
Following the methodology of the original paper we evaluate the two Llama3 models on five common logical reasoning datasets (as explained in the introduction). The models are compaired against 2 baselines 1) Standard LLMs;
and 2) Chain-of-Thought (CoT) (Wei et al., 2022b). Follwing Pan et al (TODO bron) we ensure fair comparisons, by using the same in-context examples for all models. For reproducibility, we set the temperature to 0 and select the highest-probability response from the LLMs. We evaluate model performance based on the accuracy of selecting the correct answer from multiple-choice questions. Additionally, we the research the effect of the rifiner on the two Llama-3 models by investigating the accuracy and the executable rates on the FOLIO dataset across different rounds of self refinement. 


## <a name="ltl">Extension: Linear Temporal Logic</a>
Second, we extend the Logic-LLM by introducing Linear-time Temporal Logic (LTL), which enhances standard propositional logic to express properties that hold over time-based trajectories. This extension is particularly useful in robotics and automated planning, where paths must comply with temporal constraints. 

The integration of Linear Temporal Logic (LTL) in Logic-LM involves several components, as illustrated in Figure 2. The input problem consists of a context, a question, and three multiple-choice options. The context sets the environment for answering the question. The problem formulator translates the question and options into logic formulas suitable for the solver. Specifically, the question is first converted into an easier canonical LTL representation, and then into the raw LTL formula. The options are translated into runs. The symbolic reasoner then evaluates each run to determine if it satisfies the LTL formula using a Büchi automaton. These results are passed to the result interpreter, which generates the answer. We will test and evaluate this extension based on a drone planning scenario (TODO bron dataset). Additionally we perform an experiment evaluating the performance of three LLMs in converting natural language to LTL and runs. Further details are provided in the following sections.


<table align="center">
  <tr align="center">
      <td><img src="src/pipeline_ltl.png" width=700></td>
  </tr>
  <tr align="left">
    <td colspan=2><b>Figure 1.</b> Overview of the LOGIC-LM model extended for LTL, which consists of three modules: (1) Problem Formulator generates a LTL formula and runs for the input question and options respectively with LLMs via in-context learning (2) Symbolic Reasoner performs logical inference on the formulated problem via a Büchi automaton, and (3) Result Interpreter interprets the symbolic answer.</td>
  </tr>
</table> 


**Semantics of LTL**

LTL's semantics can effectively capture command specifications in the temporal domain. Formulas in LTL over the set of atomic propositions ($P$) adhere to the grammar below. For example, to express the statement "A cat never sleeps" in LTL, you would write $G \neg sleep$ in temporal logic. In this formula, the $G$  operator (Globally) indicates that the property it precedes must hold at all times in the future, and the $\neg$ operator (Negation) indicates that the "sleep" property does not hold.

$$
\begin{align*}
\text{Syntax} & \quad \text{Description} \\
p & \quad \text{Atomic Proposition } p \in P \\
\neg \varphi & \quad \text{Negation} \\
\varphi \land \psi & \quad \text{And} \\
\varphi \lor \psi & \quad \text{Or} \\
\varphi \Rightarrow \psi & \quad \text{Imply} \\
\varphi \mathcal{U} \psi & \quad \varphi \text{ Until } \psi \\
F \varphi & \quad \text{Eventually} \\
X \varphi & \quad \text{Next} \\
G \varphi & \quad \text{Always}
\end{align*}
$$

Let $\psi$ be an LTL formula defined over the set of propositions $P$. 
For $0 \leq i \leq n$, through induction one can define if $\psi$ is true at instant $i$ (written $w, i \models \psi$) as:
- $w, i \models p$ iff $p \in L(w_0)$ 
- $w, i \models \neg \psi$ iff $w, i \not\models \psi$
- $w, i \models \psi_1 \land \psi_2$ iff $w, i \models \psi_1$ and $w, i \models \psi_2$
- $w, i \models X \psi$ iff $i < n$ and $w, i+1 \models \psi$
- $w, i \models F \psi$ iff $\exists j \geq i$ such that $w, j \models \psi$
- $w, i \models \psi_1 \mathcal{U} \psi_2$ iff there exists a $j$ with $i \le j \le n$ s.t. $w, j \models \psi_2$ and for all $i \le k < j$, $w, k \models \psi_1$
- 

### Problem Formulator

We utilize two Llama-3 models to convert natural language into Linear Temporal Logic (LTL) tasks and runs based on the context attributes (e.g., planning domain), the question, and the options (Figure 1, step 1). We provide the models with clear instructions and a few examples to facilitate few-shot learning. This approach helps establish a correspondence between natural language commands and their respective LTL formulas and runs. With the given prompts, the LLMs are directed to generate these LTL formulas and runs from natural language inputs effectively. (TODO deze zin lijkt overbodig --> )The conversion from natural language to LTL has been predominantly studied within the field of robotics [9]. 

For illustration, consider the following Natural language commands $\mu$, and their corresponding LTL formula $\psi_{\mu}$, and explanation dictionary $(D_{\psi})$ generated by a LLM.  (TODO wat is de explanaition dictionary)

> **$\mu:$ "Always avoid the green room and navigate to the third floor."**
> 
> $\psi_{\mu}$: $G( \neg greenroom) \land F thirdfloor$
> 
> $D_{\psi}$: {"Always avoid the green room": "G(¬greenroom)","Navigate to the third floor": "F thirdfloor"}


<table align="center">
  <tr align="center">
      <td><img src="src/pipeline.jpg" width=800></td>
  </tr>
  <tr align="left">
    <td colspan=2><b>Figure 2.</b>  Pipeline: Converting Natural Language to Linear Temporal Logic for Multiple Choice Answering. (TODO dit plaatje klopt vlgs mij niet, de multiple choice antwoorden zijn vragen nml?</td>
  </tr>
</table>

#### Prompt Engineering
Since Large language models are predominantly trained on natural language, they may struggle converting natural language directly into Linear Temporal Logic (LTL) formulas. The syntax of LTL (e.g. X, U, and F) is quite different from typical natural language constructs. To address this distribution shift, a study by Pan et al. (2023) proposes creating a *canonical* representation that aligns more closely with natural language [8]. For the same reason Cosler et al. (2023) prompt the LLM to turn $\mu$ into an intermediate *canoncial form*, shown as *sub-translations*, before mapping the the sentence into an LTL formula [5]. Each translation accompanies a translation dictionary in canonical form, through which th LLM is asked to explain its steps. We will use their prompting technique. (TODO wij hebben geen translation dictionary in de prompt)

The outline below encapsulates our prompt setup, comprising three main sections — (1) LTL specification for the conversion of Natural Language to LTL, (2) the conversion of multiple choice options to traces, and (3) few-shot examples. All in all, the prompt serves as a structured framework for generating LTL formulas and traces from natural language inputs.

>**Prompt**
>
>Given a context, question and options. The task is to first parse the question into a canonical formular and then from this formula to raw LTL formula. Also the options need to parsed into traces.
Below an explanaition is given of all the input you will recieve and what you should do with it.
>
>**Context**: Declares the scene in which the question needs to be answered. Use this knowledge to parse the question and the options.
>
>***Question**: Contains the question that needs to be answered. The task is to parse the question into a canonical formula and then based on the canonical formular to a raw LTL formula.*
>
>*Your raw LTL formula answers always need to follow the following output format and you always have to try to provide a LTL formula. You may repeat your answers.*
>
>*Remember that U means "until", G means "globally", F means "eventually", which means GF means "infinitely often".*
>
>*The formula should only contain atomic propositions or operators ||, &, !, U, G, F.*
>
>***Options**: The options need to be parsed into traces. These traces need to be a list ([]) containing dictionaries for each timestep ({}). In each dictionary the state of the corresponding timestep is given.*
>
>[Few shot examples]
>
>
The addition of a context in the prompt is not always necessary for correct LTL generation as the LLM is expected to infer when predictes have a mutually exclusive (mutex) relation (e.g. the predicates sleeping and eating can not hold at the same time). However, we are utilizing a drone planning dataset that contains spefic constraints, such as the impossibility of the drone simultaneously occupying the third floor and a particular room on the first floor. Therefore prompts enriched with a context are utilized in this study.

> **Context**:
>  *Our environment consists of grid-based rooms across multiple floors. Each floor features distinct rooms: the first floor has a red room and a yellow room, the second  floor has a green room, and the third floor includes a purple room, an orange room, and Landmark 1.* *The drone’s movement is limited to one floor and not more than one  room at a time within this structured environment. This setup is crucial for guiding effective planning and decision-making processes within the context of our problem.*
> 
> **Question:**
> Always avoid the green room and navigate to the third floor. Which one of the following is a possible path for the drone to follow?
> 
> **Options:**
> 
> (A) From the third floor go to the green room and stay there,
> 
> (B) Go inside the red room and then move to the green room,
> 
> (C) Go to the second floor passing the yellow room and then go to the third floor


### <a name="ltl">Symbolic Reasoner</a>
(TODO miss kan dit minder technisch?)

After the problem formulator has translated the natural language question into LTL and options into runs, we pass them to the logical reasoner (Figure 1, step 2). This reasoner checks for the validity of runs, verifying whether a given run satisfies the specified LTL formula. Runs are either accepted or rejected based on their compliance with the LTL formula, and consequently, the model is able to select one of the multiple-choice answers. 

We employ a Python module to derive its associated Deterministic Finite State Automaton $M_{\phi}$. We integrate the *Flloat* Python library (TODO bron) to translate LTL formulas (in CNF form) with finite-trace semantics into a minimal Deterministic Finite State Automaton (DFA) using MONA [3] (TODO wat is mona?). This conversion is guaranteed by Theorem 1. The resultigng  DFA ($M_{\phi}$) encapsulates the temporal constraints specified by the LTL formula, enabling efficient reasoning over finite traces. The trace-based satisfiability reasoning enhances the framework's capability to address temporal aspects of logical reasoning problems.

**Theorem 1** [Vardi and Wolper, 1994 [10]]: For any LTL formula $\psi$, a Büchi automaton $M_{\psi}$ can be constructed, having a number of states that is at most exponential in the length of $\psi$.  The language of $M_{\psi}$, denoted as $L(M_{\psi})$, encompasses the set of models of $\psi$.

The input words **w** of the Büchi automaton ($M_{\psi}$) can be infinite sequences $\sigma_0 \sigma_1 ... \sigma_n \in \Sigma^{w}$ [7]. A *run* of the automaton $(M_{\psi})$ on the word  **w** is sequence of states $\rho = q_0q_1q_2...$, where each state is a set of propositions. The initial state is $q_0$ and subsequent states are defined throught the transition function $q_{i+1} = \Delta(q_i,\sigma_i)$. The language of the automaton $M_{\psi}$ ($L(M_{\psi})$), is a set of *words* characterized by the presence of an accepting run. In this case each accepting run is a valid sequence of states that holds in the automaton. 

<!--(TODO add ref)-->
**Definition 1: (Büchi automaton)**: A deterministic Büchi automaton (DBA) is a tuple $M = (Q, \sum, \Delta, Q_0, F)$ where:
- $Q$ is a finite set of automaton states,
- $\Sigma$ is a finite alphabet of the automaton ($|\Sigma| = 2^{|P|}$),
- $\Delta : Q \times \sum  \rightarrow 2^{Q}$ is the transition function,
- $q_0 \subseteq Q$ is the set of initial stats
- $F \subseteq Q$ is the set of accepting states.

A word **w** is accepted by an automaton ($M_{\psi}$) if its run $\rho$ meets the condition $\lim(\rho) \cap F \neq \emptyset$. Meaning that that the run reaches at least one accepting state in **F**. 


$L(M_{\psi}) = \\{ w \in \Sigma^{w} | w \text{ is accepted by}  M_{\psi} \\}$

For each subplan $q_i$ of the run, the language function $L$ assigns a symbol $\sigma \in \Sigma$. These symbols collectively form a word **w** representing the sequence of symbols observed along the trace. This word **w** is then evaluated against the acceptance conditions of the DBA $M_{\psi}$. The language $L(M_{\psi})$ defines a set of infinite runs that the DFA can recognize. If **w** satisfies these acceptance conditions, then the finite run $\rho_{\psi}$ satisfies the LTL formula. Finite runs $\rho_{\psi}$ satisfiy the LTL if the word $ **w** = L(q_0)L(q_1)...L(q_n)$ is acceptable in $L(M_{\psi})$. 

Step 5 in Figure 2 shows an example output of runs corresponding to options (A) and (B). In this step, the generated runs are evaluated against the associated Deterministic Finite Automaton $M_{\psi}$ to determine their validity.

### Result interpreter
Finally, the result interpreter translates the results returned from the symbolic solver back to a natural language answer (Figure 1, step 3). The symbolic reasoner returns "True" or "False" for each of the runs (options), this results in a list. From this list the results interpreter takes the index of the "True" value and maps it to the letter corresponding to the correct answer, *e.g. translating [True, False, False] to "the answer is A"*.

### Experiments
We evaluate LOGIC-LM LTL extension on a dataset derived from commands in the *drone planning* domain, adapted from [8]. This test set is generated from the planning domain introduced by [8], This environment is a 3D grid world that consists of three floors, six rooms, and a single landmark (Figure 2). We created a test set of 50 entries with each three multiple-choice options from their natural language descriptions and corresponding LTL formulas. Mirroring the original paper, we evaluate the LOGIC-LM LTL extension against 2 baselines:  1) Standard LLMs; and 2) Chain-of-Thought (CoT) (Wei et al., 2022b). Additionally we perform an experiment evaluating how well various LLMs convert Natural Language to LTL, this will be further discussed in the following section.

<table align="center">
  <tr align="center">
      <td><img src="src/drone_domain.png" width=300></td>
  </tr>
  <tr align="left">
    <td colspan=2><b>Figure 2.</b> Planning domain for the drone navigation. Figure by [8].</td>
  </tr>
</table> 

#### Natural language to LTL
We aim to evaluate how well LLMs performs the conversion task from natural language to LTL in cases where it needs to generalize from few examples (few-shot learning). The evaluation consists of two stages: (1) the conversion of the natural language command into LTL, and (2) the subsequent conversion of the multiple choice options (each formlated in natural language) into runs. 

We test the parsing on two datasets. The first dataset is the drone planning dataset, which is priorly discussed and used for the Logic-LM LTL extension evaluation. The second dataset consists of 36 benchmark intances crafted by experts in the nl2spec study [5]. Each of these examples has been selected by LTL experts to cover a variety of ambiguities and complexities. We use their formatted intances, in addition we have prompted the LLM to replaced the propositions a,b,c,d to create more realistic sentences. For example: 

> $\mu:$ Every meal is eventually followed by dessert. $\leftrightarrow$ G(meal -> F dessert).
> 
> $\mu:$ Whenever a car starts, the engine revs three steps later. $\leftrightarrow$ G(car_starts -> X X X engine_revs).

The first dataset will be used to test both the initial conversion and the subsequent generation of runs, while the second dataset will be used to test solely the initial conversion from natural language to LTL.


## Reprodcing the original results
(TODO roos, duidelijker maken) Pan et al. (2023) employed three closed-source LLMs: ChatGPT, GPT-3.5, and GPT-4. Our extension of the Logic-LM involves open-source LLMs. However, ChatGPT is publicly accessible for manual query-based messaging. To validate the claims of Pan et al. (2023), we queried ChatGPT five times for each logic type, presenting the prompt and a new problem and question.

## <a name="results">Results</a>
### <a name="general results">LLama as a open source LLM for Logic-LM</a>
<table align="center">
	<tr align="center">
		<th align="left"></th>
		<th></th>
		<th>Llama-3 (8B)</th>
		<th></th>
		<th></th>
		<th>Llama-3 (70B)</th>
		<th></th>
	</tr>
	<tr align="center">
		<th align="left">Dataset</th>
		<th>Standard</th>
		<th>CoT</th>
		<th>Logic-LM</th>
		<th>Standard</th>
		<th>CoT</th>
		<th>Logic-LM</th>
	</tr>
	<tr align="center">
		<td align="left">ProntoQA</td>
		<td>48.80</td>
		<td><b>81.00</b></td>
		<td>67.40</td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td align="left">Proofwriter</td>
		<td>34.33</td>
		<td><b>49.17</b></td>
		<td>37.83</td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td align="left">FOLIO</td>
		<td><b>51.96</b></td>
		<td>51.00</td>
		<td>36.27</td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td align="left">LogicalDeduction</td>
		<td>35.33</td>
		<td>39.00</td>
		<td><b>60.67</b></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td align="left">AR-LSAT</td>
		<td><b>24.68</b></td>
		<td>20.80</td>
		<td>15.15</td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="left">
		<td colspan=7><b>Table 1.</b> Accuracy of standard prompting (Standard), chain-of-thought prompting (CoT), and our method (LOGICLM, without self-refinement) across five reasoning datasets using the Llama-3 model. The best results for each base LLM are highlighted.</td>
	</tr>
</table>

Table 1 shows the results of the experiments with the open-source model.  It displays that Logic-LM only scored highest on the LogicalDeduction dataset, where it scored 60.67 compared to 35.33 and 39.00 for Standard and CoT respectively. For the other datasets Logic-LM got outperformed by either the Standard or the CoT model. <!--TODO: Insert % of how much better/worse-->

Comparing these results to the GPT model results from the original paper (Pan et al., 2023), we observe that Llama generally performs worse than the GPT models. Logic-LM has significantly lower scores compared to all GPT models for the Proofwriter, FOLIO and AR-LSAT dataset and slightly lower scores for the LogicalDeduction dataset. Only on the PrOntoQA Llama achieved a higher score than gpt-3.5-turbo, while still having worse scores when using the other GPT models. For the Standard and CoT method we observe similar performance to gpt-3.5-turbo while also being outperformed by the other GPT models. (*More results and analysis will follow in final version*)


#### <a name="sr results">Self-refinement</a>
<table align="center">
	<tr align="center">
		<th align="left"></th>
		<th></th>
		<th>Llama-3 (8B)</th>
		<th></th>
		<th>Llama-3 (70B)</th>
		<th></th>
	</tr>
	<tr align="center">
		<th align="left">Dataset</th>
		<th>Refinement</th>
		<th>Exec-rate</th>
		<th>Exec-acc</th>
		<th>Exec-rate</th>
		<th>Exec-acc</th>
	</tr>
	<tr align="center">
		<td align="left">ProntoQA</td>
		<td>-</td>
		<td>91.60</td>
		<td>69.65</td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td ></td>
		<td>+</td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td align="left">Proofwriter</td>
		<td>-</td>
		<td>13.00</td>
		<td>70.51</td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td ></td>
		<td>+</td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td align="left">FOLIO</td>
		<td>-</td>
		<td>37.25</td>
		<td>48.68</td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td ></td>
		<td>+</td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td align="left">LogicalDeduction</td>
		<td>-</td>
		<td>100.00</td>
		<td>60.67</td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td ></td>
		<td>+</td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td align="left">AR-LSAT</td>
		<td>-</td>
		<td>20.35</td>
		<td>21.28</td>
		<td></td>
		<td></td>
	</tr>
	<tr align="center">
		<td ></td>
		<td>+</td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr align="left">
		<td colspan=7><b>Table 2.</b> Comparison of self-refinement on small and large LLama-3 models</td>
	</tr>
</table>
Table 2 displays a comparison of self-refinement. (*More results and analysis will follow in final version*)

### <a name="LTL results">LTL extension</a>
##### (1) Effectiveness of Problem Formulator
By testing the NL to LTL conversion on the **nl2spec** dataset, we seek to understand how well the LLM can handle the translation from natural language to LTL at various levels of complexities, and to provide insights into potential areas for improvement in future iterations of such models. <!--( ToDo **Look up further studies on NL to LTL**)-->
 xch
TO DO Accuracies over test sets
| Dataset | GPT-4.o|  GPT-3 |Llama |
|----------|----------|----------|----------|
| nl2spec original  | X/36 (%) | X/36 (%) |X/36 (%) |
| nl2spec in NL | X/36 (%) | 17/36 (47.22%)| X/36 (%) |

We observe that the  number of exact matches TO DO. 


###### Ambiguity
As pointed out by Cosler et al. [5], their dataset contains two types of ambiguities. The first type arises from the inherent limitations of natural language, such as operator precedence. The second type stems from semantic ambiguities within natural language. An illustration of the first is *a holds until b holds or always a holds* which their human experts initially translated to $(a U b) | G a$. GPT-3 returns the following:

> **$\mu:$ "The party is on until the speaker is broken or always the party is on."**
> 
> $\psi_{\mu}$: $p U (s | G p)$
> 
> $D_{\psi}$: {"The party is on": "p", "until": "U", "the speaker is broken": "s", "or": "|", "always the party is on": "G p", "The party is on until the speaker is broken or always the party is on": "p U (s | G p)"}

As both are plausible translations depending on the interpretation of the sentence, the example shows how the conversion is not as straight forward. 

An example of the second type is, *Whenever a holds, b must hold in the next two steps*, mapped to $G (a \rightarrow (b | X b))$. GPT3 returns:
> **$\mu:$ "Whenever the food is hot, the food is cold in the next two steps."**
> 
> $\psi_{\mu}$: $G (h \rightarrow X X c)$
> 
> $D_{\psi}$: {"Whenever": "->", "the food is hot": "h", "the food is cold": "c", "in the next two steps": "X X", "the food is hot implies that the food is cold in the next two steps": "h -> X X c"}

<!--**TO DO: Write about how to adjust the prompt to improve results**-->




- TO DO: Compare these results to **nl2spec** [5]. (T-5 fine tunes achieved 5.5% accurracy, nl2spec 44.4% accuracy)

##### (2) Effectiveness of trace geneation

- We plan to measure the accuracy of these conversions over a variety of LTL formulae.
- We will investigate how trace generation is affected by the **Context** of the drone planning domain.

- We aim to compare our results to results using GPT-3 or Rasa (Their source 3).
- Which model can handle unstructured natural language better?
- Mention how the few-shot prompting affect the results
- 
- Can the LLM infer that rooms belong to floors? (reasoning at abstracted levels)

The results from the multiple choice options in the *planning domain* show that the ambiguity observed in (1) might prevent exact matches, but it enables effective executions in some cases. (i.e. generates the right answer, but the LTL formula of the test set is not an exact match)

The elements within the *drona planning* grid world are organized into distinct levels of abstraction, with floors designated as level 2, rooms as level 1, and the landmark as level 0. Each natural language specification provided in our investigation is limited to a single sentence. Although there is no explicit restriction on the set of atomic propositions, specific guidelines are outlined in the task description. The LLM is asked to pick a possible path for the drone to follow, by checking if the run is valid for the $M_{\psi}$. Unlike previous approaches that utilize trajectory planners fed with LTL expressions, we introduce the predefined environment directly into the multiple-choice questions in natural language format, under the *context* section of the prompt.

### <a name="reproducibility results">Reproducibility</a>
<table align="center">
	<tr align="center">
    	<th>Dataset</th>
    	<th>Error count</th>
    	<th>Overall accuracy</th>
    	<th>Executable rate</th>
    	<th>Executable accuracy</th>
	</tr>
	<tr align="center">
    	<td>FOLIO</td>
    	<td>5</td>
    	<td>50.0</td>
    	<td>50.0</td>
    	<td>60.0</td>
	</tr>
	<tr align="center">
    	<td>AR-LSAT</td>
    	<td>9</td>
    	<td>10.0</td>
    	<td>10.0</td>
    	<td>0.0</td>
	</tr>
	<tr align="center">
    	<td>LogicalDeduction</td>
    	<td>0</td>
    	<td>50.0</td>
    	<td>100.0</td>
    	<td>50.0</td>
	</tr>
	<tr align="center">
    	<td>ProofWriter</td>
    	<td>6</td>
    	<td>50.0</td>
    	<td>40.0</td>
    	<td>100.0</td>
	</tr>
	<tr align="center">
    	<td>ProntoQA</td>
    	<td>9</td>
    	<td>30.0</td>
    	<td>10.0</td>
    	<td>100.0</td>
	</tr>
    <tr align="left">
   	 <td colspan=7><b>Table 3.</b>  Chat-GPT (GPT 3.5) Logic-LM results</td>
</table>


<table align="center">
  <tr align="center">
    <th>Dataset</th>
    <th>ChatGPT (gpt-3.5-turbo)</th>
    <th></th>
    <th></th>
    <th>GPT-3.5 (text-davinci-003)</th>
    <th></th>
    <th></th>
    <th>GPT-4 (gpt-4)</th>
    <th></th>
    <th></th>
  </tr>
  <tr align="center">
    <th></th>
    <th>Standard</th>
    <th>CoT</th>
    <th>Logic-LM</th>
    <th>Standard</th>
    <th>CoT</th>
    <th>Logic-LM</th>
    <th>Standard</th>
    <th>CoT</th>
    <th>Logic-LM</th>
  </tr>
  <tr align="center">
    <td>PrOntoQA</td>
    <td>47.40</td>
    <td><u>67.80</u></td>
    <td>61.00</td>
    <td>51.80</td>
    <td>83.00</td>
    <td><u>85.00</u></td>
    <td>77.40</td>
    <td><u>98.79</u></td>
    <td>83.20</td>
  </tr>
  <tr align="center">
    <td>ProofWriter</td>
    <td>35.50</td>
    <td>49.17</td>
    <td><u>58.33</u></td>
    <td>36.16</td>
    <td>48.33</td>
    <td><u>71.45</u></td>
    <td>52.67</td>
    <td>68.11</td>
    <td><u>79.66</u></td>
  </tr>
  <tr align="center">
    <td>FOLIO</td>
    <td>45.09</td>
    <td>57.35</td>
    <td><u>62.74</u></td>
    <td>54.60</td>
    <td>57.84</td>
    <td><u>61.27</u></td>
    <td>69.11</td>
    <td>70.58</td>
    <td><u>78.92</u></td>
  </tr>
  <tr align="center">
    <td>LogicalDeduction</td>
    <td>40.00</td>
    <td>42.33</td>
    <td><u>65.67</u></td>
    <td>41.33</td>
    <td>48.33</td>
    <td><u>62.00</u></td>
    <td>71.33</td>
    <td>75.25</td>
    <td><u>87.63</u></td>
  </tr>
  <tr align="center">
    <td>AR-LSAT</td>
    <td>20.34</td>
    <td>17.31</td>
    <td><u>26.41</u></td>
    <td>22.51</td>
    <td>22.51</td>
    <td><u>25.54</u></td>
    <td>33.33</td>
    <td>35.06</td>
    <td><u>43.04</u></td>
  </tr>
  <tr align="left">
  <td colspan=10><b>Table 3.</b>Original paper results(Pan et al., 2023): Accuracy of standard promoting (Standard), chain-of-thought promoting (CoT), and our method (LOGICLM,
without self-refinement) on five reasoning datasets. The best results within each base LLM are highlighted.</td>
</table>


Pan et al. (2023) employed three closed-source LLMs: ChatGPT, GPT-3.5, and GPT-4. Our extension of the Logic-LM involves open-source LLMs. However, ChatGPT is publicly accessible for manual query-based messaging. To validate the claims of Pan et al. (2023), we queried ChatGPT five times for each logic type, presenting the prompt and a new problem and question. Results are summarized in Table 3. ... (*qualitative results will come*)



## <a name="conclusion">Conclusion</a>
Our experiments show that it is possible to use Logic-LM with open-source language models. However the achieved performance with one SoTA open-source language model (Llama-3) is clearly lower than the performance of the closed-source GPT models. The GPT models scored better on all datasets except on PrOntoQA, where Llama performed better than ChatGPT. Interestingly with the Standard and CoT method similar performance was achieved to ChatGPT and GPT 3.5, so only Logic-LM really drops in performance with the open-source model. It should be noted that once better open-source models become available, they could perform equally as good or better than closed-source models, since the achieved performance is evidently related to the used language model. 

Using Llama-3 we observed that the performance of Logic-LM is significantly worse than the Standard and CoT methods, except on the LogicalDeduction dataset, where Logic-LM performed slightly better. This contradicts the findings of the original authors, since they found Logic-LM to outperform the other 2 methods on almost all datasets with all three GPT models. This is likely due to a difference in performance of the open-source language model itself. Moreover the difference could lead to wrong input for the logic solvers, making them unable to correctly solve the problems. (*More analysis will follow in final version*)





## Authors' Contributions
*example*
- Jonathan: Initial setup of codebase & implementation of architecture ablation studies, implementation of transformer architectures, implementation of FID metric, training of ablation models, wrote novel model architecture. Loss plots
- Ana: did ablation study for activation functions and normalization, bias research, model architecture diagram, wrote Image Editing with Diffusion Models (partly), Discovering Semantic Latent Space (training loss part), Model Architecture, Evaluating Diffusion Models and Concluding Remarks.
- Luc: did DM vs LDM research and notebook; wrote header, Image Editing Using Diffusion Models (partly), Recap on Diffusion Models, the Discovering Semantic Latent Space, Bias in Editing Directions (partly), Ablation Study, and Further Research: Latent Diffusion Models. 
- Eric: Structure of the repository, implementations, reproducibility experiment configurations, executions, visualizations, and analysis for "Reproduction of the Experiments", collaboration on the initial implementation of the transformer-based architecture, help as needed with run executions, figures, and tables for other sections.

## Bibliography

[1] Pan, L., Albalak, A., Wang, X., & Wang, W. Y. (2023). Logic-lm: Empowering large language models with symbolic solvers for faithful logical reasoning. arXiv preprint arXiv:2305.12295.

[2] Murray Shanahan. 2022. Talking about large language models. CoRR, abs/2212.03551.

[3] Francesco Fuggitti. 2019. LTLf2DFA (Version 1.0.3). Zenodo. DOI: 10.5281/zenodo.3888410. Available at: https://github.com/whitemech/LTLf2DFA and http://ltlf2dfa.diag.uniroma1.it.

[4] Y. Oh, R. Patel, T. Nguyen, B. Huang, E. Pavlick, and S. Tellex, "Planning with State Abstractions for Non-Markovian Task Specifications," CoRR, vol. abs/1905.12096, 2019. [Online]. Available: http://arxiv.org/abs/1905.12096

[5] M. Cosler, C. Hahn, D. Mendoza, F. Schmitt, and C. Trippel, "nl2spec: Interactively Translating Unstructured Natural Language to Temporal Logics with Large Language Models," Mar. 8, 2023. [Online]. Available: arXiv:2303.04864.

[6] Wang, J., Tong, J., Tan, K., Vorobeychik, Y., & Kantaros, Y. (2024). Conformal Temporal Logic Planning using Large Language Models. Retrieved from arXiv:2309.10092 [cs.RO]

[7] S. Simon and G. Röger, "Finding and Exploiting LTL Trajectory Constraints in Heuristic Search," Proceedings of the International Symposium on Combinatorial Search, vol. 6, pp. 113-121, Sep. 2021, doi: 10.1609/socs.v6i1.18361.

[8] J. Pan, G. Chou, and D. Berenson, "Data-Efficient Learning of Natural Language to Linear Temporal Logic Translators for Robot Task Specification," arXiv preprint arXiv:2303.08006, 2023.

[9] C. Wang, C. Ross, Y.-L. Kuo, B. Katz, and A. Barbu, "Learning a natural-language to LTL executable semantic parser for grounded robotics," *CoRR*, vol. abs/2008.03277, 2020. [Online]. Available: https://arxiv.org/abs/2008.03277

[10] M. Y. Vardi and P. Wolper, "Reasoning about Infinite Computations," *Information and Computation*, vol. 115, no. 1, pp. 1-37, 1994. [Online]. Available: https://doi.org/10.1006/inco.1994.1092.



