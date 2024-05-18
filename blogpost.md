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

| Problem                | Formulation | NL Sentence                                                                 |            Symbolic Formulation                                     |                Solver                  |      Dataset       |      
|------------------------|-------------|-----------------------------------------------------------------------------|---------------------------------------------------------|-----------------------------------------------------|-------------------|
| Deductive Reasoning    | LP          | If the circuit is complete and the circuit has the light bulb then the light bulb is glowing. | Complete(Circuit, True) ∧ Has(Circuit, LightBulb) → Glowing(LightBulb, True) | Pyke              | ProntoQA, ProofWriter |
| First-Order Logic      | FOL         | A Czech person wrote a book in 1946.                                        | ∃x₂∃x₁(Czech(x₁) ∧ Author(x₂, x₁) ∧ Book(x₂) ∧ Publish(x₂, 1946)) | Prover9           | FOLIO                 |
| Constraint Satisfaction| CSP         | On a shelf, there are five books. The blue book is to the right of the yellow book. | blue_book ∈ {1, 2, 3, 4, 5} yellow_book ∈ {1, 2, 3, 4, 5} blue_book > yellow_book | python-constraint | LogicalDeduction      |
| Analytical Reasoning   | SAT         | Xena and exactly three other technicians repair radios                      | repairs(Xena, radios) ∧ Count([t:technicians], t ≠ Xena ∧ repairs(t, radios)) == 3 | Z3                | AR-LSAT               |
| Temporal reasoning  | LTL         | Go through the red room to the second floor.                    |F(red_room ∧ F (second_floor)) | Buchi Automaton                | Done Planning             |

**Table 1**: A summary of the symbolic formulations and symbolic solvers we use for cateogies of logical reasoning in our study.


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


## <a name="reasons">Open-source models</a>
Our first extension is making Logic-LM work with open-source language models, instead of closed-source models like ChatGPT. To make the application as flexible as possible, this was appplied by using models from the Huggingface library TODO:Add link. This library contains a large variety of pre-trained open-source language models. For this project two versions of Meta's Llama-3 model were used, since these are current state-of-the-art open-source models (add ref). The first model is the 8B version of Llama-3 and the second is the 70B version. The former is a smaller version of the model, while the second is significantly larger and thus should have better performance. These models will be compared with the GPT models used by the original author to see how SoTA open-source models compare to closed-source models. By using two versions of this model we can also research the difference in performance between smaller and more complex models. 

## <a name="ltl">Linear Temporal Logic</a>
We extend the Logic-LLM by introducing Linear-time Temporal Logic (LTL). 
 Linear-time Temporal Logic extends standard propositional logic to express properties that hold over trajectories across time. LTL adheres to the following grammar:


| Syntax        | Description           |
|---------------|-----------------------|
| $p_a$      | Atomic Proposition    |
|$\neg \phi$ | Negation              |
| $\phi \land \psi$ | And                |
| $\phi \lor \psi$ | Or                 |
| $\phi \Rightarrow \psi$ | Imply            |
| $\phi U \psi$ | $\phi$ Until $\psi$      |
| $F \phi$    | Eventually           |
| $X \phi$    | Next                 |
| $G \phi$    | Always               |


We employ open source large language models (LLM) to convert natural language into Linear Temporal Logic (LTL) tasks based on the attributes in the planning domain. Consider the Natural language command $\mu$ : *Without stepping outside the orange room, go to landmark one*, where the terms *orange room* and *landmark one* belong to the predicates in the predetermined planning domain. From the given context, the LLM is able to identify and determine the relevant predicates such as the room and/or floor description. We use the LLM to translate $\mu$ into an LTL formula in CNF $\phi_{\mu}$ = F(landmark_1) & G (orange_room), and consequently employ a python module [3] to find its associated Determininistic Finite state Automaton $M_{\phi}$.

Since Large language models are predominantly trained on natural language and may encounter difficulties when processing text transcriptions of Linear Temporal Logic (LTL) formulas. The syntax of LTL (e.g. U and F) is quite different from typical natural language constructs. To address this distribution shift, a study [X] proposes creating a "canonical" representation that aligns more closely with natural language. In the prompt we ask the LLM to turn $\mu$ into an intermediate 'canoncial form' before mapping the the sentence into an LTL formula.

Using few shot learning we create a mapping between natural language commands and their associated LTL formula. Given the prompt below, an open source LLM can be instructed to create such LTL formulae from natural langauge. 

|Natural Language ($\mu$)| Canonical form      | Raw LTL form     |
|-----------------------------------------|-----------------------------------------|-------------------------------------|
|Always avoid the green room and navigate to the third floor. | finally ( and ( the third floor , not ( the green room ) ) ) | F ( third_floor & ! green_room ) |
|Every a is eventually followed by an e | globally ( a -> finally ( e ) )| G(a -> Fe)|
| The gate remains closed untill the train leaves the crossing| gate-closed until train-leaves  | gate-closed U train-exists| 


<table align="center">
  <tr align="center">
      <td><img src="pipeline.jpg" width=800></td>
  </tr>
  <tr align="left">
    <td colspan=2><b>Figure 1.</b> Pipeline.</td>
  </tr>
</table>

### <a name="ltl">Symbolic Reasoner</a>
### Buchi Automaton 

We incorporate a *Flloat* python library for translating LTL formulas (in CNF form) with finite-trace semantics into a minimal Deterministic Finite state Automaton (DFA) using MONA [3]. This DFA captures the temporal constraints specified by the LTL formula and enables efficient reasoning over finite traces. The trace-based satisfiability reasoning enhances the framework's ability to handle temporal aspects of logical reasoning problems. 

Traces are possible executions representing the sequence of states that the system can go through. Model checking for the validity of traces involves verifying whether a given trace satisfies the specified LTL formula. We prompt the LLM to generate a trace corresponding to each of the multiple-choice descriptions. Traces are either accepted or rejected based on their compliance with the LTL formula, and consequently, the model selects one of the multiple-choice answers. The language of a formula defines a set of infinite traces that the DFA can recognize, ensuring the logical consistency of temporal behaviors.

Step 5 in Figure 1 shows an example output of traces corresponding to options (A) and (B). In this step, the generated traces are evaluated against the associated Determininistic Finite state Automaton $M_{\phi}$ to determine their validity. 


**Definition 1: (Büchi automaton)**: A deterministic Büchi automaton (DBA) is a tuple $B = (Q, \sum, \Delta, Q_0, F)$ where:
- $Q$ is a finite set of states,
- $\sum$ is a finite alphabet,
- $\Delta \subseteq Q \times \sum \times Q$ is the transition relation,
- $Q_o \subseteq Q$ is the set of initial stats
- $F \subseteq Q$ is the set of accepting state. 



------
**Example Prompt**

*Given a context, question and options. The task is to first parse the question into a canonical formular and then from this formula to raw LTL formula. Also the options need to parsed into traces.
Below an explanaition is given of all the input you will recieve and what you should do with it.
Context: Declares the scene in which the question needs to be answered. Use this knowledge to parse the question and the options.*

*Question: Contains the question that needs to be answered. The task is to parse the question into a canonical formula and then based on the canonical formular to a raw LTL formula.*

*Your raw LTL formula answers always need to follow the following output format and you always have to try to provide a LTL formula. You may repeat your answers.*

*Remember that U means "until", G means "globally", F means "finally", which means GF means "infinitely often".*

*The formula should only contain atomic propositions or operators ||, &, !, U, G, F.*

*Options: The options need to be parsed into traces. These traces need to be a list ([]) containing dictionaries for each timestep ({}). In each dictionary the state of the corresponding timestep is given.*

[Few shot examples]

------

The prompt outline above encapsulates our methodology, showcasing its fundamental components. Comprising three main sections—LTL specification, few-shot examples, and context —the prompt serves as a structured framework for generating LTL formulas and traces from natural language inputs.

In our study, we employ a test set derived from the planning domain introduced by Oh et al. [4], featuring a 3D grid world denoted as $\epsilon_1$. This environment consists of three floors, six rooms, and a single landmark. While we manually added the multiple-choice answers, we utilized existing natural language descriptions and corresponding LTL formulas from Oh et al.'s study for testing purposes.

These elements within the grid world are organized into distinct levels of abstraction, with floors designated as level 2, rooms as level 1, and the landmark as level 0. Each natural language specification provided in our investigation is limited to a single sentence and a predefined set of atomic propositions. Although there is no explicit restriction on the set of atomic propositions, specific guidelines are outlined in the task description.

 Unlike previous approaches that utilize trajectory planners fed with LTL expressions, we introduce the predefined environment directly into the multiple-choice questions in natural language format, under the context section of the prompt.

------
##### Context:
*Our environment consists of grid-based rooms across multiple floors. Each floor features distinct rooms: the first floor has a red room and a yellow room, the second floor has a green room, and the third floor includes a purple room, an orange room, and Landmark 1.* *The drone’s movement is limited to one floor and not more than one room at a time within this structured environment. This setup is crucial for guiding effective planning and decision-making processes within the context of our problem.*

**Question:**
Always avoid the green room and navigate to the third floor. Which one of the following is a possible path for the drone to follow?
**Options:**

(A) From the third floor go to the green room and stay there,

(B) Go inside the red room and then move to the green room,

(C) Go to the second floor passing the yellow room and then go to the third floor

------

#### Language Grounding Results
The evaluation consists of two stages: first, the conversion of the question into LTL, and then the subsequent conversion of the LTL formula into traces. 

#### Effectiveness of Problem Formulator
We aim to evaluate how well the LLM performs the conversion task, especially in cases where it needs to generalize from few examples (few-shot learning). The accuracy of the conversions will be reported over the 36 benchmark inctances crafted by experts in the nl2spec study [5]. We use their formatted intances and prompt the LLM to replaced the propositions a,b,c,d. It's worth noting that these sentences are not specific to any domain, allowing us to test the LLM's capability to generalize across different problem domains. 
Through this evaluation, we seek to understand how well the LLM can handle the translation from natural language to LTL, including its strengths and limitations, and to provide insights into potential areas for improvement in future iterations of such models.

| Natural Language Sentence                                        | Canonical Form                | LTL Formula                           |
|------------------------------------------------------------------|-------------------------------|---------------------------------------|
| Every meal is eventually followed by dessert.                    |    TO DO        | G (meal -> F dessert)                 |
| It is never the case that sunshine and rain occur at the same time. |  TO DO       | G ~(sunshine & rain)                  |
| Whenever a car starts, the engine revs three steps later.        | TO DO | G (car_starts -> X X X engine_revs) |

In addition we evaluate the LLMS NltoLTL conversion in the Drone Planning domain. 

#### Effectiveness of trace geneation
We plan to measure the accuracy of these conversions over a variety of LTL formulae. 

We aim to test how well the few shot learning performs the natural language to LTL conversion. **(say how conversions can be ambigious) -  inerherent ambiguity of natural language,**
We assess the proficiency of LLM in transforming a provided problem into the symbolic representation (LTL) employed by the Buchi Automaton. The following table reports the accuracy over a variety of LTL formulae. 

In order to evaluate the effectivenss of XXXX we evaluate on the 36 benchmark instances created by experts in the *nl2spec* study [].

#### Examples with a,b,c,d replaced
- Every meal is eventually followed by dessert.
- It is never the case that sunshine and rain occur at the same time.
- Whenever a car starts, the engine revs three steps later.
- Happiness must prevail everywhere until from some point on, sadness occurs infinitely often.
- If hunger strikes at some point, eating must happen beforehand.
- Whenever laughter echoes, joy ensues.
- Both work and relaxation happen in every time step.
- Birds chirp always, and whenever reading happens, writing does not occur.
- If every journey is eventually followed by an adventure, then excitement needs to happen infinitely often.
- If exercise happens infinitely often, then relaxation follows infinitely often as well.
  

| Temporal Property                                               | Temporal Logic Formula                                      | LLAMA output |
|-----------------------------------------------------------------|--------------------------------------------------------------|---|
| Every a is eventually followed by an e                           | $G(a \rightarrow F e)$                                 |   |
| It is never the case that a and b hold at the same time         | $G(\neg(a \land b))$                                    |   |
| Whenever a is enabled, b is enabled three steps later           | $G(a \rightarrow X(X(Xb)))$                               |   |
| e must hold everywhere until from some point on, d holds infinitely often | $e \mathcal{U} (G(Fd))$                             |   |
| If b holds at some point, a has to hold somewhere beforehand     | $(Fb) \rightarrow (\neg b \mathcal{U} (a \land \neg b))$ |   |
| Whenever a holds, b holds as well                               | $G(a \rightarrow b)$                                    |   |
| Both a and b hold in every time step                            | $G(a \land b)$                                           |   |
| a holds always and whenever b holds, c does not hold            | $Ga \land G(b \rightarrow \neg c)$                       |   |
| If every a is eventually followed by a b, then c needs to holds infinitely often | $G(a \rightarrow Fb) \rightarrow GFc$           |   |
| If a holds infinitely often, then b holds infinitely often as well | $G(Fa) \rightarrow G(Fb)$                          |   |
| Either a or b holds infinitely often                            | $GFa \lor GFb$                                          |   |
| a never holds from some point in time on                        | $F G \neg a$                                            |   |
| Whenever a and b do not hold, c holds eventually                | $G(\neg(a \land b) \rightarrow Fc)$                    |   |
| a and b never occur at the same time but one of them holds in every time step | $G(\neg(a \land b)) \land G(a \lor b)$        |   |
| Whenever the inputs a and b are the same, the outputs c and d are the same | $G((a \leftrightarrow b) \rightarrow (c \leftrightarrow d))$ |   |
| a can only happen if b happened before                          | $\neg a \mathcal{U} b$                                  |   |
| Once a happened, b will not happen again                        | $G(a \rightarrow X G \neg b)$                           |   |
| a releases b                                                    | $(b \mathcal{U} (b \land \neg a)) \lor Gb$             |   |
| a and b will not occur at the same time                         | $\neg(a \land b)$                                       |   |
| Whenever a holds and b holds in the next step, then c holds one step after b | $G(a \land Xb \rightarrow XXc)$                         |   |
| Whenever a holds, b holds eventually from the next step on      | $G(a \rightarrow XFb)$                                   |   |
| a holds in every fifth step                                     | $a \land G(a \rightarrow X!a \land XX!a \land XXX!a \land XXXX!a \land XXXXXa)$ |   |
| Either a holds infinitely often or b holds in the next step     | $GFa \lor Xb$                                             |   |
| a will hold at all instances                                    | $Ga$                                                     |   |
| Whenever a holds, b must hold in the next two steps             | $G(a \rightarrow (b \lor Xb))$                            |   |
| One of the following aps will hold at all instances: a, b, c    | $G(a \lor b \lor c)$                                      |   |
| If a holds b will eventually hold                               | $G(a \rightarrow Fb)$                                     |   |
| a must always hold, but if it exceeds, it allows two timestamps to recover | $!G(\neg(a \land Xa))$                                |   |
| not a holds at most two timestamps                             | $!G(\neg(a \land Xa))$                                   |   |
| a can only hold every three timestamps                         | $G(a \rightarrow (X\neg a \lor XX\neg a \lor XXX\neg a))$ |   |
| Every a is followed by a b                                      | $G(a \rightarrow Xb)$                                     |   |
| Eventually a and b hold                                         | $F(a \land b)$                                            |   |
| Both a and b hold eventually                                    | $F a \land F b$                                           |   |
| It is always the case that a is the same as b in the next step  | $G(a \leftrightarrow Xb)$                                |   |
| If b holds then, in the next step, c holds until a holds or always c holds | $b \rightarrow X((c \mathcal{U} a) \lor Gc)$         |   |
| a holds until b holds or always a holds                        | $(a \mathcal{U} b) \lor Ga$                             |   |


[NL2LTL](https://github.com/realChrisHahn2/nl2spec/blob/main/experiments/nl2spec-paper_experiment_results.csv)



## <a name="contribution">Novel contribution</a>
*Describe your novel contribution.*


## <a name="results">Results</a>
### <a name="general results">Main results</a>
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
		<th>GoT</th>
		<th>Logic-LM</th>
		<th>Standard</th>
		<th>GoT</th>
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

Table 1 shows the results of the experiments with the open-source model.  It displays that Logic-LM only scored highest on the LogicalDeduction dataset, where it scored 60.67 compared to 35.33 and 39.00 for Standard and CoT respectively. For the other datasets Logic-LM got outperformed by either the Standard or the CoT model. TODO: Insert % of how much better/worse

Comparing these results to the GPT model results, we observe that Llama generally performs worse than the GPT models. Logic-LM has significantly lower scores compared to all GPT models for the Proofwriter, FOLIO and AR-LSAT dataset and slight lower scores for the LogicalDeduction dataset. Only on the PrOntoQA Llama achieved a higher score than gpt-3.5-turbo, while still having worse scores when using the other GPT models. For the Standard and CoT method we observe similar performance to gpt-3.5-turbo while also being outperformed by the other GPT models.


### <a name="sr results">Self-refinement</a>
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
		<td colspan=7><b>Table 2.</b>  TODO: Give title.</td>
	</tr>
</table>
Table 2 displays a comparison of self-refinement

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
        <td>0</td>
        <td>60.0</td>
        <td>100.0</td>
        <td>60.0</td>
    </tr>
    <tr align="center">
        <td>AR-LSAT</td>
        <td>5</td>
        <td>20.0</td>
        <td>0.0</td>
        <td>-</td>
    </tr>
    <tr align="center">
        <td>LogicalDeduction</td>
        <td>5</td>
        <td>40.0</td>
        <td>0.0</td>
        <td>-</td>
    </tr>
    <tr align="center">
        <td>ProofWriter</td>
        <td>4</td>
        <td>40.0</td>
        <td>20.0</td>
        <td>100.0</td>
    </tr>
	<tr align="left">
		<td colspan=7><b>Table 3.</b>  TODO: Chat-GPT results</td>
</table>



## <a name="conclusion">Conclusion</a>
Our experiments show that it is possible to use Logic-LM with open-source language models. However the achieved performance with one SoTA open-source language model (Llama-3) is clearly lower than the performance of the closed-source GPT models. The GPT models scored better on all datasets except on PrOntoQA, where Llama performed better than ChatGPT. Interestingly with the Standard and CoT method similar performance was achieved to ChatGPT and GPT 3.5, so only Logic-LM really drops in performance with the open-source model. It should be noted that once better open-source models become available, they could perform equally as good or better than closed-source models, since the achieved performance is evidently related to the used language model. 

Using Llama-3 we observed that the performance of Logic-LM is significantly worse than the Standard and CoT methods, except on the LogicalDeduction dataset, where Logic-LM performed slightly better. This contradicts the findings of the original authors, since they found Logic-LM to outperform the other 2 methods on almost all datasets with all three GPT models. This is likely due to a difference in performance of the open-source language model itself. Moreover the difference could lead to wrong input for the logic solvers, making them unable to correctly solve the problems. 





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
