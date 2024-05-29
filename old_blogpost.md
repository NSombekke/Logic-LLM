# Logic-LM integrated with Llama-3 and Linear Temporal Logic

### Authors

## Niels Sombekke, AnneLouise de Boer, Roos Hutter, Rens Baas, Sacha Buijs

_Abstract_
_We still need to write the abstract_

---

## Introduction

Logic-LM is a novel framework, proposed by Pan et al. (2023) \[1\], that combines Large Language Models (LLMs) and Symbolic Solvers for reasoning tasks . Leveraging the translative power of LLMs, they counterbalance potential inaccuracies in reasoning by employing Symbolic Solvers (Shanan, 2022) \[2\].


### Related work

<!-- Nog niet goed -->

Recent advancements in adapting Large Language Models (LLMs) for logical reasoning tasks can be categorized into two main approaches: fine-tuning and in-context learning. Fine-tuning methods optimize LLMs' reasoning ability through specialized training modules (Clark et al., 2020; Tafjord et al., 2022; Yang et al., 2022), while in-context learning designs prompts to elicit step-by-step reasoning. Chain-of-Thought prompting (Wei et al., 2022b; Wang et al., 2023) is an example of in-context learning, in which explanaitions are generated before the final answer. While these methods operate directly over natural language, the Logic-LM framework stands out by utilizing symbolic language for reasoning, transferring complex tasks to external symbolic solvers while leveraging LLMs for problem formulation. Unlike prior neuro-symbolic methods (Mao et al., 2019; Gupta et al., 2020; Manhaeve et al., 2021; Cai et al., 2021; Tian et al., 2022; Pryor et al., 2023), which often require specialized modules and suffer from optimization challenges, the Logic-LM framework integrates modern LLMs with symbolic logic without the need for complex module designs, offering a more generalizable solution. Additionally, this work explores tool-augmented LLMs, extending their capabilities beyond language comprehension by integrating external tools for improved performance on logical reasoning tasks. While auto-formalization has been widely applied in mathematical reasoning (Wu et al., 2022; Drori et al., 2022; He-Yueya et al., 2023; Jiang et al., 2023), Pan et al. (2023) pioneer its extension to a broader range of logical reasoning tasks, bridging the gap between natural language understanding and formal logic with modern LLMs.

### Logic-LM framework

The Logic-LM decomposes a logical reasoning problem into three stages: stages: _Problem Formulation_,
_Symbolic Reasoning_, and _Result Interpretation_. The _Problem Formulation_ prompts an LLM to translate a natural language problem into symbolic language, utilizing the few-shot generalization ability of LLMs. The LLM is provided with instructions about the grammar of the symbolic language alongside in-context examples. Specifically, four different symbolic formulations are used to cover four common types of logical reasoning problems: deductive reasoning, firstorder logic reasoning, constraint satisfaction problem, and analytical reasoning (Table 1). Afterwards, in the _Symbolic Reasoning_ stage, external solvers perform inference on the symbolic representation. Based on the problem type a different solver is used, such as Pyke (Frederiksen, 2008) for deductive reasoning or Z3 (de Moura and Bjørner, 2008) for SAT problems. The _Result Interpreter_ explains the output of the solver and maps it to the correct answer. Moreover, a self-refinement module is introduced which improves accuracy by iteratively revising symbolic formulations using error messages from the solvers. This module instructs the LLM to refine incorrect logical forms by prompting it with the erroneous logic form, the solver’s error message, and a set of demonstrations showing common error cases and remedies.

| Problem                 | Formulation | NL Sentence                                                                                   | Symbolic Formulation                                                               | Solver            | Dataset               |
| ----------------------- | ----------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------- | --------------------- |
| Deductive Reasoning     | LP          | If the circuit is complete and the circuit has the light bulb then the light bulb is glowing. | Complete(Circuit, True) ∧ Has(Circuit, LightBulb) → Glowing(LightBulb, True)       | Pyke              | ProntoQA, ProofWriter |
| First-Order Logic       | FOL         | A Czech person wrote a book in 1946.                                                          | ∃x₂∃x₁(Czech(x₁) ∧ Author(x₂, x₁) ∧ Book(x₂) ∧ Publish(x₂, 1946))                  | Prover9           | FOLIO                 |
| Constraint Satisfaction | CSP         | On a shelf, there are five books. The blue book is to the right of the yellow book.           | blue_book ∈ {1, 2, 3, 4, 5} yellow_book ∈ {1, 2, 3, 4, 5} blue_book > yellow_book  | python-constraint | LogicalDeduction      |
| Analytical Reasoning    | SAT         | Xena and exactly three other technicians repair radios                                        | repairs(Xena, radios) ∧ Count([t:technicians], t ≠ Xena ∧ repairs(t, radios)) == 3 | Z3                | AR-LSAT               |
| Temporal reasoning      | LTL         | Go through the red room to the second floor.                                                  | F(red_room ∧ F (second_floor))                                                     | Buchi Automaton   | Drone Planning        |

**Table 1**: A summary of the symbolic formulations and symbolic solvers we use for cateogies of logical reasoning in our study.

### Experiments

The performance of three GPT models serving as underlying models for the Problem Formulator of Logic-LM (ChatGPT, GPT-3.5, and GPT-4) is evaluated against two baselines: 1) Standard LLMs, which leverage incontext learning to directly answer the question; and 2) Chain-of-Thought (CoT) (Wei et al., 2022b), which adopts a step-by-step problem-solving approach. The performance is evaluated across five logical reasoning datasets. _PrOntoQA_ (Saparov and He, 2023)offers synthetic challenges for deductive reasoning, with the hardest 5-hop subset tested. _ProofWriter_ (Tafjord et al., 2021) presents problems in a more natural language form under the open-world assumption, focusing on different levels of reasoning depth, with the depth-5 subset chosen for evaluation. _FOLIO_ (Han et al., 2022), a challenging expert-written dataset, demands complex first-order logic reasoning. _LogicalDeduction_ (Srivastava et al.,2022) from BigBench and _AR-LSAT_ (Zhong et al., 2022) present real-world scenarios and analytical logic reasoning questions, respectively. Additionally, the effect of the refiner is researched by investigating the accuracy and the executable rates on the FOLIO dataset across different rounds of self refinement.

### Main results

Pan et al. (2023) present three main results. First, LOGIC-LM notably outperforms standard LLMs and Chain-of-Thought (CoT) across various datasets, showcasing the advantage of integrating LLMs with external symbolic solvers for logical reasoning. Second, GPT-4 exhibits superior performance compared to GPT-3.5, especially in standard prompting. Logic-LM further improves GPT-4 24.98% and 10.44% for standard
prompting and CoT prompting, respectively. Third, while CoT generally enhances LLM performance, its benefits vary across datasets, with less substantial or negative effects seen in certain scenarios. Additionally, the effectiveness of problem formulation, the robustness of reasoning, and the impact of self-refinement, highlight both the successes and challenges encountered in these areas.


## <a name="reasons">Reasons for extension</a>

_Exposition of its weaknesses/strengths/potential which triggered your group to come up with a response._

As outlined in the introduction, the Logic-LM framework relies on three LLMs: ChatGPT, GPT-3.5, and GPT-4. However, due to their closed-source nature, these models suffer from limited transparency, customization options, and opportunities for collaboration. Therefore, integrating open-source LLMs into the Logic-LM framework would be beneficial, as it increases accessibility, usability and flexibility.

The authors of Logic-LM pointed out a crucial constraint, stating that “the model’s applicability is inherently bounded by the expressiveness of the symbolic solver” (Pan et al., 2023). Currently, only four distinct symbolic solvers are employed, limiting the framework's scope to four specific types of logical reasoning problems. This limitation can be mitigated by integrating more symbolic solvers into the framework, as proposed by the authors (Pan et al., 2023). Therefore, incorporating an additional solver expands the framework’s capabilities, which is facilitated by the inherent flexibility of its design. Moreover, this addition encourages the development of a versatile logic-solving model.

## <a name="open_source">Extension: Open-source models</a>

Our first extension is making Logic-LM work with open-source language models, instead of closed-source models like ChatGPT. To make the application as flexible as possible, this was appplied by using models from the Huggingface library (https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct). Two versions of the current state-of-the-art open-source model Llama-3 have been utilized<!--(TODO add ref)-->. First, the smaller 8B version of the model is implemented and evaluated to see how well Logic-LM performs with a lower resource model. Additionally, the larger version of Llama-3 (70B) is utilized to extend Logic-LM, as it is significantly larger it is expected it outperforms the 8B variant. Both models are be compared with the GPT models used by the original author to see how SoTA open-source models compare to closed-source models.

## <a name="ltl">Extension: Linear Temporal Logic</a>

In addition to standard propositional logic, we extend the Logic-LLM by introducing Linear-time Temporal Logic (LTL), which enables the expression of properties that hold over time-based trajectories. This extension is particularly useful in robotics and automated planning, where paths must comply with temporal constraints. LTL's semantics can effectively capture command specifications in the temporal domain. 

**Syntax and Semantics**

Formulas in LTL over the set of atomic propositions ($P$) adhere to the following grammar:

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

In addition to the syntax of propositional logic, temporal operators express the following properties:

* **Eventually** ($F \varphi$): $\varphi$ will hold at some point in the trace.
* **Always** ($G \varphi$): $\varphi$ holds at every time step in the trace.
* **Until** ($\varphi \mathcal{U} \psi$): $\varphi$ holds continuously until $\psi$ holds.
* **Next** ($X \varphi$): $\varphi$ holds at the next time step.

In the context of planning, LTL formulas ($\psi$) are constructed over a set of atomic propositions ($P$). The semantics of an LTL formula $\varphi$ is given with respect to an execution trace $\sigma = (s_0, s_1, ..., s_n)$. We consider only LTL over finite traces, which is commonly called $LTL_f$, however, the semantics may descrive an execution traces of infinite length. For $0 \leq i \leq n$, through induction one can define if $\psi$ is true at instant $i$ (written $w, i \models \psi$) as:

- $w, i \models p$ iff $p \in L(w_0)$
- $w, i \models \neg \psi$ iff $w, i \not\models \psi$
- $w, i \models \psi_1 \land \psi_2$ iff $w, i \models \psi_1$ and $w, i \models \psi_2$
- $w, i \models X \psi$ iff $i < n$ and $w, i+1 \models \psi$
- $w, i \models F \psi$ iff $\exists j \geq i$ such that $w, j \models \psi$
- $w, i \models \psi_1 \mathcal{U} \psi_2$ iff there exists a $j$ with $i \le j \le n$ s.t. $w, j \models \psi_2$ and for all $i \le k < j$, $w, k \models \psi_1$

<table align="center">
  <tr align="center">
      <td><img src="misc/img/pipeline_ltl.png" width=700></td>
  </tr>
  <tr align="left">
    <td colspan=2><b>Figure 2.</b> Pipeline of Logic-LM for LTL.</td>
  </tr>
</table>


**Natural Language to LTL**

We employ the 2 Llama-3 models to convert natural language into Linear Temporal Logic (LTL) tasks based on the attributes in the context of the question (e.g. planning domain). The conversion from natural language to LTL has been predominantly studied within the field of robotics [9].

For illustration, consider the following Natural language commands $\mu$, and their corresponding LTL formula $\psi_{\mu}$, and explanation dictionary $(D_{\psi})$ generated by a LLM.

> **$\mu:$ "Every time hunger strikes, eating eventually follows."**
>
> $\psi_{\mu}$: $G(\text{ hunger} \rightarrow F \text{ eating})$
>
> $D_{\psi}$: {'Every time': 'G', 'hunger strikes': 'hunger', 'eating eventually follows': 'F eating', 'hunger strikes, eating eventually follows': 'G (hunger $\rightarrow$ F eating)'}

> **$\mu:$ "Always avoid the green room and navigate to the third floor."**
>
> $\psi_{\mu}$: $G( \neg greenroom) \land F thirdfloor$
>
> $D_{\psi}$: {"Always avoid the green room": "G(¬greenroom)","Navigate to the third floor": "F thirdfloor"}

<table align="center">
  <tr align="center">
      <td><img src="misc/img/pipeline.jpg" width=800></td>
  </tr>
  <tr align="left">
    <td colspan=2><b>Figure 1.</b>  Pipeline: Converting Natural Language to Linear Temporal Logic for Multiple Choice Answering.</td>
  </tr>
</table>

### <a name="ltl">Symbolic Reasoner</a>

Utilizing few-shot learning, we establish a correspondence between natural language commands and their respective LTL formulas. With the given prompt, an open-source LLM can be directed to generate these LTL formulas from natural language. Subsequently, we employ a Python module to derive its associated Deterministic Finite State Automaton $M_{\phi}$. We integrate the _Flloat_ Python library to translate LTL formulas (in CNF form) with finite-trace semantics into a minimal Deterministic Finite State Automaton (DFA) using MONA [3]. This conversion is guaranteed by Theorem 1. The resultigng DFA ($M_{\phi}$) encapsulates the temporal constraints specified by the LTL formula, enabling efficient reasoning over finite traces. The trace-based satisfiability reasoning enhances the framework's capability to address temporal aspects of logical reasoning problems.

**Theorem 1** [Vardi and Wolper, 1994 [10]]: For any LTL formula $\psi$, a Büchi automaton $M_{\psi}$ can be constructed, having a number of states that is at most exponential in the length of $\psi$. The language of $M_{\psi}$, denoted as $L(M_{\psi})$, encompasses the set of models of $\psi$.

The input words **w** of the Büchi automaton ($M_{\psi}$) can be infinite sequences $\sigma_0 \sigma_1 ... \sigma_n \in \Sigma^{w}$ [7]. A _run_ of the automaton $(M_{\psi})$ on the word **w** is sequence of states $\rho = q_0q_1q_2...$, where each state is a set of propositions. The initial state is $q_0$ and subsequent states are defined throught the transition function $q_{i+1} = \Delta(q_i,\sigma_i)$. The language of the automaton $M_{\psi}$ ($L(M_{\psi})$), is a set of _words_ characterized by the presence of an accepting run. In this case each accepting run is a valid sequence of states that holds in the automaton.

<!--(TODO add ref)-->

**Definition 1: (Büchi automaton)**: A deterministic Büchi automaton (DBA) is a tuple $M = (Q, \sum, \Delta, Q_0, F)$ where:

- $Q$ is a finite set of automaton states,
- $\Sigma$ is a finite alphabet of the automaton ($|\Sigma| = 2^{|P|}$),
- $\Delta : Q \times \sum  \rightarrow 2^{Q}$ is the transition function,
- $q_0 \subseteq Q$ is the set of initial stats
- $F \subseteq Q$ is the set of accepting states.

A word **w** is accepted by an automaton ($M_{\psi}$) if its run $\rho$ meets the condition $\lim(\rho) \cap F \neq \emptyset$. Meaning that that the run reaches at least one accepting state in **F**.

$L(M_{\psi}) = \\{ w \in \Sigma^{w} | w \text{ is accepted by}  M_{\psi} \\}$

Model checking for the validity of runs involves verifying whether a given run satisfies the specified LTL formula. We prompt the LLM to generate a possible finite run corresponding to each of the multiple-choice descriptions. Runs are either accepted or rejected based on their compliance with the LTL formula, and consequently, the model is able to select one of the multiple-choice answers.

For each subplan $q_i$ of the run, the language function $L$ assigns a symbol $\sigma \in \Sigma$. These symbols collectively form a word **w** representing the sequence of symbols observed along the trace. This word **w** is then evaluated against the acceptance conditions of the DBA $M_{\psi}$. The language $L(M_{\psi})$ defines a set of infinite runs that the DFA can recognize. If **w** satisfies these acceptance conditions, then the finite run $\rho_{\psi}$ satisfies the LTL formula. Finite runs $\rho_{\psi}$ satisfiy the LTL if the word $ **w** = L(q*0)L(q_1)...L(q_n)$ is acceptable in $L(M*{\psi})$.

Step 5 in Figure 1 shows an example output of runs corresponding to options (A) and (B). In this step, the generated runs are evaluated against the associated Deterministic Finite Automaton $M_{\psi}$ to determine their validity.

#### Prompt Engineering

Since Large language models are predominantly trained on natural language, they may struggle converting natural language directly into Linear Temporal Logic (LTL) formulas. The syntax of LTL (e.g. X, U, and F) is quite different from typical natural language constructs. To address this distribution shift, a study by Pan et al. (2023) proposes creating a _canonical_ representation that aligns more closely with natural language [8]. For the same reason Cosler et al. (2023) prompt the LLM to turn $\mu$ into an intermediate _canoncial form_, shown as _sub-translations_, before mapping the the sentence into an LTL formula [5]. Each translation accompanies a translation dictionary in canonical form, through which th LLM is asked to explain its steps. We will use their prompting technique.

The prompt outline below encapsulates our methodology, comprising three main sections — (1) LTL specification for the conversion of Natural Language to LTL, (2) the conversion of multiple choice options to traces, and (3) few-shot examples. All in all, the prompt serves as a structured framework for generating LTL formulas and traces from natural language inputs.

> **Prompt**
>
> Given a context, question and options. The task is to first parse the question into a canonical formular and then from this formula to raw LTL formula. Also the options need to parsed into traces.
> Below an explanaition is given of all the input you will recieve and what you should do with it.
>
> **Context**: Declares the scene in which the question needs to be answered. Use this knowledge to parse the question and the options.
>
> **\*Question**: Contains the question that needs to be answered. The task is to parse the question into a canonical formula and then based on the canonical formular to a raw LTL formula.\*
>
> _Your raw LTL formula answers always need to follow the following output format and you always have to try to provide a LTL formula. You may repeat your answers._
>
> _Remember that U means "until", G means "globally", F means "eventually", which means GF means "infinitely often"._
>
> _The formula should only contain atomic propositions or operators ||, &, !, X, U, G, F._
>
> **\*Options**: The options need to be parsed into traces. These traces need to be a list ([]) containing dictionaries for each timestep ({}). In each dictionary the state of the corresponding timestep is given.\*
>
> [Few shot examples]

Simpler examples may not necessitate contextual information for trace generation, as the LLM is expected to infer when predictes have a mutually exclusive (mutex) relation. (e.g. The predicates sleeping and eating can not hold at the same time) However, as the complexity of trace generation tasks increases, the inclusion of detailed domain descriptions becomes crucial. For instance, in scenarios where the LLM needs to understand specific constraints, such as the impossibility of the drone simultaneously occupying the third floor and a particular room on the first floor, prompts enriched with a context are utilized. To evaluate the LLM's proficiency in generating traces within predetermined domains, we generated a datasets based on the _drone planning_ domain [4]. This rigorous testing approach ensures thorough assessment of the LLM's capabilities across various levels of complexity and specificity.

> **Context**:
> _Our environment consists of grid-based rooms across multiple floors. Each floor features distinct rooms: the first floor has a red room and a yellow room, the second floor has a green room, and the third floor includes a purple room, an orange room, and Landmark 1._ _The drone’s movement is limited to one floor and not more than one room at a time within this structured environment. This setup is crucial for guiding effective planning and decision-making processes within the context of our problem._
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

#### Language Grounding Results

We test the LLms ability to parse natural language into LTL on two datasets. The first consists of 36 benchmark inctances crafted by experts in the *nl2spec* study [5]. Each of these examples has been selected by LTL experts to cover a variety of ambiguities and complexities. In addition, we have replaced the propositions a,b,c,d to create more realistic sentences in natural language (*nl2spec in NL*). For example:

> $\mu:$ Every meal is eventually followed by dessert. $\leftrightarrow$ G(meal -> F dessert).
>
> $\mu:$ Whenever a car starts, the engine revs three steps later. $\leftrightarrow$ G(car_starts -> X X X engine_revs).

The second dataset is derived from commands in the _drone planning_ domain. This test set is adapted from the planning domain introduced by [8]. This environment is a 3D grid world that consists of three floors, six rooms, and a single landmark. We created a test set with multiple-choice options from their natural language descriptions and corresponding LTL formulas.

<table align="center">
  <tr align="center">
      <td><img src="misc/img/drone_domain.png" width=300></td>
  </tr>
  <tr align="left">
    <td colspan=2><b>Figure 2.</b> Planning domain for the drone navigation. Figure by [8].</td>
  </tr>
</table>

We aim to evaluate how well the LLM performs the conversion task from natural language to LTL, especially in cases where it needs to generalize from few examples (few-shot learning). The evaluation consists of two stages: (1) the conversion of the natural language command into LTL, and (2) the subsequent conversion of the multiple choice options (each formlated in natural language) into runs.

The *nl2spec* dataset will be used to test the initial conversion from natural language to LTL, while the *drone planning* dataset will be used to test both the initial conversion and the subsequent generation of runs.


##### (1)  Evaluating the Performance of Large Language Models in NL to LTL Conversion
By testing the NL to LTL conversion on the *nl2spec* dataset [5], we seek to understand how well the LLM can handle the translation from natural language to LTL at various levels of complexities, and to provide insights into potential areas for improvement in future iterations of such models.

**Accuracies Over Test Sets (Counting the Number of Exact Matches Between Formulae)**

| Dataset             | GPT-4.0       | GPT-3         | Llama3-70b-instruct      |
|---------------------|---------------|---------------|--------------|
| nl2spec original    | X/36 (%)      | 17/36 (47.22%)      | 23/36 (63.88%)     |
| nl2spec in NL       | 26/36 (72.2%) | 17/36 (47.22%)| 19/36 (52.77%)     |

*For intersecting Büchi automata, we use the following [spot](https://spot.lre.epita.fr/app/) model checking software.*

The results presented in the table above demonstrate the effectiveness of using Large Language Models (LLMs) to parse natural language into Linear Temporal Logic (LTL) formulas. Notably, the "nl2spec original" approach, which works directly with predefined predicates, outperforms the "nl2spec in NL" approach, which extracts predicates from natural language sentences. This improvement can be attributed to the fact that predefined predicates provide a clear and concise representation of the relevant information, allowing the LLM to focus on understanding the relationships between them and generating the correct LTL formula.
Our results show that GPT-4.o significantly outperforms GPT-3.5 in translating natural language to LTL formulas, achieving an accuracy rate of 72.2% (26 out of 36) compared to 47.22% (17 out of 36) for GPT-3. This suggests that GPT-4.0 has enhanced capabilities in understanding and processing natural language semantics, making it a more reliable tool for complex logical conversions.




###### Ambiguity

As pointed out by Cosler et al. [5], natural language is prone to ambiguity. Their dataset contains two types of ambiguities.

The first type arises from the more structural limitations of natural language, such as operator precedence. The second type stems from semantic ambiguities within natural language. An illustration of the first is _a holds until b holds or always a holds_ which their human experts initially translated to $(a U b) | G a$. GPT-3.5 returns the following:

> **$\mu:$ "The party is on until the speaker is broken or always the party is on."**
>
> $\psi_{\mu}$: $p U (s | G p)$
>
> $D_{\psi}$: {"The party is on": "p", "until": "U", "the speaker is broken": "s", "or": "|", "always the party is on": "G p", "The party is on until the speaker is broken or always the party is on": "p U (s | G p)"}
> 
As both are plausible translations depending on the interpretation of action precedence, the example shows how the conversion is not as straight forward.

The second type of ambiguity is illustrated by the following. _Whenever a holds, b must hold in the next two steps_, mapped to $G (a \rightarrow (b | X b))$. However, it could also be translated as $G((a \rightarrow X(X(b))))$ as this depends on the interpretation of the semantic meaning. GPT3.5 returns the latter interpretation:

> **$\mu:$ "Whenever the food is hot, the food is cold in the next two steps."**
>
> $\psi_{\mu}$: $G (h \rightarrow X X c)$
>
> $D_{\psi}$: {"Whenever": "->", "the food is hot": "h", "the food is cold": "c", "in the next two steps": "X X", "the food is hot implies that the food is cold in the next two steps": "h -> X X c"}
>

- To mitigate these ambiguities, the *nl2spec* [5] specifies sub-clauses.  TODO





- TO DO: Compare these results to **nl2spec** [5]. (T-5 fine tunes achieved 5.5% accurracy, nl2spec 44.4% accuracy)

##### (2) Effectiveness of trace geneation

- We plan to measure the accuracy of these conversions over a variety of LTL formulae.
- We will investigate how trace generation is affected by the **Context** of the drone planning domain.

- We aim to compare our results to results using GPT-3 or Rasa (Their source 3).
- Which model can handle unstructured natural language better?
- Mention how the few-shot prompting affect the results
-
- Can the LLM infer that rooms belong to floors? (reasoning at abstracted levels)

The results from the multiple choice options in the _planning domain_ show that the ambiguity observed in (1) might prevent exact matches, but it enables effective executions in some cases. (i.e. generates the right answer, but the LTL formula of the test set is not an exact match)

The elements within the _drona planning_ grid world are organized into distinct levels of abstraction, with floors designated as level 2, rooms as level 1, and the landmark as level 0. Each natural language specification provided in our investigation is limited to a single sentence. Although there is no explicit restriction on the set of atomic propositions, specific guidelines are outlined in the task description. The LLM is asked to pick a possible path for the drone to follow, by checking if the run is valid for the $M_{\psi}$. Unlike previous approaches that utilize trajectory planners fed with LTL expressions, we introduce the predefined environment directly into the multiple-choice questions in natural language format, under the _context_ section of the prompt.

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
		<td>61.60</td>
	</tr>
	<tr align="center">
		<td align="left">Proofwriter</td>
		<td>34.33</td>
		<td><b>49.17</b></td>
		<td>37.83</td>
		<td></td>
		<td></td>
		<td>74.17</td>
	</tr>
	<tr align="center">
		<td align="left">FOLIO</td>
		<td><b>51.96</b></td>
		<td>51.00</td>
		<td>36.27</td>
		<td></td>
		<td></td>
		<td>57.35</td>
	</tr>
	<tr align="center">
		<td align="left">LogicalDeduction</td>
		<td>35.33</td>
		<td>39.00</td>
		<td><b>60.67</b></td>
		<td></td>
		<td></td>
		<td>77.00</td>
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

Table 1 shows the results of the experiments with the open-source model. For Llama-3 8B it shows that Logic-LM only scored highest on the LogicalDeduction dataset, where it scored 60.67 compared to 35.33 and 39.00 for Standard and CoT respectively. For the other datasets Logic-LM got outperformed by either the Standard or the CoT method. <!-- Complete once 70B results are in -->

One reason why Logic-LM performs worse than the other methods could be that the dataset on which Llama-3 was trained lacks logic problems that are written in symbolic language. According to https://daily.dev/blog/meta-llama-3-everything-you-need-to-know-in-one-place llama-3 was trained to be good in logical problems and reasoning, however this training was probably mostly done in logical reasoning with natural language, but not in converting natural language logic to symbolic language logic, since that is less relevant for most users. This would explain why it does perform well with the Standard and CoT method, where the model can solve the logic with natural language, but does not perform well when having to do something with symbolic language, like converting from natural to symbolic language. Logic-LM does score high on the LogicalDeduction dataset, which might mean that Llama-3 was trained more on constraint satisfaction. Another explanation could be that since the symbolic formulation of constraint satisfaction logic is much simpler and more familiar to natural language compared to other logic types, it is easier for the model to convert the natural language to symbolic logic, making it score better.

Comparing these results to the GPT model results from the original paper (Pan et al., 2023), we observe that the 8B version of Llama-3 generally performs worse than the GPT models. Logic-LM has significantly lower scores compared to all GPT models for the Proofwriter, FOLIO and AR-LSAT dataset and slightly lower scores for the LogicalDeduction dataset. Only on the PrOntoQA Llama-3 8B achieved a higher score than gpt-3.5-turbo, while still having worse scores when using the other GPT models. For the Standard and CoT method we observe similar performance to gpt-3.5-turbo while also being outperformed by the other GPT models. The 70B version however does achieve more similar scores as the OpenAI models. While still being outperformed by GPT-4 on all datasets, it does score higher than ChatGPT and GPT-3.5 on some datasets. It outperforms ChatGPT on all datasets except FOLIO and outperforms GPT 3.5 on both Proofwriter and LogicalDeduction. Llama-3 70B's better performance compared to the 8B version was to be expected, since Llama-3 70B is significantly larger and also performs better in Meta's own benchmarks (https://ai.meta.com/blog/meta-llama-3/). Taking this into account, it is noteworthy that the 8B version outperforms the 70B version on ProtoQA, achieving a score of 67.40 versus the 61.60 from 70B.
There are multiple (_More results and analysis will follow in final version_)

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
		<td>91.60%</td>
		<td>69.65</td>
		<td>100.00%</td>
		<td>61.60</td>
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
		<td>13.00%</td>
		<td>70.51</td>
		<td>80.83%</td>
		<td>81.44</td>
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
		<td>37.25%</td>
		<td>48.68</td>
		<td>67.16%</td>
		<td>72.26</td>
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
		<td>100.00%</td>
		<td>60.67</td>
		<td>100.00%</td>
		<td>77.00</td>
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
		<td>20.35%</td>
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
	<tr align="center">
    	<td>ProntoQA</td>
    	<td>4</td>
    	<td>60.0</td>
    	<td>20.0</td>
    	<td>100.0</td>
	</tr>
    <tr align="left">
   	 <td colspan=7><b>Table 3.</b>  Chat-GPT (GPT 3.5) Logic-LM results</td>
</table>

Pan et al. (2023) employed three closed-source LLMs: ChatGPT, GPT-3.5, and GPT-4. Our extension of the Logic-LM involves open-source LLMs. However, ChatGPT is publicly accessible for manual query-based messaging. To validate the claims of Pan et al. (2023), we queried ChatGPT five times for each logic type, presenting the prompt and a new problem and question. Results are summarized in Table 3. ... (_qualitative results will come_)

## <a name="conclusion">Conclusion</a>

Our experiments show that it is possible to use Logic-LM with open-source language models. However the achieved performance with one SoTA open-source language model (Llama-3) is clearly lower than the performance of the closed-source GPT models. The GPT models scored better on all datasets except on PrOntoQA, where Llama performed better than ChatGPT. Interestingly with the Standard and CoT method similar performance was achieved to ChatGPT and GPT 3.5, so only Logic-LM really drops in performance with the open-source model. It should be noted that once better open-source models become available, they could perform equally as good or better than closed-source models, since the achieved performance is evidently related to the used language model.

Using Llama-3 we observed that the performance of Logic-LM is significantly worse than the Standard and CoT methods, except on the LogicalDeduction dataset, where Logic-LM performed slightly better. This contradicts the findings of the original authors, since they found Logic-LM to outperform the other 2 methods on almost all datasets with all three GPT models. This is likely due to a difference in performance of the open-source language model itself. Moreover the difference could lead to wrong input for the logic solvers, making them unable to correctly solve the problems. (_More analysis will follow in final version_)

## Authors' Contributions

_example_

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

[9] C. Wang, C. Ross, Y.-L. Kuo, B. Katz, and A. Barbu, "Learning a natural-language to LTL executable semantic parser for grounded robotics," _CoRR_, vol. abs/2008.03277, 2020. [Online]. Available: https://arxiv.org/abs/2008.03277

[10] M. Y. Vardi and P. Wolper, "Reasoning about Infinite Computations," _Information and Computation_, vol. 115, no. 1, pp. 1-37, 1994. [Online]. Available: https://doi.org/10.1006/inco.1994.1092.