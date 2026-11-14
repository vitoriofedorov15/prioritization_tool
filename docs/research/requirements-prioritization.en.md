# User Requirements Prioritization Based on Crisp and Fuzzy Approaches

**Viktor Fedorov · Research term project · Software Engineering, Higher School of Economics**

[Original English PDF](requirements-prioritization.en.pdf) · [Research overview and source notes](README.md) · [Application README](../../README.md)

This GitHub-readable edition was assembled from the recovered English LaTeX parts dated 26–27 May 2026 and checked against the English PDF generated on 27 May 2026. The report retains its 2025 title-page context. Mathematical content, worked examples, and references are preserved; table layout, citation links, and navigation are adapted for Markdown. The PDF preserves the original pagination and typesetting.

> Source note: the PDF has 63 pages; its abstract states 75. Some historical section counts in the prose also differ from the final contents. These source statements are retained below. See the research overview for version notes.

## Contents

- [List of Contributors](#section-1)
- [Abstract](#section-2)
- [Introduction](#section-3)
- [Analysis of the MoSCoW Method for Requirements Prioritization](#section-4)
- [Analysis of the Kano Model for Requirements Prioritization](#section-5)
- [Analysis of the TOPSIS Method for Requirements Prioritization](#section-6)
- [Analysis of TOPSIS with Interval Ratings](#section-7)
- [Transition to Fuzzy TOPSIS Type-1 with Trapezoidal Membership Functions](#section-8)
- [Analysis of the Intuitionistic Fuzzy TOPSIS Method](#section-9)
- [Analysis of the Fuzzy Delphi Type-2 Method for Requirements Prioritization](#section-10)
- [Analysis of the Delphi Intuitionistic Method for Requirements Prioritization](#section-11)
- [Analysis of the Fuzzy AHP Type-1 (Analytic Hierarchy Process) Method for Requirements Prioritization](#section-12)
- [Analysis of the Fuzzy AHP Type-2 Method for Requirements Prioritization](#section-13)
- [AI-Enhanced Web Application for Requirements Prioritization](#section-14)
- [Conclusion](#section-15)
- [References](#section-16)
- [Appendix A. Description of the Software Implementation](#section-17)

---

<a id="section-1"></a>

## List of Contributors

Viktor Fedorov — student of the academic programme “Software Engineering”,\
Higher School of Economics

<a id="section-2"></a>

## Abstract

The report contains 75 pages. 37 sources were used.

**Keywords:** requirements prioritization, crisp methods, fuzzy methods, MoSCoW, Kano model, TOPSIS, Fuzzy Delphi, Fuzzy AHP, web application, REST API, AI interpretation, Google Gemini, conflict detection, Python.

**Brief description of the research object and subject:**

- **Research object:** the process of prioritizing user requirements in software development.

- **Research subject:** the use of crisp and fuzzy mathematical methods for analyzing and managing user requirements under conditions of uncertainty, and the augmentation of their outputs with generative AI interpretation.

**Project goal:**

- Development of software for automating the prioritization of user requirements using crisp and fuzzy methods, together with an AI-enhanced web interface that makes the results accessible and interpretable.

**Methods and methodology:**

- Three crisp methods were used: MoSCoW, Kano model, TOPSIS.

- Three fuzzy methods were used: Fuzzy TOPSIS (Type-1 and interval), Fuzzy Delphi (intuitionistic and Type-2), Fuzzy AHP (Type-1 and Type-2).

- Stakeholder weights, linguistic and variative ratings were taken into account; normalization and aggregation mechanisms were implemented.

- A RESTful web service (FastAPI) and a React-based single-page application were developed to expose all methods through a browser interface.

- Google Gemini 2.0 Flash was integrated to provide automatic result interpretation, stakeholder conflict analysis, and conversational assistance.

**Project results:**

- A Python desktop application (tkinter) with a graphical user interface enabling automated requirements prioritization and PDF report generation.

- A browser-based web application providing drag-and-drop CSV upload, interactive priority charts, and a multi-method comparative dashboard.

- An AI analytics layer offering natural-language interpretation of results, AI-enriched conflict detection, and a streaming conversational assistant.

**Application of results:**

- The project results can be used for educational and research purposes, as well as in requirements management practice for both agile and traditional projects.

**Economic efficiency:**

- Increased transparency of decision-making and reduced risk of incorrect prioritization.

- Reduced time spent on manual discussion and analysis of requirements through automated conflict detection and AI-generated summaries.

<a id="section-3"></a>

## Introduction

Software development is a complex, multi-stage process covering a wide range of activities, from problem domain analysis to deployment and maintenance of the software product. One of the most critical stages of this process is requirements engineering, as it is here that stakeholder expectations are formalized, the functional and non-functional characteristics of the system are defined, and the foundations of the future software architecture are established. Errors made during requirements engineering can entail significant costs and, in some cases, lead to project failure.

The Software Requirements Knowledge Area covers seven key sub-areas [\[1\]](#reference-1): software requirements fundamentals, requirements process, requirements elicitation, requirements analysis, requirements specification, requirements validation, and practical considerations. Each of these sub-areas plays a critically important role in ensuring that the developed software genuinely solves the problem it was designed to address.

At the basic level, a software requirement is defined as a property that a system must possess in order to solve a specific real-world problem [\[1\]](#reference-1). Requirements are divided into several main types. First, there are product requirements and process requirements. The former concern properties of the system itself (e.g., “the software must process orders in no more than 2 seconds”), while the latter impose constraints on the development process (e.g., “development must be carried out in Java”). There are also functional and non-functional requirements. Functional requirements define what the system must do, while non-functional requirements establish how it must do it, specifying parameters such as reliability, performance, security, maintainability, and scalability.

Some requirements belong to the category of emergent properties — they cannot be realized by individual system components but arise only as a result of their interaction. An example is a requirement for overall system throughput, which depends on the coordinated operation of software modules, servers, network components, and user interactions.

A key property of any requirement is its verifiability. Only a verifiable requirement can be formally assessed and accepted into operation. Therefore, special attention is paid to quantitative formulation of requirements, which eliminates ambiguity and subjectivity. For instance, instead of the abstract phrase “the software must be user-friendly,” a specific measurable requirement should be used, such as: “80% of users must rate the interface as ‘user-friendly’ based on usability testing results.”

The requirements management process is treated not as a one-time stage but as a continuous activity that begins at project initiation and continues throughout the entire software lifecycle. It includes identifying requirements as configuration items, change management, requirements negotiation between stakeholders, and keeping requirements up to date. This is especially important in modern development, where requirements are subject to frequent changes driven by market conditions, the business environment, and technological constraints.

One of the key tasks at this stage is requirements prioritization. Since development resources are limited, it is necessary to determine which requirements have the highest value for the business and users and should be implemented first. This is especially relevant in agile development methodologies [\[4\]](#reference-4), where planning is carried out in iterations and it is important to be able to flexibly assign priorities.

Requirements prioritization is complicated by many factors [\[2\]](#reference-2): diversity of stakeholders, differences in their interests, large volumes of requirements, varying degrees of importance and technical feasibility. Traditional approaches use crisp prioritization methods such as MoSCoW, Kano model, TOPSIS, AHP, etc. [\[6\]](#reference-6), [\[12\]](#reference-12), [\[17\]](#reference-17), [\[29\]](#reference-29). These methods formalize the selection process and produce unambiguous results. However, they often fail to account for the uncertainty and subjectivity of expert assessments [\[2\]](#reference-2), as well as the blurry boundaries between importance levels of requirements.

To address these aspects, fuzzy prioritization methods based on fuzzy set theory [\[16\]](#reference-16) are increasingly applied. Methods such as Fuzzy TOPSIS, Fuzzy Delphi, and Fuzzy AHP allow modeling of the vague concepts inherent in human perception, thereby providing a more realistic assessment of priorities. This study examines three classes of fuzzy sets: Type-1 fuzzy sets (T1FS), Type-2 fuzzy sets (T2FS), and intuitionistic fuzzy sets (IFS) [\[20\]](#reference-20), making it possible to account not only for the degree of membership but also for distrust of the rating and the level of uncertainty.

The report is organized into two parts. The first part (Sections 1–8) presents a systematic theoretical and practical analysis of eight requirements prioritization methods, illustrating each with worked examples and discussing the conditions under which it is most appropriate. The second part (Section 9) describes the development of an AI-enhanced web application that exposes all eight methods through a browser-based interface and augments the numerical results with a generative AI analytics layer built on Google Gemini 2.0 Flash.

The following sections provide a detailed examination of the following requirements prioritization approaches: the MoSCoW method, the Kano model, the TOPSIS method and its modifications with interval and fuzzy ratings, the Delphi method, and the AHP method.

The analysis of each of the listed methods will be accompanied by input data examples, calculation implementations, and a comparison of results, which will justify the choice of the most effective approaches to requirements prioritization under conditions of uncertainty.

The requirements engineering process cannot be considered in isolation. It includes the following stages: _requirements elicitation_, comprising the collection of information from various sources — business goals, domain knowledge, analysis of the system’s operational environment, and stakeholder opinions; _requirements analysis_, during which conflicts are identified and resolved, system boundaries are refined, requirements are allocated among components, and negotiations between process participants are conducted; _requirements specification_, where formal documents are produced that are subject to review, approval, and agreement; _requirements verification and validation_, including reviews, prototyping, model validation, and acceptance testing; and _change management_, aimed at keeping requirements current as the project evolves.

In practical work, special attention is paid to the iterative nature of the requirements engineering process. In practice, requirements are often elicited and refined gradually as the project progresses. This reflects the real dynamics of development, especially under conditions of high uncertainty, tight deadlines, and limited resources.

Thus, this work aims at a systematic study of requirements prioritization methods capable of functioning effectively under conditions of multi-criteria decision-making, high uncertainty, and the human factor. It not only analyzes existing approaches but also proposes possible directions for automating the prioritization process using fuzzy logic and generative AI, which is a relevant step toward improving software development quality.

<a id="section-4"></a>

## Analysis of the MoSCoW Method for Requirements Prioritization

### Introduction

The MoSCoW method is one of the most widely used approaches to requirements prioritization in software development. It was proposed by Dai Clegg in 1994 within the DSDM (Dynamic Systems Development Method) methodology [\[8\]](#reference-8). The name MoSCoW is a mnemonic acronym formed from the first letters of the four requirement categories, with lowercase “o” letters added only for ease of pronunciation [\[9\]](#reference-9).

The method allows requirements to be classified by their degree of importance and urgency, making it particularly useful under conditions of limited time and resources — for example, when working with agile development methodologies [\[6\]](#reference-6). It divides requirements into four categories:

- **M (Must-have)** — critically important features without which the product cannot be launched.

- **S (Should-have)** — important but non-critical features that are desirable to implement.

- **C (Could-have)** — useful features whose absence is not critical.

- **W (Won’t-have)** — features not planned for the current release.

### Data for Analysis

The MoSCoW method can be applied to any number of criteria that are important for product evaluation. For example, criteria such as **security, usability, business value, performance, development cost, risk**, and others may be used [\[6\]](#reference-6). In this work, for simplicity of analysis, three criteria are considered: **security, usability, and business value**. In the developed software, the user can define their own criteria in the input file for analysis using this and other prioritization methods, making the application more flexible.

#### Input Data Format

The source data are presented as a **CSV file** in which each stakeholder rates the requirements according to the MoSCoW categories. However, in real-world scenarios, stakeholders may **not be fully certain about their choice** and provide **composite ratings**, such as:

- **“M/S”** — meaning the rating oscillates between M (Must-have) and S (Should-have).

- **“80% M, 20% S”** — indicating that the stakeholder is 80% confident in M but also allows 20% for S.

Thus, **the input CSV file is organized so that each rating is represented in percentage format**, for example:

- **“100% M”** instead of simply “M”.

- **“60% S, 40% C”** instead of an intermediate choice between S and C.

The software also implements validation of composite input ratings. Only adjacent categories are permitted: M/S, S/C, and C/W. Combinations such as M/C or M/W are considered logically incorrect and are automatically rejected [\[17\]](#reference-17), [\[19\]](#reference-19), [\[16\]](#reference-16).

#### Example Table with Variative Ratings

**Table 1. MoSCoW requirement ratings with variative assessments (5 alternatives)**

| **Alternative**           | **Security** / S1 | **Security** / S2 | **Security** / S3 | **Usability** / S1 | **Usability** / S2 | **Usability** / S3 | **Business Value** / S1 | **Business Value** / S2 | **Business Value** / S3 |
| :------------------------ | :---------------: | :---------------: | :---------------: | :----------------: | :----------------: | :----------------: | :---------------------: | :---------------------: | :---------------------: |
| Social Media Login        |      100% W       |      100% W       |      100% M       |       100% W       |       100% S       |       100% M       |         100% M          |         100% S          |         100% S          |
| Two-Factor Authentication |      100% W       |   60% M, 40% S    |      100% M       |       100% W       |       100% C       |       100% C       |         100% M          |         100% W          |         100% S          |
| CRM Integration           |   60% S, 40% C    |      100% S       |   60% M, 40% S    |       100% M       |       100% C       |    60% M, 40% S    |         100% W          |      80% M, 20% S       |         100% M          |
| Data Backup               |      100% W       |   80% M, 20% S    |   60% M, 40% S    |       100% M       |       100% W       |    60% S, 40% C    |      60% S, 40% C       |      60% S, 40% C       |         100% W          |
| PDF Data Export           |      100% C       |   60% S, 40% C    |   60% S, 40% C    |       100% W       |       100% W       |       100% W       |         100% C          |      60% S, 40% C       |         100% W          |

#### Stakeholder Opinion Weight

Each stakeholder may have a **different level of influence** on decision-making, depending on factors such as industry experience, degree of project involvement, and decision-making responsibility [\[2\]](#reference-2), [\[29\]](#reference-29). In the software, each stakeholder is assigned a **weight of opinion** used during aggregation. A normalized weight scale from $`0.5`$ to $`2.0`$ is used: $`0.5`$ — reduced influence (secondary participants), $`1.0`$ — standard level of influence, $`2.0`$ — maximum influence (key decision-makers). This scale provides: a sufficient range for differentiation (a $`4\times`$ difference), intuitive clarity (doubling the weight $`\Rightarrow`$ doubling the influence), and a balance of influence without excessive skew [\[6\]](#reference-6).

**Table 2. Weight coefficients for stakeholders**

| **Stakeholder** | **Opinion Weight** |
| :-------------: | :----------------: |
|       S1        |        1.0         |
|       S2        |        1.5         |
|       S3        |        2.0         |

<span id="tab:stakeholder_weights" label="tab:stakeholder_weights"></span>

### Score Aggregation and Prioritization

Two aggregation methods can be used to obtain the final priority:

1.  **Traditional aggregation** [\[10\]](#reference-10): all ratings are combined into a single summary table where a weighted average score is calculated.

2.  **Individual-result-based aggregation** [\[6\]](#reference-6): first, an individual priority of alternatives is calculated for each stakeholder; then the resulting values are aggregated taking weights into account.

### Final Priority Calculation Methods

In addition to the basic method $`\text{Score} = 3M + 2S + C`$, the following variants are considered:

- **Weighted sum method** [\[29\]](#reference-29), [\[17\]](#reference-17):

  ```math
  \text{Score} = w_1 \cdot M + w_2 \cdot S + w_3 \cdot C + w_4 \cdot W,
  ```

  Before use in calculations, the weights must be normalized so that their sum equals one:

  ```math
  w_i^\text{norm} = \frac{w_i}{\sum_{j=1}^{4} w_j}, \quad i = 1, 2, 3, 4.
  ```

- **Logarithmic scoring method** [\[18\]](#reference-18):

  ```math
  \text{Score} = \log(1 + M) + 0.8 \log(1 + S) + 0.5 \log(1 + C),
  ```

- **Exponential growth method** [\[18\]](#reference-18):
  ```math
  \text{Score} = 4^M + 2^S + C,
  ```

### Priority Calculation with Expert Weights

Calculation methods:

- **Classical method**: $`\text{Score} = 3M + 2S + 1C + 0W`$ [\[6\]](#reference-6).

- **Exponential method**: $`\text{Score} = 4^M + 2^S + C`$ [\[18\]](#reference-18).

In each method, the final score for each alternative is first calculated using the formulas above (within a single stakeholder), after which aggregation is performed taking expert weights into account.

With the traditional aggregation method, the final priority is defined as the weighted sum of individual scores:

```math
\text{Final Priority} = \sum_{i} \left( \text{Score}_{i} \times \text{Weight}_{i} \right) \href{#reference-10}{[10]}
```

Here $`\text{Score}_{i}`$ is the calculated score (priority) for the given alternative from expert $`i`$ using the chosen formula; $`\text{Weight}_{i}`$ is the opinion weight of expert $`i`$, reflecting their degree of influence on the final result.

With the individual aggregation method, the final priority is defined as the weighted average of individual scores:

```math
\text{Average Priority} = \frac{\sum_{i} \left( \text{Score}_{i} \times \text{Weight}_{i} \right)}{\sum \text{Weight}_{i}} \href{#reference-6}{[6]}
```

This approach allows for the fact that opinions of different experts may have different significance, and preserves calculation transparency by separating the stages: first the priority value is computed for each expert, then they are aggregated.

#### Results of the Traditional Method with Weights

Priority calculations are performed taking stakeholder weights into account. In this and the following subsection, the weights are set as follows:

- S1 — 1.0

- S2 — 1.5

- S3 — 2.0

**Table 3. Calculated priorities using the traditional method with stakeholder weights**

| **Alternative**           | **Classical Method** | **Exponential Method** | **Final Priority (%)** |
| :------------------------ | :------------------: | :--------------------: | :--------------------: |
| Social Media Login        |         13.6         |           48           |          72.5          |
| Two-Factor Authentication |         15.8         |           62           |          93.1          |
| CRM Integration           |         17.9         |           70           |         100.0          |
| Data Backup               |         16.4         |           66           |          94.3          |
| PDF Data Export           |         12.2         |           44           |          62.1          |

<span id="tab:weighted_traditional_methods" label="tab:weighted_traditional_methods"></span>

#### Results of the Individual Aggregation Method with Weights

In this method, the priority is first computed separately for each stakeholder, then the results are averaged.

**Table 4. Calculated priorities using the individual aggregation method with stakeholder weights**

| **Alternative**           | **Classical Method** | **Exponential Method** | **Average Priority (%)** |
| :------------------------ | :------------------: | :--------------------: | :----------------------: |
| Social Media Login        |         12.9         |           45           |           70.2           |
| Two-Factor Authentication |         14.5         |           58           |           87.3           |
| CRM Integration           |         16.3         |           68           |           98.0           |
| Data Backup               |         15.1         |           64           |           92.1           |
| PDF Data Export           |         11.5         |           42           |           60.8           |

#### Analysis of Results and Conclusions

As can be seen from the tables, incorporating expert weights increases the influence of stakeholders with higher weights. This is particularly evident in the individual aggregation method, where each expert’s weight is taken into account when averaging the priorities.

The results presented are normalized on a percentage scale where **the maximum priority is set to 100%**. This makes it easier to compare the importance of alternatives and make decisions based on relative values.

Moreover, the results depend on the Score calculation method. The **classical method** produces a uniform distribution in which Must-have requirements receive the maximum weight and Won’t-have are excluded. At the same time, the **exponential method** significantly increases the gap between high- and low-priority alternatives, since Must-have requirements receive **exponentially greater influence**.

The aggregation method also plays an important role. The **traditional method** combines all ratings at once, providing a holistic picture of priorities, while the **individual aggregation method** allows for varying degrees of stakeholder confidence and differences in their priorities, making it more flexible.

The choice of method depends on the analysis objectives: the exponential method is better at identifying **key priorities**, while the classical method provides a **balanced priority distribution**. It should be noted that a balanced priority distribution is not always a goal in itself. The main objective is not to distribute scores evenly, but to form a **rational priority list** that reflects the actual significance of requirements, taking into account expert opinions, their confidence, and their weights. Such a list supports effective decision-making.

Thus, the MoSCoW method with variative ratings, stakeholder weights, and different aggregation methods allows flexible assessment of requirements and adaptation of the analysis to specific project conditions.

<a id="section-5"></a>

## Analysis of the Kano Model for Requirements Prioritization

### Introduction

The Kano model is used to assess the impact of requirements on user satisfaction. It was proposed by Japanese professor Noriaki Kano in 1984 and is used to classify requirements based on how their presence or absence affects the end users’ perception of the product [\[11\]](#reference-11).

The method classifies requirements into the following categories [\[12\]](#reference-12), [\[13\]](#reference-13):

- **Must-be (Basic)** — absence causes strong dissatisfaction; presence is taken for granted.

- **Performance (One-dimensional)** — the better it is implemented, the higher the satisfaction.

- **Attractive (Excitement)** — unexpected but pleasant features whose absence does not cause dissatisfaction.

- **Indifferent** — have no significant impact on satisfaction.

- **Reverse** — may cause a negative reaction if present.

To determine the category of a requirement, the Kano questionnaire is used, which includes two questions:

1.  How do you feel if this feature is present?

2.  How do you feel if this feature is absent?

The answers are analyzed using the **Kano matrix**, which determines membership in one of the categories [\[12\]](#reference-12), [\[15\]](#reference-15).

### Data for Analysis

The Kano model can be applied to any number of criteria important for product evaluation. For example, criteria such as **security, usability, business value, performance, development cost, risk**, and others may be used. In this work, for simplicity of analysis, three criteria are considered: **security, usability, and business value**. However, the proposed data processing methods remain applicable for a larger number of criteria. Similarly to the MoSCoW implementation, in the developed software the user can define their own criteria in the input file [\[6\]](#reference-6), [\[12\]](#reference-12).

#### Input Data Format

The source data are presented as a **CSV file** in which each stakeholder rates requirements on the Kano scale. For each criterion, stakeholders answer the functional and dysfunctional questions, and the results are aggregated to obtain the final category [\[13\]](#reference-13), [\[14\]](#reference-14).

#### Example CSV File

The data are organized in a CSV file of the following format:

    Alternative,Stakeholder,Functional,Dysfunctional,Weight
    Social Media Login,S1,Must-be,Indifferent,1.0
    Two-Factor Authentication,S1,Must-be,Must-be,1.0
    PDF Data Export,S1,Performance,Indifferent,1.0
    CRM Integration,S1,Attractive,Indifferent,1.0
    Data Backup,S1,Must-be,Performance,1.0
    Social Media Login,S2,Performance,Indifferent,1.5
    Two-Factor Authentication,S2,Must-be,Must-be,1.5
    PDF Data Export,S2,Attractive,Indifferent,1.5
    CRM Integration,S2,Indifferent,Reverse,1.5
    Data Backup,S2,Must-be,Performance,1.5
    Social Media Login,S3,Attractive,Indifferent,2.0
    Two-Factor Authentication,S3,Performance,Indifferent,2.0
    PDF Data Export,S3,Must-be,Must-be,2.0
    CRM Integration,S3,Indifferent,Reverse,2.0
    Data Backup,S3,Must-be,Performance,2.0

Each row corresponds to one stakeholder’s assessment of one alternative. The columns are:

- **Alternative** — the feature or requirement under consideration;

- **Stakeholder** — the identifier of the participant who provided the rating (e.g., S1, S2, S3);

- **Functional** — the user’s reaction when the feature is present (e.g., Must-be, Performance, Attractive, etc.);

- **Dysfunctional** — the reaction when the feature is absent (e.g., Indifferent, Reverse, etc.);

- **Weight** — the relative significance of this stakeholder’s opinion [\[11\]](#reference-11), [\[13\]](#reference-13).

This format allows data to be processed programmatically, scores to be aggregated by weights, and the Kano classification rules to be applied automatically [\[12\]](#reference-12), [\[15\]](#reference-15).

#### Description of Stakeholder Weights

Each stakeholder has their own **weight** reflecting their influence on decision-making. The weight may be assigned based on factors such as:

- The stakeholder’s industry experience.

- Degree of project involvement.

- Responsibility for decision-making.

Using weights in the Kano model makes it possible to precisely account for the contribution of each expert to the final classification [\[12\]](#reference-12), [\[13\]](#reference-13).

In this example, a scenario with 3 stakeholders is considered. For clarity of the calculations, stakeholder weights are distributed as follows:

- **S1**: Weight = 1.0 (baseline level of influence).

- **S2**: Weight = 1.5 (moderate influence).

- **S3**: Weight = 2.0 (high influence).

#### Example Rating Table

**Table 5. Kano questionnaire results for Stakeholder 1**

|                           |                   |                   |
| :------------------------ | :---------------: | :---------------: |
| **Alternative**           | **Stakeholder 1** | **Stakeholder 1** |
|                           |    Functional     |   Dysfunctional   |
| Social Media Login        |      Must-be      |    Indifferent    |
| Two-Factor Authentication |      Must-be      |      Must-be      |
| PDF Data Export           |    Performance    |    Indifferent    |
| CRM Integration           |    Attractive     |    Indifferent    |
| Data Backup               |      Must-be      |    Performance    |

<span id="tab:kano_ratings_1" label="tab:kano_ratings_1"></span>

**Table 6. Kano questionnaire results for Stakeholder 2**

|                           |                   |                   |
| :------------------------ | :---------------: | :---------------: |
| **Alternative**           | **Stakeholder 2** | **Stakeholder 2** |
|                           |    Functional     |   Dysfunctional   |
| Social Media Login        |    Performance    |    Indifferent    |
| Two-Factor Authentication |      Must-be      |      Must-be      |
| PDF Data Export           |    Attractive     |    Indifferent    |
| CRM Integration           |    Indifferent    |      Reverse      |
| Data Backup               |      Must-be      |    Performance    |

<span id="tab:kano_ratings_2" label="tab:kano_ratings_2"></span>

**Table 7. Kano questionnaire results for Stakeholder 3**

|                           |                   |                   |
| :------------------------ | :---------------: | :---------------: |
| **Alternative**           | **Stakeholder 3** | **Stakeholder 3** |
|                           |    Functional     |   Dysfunctional   |
| Social Media Login        |    Attractive     |    Indifferent    |
| Two-Factor Authentication |    Performance    |    Indifferent    |
| PDF Data Export           |      Must-be      |      Must-be      |
| CRM Integration           |    Indifferent    |      Reverse      |
| Data Backup               |      Must-be      |    Performance    |

<span id="tab:kano_ratings_3" label="tab:kano_ratings_3"></span>

### Score Aggregation

To convert categories to a numerical scale, the following weights were used [\[12\]](#reference-12), [\[13\]](#reference-13):

- Must-be: 4

- Performance: 3

- Attractive: 2

- Indifferent: 1

- Reverse: 0

#### Traditional Aggregation Method

The final priority of each alternative is calculated taking the spread of opinions into account using the formula:

```math
\text{Score} = \text{Mean} - 0.5 \times \text{Standard Deviation}
```

[\[13\]](#reference-13). The higher the final priority, the more important the feature. This approach not only accounts for the average score but also penalizes importance in the case of strong disagreement among opinions, which is important in multi-criteria decision-making.

#### Weighted Aggregation Method

This method takes stakeholder weights into account. The formula for calculating the priority is:

```math
\text{Score} = \frac{\sum_{i} \left( \text{Score}_{i} \times \text{Weight}_{i} \right)}{\sum \text{Weight}_{i}}
```

[\[2\]](#reference-2), [\[12\]](#reference-12), where $`\text{Score}_{i}`$ is the score of stakeholder $`i`$ and $`\text{Weight}_{i}`$ is their weight. The method accounts for the heterogeneous influence of different participants, which is critical in systems with key stakeholders.

### Method Results

**Table 8. Comparison of traditional and weighted aggregation methods**

| **Alternative**           | **Traditional** **Method** | **Weighted** **Method** | **Final Priority** **(traditional method, %)** | **Final Priority** **(weighted method, %)** |
| :------------------------ | :------------------------: | :---------------------: | :--------------------------------------------: | :-----------------------------------------: |
| Data Backup               |            3.50            |          3.65           |                   **100.0**                    |                  **100.0**                  |
| Two-Factor Authentication |            3.33            |          3.45           |                      95.1                      |                    94.5                     |
| PDF Data Export           |            2.50            |          2.60           |                      71.4                      |                    71.2                     |
| Social Media Login        |            2.00            |          2.10           |                      57.1                      |                    57.5                     |
| CRM Integration           |            0.83            |          0.90           |                      23.7                      |                    24.7                     |

#### Calculation of the Final Priority as a Percentage

The final priority is calculated using the formula:

```math
\text{Priority (\%)} = \frac{\text{Score}}{\text{Max Score}} \times 100
```

[\[18\]](#reference-18)

where $`\text{Max Score}`$ is the highest result among all alternatives (for the traditional and weighted method respectively). Such normalization is widely used in multi-criteria analysis systems and allows direct comparison between alternatives.

### Conclusions

Based on the data obtained, the following conclusions can be drawn:

- **Data Backup** and **Two-Factor Authentication** received the highest scores and are critically important requirements.

- **PDF Data Export** and **Social Media Login** have medium priority and can be implemented as needed.

- **CRM Integration** has the lowest priority; its implementation can be deferred.

The Kano model, accounting for the spread of opinions and stakeholder weights, allows not only determining the importance of requirements but also considering the degree of opinion consensus in decision-making [\[13\]](#reference-13), [\[12\]](#reference-12). The **traditional method** provides a balanced assessment, while the **weighted method** accounts for the influence of more authoritative stakeholders [\[2\]](#reference-2).

<a id="section-6"></a>

## Analysis of the TOPSIS Method for Requirements Prioritization

### Introduction

The TOPSIS method (Technique for Order Preference by Similarity to Ideal Solution) is one of the most popular multi-criteria decision-making methods used for ranking alternatives. The method was proposed by Ching-Lai Hwang and Kwangsun Yoon in 1981 [\[21\]](#reference-21). The name TOPSIS is an acronym formed from the initial letters of the English name of the method.

The method is based on two principles [\[17\]](#reference-17):

1.  The best alternative should be as close as possible to the Positive Ideal Solution (PIS).

2.  The best alternative should be as far as possible from the Negative Ideal Solution (NIS).

The **Positive Ideal Solution (PIS)** is the alternative that has the best values across all criteria (e.g., maximum value, minimum cost, highest security, etc.). The **Negative Ideal Solution (NIS)** is a hypothetical alternative that has the worst possible values across the same criteria.

Thus, the TOPSIS method assumes that preference is given to alternatives that are simultaneously as close as possible to the PIS and as far as possible from the NIS, allowing both positive and negative aspects to be considered in decision-making [\[21\]](#reference-21).

This method allows alternatives to be evaluated and compared using the concept of spatial distance between each alternative and two reference points [\[17\]](#reference-17).

### Advantages of the TOPSIS Method

- Simplicity and clarity — the method is easy to implement and interpret [\[21\]](#reference-21).

- Considers multiple criteria simultaneously — allows objective evaluation of alternatives even with conflicting indicators [\[17\]](#reference-17).

- Applicable to various data types — both quantitative and qualitative criteria can be used.

- Provides clear ordering of alternatives — the final value $`C_i`$ immediately identifies the best alternative.

- Ability to account for criterion weights — different degrees of importance can be assigned to each criterion [\[29\]](#reference-29).

- Accounts for criterion directionality — the method correctly handles both benefit criteria (to be maximized) and non-benefit criteria (to be minimized) [\[21\]](#reference-21).

### Data for Analysis

A table of alternatives and their values by criteria is used for analysis. Stakeholder weights are specified in the CSV file and taken into account in calculations [\[17\]](#reference-17), [\[6\]](#reference-6).

Example CSV file:

    Alternative,Security,Usability,Business Value,Stakeholder Weight
    Social Media Login,7,8,6,0.3
    Two-Factor Authentication,9,6,5,0.4
    PDF Data Export,6,9,7,0.2
    CRM Integration,5,7,9,0.1
    Data Backup,8,6,8,0.5

In the table, each row corresponds to one alternative. The columns are:

- **Alternative** — the name of the feature or requirement;

- **Security, Usability, Business Value** — scores on the respective criteria (on a numerical scale, e.g., from 1 to 10);

- **Stakeholder Weight** — the relative significance of the rating given by a particular participant (e.g., 0.3, 0.4, etc.), used in aggregation [\[2\]](#reference-2).

### Data Normalization

Since stakeholders may provide answers on different scales, the data are normalized to bring them to a common scale. The following normalization method was selected as an example [\[21\]](#reference-21):

```math
r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{n} x_{ij}^2}}
```

where $`x_{ij}`$ is the raw value of criterion $`j`$ for alternative $`i`$; $`r_{ij}`$ is the normalized value of criterion $`j`$ for alternative $`i`$; $`n`$ is the number of alternatives.

Other normalization approaches also exist. Normalization eliminates the effect of different units of measurement and value ranges, making criteria comparable.

### Data Weighting

Normalized values are multiplied by stakeholder weights to account for the importance of each criterion:

```math
v_{ij} = w_j \cdot r_{ij}
```

where $`w_j`$ is the weight of criterion $`j`$ and $`v_{ij}`$ is the weighted normalized value [\[17\]](#reference-17), [\[29\]](#reference-29).

### Determining PIS and NIS

Based on the weighted normalized matrix, the following are determined:

- **Positive Ideal Solution (PIS)** — the best values for each criterion.

- **Negative Ideal Solution (NIS)** — the worst values for each criterion.

Calculation formulas:

```math
PIS_j = \max v_{ij}, \quad j = 1, 2, \ldots, m
```

```math
NIS_j = \min v_{ij}, \quad j = 1, 2, \ldots, m
```

[\[17\]](#reference-17), [\[21\]](#reference-21)

Computations for the CSV file table:

**Table 9. Example source data from the CSV file**

| **Alternative**           | **Security** | **Usability** | **Business Value** | **Stakeholder Weight** |
| :------------------------ | :----------: | :-----------: | :----------------: | :--------------------: |
| Social Media Login        |      7       |       8       |         6          |          0.3           |
| Two-Factor Authentication |      9       |       6       |         5          |          0.4           |
| PDF Data Export           |      6       |       9       |         7          |          0.2           |
| CRM Integration           |      5       |       7       |         9          |          0.1           |
| Data Backup               |      8       |       6       |         8          |          0.5           |

Calculated values:

**Table 10. Positive and Negative Ideal Solutions**

| **Criterion**  | **PIS** | **NIS** |
| :------------: | :-----: | :-----: |
|    Security    |  0.400  |  0.050  |
|   Usability    |  0.300  |  0.070  |
| Business Value |  0.400  |  0.090  |

<span id="tab:topsis_ideal" label="tab:topsis_ideal"></span>

### Calculation of Distances to PIS and NIS

Distances to PIS and NIS are computed using the Euclidean metric [\[17\]](#reference-17), [\[21\]](#reference-21):

```math
D^+_i = \sqrt{\sum_{j=1}^{m} (v_{ij} - PIS_j)^2}
```

```math
D^-_i = \sqrt{\sum_{j=1}^{m} (v_{ij} - NIS_j)^2}
```

where $`D^+_i`$ is the distance from alternative $`i`$ to the PIS, $`D^-_i`$ is the distance from alternative $`i`$ to the NIS.

Calculated distances:

**Table 11. Distances to the ideal solutions**

| **Alternative**           | **Distance to PIS ($`D^+`$)** | **Distance to NIS ($`D^-`$)** |
| :------------------------ | :---------------------------: | :---------------------------: |
| Social Media Login        |             0.290             |             0.130             |
| Two-Factor Authentication |             0.140             |             0.310             |
| PDF Data Export           |             0.380             |             0.110             |
| CRM Integration           |             0.450             |             0.050             |
| Data Backup               |             0.100             |             0.350             |

<span id="tab:topsis_distances" label="tab:topsis_distances"></span>

### Calculation of the Final Alternative Priority

The final priority is computed using the formula [\[17\]](#reference-17), [\[21\]](#reference-21):

```math
C_i = \frac{D^-_i}{D^+_i + D^-_i}
```

The higher $`C_i`$, the closer the alternative is to the ideal solution.

Final alternative ranking:

**Table 12. Final alternative ranking by the TOPSIS method**

| **Alternative**           | **Final Priority ($`C_i`$)** |
| :------------------------ | :--------------------------: |
| Data Backup               |            0.778             |
| Two-Factor Authentication |            0.689             |
| Social Media Login        |            0.310             |
| PDF Data Export           |            0.224             |
| CRM Integration           |            0.100             |

### Conclusions

For qualitative interpretation of the obtained values, the following ranges may be used [\[21\]](#reference-21), [\[17\]](#reference-17):

- $`C_i > 0.65`$ — high priority (implement first);

- $`0.4 \leq C_i \leq 0.65`$ — medium priority (possible implementation if resources are available; requires analysis);

- $`C_i < 0.4`$ — low priority (can be deferred).

This approach links the quantitative results of the TOPSIS method to verbal characteristics, facilitating decision-making under conditions of limited resources and high uncertainty [\[17\]](#reference-17).

- **Data Backup** has the highest priority (0.778) and should be implemented first.

- **Two-Factor Authentication** also has a high priority (0.689).

- **Social Media Login** and **PDF Data Export** have medium priority.

- **CRM Integration** has the lowest priority and can be deferred.

<a id="section-7"></a>

## Analysis of TOPSIS with Interval Ratings

### Introduction

The **TOPSIS with interval ratings** method is a modification of the classical TOPSIS method that allows uncertainty (imprecision) in expert assessments to be taken into account [\[17\]](#reference-17), [\[18\]](#reference-18). Instead of a single precise value for each characteristic, each expert specifies a **range of values** reflecting their personal uncertainty [\[21\]](#reference-21).

This approach is an important **transitional step** between crisp analysis and fuzzy sets [\[18\]](#reference-18):

- Classical TOPSIS uses **fixed numbers**.

- This variant of TOPSIS uses **interval analysis**.

- Later we will move on to **Type-1 Fuzzy TOPSIS**, where intervals will be replaced by **membership functions** [\[17\]](#reference-17).

### Description of the Expert Rating Scale

A **verbal scale** was created to translate expert responses into numerical intervals [\[18\]](#reference-18):

**Table 13. Scale for converting expert ratings to intervals (with 0.4 overlap)**

| **Expert Rating** | **Interval (min – max)** |
| :---------------: | :----------------------: |
|     Very Low      |       \[1.0, 3.2\]       |
|        Low        |       \[2.8, 5.2\]       |
|      Medium       |       \[4.8, 7.2\]       |
|       High        |       \[6.8, 9.2\]       |
|     Very High     |      \[8.8, 10.0\]       |

<span id="tab:scale_conversion" label="tab:scale_conversion"></span>

Experts completed the questionnaire by providing **only verbal ratings**, which were then automatically converted to intervals.

In the classical expert rating scale, intervals are defined strictly; for example, “Medium” corresponds to \[5, 7\] and “High” to \[7, 9\]. However, in reality, category boundaries are not sharp, as expert assessments are subjective. Adding a small overlap allows us to:

- **Reflect the natural uncertainty** in the perception of rating boundaries.

- **Smooth transitions between categories**, reducing sharp jumps.

- **Make the method more flexible**, which is important when working with data obtained from a group of experts [\[19\]](#reference-19).

### Expert Rating Table

**Table 14. Questionnaire results with interval ratings**

| **Alternative**           | **Security (min – max)** | **Usability (min – max)** | **Business Value (min – max)** |
| :------------------------ | :----------------------: | :-----------------------: | :----------------------------: |
| Social Media Login        |       \[6.8, 9.2\]       |       \[4.8, 7.2\]        |          \[2.8, 5.2\]          |
| Two-Factor Authentication |      \[8.8, 10.0\]       |       \[6.8, 9.2\]        |          \[4.8, 7.2\]          |
| PDF Data Export           |       \[4.8, 7.2\]       |       \[8.8, 10.0\]       |          \[6.8, 9.2\]          |
| CRM Integration           |       \[2.8, 5.2\]       |       \[6.8, 9.2\]        |         \[8.8, 10.0\]          |
| Data Backup               |       \[6.8, 9.2\]       |       \[4.8, 7.2\]        |          \[6.8, 9.2\]          |

<span id="tab:interval_assessments" label="tab:interval_assessments"></span>

### Normalization and Calculations

Interval values were normalized as follows [\[21\]](#reference-21):

```math
r_{ij}^{min} = \frac{x_{ij}^{min}}{\sqrt{\sum_{i=1}^{n} (x_{ij}^{max})^2}}
```

```math
r_{ij}^{max} = \frac{x_{ij}^{max}}{\sqrt{\sum_{i=1}^{n} (x_{ij}^{max})^2}}
```

Here: $`x_{ij}^{min}`$, $`x_{ij}^{max}`$ are the lower and upper bounds of the interval rating of criterion $`j`$ for alternative $`i`$; $`r_{ij}^{min}`$, $`r_{ij}^{max}`$ are the corresponding normalized values; $`n`$ is the number of alternatives. Normalization brings all values to a common scale and makes them comparable even if they were originally expressed in different ranges [\[17\]](#reference-17).

The **Positive Ideal (PIS)** and **Negative Ideal (NIS)** solutions were then determined for each criterion:

```math
PIS_j^{max} = \max(r_{ij}^{max}), \quad PIS_j^{min} = \max(r_{ij}^{min})
```

```math
NIS_j^{max} = \min(r_{ij}^{max}), \quad NIS_j^{min} = \min(r_{ij}^{min})
```

For each criterion we find the highest values (PIS) and the lowest values (NIS), separately for the upper and lower bounds of the intervals. This gives two reference solutions — one positive and one negative. The distances from each alternative to the ideal solutions are then calculated:

```math
D^+_i = \sqrt{\sum_{j=1}^{m} (r_{ij}^{max} - PIS_j^{max})^2}
```

```math
D^-_i = \sqrt{\sum_{j=1}^{m} (r_{ij}^{min} - NIS_j^{min})^2}
```

These formulas adapt the classical TOPSIS metrics to interval data [\[21\]](#reference-21), [\[17\]](#reference-17). Here: $`D^+_i`$ is the distance from alternative $`i`$ to the positive ideal (PIS), computed on upper bounds; $`D^-_i`$ is the distance from alternative $`i`$ to the negative ideal (NIS), computed on lower bounds; $`m`$ is the number of criteria.

Finally, the priority interval bounds are calculated for each alternative [\[17\]](#reference-17):

```math
C_i^{min} = \frac{D^-_i{}^{min}}{D^+_i{}^{max} + D^-_i{}^{min}}, \quad
    C_i^{max} = \frac{D^-_i{}^{max}}{D^+_i{}^{min} + D^-_i{}^{max}}
```

Thus, each alternative receives not a single priority value but an interval. This reflects the degree of uncertainty in the expert ratings and makes the conclusions more flexible [\[18\]](#reference-18).

### Calculation Results

**Table 15. Final alternative priorities using the TOPSIS method**

| **Alternative**           | **Priority (min)** | **Priority (max)** |
| :------------------------ | :----------------: | :----------------: |
| Two-Factor Authentication |       0.6948       |       0.6948       |
| PDF Data Export           |       0.6699       |       0.6699       |
| Data Backup               |       0.6586       |       0.6586       |
| CRM Integration           |       0.5646       |       0.5646       |
| Social Media Login        |       0.4181       |       0.4181       |

<span id="tab:topsis_interval_results" label="tab:topsis_interval_results"></span>

**Conclusions:**

- **Two-Factor Authentication** has the highest priority (0.6948) and is the most preferred alternative.

- **PDF Data Export** and **Data Backup** also have high priorities.

- **CRM Integration** and **Social Media Login** received lower values, indicating lesser significance of these alternatives.

- The TOPSIS method made it possible to account for interval ratings and rank alternatives based on their proximity to the ideal solution [\[17\]](#reference-17).

TOPSIS with interval ratings serves as a bridge to Type-1 Fuzzy TOPSIS, where intervals will be replaced by membership functions [\[18\]](#reference-18).

<a id="section-8"></a>

## Transition to Fuzzy TOPSIS Type-1 with Trapezoidal Membership Functions

### Introduction

The **Fuzzy TOPSIS Type-1** method is an extension of the classical TOPSIS method that accounts for the uncertainty and subjectivity of expert assessments [\[17\]](#reference-17). The key distinction from crisp TOPSIS lies in the use of **fuzzy sets**, which allows the perception of criteria by different stakeholders to be modeled more accurately [\[16\]](#reference-16).

The term _fuzzy sets_ was introduced in 1965 by the American scientist Lotfi Zadeh [\[16\]](#reference-16). He proposed a mathematical framework for describing situations in which the boundaries of concepts are vague, and elements may belong to a set not strictly (as in classical logic) but with some degree of membership in the interval from 0 to 1. This idea proved especially useful when working with linguistic variables, approximate judgments, human subjectivity, and incomplete information.

The application of fuzzy logic in multi-criteria methods allows real expert opinions to be better reflected, especially in cases where precise numerical ratings are difficult or undesirable [\[18\]](#reference-18), [\[19\]](#reference-19). The Type-1 Fuzzy TOPSIS method implements this approach by using **trapezoidal membership functions** to represent criterion values [\[17\]](#reference-17).

Unlike interval ratings, fuzzy values do not merely define a spread boundary but describe the degree of confidence in each possible value of the criterion. This provides a richer representation of expert uncertainty and increases the flexibility of the prioritization analysis.

### Fuzzy Sets and Membership Functions

In the classical approach, expert assessments are expressed as crisp numbers, which imposes rigid constraints on the decision-making process. In reality, however, the perception of alternative characteristics is often **fuzzy** and varies depending on subjective factors [\[16\]](#reference-16).

A fuzzy set $`\tilde{A}`$ on a universe of discourse $`X`$ is defined by a **membership function** $`\mu_{\tilde{A}}(x)`$ that maps each element $`x`$ to the interval $`[0,1]`$:

```math
\mu_{\tilde{A}}(x) : X \to [0,1]
```

where $`\mu_{\tilde{A}}(x) = 1`$ means that element $`x`$ fully belongs to set $`\tilde{A}`$; $`\mu_{\tilde{A}}(x) = 0`$ means that element $`x`$ does not belong to set $`\tilde{A}`$; $`0 < \mu_{\tilde{A}}(x) < 1`$ means that the membership of the element is **fuzzy** and is determined by the degree of confidence in its membership.

### Trapezoidal Fuzzy Numbers and Their Application

In the context of the Fuzzy TOPSIS method, **Trapezoidal Fuzzy Numbers (TrFN)** are used as the membership function [\[17\]](#reference-17), [\[18\]](#reference-18). A trapezoidal fuzzy number is defined by four parameters:

```math
\tilde{A} = (a_l, a_{ml}, a_{mu}, a_u)
```

where $`a_l`$ is the **lower bound**, below which the value is not considered; $`a_{ml}`$ is the **left modal value**, the minimum value considered possible; $`a_{mu}`$ is the **right modal value**, the maximum value considered possible; $`a_u`$ is the **upper bound**, above which the value is not considered.

The membership function for a trapezoidal number is defined as follows:

```math
\mu_{\tilde{A}}(x) =
\begin{cases}
0, & x \leq a_l \text{ or } x \geq a_u \\
\dfrac{x - a_l}{a_{ml} - a_l}, & a_l \leq x \leq a_{ml} \\
1, & a_{ml} \leq x \leq a_{mu} \\
\dfrac{a_u - x}{a_u - a_{mu}}, & a_{mu} \leq x \leq a_u
\end{cases}
```

This form of membership function is used in most implementations of Type-1 fuzzy numbers [\[17\]](#reference-17), [\[34\]](#reference-34).

### Advantages of Using Trapezoidal Numbers

The use of **trapezoidal functions** allows:

1.  **Flexible modeling of subjective expert assessments** by defining zones of **high confidence** (the range from $`a_{ml}`$ to $`a_{mu}`$) and regions of **uncertainty** (the range from $`a_l`$ to $`a_{ml}`$, and from $`a_{mu}`$ to $`a_u`$) [\[18\]](#reference-18).

2.  **Accounting for the variability of expert opinions**, especially when different experts give slightly differing assessments [\[19\]](#reference-19).

3.  **Creating a transitional step between interval TOPSIS and more complex models**, such as Type-2 Fuzzy TOPSIS or intuitionistic fuzzy sets [\[34\]](#reference-34), [\[35\]](#reference-35).

### Scale for Converting Expert Ratings to Trapezoidal Numbers

The following scale was created to translate verbal expert assessments into trapezoidal fuzzy numbers [\[17\]](#reference-17), [\[18\]](#reference-18):

**Table 16. Scale for converting expert ratings to trapezoidal fuzzy numbers**

| **Expert Rating** | **Fuzzy Number** |
| :---------------: | :--------------: |
|     Very Low      |   (1, 1, 2, 3)   |
|        Low        |   (2, 3, 4, 5)   |
|      Medium       |   (4, 5, 6, 7)   |
|       High        |   (6, 7, 8, 9)   |
|     Very High     |  (8, 9, 10, 10)  |

<span id="tab:trfn_scale" label="tab:trfn_scale"></span>

Now each expert in the questionnaire **selects a verbal description**, which is then automatically converted to a trapezoidal number [\[16\]](#reference-16), [\[34\]](#reference-34).

The software provides the ability to flexibly configure the bounds of the trapezoidal numbers. The user can adjust the scale parameters by changing the numerical boundaries of the corresponding ratings. This allows the method to be adapted to specific analysis conditions, for example:

- Decrease or increase the spread of values for each category.

- Shift the boundaries of adjacent intervals to account for the specifics of expert assessments.

- Optimize the scale depending on the application domain (finance, industry, healthcare, etc.) [\[18\]](#reference-18), [\[19\]](#reference-19).

Thus, the system is not limited to fixed boundaries but allows parameters to be customized according to user requirements [\[34\]](#reference-34), [\[35\]](#reference-35).

All subsequent calculations are performed on a concrete example with the defined expert rating scale.

### Expert Rating Table

Based on the expert rating scale presented in Table 16, the following assessments were obtained [\[17\]](#reference-17), [\[34\]](#reference-34):

**Table 17. Expert assessments in trapezoidal fuzzy format**

| **Alternative**           | **Security** | **Usability** | **Business Value** |
| :------------------------ | :----------: | :-----------: | :----------------: |
| Social Media Login        |  (6,7,8,9)   |   (4,5,6,7)   |     (2,3,4,5)      |
| Two-Factor Authentication |  (8,9,9,10)  |   (6,7,8,9)   |     (4,5,6,7)      |
| PDF Data Export           |  (4,5,6,7)   |  (8,9,10,10)  |     (6,7,8,9)      |
| CRM Integration           |  (2,3,4,5)   |   (6,7,8,9)   |    (8,9,10,10)     |
| Data Backup               |  (6,7,8,9)   |   (4,5,6,7)   |     (6,7,8,9)      |

<span id="tab:fuzzy_topsis_input" label="tab:fuzzy_topsis_input"></span>

### Calculations Using the Fuzzy TOPSIS Type-1 Method

#### Normalization of Fuzzy Ratings

Linear normalization is used to normalize the fuzzy values [\[17\]](#reference-17), [\[18\]](#reference-18):

```math
r_{ij}^{l} = \frac{a_{ij}^{l}}{\max a_{j}^{u}}, \quad
    r_{ij}^{m} = \frac{a_{ij}^{m}}{\max a_{j}^{u}}, \quad
    r_{ij}^{u} = \frac{a_{ij}^{u}}{\max a_{j}^{u}}
```

where $`a_{ij}^{l}, a_{ij}^{m}, a_{ij}^{u}`$ are the components of the trapezoidal fuzzy number, and $`\max a_{j}^{u}`$ is the largest upper value among all alternatives.

### Determining the Positive and Negative Ideal Solutions

Two ideal solutions are determined [\[17\]](#reference-17):

```math
\tilde{A}^{+} = (a_1^+, a_2^+, \ldots, a_n^+), \quad
    \tilde{A}^{-} = (a_1^-, a_2^-, \ldots, a_n^-)
```

where $`a_j^+ = (\max r_{ij}^{l}, \max r_{ij}^{m}, \max r_{ij}^{u})`$ is the **positive ideal solution**; $`a_j^- = (\min r_{ij}^{l}, \min r_{ij}^{m}, \min r_{ij}^{u})`$ is the **negative ideal solution**.

#### Calculation of Distances to the Ideal Solutions

The distances from each alternative to the positive and negative ideal solutions are computed using the following formulas [\[17\]](#reference-17):

```math
D^+_i = \sqrt{\sum_{j=1}^{m} d(\tilde{r}_{ij}, \tilde{A}_j^+)^2}
```

```math
D^-_i = \sqrt{\sum_{j=1}^{m} d(\tilde{r}_{ij}, \tilde{A}_j^-)^2}
```

where $`d(\tilde{A}, \tilde{B})`$ is the distance between two fuzzy numbers, calculated, for example, using the generalized Euclidean metric for trapezoidal numbers [\[17\]](#reference-17), [\[18\]](#reference-18).

#### Determining Priorities

The final priority of each alternative is determined as follows [\[17\]](#reference-17):

```math
C_i = \frac{D^-_i}{D^+_i + D^-_i}
```

where $`C_i`$ is the final priority of the alternative; $`D^-_i`$ is the distance to the negative ideal solution; $`D^+_i`$ is the distance to the positive ideal solution. The higher $`C_i`$, the more preferred the alternative.

### Calculation Results

After applying the Type-1 Fuzzy TOPSIS method, the following results were obtained:

**Table 18. Results of the Type-1 Fuzzy TOPSIS method**

| **Alternative**           | **Distance to PIS ($`D^+`$)** | **Distance to NIS ($`D^-`$)** | **Priority ($`C_i`$)** |
| :------------------------ | :---------------------------: | :---------------------------: | :--------------------: |
| Two-Factor Authentication |             0.837             |             1.241             |         0.597          |
| PDF Data Export           |             0.794             |             1.170             |         0.596          |
| Data Backup               |             0.894             |             1.131             |         0.558          |
| CRM Integration           |             1.162             |             1.221             |         0.512          |
| Social Media Login        |             1.414             |             0.800             |         0.361          |

<span id="tab:fuzzy_topsis_results" label="tab:fuzzy_topsis_results"></span>

### Conclusions

Based on the analysis performed using the Type-1 Fuzzy TOPSIS method for our expert rating table, the following results were obtained:

- **Two-Factor Authentication** ($`C_i = 0.597`$) has the highest priority. This means that this feature most closely corresponds to the ideal solution taking into account expert assessments on the criteria of security, usability, and business value. Its implementation should be prioritized.

- **PDF Data Export** ($`C_i = 0.596`$) ranks second in importance. However, the priority value differs from the first by only a negligible amount (0.001), so both alternatives can be considered practically equivalent in importance. The feature has high value and is recommended for implementation alongside two-factor authentication.

- **Data Backup** ($`C_i = 0.558`$) also has a high priority but slightly trails the top two alternatives. This indicates that the feature is important but can be implemented after the most critical ones.

- **CRM Integration** ($`C_i = 0.512`$) received a medium priority, indicating that its significance is not critical compared to the other alternatives.

- **Social Media Login** ($`C_i = 0.361`$) received the lowest priority. This means that, from the experts’ perspective, this feature has the least value and can be deferred to a later stage.

Thus, the Type-1 Fuzzy TOPSIS method made it possible to incorporate subjective expert assessments in the form of fuzzy trapezoidal numbers and produce a ranking of alternatives [\[17\]](#reference-17), [\[34\]](#reference-34). As a result, the priority features for implementation are two-factor authentication, PDF data export, and data backup, while CRM integration and social media login have lower priority.

<a id="section-9"></a>

## Analysis of the Intuitionistic Fuzzy TOPSIS Method

### Introduction

The **Intuitionistic Fuzzy TOPSIS** method is a further development of Fuzzy TOPSIS that extends it by introducing an additional parameter — the **degree of uncertainty** ($`\pi`$) [\[19\]](#reference-19), [\[23\]](#reference-23). This allows not only the degree of membership and non-membership to be taken into account, but also the level of the expert’s uncertainty in their assessment.

The concept of **Intuitionistic Fuzzy Sets (IFS)** was proposed by the Bulgarian mathematician K. T. Atanassov in 1986 [\[20\]](#reference-20) as a generalization of the classical fuzzy sets of L. Zadeh [\[16\]](#reference-16). Unlike ordinary fuzzy sets, where each element $`x`$ is described only by a membership function $`\mu(x)`$, in intuitionistic theory each element is associated with:

- a degree of membership $`\mu(x) \in [0,1]`$,

- a degree of non-membership $`\nu(x) \in [0,1]`$,

- and a degree of uncertainty $`\pi(x) = 1 - \mu(x) - \nu(x)`$,

subject to the condition $`0 \leq \mu(x) + \nu(x) \leq 1`$. The value $`\pi(x)`$ characterizes the region in which the expert finds it difficult to give an unambiguous assessment [\[19\]](#reference-19).

By introducing this additional characteristic, the model becomes more sensitive to situations in which the expert finds it difficult to express their opinion or entertains doubts. This is especially important in requirements prioritization tasks, where it is not always possible to clearly determine the significance of a given criterion [\[28\]](#reference-28).

Thus, the Intuitionistic Fuzzy TOPSIS method allows alternatives to be ranked taking into account not only the degree of confidence but also the degree of doubt, making it a more flexible tool under conditions of high uncertainty and the human factor [\[19\]](#reference-19), [\[23\]](#reference-23).

### Foundations of Intuitionistic Fuzzy Sets

As already mentioned, an intuitionistic fuzzy set $`\tilde{A}`$ on a universe of discourse $`X`$ is defined by two functions:

```math
\mu_{\tilde{A}}(x): X \to [0,1], \quad
\nu_{\tilde{A}}(x): X \to [0,1]
```

where $`\mu_{\tilde{A}}(x)`$ is the degree of membership of element $`x`$ in set $`\tilde{A}`$, and $`\nu_{\tilde{A}}(x)`$ is the degree of non-membership of element $`x`$ in set $`\tilde{A}`$ [\[20\]](#reference-20).

Additionally, the **degree of uncertainty** (hesitancy) is introduced:

```math
\pi_{\tilde{A}}(x) = 1 - \mu_{\tilde{A}}(x) - \nu_{\tilde{A}}(x)
```

Thus, each value is characterized not only by the degree of membership and non-membership but also by the expert’s level of doubt [\[19\]](#reference-19), [\[23\]](#reference-23).

### Scale for Converting Expert Ratings

The following scale was developed to translate verbal expert assessments into intuitionistic fuzzy numbers [\[28\]](#reference-28), [\[23\]](#reference-23):

**Table 19. Scale for converting expert ratings to intuitionistic fuzzy numbers**

|            **Expert Rating**            | **Degree of Membership ($`\mu`$)** | **Degree of Non-membership ($`\nu`$)** | **Degree of Uncertainty ($`\pi`$)** |
| :-------------------------------------: | :--------------------------------: | :------------------------------------: | :---------------------------------: |
|    Very important, and I am certain     |                0.9                 |                  0.05                  |                0.05                 |
|    Very important, but I have doubts    |                0.9                 |                  0.1                   |                 0.0                 |
|       Important, and I am certain       |                0.7                 |                  0.2                   |                 0.1                 |
|      Important, but I have doubts       |                0.7                 |                  0.1                   |                 0.2                 |
| Moderately important, and I am certain  |                0.5                 |                  0.4                   |                 0.1                 |
| Moderately important, but I have doubts |                0.5                 |                  0.3                   |                 0.2                 |
|  Slightly important, and I am certain   |                0.3                 |                  0.6                   |                 0.1                 |
|  Slightly important, but I have doubts  |                0.3                 |                  0.5                   |                 0.2                 |
|     Not important, and I am certain     |                0.1                 |                  0.8                   |                 0.1                 |
|    Not important, but I have doubts     |                0.1                 |                  0.7                   |                 0.2                 |

<span id="tab:intuitionistic_scale" label="tab:intuitionistic_scale"></span>

### Expert Rating Matrix

**Table 20. Expert assessments in intuitionistic fuzzy form**

| **Alternative**           |   **Security**    |   **Usability**   | **Business Value** |
| :------------------------ | :---------------: | :---------------: | :----------------: |
| Social Media Login        |  (0.7, 0.2, 0.1)  |  (0.5, 0.3, 0.2)  |  (0.3, 0.6, 0.1)   |
| Two-Factor Authentication | (0.9, 0.05, 0.05) |  (0.7, 0.2, 0.1)  |  (0.5, 0.3, 0.2)   |
| PDF Data Export           |  (0.5, 0.3, 0.2)  | (0.9, 0.05, 0.05) |  (0.7, 0.1, 0.2)   |
| CRM Integration           |  (0.3, 0.6, 0.1)  |  (0.7, 0.2, 0.1)  | (0.9, 0.05, 0.05)  |
| Data Backup               |  (0.7, 0.2, 0.1)  |  (0.5, 0.3, 0.2)  |  (0.7, 0.2, 0.1)   |

<span id="tab:intuitionistic_fuzzy_input" label="tab:intuitionistic_fuzzy_input"></span>

### Calculations Using the Intuitionistic Fuzzy TOPSIS Method

#### Determining the Ideal Solutions

```math
\tilde{A}^{+} = (\mu^+_1, \nu^-_1, \pi^-_1), \quad
\tilde{A}^{-} = (\mu^-_1, \nu^+_1, \pi^+_1)
```

where $`\mu^+ = \max \mu_{ij}`$, $`\nu^- = \min \nu_{ij}`$, $`\pi^- = \min \pi_{ij}`$ form the positive ideal solution; $`\mu^- = \min \mu_{ij}`$, $`\nu^+ = \max \nu_{ij}`$, $`\pi^+ = \max \pi_{ij}`$ form the negative ideal solution [\[19\]](#reference-19), [\[23\]](#reference-23).

#### Determining Priorities

After computing the distances to the positive ideal ($`D^+`$) and negative ideal ($`D^-`$) solutions, the final priority of the alternative is determined as the closeness index [\[19\]](#reference-19), [\[28\]](#reference-28):

```math
C_i = \frac{D^-_i}{D^+_i + D^-_i}
```

where $`D^+_i`$ is the distance from alternative $`i`$ to the positive ideal solution (PIS), and $`D^-_i`$ is the distance from alternative $`i`$ to the negative ideal solution (NIS). The larger the value of $`C_i`$, the closer the alternative is to the positive ideal solution and the higher its priority.

##### Interpretation of the priority index:

- If $`C_i \to 1`$, the alternative is maximally close to the positive ideal.

- If $`C_i \to 0`$, the alternative is close to the negative ideal.

- Alternatives are ordered by descending $`C_i`$, allowing their priority to be determined.

### Calculation Results

**Table 21. Results of the Intuitionistic Fuzzy TOPSIS method**

| **Alternative**           | **Distance to PIS** | **Distance to NIS** | **Priority ($`C_i`$)** |
| :------------------------ | :-----------------: | :-----------------: | :--------------------: |
| Two-Factor Authentication |        0.294        |        0.437        |         0.598          |
| Data Backup               |        0.278        |        0.400        |         0.590          |
| CRM Integration           |        0.389        |        0.460        |         0.542          |
| PDF Data Export           |        0.328        |        0.374        |         0.533          |
| Social Media Login        |        0.532        |        0.200        |         0.273          |

### Conclusions

Based on the Intuitionistic Fuzzy TOPSIS method and the calculations performed, the following conclusions can be drawn [\[28\]](#reference-28), [\[19\]](#reference-19):

- **Two-Factor Authentication** received the highest priority index ($`C = 0.598`$), meaning that this feature is the most important from the perspective of all criteria. It has a high degree of membership and minimal degree of non-membership, as well as a relatively low level of uncertainty in the expert assessments. Therefore, its implementation should be prioritized.

- **Data Backup** also occupies a high position in terms of the priority index ($`C = 0.590`$). This means that experts regard it as an important feature that plays a key role in the system. The high degree of membership points to its significance from the perspective of security and business value, so its deployment is recommended at an early stage.

- **CRM Integration** ($`C = 0.542`$) and **PDF Data Export** ($`C = 0.533`$) received medium priority index values. This indicates that these functionalities are useful but not critical. CRM Integration received a high level of uncertainty among experts, indicating disagreement about its necessity. PDF Data Export, by contrast, proved to be a more consistent feature, but its value is lower compared to the leading alternatives. Both requirements can be implemented in a second phase.

- **Social Media Login** received the lowest priority index ($`C = 0.273`$). This means that this functionality is considered the least important relative to the other criteria. The high degree of non-membership and significant level of uncertainty show that this feature is either not a priority or its value is ambiguous for the experts. Implementation of this feature can be considered as an additional stage planned for later releases.

The IF-TOPSIS method made it possible to account for the degree of uncertainty in expert assessments, providing a more flexible analysis of requirements prioritization [\[19\]](#reference-19), [\[23\]](#reference-23), [\[28\]](#reference-28).

<a id="section-10"></a>

## Analysis of the Fuzzy Delphi Type-2 Method for Requirements Prioritization

### Introduction

The **Fuzzy Delphi Type-2** method is an enhanced version of the classical Delphi method that accounts for second-order uncertainty using **Interval Type-2 Fuzzy Sets (IT2FS)**. Unlike the classical Delphi, this method does not require multiple rounds of surveys, as uncertainty is already accounted for at the first stage [\[22\]](#reference-22), [\[26\]](#reference-26).

#### Key Features of the Method

- Experts express their assessments **verbally**, which are then converted into **fuzzy interval values** [\[24\]](#reference-24).

- The method accounts for the **varying confidence levels** of experts in their judgments [\[25\]](#reference-25).

- The **Footprint of Uncertainty (FOU)** is computed to evaluate the consistency of responses [\[26\]](#reference-26).

- Expert weights are affected: **if their uncertainty is too high, their contribution is reduced**.

- **Applicable to complex multi-criteria decisions** where a high level of uncertainty exists.

### Input Data Format (CSV File)

The input data represent **expert survey results**, where each expert responds **verbally**. These responses are then converted into interval fuzzy sets **IT2FS** [\[22\]](#reference-22).

#### CSV File Structure

Experts evaluate **alternatives by criteria**, giving **verbal responses**.

**Table 22. Expert ratings by criterion**

|      **Alternative**      | **Expert** |           **Security**           |       **Usability**        |     **Business Value**      | **Expert Weight** |
| :-----------------------: | :--------: | :------------------------------: | :------------------------: | :-------------------------: | :---------------: |
|    Social Media Login     |  Expert 1  |      High confidence – High      | Medium confidence – Medium |    Low confidence – Low     |        0.6        |
|    Social Media Login     |  Expert 2  |    Medium confidence – Medium    |   High confidence – High   | High confidence – Very High |        0.4        |
| Two-Factor Authentication |  Expert 1  | Very high confidence – Very High |   High confidence – High   | Medium confidence – Medium  |        0.6        |
| Two-Factor Authentication |  Expert 2  |      High confidence – High      | Medium confidence – Medium |    Low confidence – Low     |        0.4        |

### Converting Verbal Ratings to IT2FS

Since experts provide **verbal assessments**, they are converted into **interval fuzzy sets** [\[26\]](#reference-26), [\[25\]](#reference-25).

**Table 23. Conversion table of expert ratings to IT2FS**

| **Verbal Rating** | **Central Value** | **Left Bound** | **Right Bound** |
| :---------------: | :---------------: | :------------: | :-------------: |
|     Very Low      |        0.1        |      0.0       |       0.2       |
|        Low        |        0.3        |      0.2       |       0.4       |
|      Medium       |        0.5        |      0.3       |       0.7       |
|       High        |        0.7        |      0.5       |       0.9       |
|     Very High     |        0.9        |      0.8       |       1.0       |

### Computing the Footprint of Uncertainty (FOU)

#### FOU Formula

The Footprint of Uncertainty (**FOU**) reflects the degree of fuzziness of a fuzzy value and is computed as the difference between the upper and lower bounds of the membership function [\[25\]](#reference-25), [\[26\]](#reference-26):

```math
FOU(A_j) = \mu_{\tilde{A}_j}^U - \mu_{\tilde{A}_j}^L
\label{eq:fou}
```

where $`\mu_{\tilde{A}_j}^U`$ is the upper bound of the membership function for criterion $`j`$, and $`\mu_{\tilde{A}_j}^L`$ is the lower bound of the membership function for the same criterion. The FOU value shows how wide the range of possible assessments is — that is, how uncertain the expert (or group of experts) is about the value of this criterion. The larger the FOU, the greater the uncertainty associated with the perception of this feature.

#### Example FOU Calculation

**Table 24. Footprint of Uncertainty (FOU) for alternatives**

|      **Alternative**      | **Security (FOU)** | **Usability (FOU)** | **Business Value (FOU)** |
| :-----------------------: | :----------------: | :-----------------: | :----------------------: |
|    Social Media Login     |        0.1         |         0.2         |           0.3            |
| Two-Factor Authentication |        0.05        |         0.1         |           0.2            |

### Correction of Expert Weights at High FOU

If an expert **diverges significantly** from others, their contribution **is reduced**, consistent with the recommendations on adaptive weighting in fuzzy systems [\[26\]](#reference-26), [\[25\]](#reference-25):

```math
W_i^{\text{new}} = W_i \times \frac{1}{1 + (\Delta_j - \Delta_{\max})}
\label{eq:weight_correction}
```

where $`\Delta_j`$ is the observed uncertainty (FOU) of the expert for criterion $`j`$, and $`\Delta_{\max}`$ is the permissible maximum value. This approach reduces the contribution of experts whose assessments are too diffuse, thereby increasing the consistency of the result.

#### Boundary Cases of Weight Correction

- If $`\Delta_j = 0`$, then $`W_i^{\text{new}} = W_i`$. An expert with perfectly precise assessments retains their weight.

- If $`\Delta_j \gg \Delta_{\max}`$, then $`W_i^{\text{new}} \approx 0`$. An expert with extremely uncertain assessments is excluded from the analysis.

- If the expert is not confident in their answer, their weight is reduced proportionally to the level of uncertainty.

### Consistency Check and Result Interpretation

Consistency among experts can be monitored by analyzing FOU values and dynamic weight changes [\[22\]](#reference-22), [\[26\]](#reference-26).

#### Ways to Improve Consistency

- Excluding experts with high uncertainty.

- Re-normalizing ratings without re-surveying.

- Using a dynamic consistency threshold depending on the number of experts.

### Final Results Table

**Table 25. Final results table**

|      **Alternative**      | **Security (corrected)** |   **Usability**   | **Business Value** | **Confidence Index** |
| :-----------------------: | :----------------------: | :---------------: | :----------------: | :------------------: |
|    Social Media Login     |    (0.68, 0.22, 0.1)     | (0.52, 0.28, 0.2) | (0.35, 0.55, 0.1)  |         0.75         |
| Two-Factor Authentication |    (0.88, 0.06, 0.05)    | (0.72, 0.18, 0.1) | (0.52, 0.28, 0.2)  |         0.90         |

### Conclusions

- The Fuzzy Delphi Type-2 method allows the uncertainty of expert assessments to be taken into account [\[25\]](#reference-25), [\[22\]](#reference-22).

- It automatically reduces the influence of experts with high uncertainty, which is especially important in the absence of repeated survey rounds [\[26\]](#reference-26).

- It generates interval results that are robust to disagreements among experts.

- It can be automated for the analysis of alternatives in multi-criteria decision-making tasks.

<a id="section-11"></a>

## Analysis of the Delphi Intuitionistic Method for Requirements Prioritization

### Introduction

The **Delphi Intuitionistic** method is a development of the traditional Delphi method, adapted for conditions of uncertainty and fuzziness in expert assessments. Unlike **Fuzzy Delphi Type-2**, which uses interval fuzzy sets, **Delphi Intuitionistic** is based on **Intuitionistic Fuzzy Sets (IFS)**, proposed by Atanassov in 1986 [\[20\]](#reference-20).

Intuitionistic Fuzzy Sets (IFS) include three key parameters:

- **Degree of membership** ($`\mu`$) — shows how much an object belongs to the class under consideration.

- **Degree of non-membership** ($`\nu`$) — shows how much an object does not belong to the class under consideration.

- **Degree of uncertainty** ($`\pi = 1 - (\mu + \nu)`$) — reflects the expert’s level of hesitancy [\[19\]](#reference-19).

Thus, unlike traditional fuzzy systems, the Delphi Intuitionistic method accounts not only for the degree of membership but also for the degree of rejection, making it more precise when analyzing expert opinions.

### Key Features of the Method

The **Delphi Intuitionistic** method has several important advantages over other expert analysis methods:

- Accounts for **not only the degree of confidence but also the degree of rejection** [\[23\]](#reference-23);

- Considers **neutral assessments** when the expert **cannot make a choice**;

- Provides **more accurate identification of disagreements among experts**;

- Applicable in tasks **where experts express partial agreement and have a high level of uncertainty** [\[28\]](#reference-28).

### Input Data Format (CSV File)

The Delphi Intuitionistic method requires expert assessments to contain three values: **degree of membership**, **degree of non-membership**, and **degree of uncertainty**. The input data are presented as a table where, for each alternative and each criterion, experts specify these three parameters.

**Table 26. Example input data structure for the Delphi Intuitionistic method**

|      **Alternative**      | **Expert** | **Security** ($`\mu, \nu, \pi`$) | **Usability** ($`\mu, \nu, \pi`$) | **Business Value** ($`\mu, \nu, \pi`$) | **Expert Weight** |
| :-----------------------: | :--------: | :------------------------------: | :-------------------------------: | :------------------------------------: | :---------------: |
|    Social Media Login     |  Expert 1  |         (0.7, 0.2, 0.1)          |          (0.6, 0.3, 0.1)          |            (0.5, 0.4, 0.1)             |        0.6        |
|    Social Media Login     |  Expert 2  |         (0.5, 0.4, 0.1)          |          (0.7, 0.2, 0.1)          |            (0.8, 0.1, 0.1)             |        0.4        |
| Two-Factor Authentication |  Expert 1  |        (0.9, 0.05, 0.05)         |          (0.7, 0.2, 0.1)          |            (0.6, 0.3, 0.1)             |        0.6        |
| Two-Factor Authentication |  Expert 2  |         (0.8, 0.1, 0.1)          |          (0.6, 0.3, 0.1)          |            (0.4, 0.5, 0.1)             |        0.4        |

### Converting Expert Ratings to Intuitionistic Fuzzy Sets

To process expert assessments, a system for converting verbal values to the numerical parameters $`\mu`$, $`\nu`$, and $`\pi`$ must be used [\[18\]](#reference-18).

**Table 27. Verbal rating to IFS correspondence table**

| **Verbal Rating** | $`\mu`$ (membership) | $`\nu`$ (non-membership) | $`\pi`$ (uncertainty) |
| :---------------: | :------------------: | :----------------------: | :-------------------: |
|     Very Low      |         0.1          |           0.8            |          0.1          |
|        Low        |         0.3          |           0.6            |          0.1          |
|      Medium       |         0.5          |           0.4            |          0.1          |
|       High        |         0.7          |           0.2            |          0.1          |
|     Very High     |         0.9          |           0.05           |         0.05          |

### Computing the Footprint of Uncertainty (FOU)

#### Uncertainty Formula

In the Delphi Intuitionistic method, the Footprint of Uncertainty (**FOU**) is calculated based on intuitionistic fuzzy sets proposed in [\[20\]](#reference-20). Recall that each expert assessment is represented by three values:

- **Degree of membership** $`\mu`$

- **Degree of non-membership** $`\nu`$

- **Degree of uncertainty** $`\pi = 1 - (\mu + \nu)`$

The footprint of uncertainty for an alternative is computed as:

```math
FOU(A_i) = \max(\pi_i) - \min(\pi_i), \quad i \in \{\text{experts}\}
```

where $`\pi_i`$ is the degree of uncertainty assigned to alternative $`A_i`$ by different experts. If the FOU value is too high, this indicates significant disagreement among experts.

#### FOU Calculation Example

Suppose we have two alternatives with ratings from two experts:

**Table 28. Example of alternative ratings by experts**

|      **Alternative**      | **Expert** | $`\mu`$ | $`\nu`$ | $`\pi`$ |
| :-----------------------: | :--------: | :-----: | :-----: | :-----: |
|    Social Media Login     |  Expert 1  |   0.7   |   0.2   |   0.1   |
|    Social Media Login     |  Expert 2  |   0.5   |   0.4   |   0.1   |
| Two-Factor Authentication |  Expert 1  |   0.9   |  0.05   |  0.05   |
| Two-Factor Authentication |  Expert 2  |   0.8   |   0.1   |   0.1   |

Computing FOU:

```math
FOU_{\text{Social Media Login}} = \max(0.1, 0.1) - \min(0.1, 0.1) = 0
```

```math
FOU_{\text{Two-Factor Authentication}} = \max(0.05, 0.1) - \min(0.05, 0.1) = 0.05
```

Thus, **Social Media Login** has **zero uncertainty**, while **Two-Factor Authentication** has a small uncertainty, confirming the consensus of expert opinions on the first alternative.

### Expert Weight Correction

The Delphi Intuitionistic method also implements a **dynamic expert weight correction** mechanism, analogous to that proposed in [\[23\]](#reference-23), taking the level of uncertainty into account.

#### Weight Correction Formula

The weight of expert $`W_i`$ is recalculated as follows:

```math
W_i^{\text{new}} = W_i \times \frac{1}{1 + (\pi_i - \pi_{\text{avg}})}
```

where $`W_i`$ is the initial weight of the expert, $`\pi_i`$ is the average uncertainty across all assessments of this expert, and $`\pi_{\text{avg}}`$ is the average uncertainty across all experts.

#### Weight Correction Examples

**Table 29. Expert weight correction**

| **Expert** | **Initial Weight** | **Average Uncertainty** ($`\pi_i`$) |               **Corrected Weight**                |
| :--------: | :----------------: | :---------------------------------: | :-----------------------------------------------: |
|  Expert 1  |        0.6         |                 0.1                 | $`0.6 \times \dfrac{1}{1 + (0.1 - 0.15)} = 0.63`$ |
|  Expert 2  |        0.4         |                 0.3                 | $`0.4 \times \dfrac{1}{1 + (0.3 - 0.15)} = 0.35`$ |

### Final Results Table

After normalizing the assessments and correcting the weights, a final table is formed reflecting the adjusted values:

**Table 30. Final alternative assessments**

|      **Alternative**      | **Security (corrected)** |   **Usability**   | **Business Value** | **Confidence Index** |
| :-----------------------: | :----------------------: | :---------------: | :----------------: | :------------------: |
|    Social Media Login     |    (0.68, 0.22, 0.1)     | (0.52, 0.28, 0.2) | (0.35, 0.55, 0.1)  |         0.75         |
| Two-Factor Authentication |    (0.88, 0.06, 0.05)    | (0.72, 0.18, 0.1) | (0.52, 0.28, 0.2)  |         0.90         |

**Interpretation:**

- **Two-Factor Authentication** demonstrates high consistency of assessments and receives the highest confidence index.

- **Social Media Login** is characterized by a greater degree of uncertainty and a less reliable expert assessment.

### Conclusions

- The Delphi Intuitionistic method extends the capabilities of **Fuzzy Delphi Type-2** [\[22\]](#reference-22), allowing membership, rejection, and uncertainty all to be taken into account.

- The use of Intuitionistic Fuzzy Sets (IFS) provides a deeper analysis of expert opinions [\[19\]](#reference-19).

- Automatic weight correction increases objectivity and reduces the influence of highly uncertain assessments [\[23\]](#reference-23).

- The method can be effectively applied in decision support systems and automated within software solutions [\[28\]](#reference-28).

<a id="section-12"></a>

## Analysis of the Fuzzy AHP Type-1 (Analytic Hierarchy Process) Method for Requirements Prioritization

### Introduction

The **Fuzzy AHP Type-1** method is a **fuzzy extension of the classical Analytic Hierarchy Process (AHP)**, proposed by T. Saaty [\[29\]](#reference-29). The key distinction is that instead of crisp numbers for comparing criteria and alternatives, **fuzzy numbers** are used, making it possible to model **subjective expert preferences** and account for **uncertainty in judgments** [\[30\]](#reference-30), [\[31\]](#reference-31).

#### What Makes Fuzzy AHP Type-1 Better than Classical AHP?

- Allows experts to express **uncertainty in assessments** through fuzzy numbers.

- Enables **weighting of opinions from different experts** with varying degrees of importance [\[32\]](#reference-32).

- Enables **automatic consistency checking** of assessments, reducing errors [\[33\]](#reference-33).

- Uses **pairwise comparison**, ensuring objectivity.

### Input Data Format (CSV File)

The method supports any number of criteria and alternatives, but for demonstration purposes three criteria and five alternatives will be used.

The CSV file contains three main data blocks:

1.  Criteria importance assessments (pairwise comparison)

2.  Alternative assessments for each criterion

3.  Expert weight coefficients

#### File Structure

**Table 31. Example CSV file for criteria comparison**

|   Criterion    | Security | Usability | Business Value |
| :------------: | :------: | :-------: | :------------: |
|    Security    |    1     |     3     |       7        |
|   Usability    |   1/3    |     1     |       5        |
| Business Value |   1/7    |    1/5    |       1        |

Values are converted to fuzzy numbers using the Saaty scale [\[29\]](#reference-29).

#### Expert Questionnaire and Rating Conversion Scale

Experts are presented with varied questions, for example:

- How much more important is “Security” compared to “Usability” when choosing an authentication system?

- How much is “Two-Factor Authentication” preferable to “Social Media Login”?

- What is the significance of “CRM Integration” relative to “PDF Data Export”?

Answers are given in verbal form and converted to fuzzy numbers.

#### Updated Rating Conversion Scale (Fuzzy Saaty Scale)

**Table 32. Expert rating conversion scale**

|        Rating         | Crisp value (AHP) | Triangular fuzzy number (TFN) |
| :-------------------: | :---------------: | :---------------------------: |
|   Equally important   |         1         |        (1.0, 1.0, 1.0)        |
|   Weakly preferable   |         2         |        (1.5, 2.0, 2.5)        |
| Moderately preferable |         3         |        (2.5, 3.0, 3.5)        |
|  Strongly preferable  |         5         |        (4.5, 5.0, 5.5)        |
| Absolutely preferable |         9         |        (8.5, 9.0, 9.5)        |

### Consistency Check

The Consistency Index (CI) is computed as:

```math
CI = \frac{\lambda_{\max} - n}{n - 1}
```

where $`\lambda_{\max}`$ is the maximum eigenvalue of the matrix and $`n`$ is the number of criteria.

Then the **Consistency Ratio (CR)** is computed:

```math
CR = \frac{CI}{RI}
```

Where $`RI`$ is the **Random Consistency Index**, calculated as the average value over random matrices [\[10\]](#reference-10):

**Table 33. Random Consistency Index (RI)**

| Number of criteria ($`n`$) | Random Index $`RI`$ |
| :------------------------: | :-----------------: |
|             1              |          0          |
|             2              |          0          |
|             3              |        0.58         |
|             4              |        0.90         |
|             5              |        1.12         |
|             6              |        1.24         |

**If $`CR < 0.1`$, the matrix is considered consistent.**

If $`CR > 0.1`$, possible remedies include:

- Revising **contradictory comparisons**

- Adding **more experts**

- Refining **fuzzy boundaries**

### Calculation of Alternative Priorities

The final priorities of the alternatives are calculated using the following formula:

```math
P_i = \sum_{j=1}^m W_j \times W_{ij}
```

where $`P_i`$ is the priority of alternative $`i`$, $`W_j`$ is the weight of criterion $`j`$, and $`W_{ij}`$ is the local priority of alternative $`i`$ with respect to criterion $`j`$ [\[32\]](#reference-32), [\[37\]](#reference-37). Thus, each alternative receives an aggregated score reflecting its overall significance accounting for the relative importance of all criteria.

#### Example of Final Priorities

**Table 34. Final alternative priorities**

| Alternative | Final priority |
| :---------: | :------------: |
|     A4      |     0.312      |
|     A1      |     0.274      |
|     A3      |     0.215      |
|     A2      |     0.128      |
|     A5      |     0.071      |

### Conclusions

The **Fuzzy AHP Type-1** method has the following advantages:

- Accounts for **subjectivity** and **uncertainty** in expert assessments.

- Produces **more accurate results** than classical AHP [\[30\]](#reference-30).

- Verifies **logical consistency of expert assessments**, detecting inconsistencies.

- Allows **errors in judgments** to be corrected and the model to be refined.

<a id="section-13"></a>

## Analysis of the Fuzzy AHP Type-2 Method for Requirements Prioritization

### Introduction

**Fuzzy AHP Type-2** is an **enhanced fuzzy extension of the AHP method**, developed to model both **uncertainty** and **subjective divergences** in expert assessments. Unlike Fuzzy AHP Type-1, which operates with Type-1 triangular or trapezoidal fuzzy numbers, the Type-2 method makes it possible to account for **interval fluctuations in opinions** and **non-probabilistic uncertainty**, particularly characteristic of collective expert evaluation [\[25\]](#reference-25), [\[26\]](#reference-26).

#### Why Is Type-2 More Effective than Type-1?

- **Type-1** models only the imprecision of values (e.g., “around 5”), whereas **Type-2** models both imprecision and **membership uncertainty** — that is, how much “5” actually belongs to a given preference.

- Type-2 is applicable when **an expert is not confident** in their rating or provides a range of possible values.

- Type-2 is especially useful in **group evaluation**, when opinions of different experts differ — the method aggregates them via interval sets, reflecting the degree of disagreement [\[35\]](#reference-35).

### Representation of Interval Type-2 Fuzzy Numbers (IT2FN)

IT2FN models uncertainty at two levels:

- **First level (X)** — set of values (e.g., preference $`5 \pm 1`$);

- **Second level (Y)** — degree of confidence that a value belongs to the first level.

Under interval approximation (Interval Type-2 Fuzzy Set), the Y domain is simplified and becomes uniform across the full height of the function [\[26\]](#reference-26).

The canonical representation of an Interval Type-2 Fuzzy Number (IT2FN) is written as:

```math
\tilde{A} = \left[ (l_1, m_1, m_2, u_1); \ (l_2, m_1, m_2, u_2) \right]
```

where $`(l_1, m_1, m_2, u_1)`$ and $`(l_2, m_1, m_2, u_2)`$ are the boundaries of the lower and upper trapezoidal membership functions, respectively. The values $`l_1`$ and $`u_1`$ define the boundaries of the lower level (Lower Membership Function), while $`l_2`$ and $`u_2`$ define the boundaries of the upper level (Upper Membership Function). The values $`m_1`$ and $`m_2`$ are shared by both levels and define the central preference region. This representation makes it possible to model both the “spread” of the assessments themselves and the degree of expert uncertainty in each of them.

**Type-2 is important because:**

- It allows membership itself to be **fuzzy**.

- Unlike Type-1, which says “with confidence 0.7 — this is 5”, Type-2 says “this confidence fluctuates between 0.6 and 0.8”.

### Scale for Converting Ratings into IT2FN

**Table 35. Saaty scale for Type-2 Fuzzy AHP**

|      **Rating**       |        **IT2FN (lower; upper)**         |
| :-------------------: | :-------------------------------------: |
|   Equally important   |     $`(1, 1, 1, 1); (1, 1, 1, 1)`$      |
|   Weakly preferable   | $`(1.5, 2, 2, 2.5); (1.3, 2, 2, 2.7)`$  |
| Moderately preferable | $`(2.5, 3, 3, 3.5); (2.2, 3, 3, 3.8)`$  |
|  Strongly preferable  | $`(4.5, 5, 5, 5.5); (4.0, 5, 5, 6.0)`$  |
| Absolutely preferable | $`(8.5, 9, 9, 9.5); (8.0, 9, 9, 10.0)`$ |

### Input Data and CSV Format

The input file consists of rows containing:

- Expert name

- Expert weight

- Pairwise criterion comparison ratings

**Example CSV structure:**

    Expert,Weight,Security > Usability,Security > Business,Usability > Business
    Expert 1,0.5,Strongly,Absolutely,Moderately
    Expert 2,0.3,Moderately,Strongly,Weakly
    Expert 3,0.2,Strongly,Strongly,Equally

**Note:** when aggregating expert ratings in the context of Type-2 fuzzy logic, the following formula is used:

```math
\bar{A}_{ij} = \sum_{k=1}^{N} w_k \cdot \tilde{A}_{ij}^{(k)}
```

where $`\bar{A}_{ij}`$ is the aggregated fuzzy rating of alternative $`i`$ with respect to criterion $`j`$, obtained by combining the opinions of all experts; $`\tilde{A}_{ij}^{(k)}`$ is the fuzzy rating provided by expert $`k`$; $`w_k`$ is the weight (degree of trust) assigned to that expert’s opinion; $`N`$ is the total number of experts. Aggregation is performed component-wise over the fuzzy numbers (e.g., over the trapezoidal boundaries), preserving the IT2FN structure [\[25\]](#reference-25), [\[35\]](#reference-35), [\[26\]](#reference-26). Thus, each expert’s opinion contributes proportionally to their weight, allowing different levels of expertise or involvement to be taken into account.

Aggregation is performed separately for the lower and upper bounds.

### Processing Type-2 Numbers: Aggregation and Type Reduction

Aggregation is performed component-wise (e.g., $`l_1, l_2, u_1, u_2`$) with expert weights taken into account.

This is followed by Type Reduction [\[35\]](#reference-35):

- The Karnik–Mendel method or centroid computation is applied;

- A **single reduced trapezoidal number** is obtained;

- This number is then defuzzified (e.g., via the centroid method).

**Defuzzification**:

```math
\text{Defuzz}( \tilde{A} ) = \frac{l + 2m + u}{4}
```

### Example: Aggregated Comparison Matrix

**Table 36. Final aggregated comparison matrix with defuzzification**

|          Criteria           |  Lower IT2FN bound   |   Upper IT2FN bound   | Defuzzified value |
| :-------------------------: | :------------------: | :-------------------: | :---------------: |
|    Security \> Usability    | (4.2, 5.0, 5.0, 5.5) | (4.0, 5.0, 5.0, 6.0)  |        5.0        |
| Security \> Business Value  | (8.5, 9.0, 9.0, 9.5) | (8.0, 9.0, 9.0, 10.0) |        9.0        |
| Usability \> Business Value | (2.5, 3.0, 3.0, 3.5) | (2.2, 3.0, 3.0, 3.8)  |        3.0        |

### Calculation of Criteria Weights and Alternative Priorities Accounting for Expert Weights

After each pairwise comparison has been converted into Interval Type-2 Fuzzy Numbers (IT2FN), the procedure of aggregating expert opinions with their individual weights $`w_k`$ is performed, subject to the normalization condition: $`\sum_{k=1}^{n} w_k = 1`$.

#### Aggregation of Criterion Ratings by Expert Weights

Let $`\tilde{A}_{ij}^{(k)}`$ denote the IT2FN rating from expert $`k`$ for the pair of criteria $`i`$ and $`j`$. Then the aggregated rating is computed as:

```math
\tilde{A}_{ij}^{\text{agg}} = \sum_{k=1}^{n} w_k \cdot \tilde{A}_{ij}^{(k)}
```

where $`\tilde{A}_{ij}^{\text{agg}}`$ is the final combined IT2FN rating obtained by weighted summation of the individual expert opinions.

When using the trapezoidal representation, aggregation is performed separately over each component of the lower and upper membership functions:

```math
\tilde{A}_{ij}^{\text{agg}} = \left[
\begin{aligned}
&\left( \sum w_k \cdot l_1^{(k)}, \sum w_k \cdot m_1^{(k)}, \sum w_k \cdot m_2^{(k)}, \sum w_k \cdot u_1^{(k)} \right); \\
&\left( \sum w_k \cdot l_2^{(k)}, m_1, m_2, \sum w_k \cdot u_2^{(k)} \right)
\end{aligned}
\right]
```

Here aggregation is performed separately for the left and right boundaries of the lower ($`l_1^{(k)}, u_1^{(k)}`$) and upper ($`l_2^{(k)}, u_2^{(k)}`$) trapezoidal levels. The modal values $`m_1, m_2`$ are typically kept fixed or computed as expert-weighted averages.

#### Type Reduction and Defuzzification

After obtaining the aggregated IT2FN rating, it is necessary to obtain a crisp numerical value. This is achieved via **type-reduction**, for example using the _Centroid Min-Max_ approach:

```math
\text{C}_{ij} = \left( \frac{l_1 + 2m_1 + u_1}{4}, \frac{l_2 + 2m_2 + u_2}{4} \right)
```

where $`C_{ij}^{(1)}`$ and $`C_{ij}^{(2)}`$ are the centroids of the lower and upper levels of the corresponding trapezoidal function. The formula reflects a balanced weighting of the central part, assigning greater importance to modal values.

To obtain a single final crisp value, the two centroids are averaged:

```math
\text{Defuzz}(\tilde{A}_{ij}) = \frac{C_{ij}^{(1)} + C_{ij}^{(2)}}{2}
```

where $`\text{Defuzz}(\tilde{A}_{ij})`$ is the defuzzified rating of the criteria pair $`i`$ and $`j`$, obtained as the simple mean of the lower and upper centroids. This procedure makes it possible to rank alternatives or criteria on a crisp scale while preserving the effect of uncertainty modeling [\[35\]](#reference-35), [\[26\]](#reference-26).

Based on the defuzzified matrix, normalization is performed and the **eigenvector** corresponding to the criteria weights is extracted.

**Table 37. Criteria weights after aggregation with expert weights**

|   Criterion    | Weight |
| :------------: | :----: |
|    Security    | 0.512  |
|   Usability    | 0.308  |
| Business Value | 0.180  |

#### Calculation of Alternative Priorities

For each alternative and criterion, interval fuzzy ratings from each expert are specified. These are also aggregated with expert weights using an analogous formula.

After type-reduction and defuzzification of alternative ratings $`W_{ij}`$ for each criterion $`j`$, the final priority of alternative $`A_i`$ is calculated:

```math
P_i = \sum_{j=1}^{m} W_j \cdot W_{ij}
```

### Final Alternative Priorities (Expert Weights and Uncertainty Accounted For)

Example calculation after aggregation and defuzzification:

**Table 38. Alternative ranking with expert weights in Fuzzy AHP Type-2**

|          Alternative           | Final priority |
| :----------------------------: | :------------: |
| A2 (Two-Factor Authentication) |     0.334      |
|    A1 (Social Media Login)     |     0.289      |
|        A3 (PDF Export)         |     0.221      |
|      A4 (CRM Integration)      |     0.106      |
|        A5 (Data Backup)        |     0.050      |

### Conclusions

The **Fuzzy AHP Type-2** method with expert weights represents one of the most **flexible and realistic decision-making models** currently available for conditions of uncertainty and collective expert evaluation.

- **Dual uncertainty** is accounted for: imprecision of values and variability of confidence in them.

- The method **reflects the diversity of judgments**, providing a robust model when opinions diverge.

<a id="section-14"></a>

## AI-Enhanced Web Application for Requirements Prioritization

### Motivation and Overview

The theoretical analysis carried out in Sections 1–8 of this report examined eight methods for requirements prioritization and demonstrated their respective strengths under varying conditions of uncertainty. However, practical application of these methods requires not only mathematical understanding but also accessible tooling that enables analysts and project managers to perform computations without manual implementation. To address this gap, the second part of this project consists of the development of an interactive web application that exposes all prioritization algorithms through a browser-based interface and augments the computation results with an AI analytics layer powered by a large language model.

The primary objectives of the web application are threefold. First, to provide a uniform, method-agnostic interface for uploading structured input data and triggering any of the six prioritization families. Second, to visualize the resulting priority rankings through interactive charts and support side-by-side comparison of multiple methods on the same dataset. Third, to integrate a generative AI component capable of interpreting numerical results in natural language, identifying stakeholder conflicts, and engaging in a conversational dialogue about the analysis.

The application follows a client–server architecture comprising three logical layers: a React-based single-page frontend, a Python FastAPI backend, and an external AI service provided by Google Gemini 2.0 Flash via REST. The original tkinter desktop application developed during the first phase of the project serves as the algorithmic core; its logic modules are reused without modification through a dedicated logic bridge layer in the backend. A summary of the technology stack is given in Table 39.

**Table 39. Technology stack of the web application**

| **Layer**       | **Technology**                            |
| :-------------- | :---------------------------------------- |
| Backend         | Python 3.9+, FastAPI, Uvicorn             |
| Frontend        | React 18, Vite, Tailwind CSS, Recharts    |
| AI service      | Google Gemini 2.0 Flash (REST, free tier) |
| Session storage | In-memory (no database required)          |

### Backend: FastAPI Service

The backend is implemented in Python 3.9+ using the FastAPI framework and served by Uvicorn. It is organized into three routers:

- `upload.py` — handles `POST /api/upload` requests, receives one or more CSV files via multipart form data, stores them in an in-memory session store, and returns a `session_id` token.

- `analysis.py` — handles `POST /api/analyze/{method}` requests, retrieves the session data, invokes the corresponding algorithm from the logic bridge, and returns structured results alongside any detected stakeholder conflicts.

- `ai.py` — exposes three AI-related endpoints: `POST /api/ai/interpret`, `POST /api/ai/conflicts`, and `POST /api/ai/chat` (Server-Sent Events stream).

The full set of REST endpoints is summarized in Table 40.

**Table 40. REST API endpoint reference**

| **Method** | **Endpoint**            | **Description**                                                                                 |
| :--------- | :---------------------- | :---------------------------------------------------------------------------------------------- |
| `POST`     | `/api/upload`           | Upload one or more CSV files; returns `session_id`                                              |
| `POST`     | `/api/analyze/{method}` | Run prioritization analysis; returns ranked results and conflict data                           |
| `POST`     | `/api/ai/interpret`     | Generate a natural-language summary of the current session’s results                            |
| `POST`     | `/api/ai/conflicts`     | Enrich detected conflicts with AI-generated root-cause analysis and resolution advice           |
| `POST`     | `/api/ai/chat`          | Streaming conversational assistant (SSE); full analysis context injected into the system prompt |
| `GET`      | `/api/session/{id}`     | Retrieve session data including uploaded files and all prior analysis results                   |

Session state is held entirely in memory using a Python dictionary keyed by UUID. This design choice eliminates the need for a database and simplifies deployment: the application requires no external infrastructure beyond a Python runtime and a Node.js environment for the frontend build. The trade-off is that sessions are ephemeral and do not persist across server restarts, which is acceptable for the educational and research context of this project.

The logic bridge module (`logic_bridge.py`) imports the algorithm files from the original tkinter application without any modification. This preserves the correctness of the mathematical implementations verified in Sections 1–8 and avoids code duplication. Each algorithm is invoked through a thin adapter that converts the structured session data into the format expected by the original logic and maps the output back into a JSON-serializable structure.

Conflict detection is performed within the analysis router before the results are returned to the frontend. The system classifies disagreements into two categories: _hard conflicts_, where two or more stakeholders assign diametrically opposed rankings to the same alternative (e.g., one stakeholder considers a feature critical while another considers it unnecessary), and _soft conflicts_, where moderate but non-trivial divergences exist. The detected conflicts are stored in the session object and can subsequently be enriched with AI-generated explanations.

### Frontend: React Application

The frontend is a single-page application built with React 18, Vite, Tailwind CSS, and the Recharts charting library. It consists of three main pages:

- **Home** — displays six method-selection cards, each indicating the method name, a brief description, and the number of CSV files required. Clicking a card navigates to the Analysis page for the selected method.

- **Analysis** — provides drag-and-drop CSV upload zones (one per required file), a method-specific file format guide, a results section with an interactive horizontal bar chart, an expandable conflict alert panel, an AI interpretation block, and a collapsible streaming chat sidebar.

- **Dashboard** — aggregates results from two or more analyses performed in the current session into a comparative side-by-side bar chart and a ranked results table, enabling direct visual comparison of method outputs.

The drag-and-drop upload mechanism is implemented without third-party dependencies using the native HTML5 File API. Each upload zone validates the file extension and provides inline feedback. Upon successful upload, the frontend receives a `session_id` from the backend, which is stored in component state and attached as a header to all subsequent API requests within the session.

Results are rendered as color-coded horizontal bar charts. Each bar represents one alternative, and its length encodes the priority score returned by the selected method. The chart is interactive: hovering over a bar displays the exact numeric score in a tooltip. This design was chosen over vertical bar charts because alternative names are typically multi-word strings that are easier to read on a horizontal axis.

### AI Integration: Google Gemini 2.0 Flash

The AI layer is built around Google Gemini 2.0 Flash, accessed via the Gemini REST API using a free-tier key. All AI calls are encapsulated in `ai_service.py`, which exposes three functions corresponding to the three AI endpoints. The service degrades gracefully when the daily or per-minute quota is exhausted: the frontend renders an informative message instead of a generic error state, and all prioritization computations continue to function normally.

#### Automatic Result Interpretation

After each analysis run, the frontend automatically requests an AI-generated interpretation of the results. The backend constructs a structured prompt that includes the method name, the ranked list of alternatives with their scores, and any detected conflicts, then queries the Gemini API and returns the response to the client. The resulting summary is 3–4 sentences long and addresses the following points: which alternatives emerged as high-priority, what the score distribution suggests about the dataset, and whether the results are consistent with domain intuition.

This feature addresses one of the practical barriers to adopting mathematical prioritization methods: analysts unfamiliar with TOPSIS or Fuzzy AHP may not know how to interpret a ranked list of defuzzified scores. The natural-language summary bridges this gap by translating numerical output into actionable insight without requiring domain expertise in fuzzy mathematics.

#### Stakeholder Conflict Detection and AI Analysis

Stakeholder conflict detection operates at two stages. At the algorithmic stage, the analysis router examines the weight matrices and rating vectors to identify pairs of stakeholders whose assessments diverge beyond configurable thresholds. At the AI stage, the `/api/ai/conflicts` endpoint takes the detected conflict records and asks Gemini to explain the probable business or organizational root cause of each disagreement and to suggest a concrete resolution strategy.

The AI-enriched conflict cards are displayed in the Analysis page as expandable panels. Each card shows the conflicting stakeholders, the specific alternatives on which they disagree, the degree of divergence, and the AI-generated analysis. This two-stage approach — deterministic detection followed by generative explanation — ensures that the conflict identification is reproducible and not subject to hallucination, while the explanation benefits from the language model’s broad knowledge of organizational dynamics and requirements management practice.

#### Conversational Assistant

The chat panel provides a persistent conversational interface throughout the analysis session. When the user opens the chat, the backend constructs a detailed system prompt that includes all results stored in the session: method names, ranked alternatives with scores, detected conflicts, and any AI interpretations already generated. This context is passed to the Gemini API on every message, enabling the model to answer follow-up questions such as “Why is Two-Factor Authentication ranked above CRM Integration in Fuzzy AHP but below it in MoSCoW?” or “Which method would you recommend given that we have a tight security budget?”

Responses are streamed to the frontend using Server-Sent Events (SSE), so the user sees text appear progressively rather than waiting for the full response. The chat history is maintained in the React component state and included in each request to preserve conversational continuity within the session.

### Supported Methods and Input Formats

All six prioritization families implemented in the desktop application are exposed through the web interface. Table 41 summarizes the supported methods, their algorithmic variants, and the number of CSV files required per analysis.

**Table 41. Prioritization methods supported by the web application**

| **Method**   | **Variants**                                     |            **Input files**             |
| :----------- | :----------------------------------------------- | :------------------------------------: |
| MoSCoW       | —                                                | 2 (requirements + stakeholder weights) |
| TOPSIS       | —                                                |                   1                    |
| Kano Model   | —                                                |                   1                    |
| Fuzzy AHP    | Type-1 (triangular), Type-2 (interval)           |                  1–3                   |
| Fuzzy TOPSIS | Fuzzy Type-1 (trapezoidal), Intuitionistic (IFS) |                   2                    |
| Fuzzy Delphi | IT2FS, Intuitionistic (IFS)                      |                   1                    |

Each method’s Analysis page displays an inline file-format guide specifying required column names and permissible values for every CSV file. Example CSV files covering all methods and variants are bundled with the application in the `prioritization_tool/assets/` directory, allowing users to test the system immediately after installation.

### Key Design Decisions

Several architectural decisions deserve explicit discussion, as they reflect deliberate trade-offs appropriate to the project’s educational and research context.

_Stateless in-memory sessions._ Choosing in-memory session storage over a persistent database significantly simplifies deployment and eliminates infrastructure dependencies. The application starts with a single shell script (`start.sh`) that launches both the backend and frontend servers simultaneously. The cost is that sessions are lost on server restart, but for an analytical tool used in short interactive sessions this is acceptable.

_Logic bridge pattern._ Reusing the original tkinter application’s algorithm files without modification was a deliberate choice to ensure mathematical correctness. All eight algorithm implementations had been verified during the first phase of the project. Reimplementing them in a REST-oriented style would have introduced regression risk. The bridge layer adds negligible overhead while preserving the full fidelity of the mathematical models described in Sections 1–8.

_Graceful AI degradation._ The free Gemini tier allows 1,500 requests per day and 15 requests per minute. When the quota is exhausted, the AI service returns a structured error that the frontend renders as an informative message rather than a generic error state. All prioritization computations continue to function normally; only the AI interpretation, conflict analysis, and chat features are temporarily unavailable. This design ensures that the core analytical functionality is never blocked by external API quota limits.

_CSV as the universal data format._ All six method families accept input as CSV files. This decision maximizes compatibility with the tools analysts already use — spreadsheet software, survey exports, data pipelines — and avoids the need for a custom data-entry interface. Column names and structures are method-specific and documented in the per-method file guides shown on the Analysis page.

### Conclusions

The AI-enhanced web application developed in this section complements the theoretical analysis of Sections 1–8 by providing a practical, accessible implementation of all eight prioritization methods in a unified interface. The three AI features — automatic interpretation, conflict detection with root-cause analysis, and conversational assistance — address the main usability barriers associated with applying advanced fuzzy methods in practice: difficulty in interpreting numerical outputs, identifying stakeholder disagreements, and navigating multi-method results.

The application demonstrates that generative AI can serve as an effective interpretive layer on top of deterministic mathematical algorithms, combining the reproducibility and formal rigor of fuzzy prioritization with the explanatory power of large language models. The architecture is designed for extensibility: adding a new prioritization method requires only implementing the algorithm module and registering it in the logic bridge and frontend routing — the AI, session, and upload infrastructure require no changes.

<a id="section-15"></a>

## Conclusion

In the course of this work, several requirements prioritization methods were examined and analyzed — both classical (crisp) ones and those based on fuzzy logic and interval assessments. Each of them demonstrated its own characteristics and specifics of application, enabling a deeper understanding of how much requirements prioritization is complicated by the subjectivity of expert opinions, multi-criteria nature, and the presence of varying degrees of confidence in assessments. The main conclusions and a summarizing analysis are presented below.

First, crisp methods (MoSCoW, the Kano Model, classical TOPSIS) performed well in situations where sufficiently clear metrics exist and where experts (or stakeholders) can give unambiguous answers to the questions of “how important is a requirement” and “what happens if a given feature is not implemented.” For example, in MoSCoW the final categories (Must-have, Should-have, Could-have, Won’t-have) allow requirements to be quickly divided by priority and an ordered implementation list to be formed. In the Kano Model, the relationship between the presence/absence of a feature and user satisfaction is clearly traced: we obtain important, “explosive” (Attractive) or Indifferent requirements, which simplifies communication with business customers and end users. In classical TOPSIS, multiple criteria (security, usability, business value, etc.) and distances to ideal alternatives are taken into account simultaneously. All three approaches demonstrated that in most cases requirements related to reliability and security (for example, Two-Factor Authentication, Data Backup) consistently come out on top in priority. This speaks to the consistency of the overall logic: across all methods such requirements are indeed seen as critically important from the business and user perspective.

However, it is important to note that when moving from one method to another, some differences in rank distribution are observed. This is explained by the fact that each method is oriented around its own decision-making model and interprets the “significance” of features differently. MoSCoW gives a more “discrete” picture (four categories), whereas TOPSIS provides quantitative ordering. Kano, in turn, focuses on how a feature affects satisfaction. Such divergences do not contradict each other but rather complement the picture, offering several independent perspectives. For projects with tight resource constraints it is convenient to start from MoSCoW, while for a large set of criteria (for example, when it is also necessary to account for cost, risks, system response time, etc.) classical TOPSIS or its variants prevail.

Second, the work demonstrated approaches for accounting for stakeholder weights. Practice shows that if certain experts have significantly greater experience, higher responsibility, or bear key decision-making duties, their opinions should carry greater weight during aggregation. Applying such weights (in MoSCoW, Kano, or TOPSIS) realistically reflects the balance of forces within the team and can lead to the situation where the “weights” of individual criteria or individual ratings begin to significantly shift the final priority list. This embeds a managerial trade-off: on the one hand, accuracy increases, since a “lead” expert provides a more reliable opinion; on the other hand, the risk of a single viewpoint dominating grows. Consistency in the examples presented in this work was maintained, since even with elevated weights for one stakeholder all methods pointed to high priority for features affecting security and business value.

Third, methods with interval and fuzzy assessments (Interval TOPSIS, Fuzzy TOPSIS Type-1) made it possible to account for situations where experts cannot give an exact number but say, for example, “security is rather medium, but possibly closer to high,” or indicate blurred boundaries. The results showed that prioritization outcomes largely preserve the general trend of classical TOPSIS (again, features related to security come out on top), but now each requirement receives not a point estimate “rank = 0.7” but rather a range (interval) or fuzzy membership function. This gives a more flexible picture: a project manager can see, for example, that “Two-Factor Authentication” or “Data Backup” fall in the interval \[0.65; 0.78\] in importance, while “CRM Integration” falls in \[0.40; 0.50\]. If the team has an opportunity to vary budgets and time during planning, these intervals help set boundaries more finely, since they make it possible to answer questions like “how large is the risk that under different input data the priorities will shift?”

The fourth important observation is that despite differences in methodologies, most approaches demonstrate consistency of results at the extremes of the priority scale — both among the most significant and among the least important requirements. The main divergences arise in the middle part, where the final rating is largely determined by the features of expert perception, the level of subjectivity, and the specifics of the business context, which is not always amenable to formalization. In this context, interval and fuzzy methods prove to be especially useful, since they make it possible to explicitly account for the zone of uncertainty. They demonstrate that prioritization in this area is not a fixed and unambiguous result, but reflects permissible variations in the interpretation of requirement significance. In classical methods, analogous uncertainty is typically masked by averaging or by a forced choice between fixed categories.

Finally, it is worth emphasizing that the practical web application developed in the second part of this project demonstrates how the gap between mathematically rigorous prioritization and day-to-day analytical practice can be bridged. The AI-enhanced interface reduces the expertise barrier for adopting fuzzy methods: a project manager who has never encountered defuzzification or Footprint of Uncertainty receives an actionable plain-language interpretation of every analysis result. The automated conflict detection component surfaces stakeholder disagreements that might otherwise go unnoticed until they cause planning failures. The conversational assistant allows the user to interrogate the results interactively, exploring “what if” scenarios without rerunning the full analysis pipeline.

Thus, the examined methods and calculation examples demonstrate that:

1.  **Crisp techniques** (MoSCoW, Kano, classical TOPSIS) are well suited for relatively clear and established domains where experts can provide specific and unambiguous assessments.

2.  **Interval and fuzzy methods** (Interval TOPSIS, Fuzzy TOPSIS, including Type-1, and prospectively more advanced ones — Type-2, intuitionistic fuzzy sets) prove more flexible when it is necessary to account for blurred boundaries and human uncertainty.

3.  All methods agree that key (often “non-negotiable”) requirements such as security, reliability, and critically important functionality consistently occupy the top positions regardless of methodology, thereby indicating consistency of the overall result structure.

4.  Differences in mid-range and low-priority requirements are natural and can be explained by how a given method interprets the significance of criteria and their weights: MoSCoW uses a categorical approach, Kano focuses on impact on satisfaction, TOPSIS on geometric proximity to the “ideal” solution, and fuzzy methods on the degree of membership in fuzzy concepts of “high” or “medium” importance.

5.  The AI analytics layer demonstrates that generative language models can serve as effective interpretive bridges between formal mathematical methods and practical decision-making, without compromising the reproducibility of the underlying computations.

Ultimately, the proposed set of methods should not be viewed as competing but rather as complementary. In a real project it is often advisable to use a **combination** of several approaches: begin with simple categorization (MoSCoW, Kano) for quickly separating truly critical features from secondary ones, and then, on the already sorted set, apply TOPSIS or Fuzzy TOPSIS for detailed quantitative analysis. The web application developed in this project supports precisely this workflow: the Dashboard page displays results from all methods side by side, and the AI assistant can reason across methods to help the analyst arrive at a final prioritized backlog.

Therefore, the main value of the conducted research is to show that prioritization methods are not universal, yet they combine well. If working with one method yields an ambiguous result, it makes sense to check it with a different approach (crisp or fuzzy) to guard against errors of subjectivity. The application of interval and fuzzy techniques reveals the scale of uncertainty embedded in decisions. And the AI layer makes that uncertainty legible to practitioners who are not specialists in fuzzy mathematics. Thus, the developed system — comprising the algorithmic implementations, the web interface, and the AI analytics layer — can substantially increase the transparency of the decision-making process in requirements prioritization, which ultimately affects project success.

<a id="section-16"></a>

## References

<a id="reference-1"></a>

**[1]** Bourque P., Fairley R. (eds.) [_Guide to the Software Engineering Body of Knowledge (SWEBOK)_](https://www.computer.org/education/bodies-of-knowledge/software-engineering). Version 3.0. IEEE Computer Society, 2014.

<a id="reference-2"></a>

**[2]** Babar M.A., Zhang H., Zhu L. [_An empirical study of stakeholder prioritization in requirements engineering_](https://www.researchgate.net/publication/266078340_Systematic_Reviews_in_Requirements_Engineering_A_Systematic_Review). Empirical Software Engineering. 2018. Vol. 23, No. 1. Pp. 233–265.

<a id="reference-3"></a>

**[3]** Davis A., Dieste O., Hickey A., Juristo N., Moreno A.M. [_Effectiveness of requirements elicitation techniques: empirical results derived from a systematic review_](https://ieeexplore.ieee.org/document/1704061). Requirements Engineering. 2006. Vol. 11. Pp. 179–202.

<a id="reference-4"></a>

**[4]** Wiegers K., Beatty J. [_Software Requirements_](https://www.oreilly.com/library/view/software-requirements-3rd/9780735679658/). 3rd ed. Microsoft Press, 2013. 648 p.

<a id="reference-5"></a>

**[5]** Holla R. [_Assessing the Effectiveness of MoSCoW Prioritization in Software Development: A Holistic Analysis across Methodologies_](https://doi.org/10.4108/eetiot.6515). EAI Endorsed Transactions on Internet of Things. October 2024.

<a id="reference-6"></a>

**[6]** Kravchenko T., Bogdanova T., Shevgunov T. [_Ranking Requirements Using MoSCoW Methodology in Practice_](https://doi.org/10.1007/978-3-031-09073-8_18). In: _Cybernetics Perspectives in Systems_. Springer, 2022. Pp. 188–199.

<a id="reference-7"></a>

**[7]** del Sagrado J., del Águila I.M. [_Assisted Requirements Selection by Clustering_](https://arxiv.org/abs/2401.12634). arXiv preprint. 2024. arXiv:2401.12634.

<a id="reference-8"></a>

**[8]** Clegg D. [_CASE Method Fast-Track: A RAD Approach_](https://archive.org/details/fasttrackradappr0000cleg). Addison-Wesley, 1994. 192 p.

<a id="reference-9"></a>

**[9]** Clegg D. [_MoSCoW Prioritisation_](https://www.agilebusiness.org/dsdm-project-framework/moscow-prioririsation.html). DSDM Project Framework.

<a id="reference-10"></a>

**[10]** Saaty T.L. [_Scaling method for priorities in hierarchical structures_](https://superdecisions.com/sd_resources/Paper_ScalingMethod.pdf). Journal of Mathematical Psychology. 1987. Vol. 15, No. 3. Pp. 234–281.

<a id="reference-11"></a>

**[11]** Sauerwein E., Bailom F., Matzler K., Hinterhuber H. [_The Kano model: How to delight your customers_](https://www.researchgate.net/publication/240462191_The_Kano_Model_How_to_Delight_Your_Customers). International Working Seminar on Production Economics. 2001. Vol. 1, No. 4. Pp. 313–327.

<a id="reference-12"></a>

**[12]** Shamsuzzoha A., Helo P. [_Kano model: A dynamic approach for classifying and prioritizing travellers’ requirements_](https://doi.org/10.1016/j.rtbm.2016.07.001). Research in Transportation Business & Management. 2016. Vol. 20. Pp. 39–47.

<a id="reference-13"></a>

**[13]** Wang H., Liang L., Lu T., et al. [_Kano Model Categorization Methods: Typology and Systematic Review_](https://doi.org/10.1177/10963480241230957). Journal of Hospitality & Tourism Research. 2024.

<a id="reference-14"></a>

**[14]** Sehlhorst S. [_Prioritizing Software Requirements with Kano Analysis_](https://www.pragmaticinstitute.com/resources/articles/product/prioritizing-software-requirements-with-kano-analysis). Pragmatic Institute.

<a id="reference-15"></a>

**[15]** Goldstein K. [_Kano Analysis: the Kano Model Explained_](https://www.qualtrics.com/experience-management/research/kano-analysis/). Qualtrics.

<a id="reference-16"></a>

**[16]** Zadeh L.A. [_Fuzzy sets_](<https://doi.org/10.1016/S0019-9958(65)90241-X>). Information and Control. 1965. Vol. 8, No. 3. Pp. 338–353.

<a id="reference-17"></a>

**[17]** Chen C.T. [_Extensions of the TOPSIS for group decision-making under fuzzy environment_](<https://doi.org/10.1016/S0165-0114(97)00377-1>). Fuzzy Sets and Systems. 2000. Vol. 114, No. 1. Pp. 1–9.

<a id="reference-18"></a>

**[18]** Torra V., Narukawa Y. [_Modeling Decisions: Information Fusion and Aggregation Operators_](https://www.researchgate.net/publication/220693669_Modeling_Decisions_Information_Fusion_and_Aggregation_Operators). Springer, 2010. 180 p.

<a id="reference-19"></a>

**[19]** Xu Z., Yager R.R. [_Intuitionistic fuzzy aggregation operators_](https://www.researchgate.net/publication/3336510_Intuitionistic_Fuzzy_Aggregation_Operators). IEEE Transactions on Fuzzy Systems. 2008. Vol. 16, No. 4. Pp. 761–774.

<a id="reference-20"></a>

**[20]** Atanassov K.T. [_Intuitionistic fuzzy sets_](<https://doi.org/10.1016/S0165-0114(86)80034-3>). Fuzzy Sets and Systems. 1986. Vol. 20, No. 1. Pp. 87–96.

<a id="reference-21"></a>

**[21]** Shih H.S., Shyur H.J., Lee E.S. [_An extension of TOPSIS for group decision making_](https://www.sciencedirect.com/science/article/pii/S0895717706003025). Mathematical and Computer Modelling. 2007. Vol. 45. Pp. 801–813.

<a id="reference-22"></a>

**[22]** Tang T.Y., Hanif H. _[Fuzzy Delphi Method: A Step-by-Step Guide to Obtain Expert Consensus on MUETBot Functionalities](https://kwpublications.com/papers_submitted/9950/fuzzy-delphi-method-a-step-by-step-guide-to-obtain-expert-consensus-on-muetbot-functionalities.pdf)_. International Journal of Academic Research in Business and Social Sciences, 2024.

<a id="reference-23"></a>

**[23]** garai A. _[Weighted Intuitionistic Fuzzy Delphi Method](https://www.rroij.com/open-access/weighted-intuitionistic-fuzzy-delphi-method.php?aid=38810)_. Journal of Global Research in Computer Science, 2013, Vol. 4, No. 7, pp. 38–42.

<a id="reference-24"></a>

**[24]** Hsu Y.L., Lee C.H., Kreng V.B. _[The Application of Fuzzy Delphi Method and Fuzzy AHP in Lubricant Regenerative Technology Selection](https://doi.org/10.1016/j.eswa.2009.05.068)_. Expert Systems with Applications, 2010, Vol. 37, No. 1, pp. 419–425.

<a id="reference-25"></a>

**[25]** Mendel J.M., John R.I. [_Type-2 Fuzzy Sets Made Simple_](https://ieeexplore.ieee.org/document/995115). IEEE Transactions on Fuzzy Systems. 2002. Vol. 10(2). Pp. 117–127.

<a id="reference-26"></a>

**[26]** Wu D., Mendel J.M. [_Recommendations on Designing Practical Interval Type-2 Fuzzy Systems_](https://arxiv.org/abs/1907.01697). arXiv preprint. 2019. arXiv:1907.01697.

<a id="reference-27"></a>

**[27]** Sudžum R., Nestić S., Komatina N., Kraišnik M. [_An Intuitionistic Fuzzy Multi-Criteria Approach for Prioritizing Failures That Cause Overproduction: A Case Study in Process Manufacturing_](https://www.mdpi.com/2075-1680/13/6/357). Axioms. 2024. Vol. 13(6). No. 357.

<a id="reference-28"></a>

**[28]** Rajaprakash S., Ponnusamy R., Pandurangan J. [_Intuitionistic Fuzzy Analytical Hierarchy Process with Fuzzy Delphi Method_](https://www.researchgate.net/publication/316090463_Intuitionistic_fuzzy_analytical_hierarchy_process_with_fuzzy_Delphi_method). International Journal of Fuzzy Systems. 2017. Vol. 19(3). Pp. 726–737.

<a id="reference-29"></a>

**[29]** Saaty T. [_The Analytic Hierarchy Process_](https://www.researchgate.net/publication/362349026_The_Analytic_Hierarchy_Process). McGraw-Hill, 1980.

<a id="reference-30"></a>

**[30]** Buckley J. [_Fuzzy hierarchical analysis_](<https://doi.org/10.1016/0165-0114(85)90090-9>). Fuzzy Sets and Systems, 17(3), 1985.

<a id="reference-31"></a>

**[31]** Chang D.-Y. [_Applications of the extent analysis method on fuzzy AHP_](https://www.expertchoice.ir/wp-content/uploads/2017/08/FAHP-Chang-1996.pdf). European Journal of Operational Research, 95(3), 1996.

<a id="reference-32"></a>

**[32]** Kahraman C., Cebeci U., Ulukan Z. [_Multi-criteria supplier selection using fuzzy AHP_](https://www.researchgate.net/publication/235277936_Multi-criteria_supplier_selection_using_fuzzy_AHP). Engineering Applications of Artificial Intelligence, 17(6), 2004.

<a id="reference-33"></a>

**[33]** Mikhailov L. [_Deriving priorities from fuzzy pairwise comparison judgements_](https://www.researchgate.net/publication/222511354_Deriving_priorities_from_fuzzy_pairwise_comparison_judgements). Knowledge-Based Systems, 15(6), 2003.

<a id="reference-34"></a>

**[34]** Mendel J.M. [_Uncertain Rule-Based Fuzzy Logic Systems: Introduction and New Directions_](https://www.researchgate.net/publication/224285703_Uncertain_rule-based_fuzzy_logic_systems_introduction_and_new_directions). Prentice-Hall, 2001.

<a id="reference-35"></a>

**[35]** Mendel J.M., Bob John R.I. [_Type-2 Fuzzy Sets Made Simple_](https://sipi.usc.edu/~mendel/publications/Mendel%26John%202002.pdf). IEEE Transactions on Fuzzy Systems, 14(6), 2006.

<a id="reference-36"></a>

**[36]** Kulak O., Kahraman C. [_Fuzzy multi-attribute selection among transportation companies using axiomatic design and analytic hierarchy process_](https://www.researchgate.net/publication/222548501_Fuzzy_Multi-Attribute_Selection_Among_Transportation_Companies_using_Axiomatic_Design_and_Analytic_Hierarchy_Process). International Journal of Production Economics, 90(1), 2005.

<a id="reference-37"></a>

**[37]** Mikhailov L., Tsvetinov P. [_Evaluation of services using a fuzzy analytic hierarchy process_](https://www.researchgate.net/publication/222670785_Tsvetinov_P_Evaluation_of_services_using_a_fuzzy_analytic_hierarchy_process_Appl_Soft_Comput_5_23-33). Applied Soft Computing, 4(1), 2004.

<a id="section-17"></a>

## Appendix A. Description of the Software Implementation

### Purpose of the Application

The developed application implements automated prioritization of software requirements using both classical and fuzzy methods. The program is intended to support decision-making when planning system functionality, especially under conditions of multiple criteria and expert uncertainty. Particular attention has been paid to the flexibility of input formats and support for various fuzziness models, making the application a universal tool for requirements analysis.

### General Information

The program is written in Python using the following libraries:

- `tkinter` — for the graphical user interface;

- `pandas`, `numpy` — for data processing;

- `matplotlib` — for building charts;

- `fpdf` — for generating PDF reports.

### Main Window and Navigation

Upon launch, the main window opens, in which:

- a brief description of the program’s purpose is displayed;

- buttons for selecting the prioritization method are presented:

  - `MoSCoW`

  - `Kano`

  - `TOPSIS`

  - `Fuzzy TOPSIS`

  - `Fuzzy Delphi`

  - `Fuzzy AHP`

The user selects the required method by clicking the corresponding button. After that, the interface:

1.  hides all previous elements;

2.  displays a detailed text description of the input file format;

3.  shows upload buttons for each required file;

4.  activates the calculation launch button;

5.  shows the PDF report generation button.

All actions are accompanied by hints and validity checks for the uploaded files.

### MoSCoW Method

**Number of files:** one main file + a separate stakeholder weights file.

- **Main file (CSV):**

  - Columns: `"Alternative"`, `"Criterion"`, `"Stakeholder"`, `"Rating"`.

  - **Rating** is specified as:

    - `"100% M"` (single rating);

    - `"60% S, 40% C"` (mixed rating).

  - Permitted rating type pairs: `M/S`, `S/C`, `C/W`.

- **Weights file (CSV)**

  - Columns: `"Stakeholder"`, `"Weight"`.

  - When this file is present, the program applies the weight coefficient during calculation.

**Algorithm:**

1.  Reading ratings and stakeholder weights.

2.  Converting mixed ratings into numeric coefficients.

3.  Aggregating values for each alternative.

4.  Final classification on the MoSCoW scale.

### Kano Method

**Number of files:** one (CSV).

- Columns: `"Alternative"`, `"Stakeholder"`, `"Functional Response"`, `"Dysfunctional Response"`, `"Weight"`.

- Permitted categories: `Must-be`, `Attractive`, `One-dimensional`, `Indifferent`, `Reverse`, `Questionable`.

**Algorithm:**

1.  For each requirement the corresponding category is determined (by matching functional and dysfunctional responses).

2.  Weights are tallied and priorities are distributed across the full set of requirements.

3.  Based on the results, the most critical or attractive features are identified.

### TOPSIS Method

**Number of files:** one (CSV).

- First row — headers: `"Alternative"`, followed by criterion names, then `"Stakeholder Weight"`.

- Alternatives are listed row by row. For each alternative, numeric criterion values are specified along with the weight of one stakeholder (e.g., `0.4`).

**Algorithm:**

1.  Normalization of criteria.

2.  Weighting of values (using `"Stakeholder Weight"`).

3.  Computation of distances to the ideal and anti-ideal solutions.

4.  Calculation of final priorities.

### Fuzzy TOPSIS Method

**Number of files:** four. For each of the two approaches (Type-1 and Intuitionistic), two files are required: (1) requirements data and (2) a linguistic rating mapping scale.

**Type-1 (trapezoidal numbers):**

- **Requirements file (CSV):**

  - First column: `"Alternative"`.

  - Remaining columns: criterion names.

  - Values: text labels (`"Very Low"`, `"Low"`, `"Medium"`, `"High"`, `"Very High"`)

- **Scale file (CSV):**

  - Columns: `"Rating"`, `"(a, b, c, d)"`.

  - Used to convert linguistic labels into trapezoidal numbers.

**Intuitionistic (triads $`(\mu, \nu, \pi)`$):**

- **Requirements file (CSV):**

  - First column: `"Alternative"`.

  - Remaining columns: criteria.

  - Values: linguistic labels (e.g., `"Very Important, but with Doubts"`).

- **Scale file (CSV):**

  - Columns: `"Expert Rating"`, `"Membership Degree"`, `"Non-Membership Degree"`, `"Uncertainty Degree"`.

  - Example: `"Very Important, but with Doubts"`,`"(0.9,0.05,0.05)"`. Next to each file upload button there is an example showing what the input file should look like.

**Algorithm for both variants:**

1.  Converting linguistic values into fuzzy numbers (if necessary, using the uploaded scale).

2.  Normalization (for trapezoidal or intuitionistic ratings).

3.  Determining the positive and negative ideal solutions.

4.  Computing distances to the ideals and the final priorities.

5.  Forming the alternative ranking.

Results for the Type-1 and Intuitionistic versions are included in a single PDF report.

### Fuzzy Delphi Method

**Number of files:** two — one for each fuzziness type (Type-2 and Intuitionistic). The program demonstrates how different stakeholders can provide ratings: in linguistic form (Type-2) or in intuitionistic form (Intuitionistic).

**Type-2 file (CSV):**

- Required columns:

  - `"Alternative"` — e.g., the name of a feature.

  - `"Expert"` — the specialist’s identifier or name.

  - Several criterion columns (`"Criterion_1"`, `"Criterion_2"`, etc.).

  - `"Expert Weight"` — a number in the range from 0 to 1.

- Criterion values are specified in linguistic form (e.g., `"High Confidence -- Medium"`), which is internally converted into interval sets (Type-2 Fuzzy Sets).

**Intuitionistic file (CSV):**

- Analogous column structure:

  - `"Alternative"`

  - `"Expert"`

  - Several criterion columns

  - `"Expert Weight"`

- Values are given explicitly as `"(0.7, 0.2, 0.1)"`.

**Algorithm (both versions):**

1.  **Collection of expert ratings.** The program reads alternatives, criteria, experts, and their weights.

2.  **Conversion of linguistic values** into interval sets (for Type-2).

3.  **Calculation of averaged values** per criterion with expert weights taken into account.

4.  **Determination of the Footprint of Uncertainty (FOU)** and the confidence index, if required by the selected fuzziness model.

5.  **Formation of group consensus.** Final ratings are accumulated and can be analyzed for further requirements refinement.

### Fuzzy AHP Method

Two approaches are supported: numerical (Type-1) and linguistic (Type-2).

**Type-1 (numerical values):**

- **File 1:** Pairwise criteria comparison matrix (numbers `"1"`, `"3"`, `"1/3"`, etc.).

- **File 2:** Alternative ratings by criteria (fuzzy numbers of the form `"(1.5, 2.0, 2.5)"`).

- **File 3:** Expert weight coefficients (`"Expert"`, `"Weight"`).

**Type-2 (linguistic values):**

- **File 1:**

  - Columns: `"Expert"`, `"Weight"`, followed by criterion pairs (`"Security > Usability"`).

  - Values — linguistic ratings (`"Weakly"`, `"Strongly"`, `"Equally"`, etc.).

- Conversion of linguistic values is performed via the built-in scale.

**Algorithm:**

1.  Converting linguistic (or fuzzy) ratings into a numeric scale.

2.  Building the aggregated pairwise comparison matrix.

3.  Consistency check (CI, CR).

4.  Computing global priorities of criteria and alternatives.

### Report Generation

After the calculations for the selected method are complete, the user can click the `"Save PDF"` button, and the program will:

- automatically create a report file;

- include in it the method name, source and intermediate data, and final results;

- add priority charts and explanatory text;

- save the file to the `output` folder.

### Conclusion

The developed application demonstrates flexibility in supporting various prioritization methods — from classical to fuzzy. Each method is implemented as an independent module and admits a variety of input formats: both numeric values and linguistic ratings, which are automatically interpreted and converted. This makes it possible to adapt the tool to different analysis scenarios and levels of user preparation — from novice analysts to experienced researchers in the field of decision-making.

In the TOPSIS method, only one stakeholder’s opinion is included for clarity, which simplifies the demonstration of the calculation steps. In Fuzzy Delphi and Fuzzy AHP, ratings can be provided in different forms: linguistic (via a correspondence table) or as ready-made fuzzy numbers. Similarly, in Fuzzy TOPSIS the user can upload their own conversion scale for trapezoidal or intuitionistic ratings. Thus, the application provides a wide range of approaches to accounting for expert uncertainty and is suitable for a great variety of software planning and development scenarios.
