# Swimm Writing Examples

This file contains exemplary blog posts from Swimm that demonstrate the brand voice, style, and quality standards. Use these as reference when writing new content.

---

## Example 1: To Trust an LLM, Make Lying Harder Than Telling the Truth

**URL**: https://swimm.io/blog/to-trust-an-llm-make-lying-harder-than-telling-the-truth
**Primary Keyword**: LLM reliability, LLM hallucination
**Word Count**: ~2,500 words
**Publication Date**: October 30, 2025

**What Makes It Great**:
- Shares real-world experience from building production systems, making abstract concepts concrete through iterative problem-solving
- Uses narrative structure that teaches readers the "why" behind each decision, not just the "what"
- Balances technical depth with accessibility through clear examples and actionable takeaways

**Full Content**:
```
To trust an LLM, make lying harder than telling the truth

By Omer Rosenbaum, October 30, 2025

The LLM Said It Found a Match. It Was Lying.

At Swimm, the company relies on deterministic methods and LLMs to generate functional specifications. To ensure reliability, they need to validate these specs—but the validator itself uses an LLM. This creates a circular challenge: validating the validator requires understanding when LLMs lie, hallucinate, or forget.

The author built a semantic equivalence checker for specs, observed it fail dramatically, and discovered precisely when and why LLMs cannot be trusted. The solution involved forcing LLMs to be explicit about their reasoning.

Setting the Stage

Swimm generates functional specifications for complex applications based on code analysis. They combine static analysis, symbolic methods, and LLMs to create human-readable specs capturing business logic and domain terminology. This balance creates tension between clarity and consistency.

A reliable spec accurately describes application functionality—including all features present and excluding features absent. Measuring reliability requires comparing generated specs against known-correct specifications.

"True Spec" vs "Generated Spec"

The methodology involves creating manually-verified "true" specifications for real applications, then automatically generating specs using their system. This produces pairs for comparison: does generatedSpec(Program) ≈ trueSpec(Program)?

The entire approach depends on reliably determining semantic equivalence between textual specifications.

Validating the Semantic Equivalence Checker

The task requires determining if two textual descriptions are semantically equivalent despite different wording, ordering, or phrasing. Test datasets include pairs that are equivalent despite variations and pairs with semantic differences.

Let's Start Simple

Simple test cases demonstrate variations:

specA1 (baseline): Username must be unique and alphanumeric; password must be 8+ characters with mixed types; email must be valid format.

specB1 (reordered): Same requirements, different sequence.

specB2 (rewording): Similar meaning with different phrasing.

specB3 (decomposed): Breaking compound sentences into separate lines.

Negative cases include removing requirements, adding new ones, or changing values.

Attempt #1: Direct Comparison

Initial testing used a straightforward prompt asking if two specs were semantically equivalent.

Results: 114 of 117 checks passed (97.4% accuracy). However, three consistent failures emerged—all involving missing requirements in longer specifications. The LLM failed to detect differences only in lengthy specs (exceeding ten lines).

Attempt #2: Decomposition

Attempting to improve by breaking tasks into smaller steps backfired. The approach extracted requirements separately, then cross-checked them. Results dropped dramatically to 54 passed, 63 failed (46% accuracy).

The LLM exhibited hallucination, claiming requirements existed in specifications where they didn't appear. It fabricated matching statements, completing patterns from training data rather than finding actual matches.

Attempt #3: Adding Structure

Adding specific verdict categories reduced hallucination somewhat but didn't eliminate it completely. The LLM continued claiming requirements matched when they didn't.

Attempt #4: Forcing Evidence

The breakthrough came from requiring matchingIds and statementInOtherSpec fields before the matched boolean. This forced the LLM to find evidence before declaring matches.

Results transformed dramatically. Instead of hallucinating matches, the LLM returned: "Matching Ids: [], Statement in Other Spec: N/A" when requirements weren't found.

When Did the LLM Lie? What Can It Teach Us?

The LLM didn't technically lie—it optimized for the wrong objective. With maximum freedom interpreting vague questions, it took shortcuts with long specs. When decomposing tasks, it pattern-matched against training data, generating plausible-sounding false matches.

The breakthrough came through forced explicitness: requiring specific verdict categories, committing to particular IDs, grounding reasoning in actual text, and ordering outputs so evidence preceded conclusions.

The Key Insight: LLMs Don't Lie When Cornered with Specificity

"When the LLM could say 'matched: true' without providing evidence, it happily did so. When forced to produce the actual matching text and IDs, it suddenly became honest."

Key lessons:
- Vague outputs enable hallucination through pattern-matching
- Structured outputs requiring verifiable facts create accountability
- Long context demands structured decomposition
- Evidence-first reasoning prevents post-hoc rationalization

The Broader Lesson

Output quality depends on the response structure demanded, not just prompting. Making hallucination easy produces hallucination.

For reliability-critical LLM systems:
- Avoid binary judgments without evidence
- Structure outputs requiring grounding in verifiable facts
- Force commitment to specifics before conclusions
- Test extensively on complex, lengthy inputs

At Swimm, this approach powers production spec validation, checking thousands of generated specifications with required reliability standards. Trusting an LLM means designing interfaces that "make lying harder than telling the truth."
```

---

## Example 2: Blackbox to Blueprint - Extracting Business Logic from COBOL Applications

**URL**: https://swimm.io/blog/blackbox-to-blueprint-extracting-business-logic-from-cobol-applications
**Primary Keyword**: COBOL business logic extraction, legacy system modernization
**Word Count**: ~3,800 words
**Publication Date**: July 2, 2025

**What Makes It Great**:
- Uses a progression framework (complexity spectrum) to break down an overwhelming problem into manageable steps
- Provides concrete code examples that demonstrate the same business logic with increasing complexity
- Combines technical detail with practical strategy, showing both "what" challenges exist and "how" to address them

**Full Content**:
```
Blackbox to blueprint: Extracting business logic from COBOL applications

By Omer Rosenbaum | 2 Jul 2025 | 12 min read

Introduction

In this post, we will discuss how to extract business logic from COBOL applications.

What are business rules?

Business rules are the rules that govern the operation of a business.

There have been many attempts to define "business rules" formally (for example, by the Business Rules Group), which stated that a business rule is "a statement that defines or constrains some aspect of the business".

In essence, business rules are the specific constraints, conditions, and actions embedded within a software system that reflect the policies and procedures of an organization. Legacy systems contain strategic business rules that govern the business processes, whether these rules are explicit or implicit.

For example, within the process of transferring money between bank accounts, business rules would include constraints like:

- A customer cannot transfer more money than is available in their account (overdraft limits notwithstanding)
- Certain high-value transfers may require additional verification steps
- Transfers between accounts in different currencies must apply the current exchange rate

A technical definition

Some sources define Business Rules as consisting of three basic elements – Event, Condition and Action. The standard rule pattern is:

ON <Event>
IF <(Condition)>
THEN <Action>
ELSE <Action>

We will sometimes adopt this definition in this post.

A working example

Throughout this post, I will use a toy example to illustrate the process of extracting business rules from COBOL applications.

We will consider a simple COBOL program that calculates a "Risk Score" based on certain criteria. The Risk Score is then used to determine the status of an application (e.g., "Auto-Approved", "Pending Review", "Manual Review").

The challenge of extracting business rules from COBOL applications

Extracting business rules or business logic from applications has been a challenge for many years. In this section, we will better understand some of the challenges associated with extracting business rules from COBOL applications. This will allow us to devise a strategy to face these challenges.

As some of these challenges are technical and are closely related to the nature of COBOL and Mainframe applications, and some are non-technical, we will discuss them separately.

Technical challenges

- Scattered and intertwined logic: The business logic within COBOL systems is often scattered throughout the code. Especially in COBOL, tracking the flow of logic can be challenging, both within a single file and across multiple files. Furthermore, this logic is frequently intertwined with presentation logic, technical code, and auxiliary code. COBOL programs can have complex control flow structures, including deep calling hierarchies (PERFORMs) and sometimes GOTOs, making it hard to trace the sequence of operations that constitute a business rule.

- Technical environment complexity: A significant portion of the COBOL code (as much as 70-80% according to some sources) might be dedicated to the technical environment and infrastructure (e.g., IMS, CICS, DB2) rather than the core business logic. Identifying and filtering out this implementation-dependent logic is a major challenge. Specifically, distinguishing between data variables that are relevant to the business and those that are part of the technical framework is crucial but difficult. Technical variables (e.g., related to middleware or database interactions) need to be screened out to focus on business-related data.

- Naming Conventions: It is common for COBOL code to include cryptic variable or paragraph names that do not provide any insight into the purpose of the code.

Non-technical challenges

- Evolution over time: COBOL systems have often been maintained and evolved over many years, sometimes decades. This long history can lead to a situation where it is unclear which business rules are still actively enforced or if they are consistent with current organizational policies.

- Obsolete business logic: Legacy systems may contain obsolete business logic that was never removed from the code base. Identifying and distinguishing this from current, active rules adds to the difficulty of extraction.

- Skill shortage: It is increasingly difficult to find professionals with deep knowledge of both COBOL and the specific business domain. This knowledge gap complicates the process of accurately interpreting and extracting business rules from legacy code.

- Business knowledge loss: Over time, the original developers and business analysts who understood the rationale behind certain rules may have left the organization, taking their knowledge with them. This loss of institutional memory makes it challenging to validate extracted rules.

A roadmap and a north star

Our goal would be to extract the business rules from the COBOL application and represent them in a clear and concise manner – just like the flowchart we saw earlier.

We can define a tool that receives this COBOL code and outputs a set of business rules in a structured format, or a flowchart. For simplicity, let's assume we want to output a set of business rules in a single flowchart.

"Level 1" – all in one file, with clear paragraph names and variable names

This example is the simplest one. Despite being unrealistic, it is a good starting point as we will have to make sure we can handle the simplest case before moving on to more complex ones.

The complexity spectrum of COBOL business rule extraction

Unlike the previous example, real-world COBOL applications rarely present their business rules so neatly. To build an effective extraction tool, we need to understand the spectrum of challenges it might face.

Each factor represents a dimension of complexity that can be independently "dialed up" to create more challenging extraction scenarios. Starting with our simple example (Level 1 across all factors), we can gradually introduce complexity by adjusting specific factors while keeping others constant.

The overall extraction difficulty depends on combinations of these factors. For example:

- Example 1: Level 1 across all factors = Straightforward extraction
- Example 2: Level 3 Variable Names + Level 1 everything else = Moderate difficulty
- Example 3: Level 2-3 across most factors = Challenging extraction
- Example 4: Level 3-4 across all factors = Very complex extraction

For a practical challenge progression, we will increase difficulty across 1-2 factors at a time while keeping others stable, then gradually introduce more difficult combinations.

For instance, we might keep the clear paragraph names and comments but introduce cryptic variable names, forcing our extraction tool to infer meaning from context. Or we could maintain clear variables but distribute the logic across multiple files, requiring the tool to trace execution flow across program boundaries.

The beauty of this approach is that it allows for incremental development of our extraction capabilities. By tackling one complexity dimension at a time, we can build, test, and refine our tool's ability to handle progressively more realistic COBOL applications.

It also provides a framework for measuring extraction success—each level represents a milestone in the tool's sophistication.

Real-world COBOL systems typically fall somewhere between Levels 2 and 4 across most factors, with legacy mainframe applications often trending toward the higher end of the spectrum.

"Level 3" example – multiple files, cryptic variable names…

Below we provide the exact same COBOL program as before in terms of business logic, yet the implementation is different.

How different is it?

Despite being a relatively simple business logic, the implementation is significantly more complex (and realistic) than the previous example. Note this this is still a very short example, and real-world applications can be much more complex.

The main differences are:

(1) File Structure: The application is now split across multiple files:

- RSKMNT.CBL – Main CICS transaction program
- RSKPRC.CBL – Processing module that contains the business logic
- VARDEF.CPY – Copybook with cryptic variable definitions
- PSTCHK.CPY – Copybook with postcode risk logic
- STATCALC.CPY – Copybook with status determination logic
- PRPMSET.BMS – BMS map definition for the CICS screen interface

(2) Cryptic Elements

- Variable names: are now V1 (was PROPERTY-TYPE), V2 (was PROPERTY-POSTCODE), V3 (was RISK-SCORE), V4 (was RISK-STATUS), V5 (new, represents an error flag).
- Paragraph names: Changed to single letters with numbers (A100, P200, etc.)
- No comments or DISPLAY statements.

(3) Control Flow

- Added GOTO statements throughout the processing module.
- Split logic across copybooks
- Added complexity with error handling and CICS transaction flow

(4) CICS Integration

- Added proper CICS commands for screen handling
- Used COMMAREA for data passing between programs
- Added BMS map definition for screen handling

The business logic remains the same

Despite all these changes, the business logic remains identical:

1. Base score starts at 100
2. Property type risk adjustment (Warehouse: +50, Factory: +75, Office: +25, Retail: +40)
3. High risk postcode check adds 30 points for FL/CR
4. Status determination (>200: Status 2, 151-200: Status 1, ≤150: Status 0)

This complex version would present a significant challenge for business rule extraction tools while still implementing the exact same logic from your original flowchart.

Facing the challenge – example

In this section, we will consider one example of how to face the challenge of extracting business rules from COBOL applications – specifically, when the variable names are cryptic.

When trying to understand the business logic of a program by looking at its code, one of the most helpful things are names – variable names, function names, etc. I will focus on variable names, but the same applies to sections, programs etc. In Cobol, variable names are usually quite cryptic for various reasons.

Using static code analysis, we can provide the LLM with all of this relevant context from the program. But it doesn't stop there – to understand the meaning of these variables, the LLM would need to understand the context in which they are used as part of the flow of the program.

One can suggest that by providing the entire codebase to the LLM, it would be able to understand the context in which these variables are used. Besides the downsides of cost, time and feasibility due to token limits, this approach would still not be enough. On the contrary – if there is another variable called V4 in another part of the codebase, the LLM might confuse the two, and provide inaccurate description of this specific V4 variable.

Ambiguity resolution is something that deep code analyzers excel at, and this is one way where they can complement LLMs in understanding Cobol mainframe code. A tool that performs deep-analysis of Cobol code would provide the LLM with all the context it needs in order to explain a variable, function or program – and only that context, to avoid "confusion" by the LLM.

This is only a single part of the puzzle, and there are many other challenges that need to be faced in order to extract business rules from Cobol applications, but I hope this example illustrates the point of how using LLMs in conjunction with deep code analyzers can help us understand Cobol code better.

Conclusion

Extracting business logic from COBOL applications remains a significant challenge in the modernization of legacy systems. As we've seen throughout this exploration, the task involves navigating a spectrum of complexities – from cryptic variable names and scattered logic to the intertwining of business rules with technical implementation details.

The roadmap we've outlined recognizes that this is not a one-size-fits-all problem. By categorizing the complexity factors and approaching them systematically, we can develop incremental strategies that evolve from handling the simplest cases to tackling the most convoluted legacy codebases.

What becomes clear is that modern approaches benefit from combining multiple techniques. Static code analysis tools provide the necessary context and disambiguation that LLMs need to interpret the code meaningfully. Meanwhile, LLMs offer the flexibility to understand patterns and express business logic in human-readable formats once provided with properly contextualized information.

While our simple risk assessment example illustrates the principles, real-world applications will present more diverse challenges. The approach outlined here – progressively handling increasing levels of complexity while maintaining focus on the ultimate goal of clear, concise business rule representation – provides a framework that can be adapted to various legacy modernization contexts.

By combining deep code analysis, modern AI techniques, and disciplined methodology, we can bridge the gap between decades-old implementations and contemporary business needs.
```

---

## Example 3: Blackbox to Blueprint - Illuminating COBOL Systems

**URL**: https://swimm.io/blog/blackbox-to-blueprint-illuminating-cobol-systems
**Primary Keyword**: COBOL system understanding, mainframe application documentation
**Word Count**: ~2,400 words
**Publication Date**: June 4, 2025

**What Makes It Great**:
- Opens with compelling statistics that anchor the problem in real-world impact (80% of credit card transactions, 95% of ATMs)
- Uses a clear framework (screens, batches, utilities) to organize overwhelming information into digestible categories
- Demonstrates the product's value through specific examples rather than abstract claims

**Full Content**:
```
Blackbox to blueprint: Illuminating COBOL systems

By Omer Rosenbaum | 4 Jun 2025 | 9 min read

So, you need to make sense of a massive COBOL codebase. Perhaps you're modernizing it, debugging an issue, or just trying to untangle decades of business logic.

If you're here, you already know that COBOL still powers mission-critical systems in banking, retail, insurance, and beyond. In fact, COBOL supports 80% of in-person credit card transactions and 95% of all ATM transactions. For those who know COBOL, the real challenge isn't about understanding the language—it's deciphering layers of updates, patches, and undocumented logic built over decades. Manually mapping out a large COBOL system can take months. But what if AI could do the heavy lifting for you?

Most technical posts focus on how we solved a problem. This one is about you—what you need to efficiently understand a COBOL system and how AI can help transform a black box into a blueprint.

Understanding the essential: Gaining observability

To effectively navigate a COBOL mainframe application, you need a clear view of its core components. We found that most systems can be broken down into three main entities:

1. Online operations: Screens and the workflows they interact with
2. Batch operations: Jobs, often written in JCL, that handle high-volume, repetitive tasks
3. Utilities: Copybooks and complex shared logic

If you want to understand what a mainframe application actually does, you can get a very good idea by focusing on these key areas:

1. User screens: What screens are available to the user?
2. Screen interactions: What actions can be performed on each screen?
3. Batch operations: What batch jobs exist, and when do they run?
4. Batch job logic: What does each batch job do?
5. Shared logic: Are they complex routines used across multiple operations? If so, what do they handle?

Being able to answer these questions gives you a solid, high-level understanding of the application. But understanding isn't just about collecting details—it's about filtering the noise.

A system with thousands of screens can quickly become overwhelming. The key is to separate the signal from the noise, identifying patterns and grouping similar components together. Too much raw information isn't helpful; the real goal is to extract the essence of how the system functions.

Consider this example:

When looking at a COBOL codebase, it is common to get a flat folder with all (or most of) the source files. If you're lucky, the files have extensions – making it easier to separate programs (.cbl) from copybooks (.cpy) and perhaps other files (e.g., .jcl). Even if that is the case, the filenames are usually cryptic.

Swimm's approach helps you navigate the codebase in a few ways. One is to group together jobs, screens, copybooks and programs. Notice that Swimm doesn't only group the files by type, but it also provides meaningful names – so you see Employee Data Entry in addition to the file's name (EMPENT).

Then, when you select an entry point (say, a screen or a program) - you can see other files that relate to your entry point. So if you want to understand the payroll calculation process, you might start with the program that actually performs the calculation, and then find it can be triggered via a recurring JCL Job, or find a screen that triggers it as well. You will also see that it uses other programs that you may want to consider.

Drilling down: Understanding screen behavior

So, now you've identified a specific screen and know what it does at a high level. But what if you need to go deeper? Maybe you're rewriting this screen's logic on a modern platform, or modifying its behavior to meet new business requirements.

To fully understand a screen's functionality, you need answers to key questions:

1. What is the screen's goal?
2. What are the input limitations and validations?
3. What happens when a user interacts with the screen?
4. How is the underlying logic implemented?
5. What business rules apply?

A truly useful document should provide all this information in a clear, structured way. Enter Swimm.

How Swimm brings a screen to life

1. Understanding the screen's goal

Sometimes, just seeing a screen already gives you significant insight. Swimm reconstructs screens from the underlying code, presenting them in a way that mirrors how users interact with them.

Beyond visuals, Swimm also provides concise textual descriptions, like: "The Bill Payment screen (COBIL00) is a CICS COBOL program that allows users to pay their credit card balance in full through an online interface."

This instantly clarifies the screen's purpose, making it easier to grasp its function within the system.

2. Input limitations and validations

If you need to replicate the screen's behavior or modify input rules, you'll want to understand exactly how inputs are validated. Swimm automatically extracts this information, detailing field constraints like:

Account ID Input Field (ACTIDIN):
- Length: 11 characters
- Required field
- Becomes read-only after initial entry

Current Balance Display (CURBAL):
- Format: Signed numeric
- Read-only

Payment Confirmation (CONFIRM):
- Single-character input (yes or no)
- Case-insensitive validation

Swimm doesn't just list validations—it connects them to their source.

3. Understanding user interactions

What actually happens when a user interacts with the screen? Answering this requires both clarity and accuracy—a challenge Swimm tackles through visual flowcharts that illustrate all possible interactions.

For example, Swimm's generated diagrams might show:

- The sequence of operations triggered by different inputs
- How data flows between screens and backend systems
- Conditional branches based on user actions

If you need a different level of detail, Swimm's visualization tools can adapt to your needs, letting you refine the diagram to highlight the most relevant flows.

4. Step-by-step code walkthroughs

For deeper technical insights, a high-level diagram isn't enough—you need to see the exact logic behind key operations. Swimm provides step-by-step walkthroughs, aligning code snippets with clear explanations.

For instance, if you're analyzing how the user account ID is validated, Swimm will:

- Extract the relevant COBOL routines
- Provide inline comments explaining each step
- Highlight dependencies between different parts of the code

This approach allows you to trace a function's execution path without manually searching through thousands of lines of legacy code.

Understanding batch operations

While individual screens provide critical insight into a mainframe application, much of the core business logic often resides in batch operations. These jobs process large volumes of data, execute key financial calculations, and generate essential system updates.

Let's say you already have a high-level understanding of a batch operation. Now, you need to go deeper—whether to debug an issue, modify existing functionality, or rewrite the logic in a modern environment.

For example, consider Swimm's auto-generated summary for CBACT04C: "The Interest Calculator (CBACT04C) is a COBOL batch program that calculates interest charges for credit card accounts based on transaction category balances. It processes account balances, applies appropriate interest rates, and generates interest transactions."

While this does give you a broad, succinct understanding of the program's purpose—many critical questions still remain:

1. Does the process process new accounts differently?
2. How is the interest rate calculated?
3. What is the result of the interest transaction generated?
4. What are the input files and formats?
5. How are edge cases handled?

How Swimm helps

To answer the question: Does the program process new accounts differently? Swimm generates a flowchart that visually maps the decision logic. Instead of manually tracing COBOL conditionals and nested IF statements, you can instantly see:

- What changes when processing a new account vs. an existing one
- Which processing steps remain the same regardless of account type
- Where business rules apply to different categories of accounts

This lets you quickly identify critical paths in the batch job's execution without sifting through thousands of lines of COBOL.

Breaking down the interest calculation logic

Understanding how interest is calculated requires more than just an overview—you need to see:

- The formula used to apply interest rates
- Any conditional adjustments based on account status, balance type, or transaction history
- Where rounding, thresholds, or caps are applied

Swimm extracts and annotates the relevant COBOL logic, mapping it to a step-by-step explanation. This eliminates the need for manual code spelunking, letting you focus on what truly matters.

Connecting input data to processing logic

Batch jobs don't operate in isolation—they rely on structured input files. To fully understand a job, you need answers to:

- What files are used as input?
- What is the format of these files?
- How are records parsed and processed?
- Which fields impact downstream calculations?

Swimm automatically links the batch program's file-handling routines to their definitions, helping you trace:

- Where data comes from
- How records are validated and transformed
- Where processed data is written

This ensures that if you modify the job, you don't accidentally disrupt upstream or downstream processes.

What about edge cases and exceptions?

Every batch process must deal with unexpected conditions, such as:

- Accounts with zero balances
- Transactions missing required fields
- Invalid or outdated interest rate tables
- System failures or partial job executions

Swimm highlights exception-handling routines, making it easy to see:

- How the program detects errors
- Whether errors trigger retries, logging, or alerts
- Whether certain failures halt processing or allow partial execution

Next up: Business logic

In part 2, we dive into how you can use AI to extract decades of missing business logic.
```

---

## Example 4: The Hidden Landmine in COBOL's PERFORM Statement

**URL**: https://swimm.io/blog/the-hidden-landmine-in-cobols-perform-statement-a-control-flow-puzzle
**Primary Keyword**: COBOL PERFORM statement, COBOL control flow
**Word Count**: ~2,000 words
**Publication Date**: April 22, 2025

**What Makes It Great**:
- Engages readers with an interactive puzzle that makes them think before revealing the answer
- Explains a highly technical concept (stack-based control flow) through accessible metaphors ("armed mine")
- Connects deep technical detail to practical implications for legacy code analysis

**Full Content**:
```
The hidden landmine in COBOL's PERFORM statement: a control flow puzzle

By Omer Rosenbaum | 22 Apr 2025 | 6 min read

At Swimm, we perform static code analysis in order to understand large and complex codebases. While working on parsing COBOL code, I discovered some weird and surprising behaviors. As I started sharing them with friends, I found out they were interesting for other (geeks 😇) as well.

Let's review one such surprising behavior.

COBOL's PERFORM Statement for Non-COBOL Programmers

To understand this behavior, let's quickly review how COBOL's PERFORM statement works.

COBOL programs are organized into sections and paragraphs (similar to functions in modern languages). Each paragraph has a name followed by a period.

The PERFORM statement allows you to execute a sequence of paragraphs:

PERFORM paragraph-name THRU exit-paragraph.

This command tells the computer to:

1. Jump to "paragraph-name"
2. Execute all paragraphs from there until "exit-paragraph" is completed
3. Return to the statement immediately following the PERFORM

It is similar to function calling in other languages, without using arguments – within a COBOL program the state is managed by global variables.

A COBOL Control Flow Puzzle

Take a look at this COBOL code segment and see if you can predict what would happen:

A. DISPLAY "1. Starting program".
   PERFORM D THRU E.
B. DISPLAY "5. Second stage".
   PERFORM C THRU F.
   DISPLAY "9. Program complete".
   STOP RUN.
C. DISPLAY "6. In paragraph C".
D. DISPLAY "2. In paragraph D".
   IF FIRST-RUN
      DISPLAY "3. Error on first run - going to B"
      MOVE FALSE TO FIRST-RUN
      GOTO B.
   DISPLAY "X. This line only executes on second run".
E. DISPLAY "4. In paragraph E".
F. DISPLAY "8. In paragraph F".

Assume FIRST-RUN is a condition that's true on the first execution of paragraph D, but false on subsequent executions. What output would you expect to see?

Think about it for a moment before reading on.

The Surprising Answer

Most people would expect something like this:

1. Starting program
2. In paragraph D
3. Error on first run – going to B
5. Second stage
6. In paragraph C
2. In paragraph D
X. This line only executes on second run
4. In paragraph E
8. In paragraph F
9. Program complete

But the actual output is:

1. Starting program
2. In paragraph D
3. Error on first run – going to B
5. Second stage
6. In paragraph C
2. In paragraph D
X. This line only executes on second run
4. In paragraph E
5. Second stage       <– Wait, what? Why are we back at B?
6. In paragraph C
2. In paragraph D
X. This line only executes on second run
4. In paragraph E
8. In paragraph F
9. Program complete

Did you notice what happened? After executing paragraph E the first time, the program unexpectedly jumped back to B instead of continuing to F!

Technical Implementation Details: How PERFORM Actually Works

To understand the "armed mine" issue, we need to look at how COBOL implements the PERFORM statement internally:

1. Control Block Structure: When COBOL encounters a PERFORM statement, it creates a control block containing:
   - The entry point (beginning paragraph address)
   - The exit point (ending paragraph address)
   - The continuation address (where to return after completion)

2. PERFORM Stack: These control blocks are managed in a stack-like structure:
   - When a PERFORM executes, its control block is pushed onto the stack
   - When an exit paragraph is reached, the runtime checks if it matches the most recent exit point on the stack
   - If it matches, the control block is popped and execution returns to the saved continuation address

3. Exit Paragraph Detection: When execution reaches any paragraph, COBOL:
   - Checks if this paragraph matches the current exit paragraph on the stack
   - If it matches, pops the stack and jumps to the saved return address
   - If not, it simply executes the paragraph and continues normally

4. Normal Cleanup: In proper structured programming:
   - Each PERFORM statement gets a corresponding exit paragraph execution
   - Control blocks are properly pushed and popped in a balanced way
   - The stack empties naturally as execution proceeds

Now we can understand what happens when a GOTO disrupts this delicate stack management!

The "Armed Mine" Explanation

Now let's walk through our example step by step with this technical understanding:

1. Execution begins at statement A: PERFORM D THRU E
   - COBOL pushes a control block onto the stack:
     - Exit point: paragraph E
     - Continuation address: statement B
   - "1. Starting program" is displayed
   - Execution jumps to paragraph D

2. In paragraph D, the condition FIRST-RUN is true:
   - "2. In paragraph D" is displayed
   - "3. Error on first run – going to B" is displayed
   - FIRST-RUN is set to FALSE
   - GOTO B jumps directly to paragraph B
   - Critical point: The control block for the PERFORM remains on the stack!
   - This is the "armed mine" – paragraph E is still associated with a return to B

3. Execution continues at B:
   - "5. Second stage" is displayed
   - PERFORM C THRU F is executed
   - COBOL pushes another control block onto the stack:
     - Exit point: paragraph F
     - Continuation address: "DISPLAY '9. Program complete'"
   - The stack now has two control blocks: [E→B, F→"9. Program complete"]

4. Paragraphs C and D execute:
   - "6. In paragraph C" is displayed
   - "2. In paragraph D" is displayed again
   - This time FIRST-RUN is false, so execution continues
   - "X. This line only executes on second run" is displayed

5. When execution reaches paragraph E:
   - "4. In paragraph E" is displayed
   - COBOL checks if E matches any exit point on the stack
   - It matches the first PERFORM's exit point!
   - The "mine" detonates:
     - COBOL pops the first control block
     - Execution jumps to the saved continuation address (B)
   - Note that the second PERFORM's control block remains on the stack

6. Execution repeats from B:
   - "5. Second stage" is displayed again
   - PERFORM C THRU F executes a second time
   - The stack now has two control blocks again
   - Paragraphs C through F execute fully this time
   - When F is reached, its control block is popped and execution returns to "DISPLAY '9. Program complete'"

This surprising behavior occurs because GOTO bypassed normal control flow, but didn't clean up the PERFORM stack. The "armed mine" remains dormant until paragraph E is reached through a different path.

Technical Implementation Details (Detailed)

Behind the scenes, COBOL maintains a control stack structure that manages these execution paths:

1. Control Block Structure: When a PERFORM statement is encountered, COBOL creates a control block containing:
   - The entry point (beginning paragraph address)
   - The exit point (ending paragraph address)
   - The continuation address (where to return after completion)

2. PERFORM Stack: These control blocks are pushed onto a conceptual stack, with multiple active PERFORMs creating nested layers.

3. The GOTO Problem: When a GOTO jumps out of a PERFORM range:
   - The control block remains active on the stack
   - The exit point (E in our example) is still associated with its continuation address (B)
   - When execution later reaches that exit point through a different path, it "detonates" the mine

Accurate Analysis of COBOL Code is Complex

In this post we saw a specific example, where the PERFORM/GOTO interaction creates a form of implicit state that persists beyond the visible control flow of the program. It's almost like a hidden variable that gets set during execution but isn't visible in the source code.

When we parse and analyze legacy COBOL code, we're not just dealing with the visible structure of the program but also with these invisible continuation addresses that can dramatically alter control flow in ways not obvious from reading the source.

To correctly analyze COBOL code and be able to understand it, we need to deeply understand its underlying mechanisms.
```

---

## Example 5: Strategic Thought Leadership (Template)

**Type**: thought-leadership
**Primary Topic**: Strategic framework / industry analysis
**Word Count**: ~1,800-2,200 words
**Audience**: Enterprise leadership and decision-makers

**What Makes It Different from Examples 1-4**:
- Argument-driven rather than educational or tutorial-based
- Builds a framework or takes a position rather than explaining how something works
- Uses industry experience and patterns as evidence rather than code examples
- Addresses trade-offs and counterarguments honestly
- Lighter product integration - Swimm mentioned only if genuinely part of the argument

**Structural Template**:
```
[Title that captures the position or framework]

By [Author] | [Date] | [Read time]

[Opening: 150-250 words]
Start with an observation, tension, or pattern from industry experience.
State what's at stake. Declare the thesis within the first 200 words.
The reader should know immediately what argument this article is making.

Example opening pattern:
"Enterprise modernization programs have a vocabulary problem.
Everyone says 'agentic' now. The pitch is compelling: point an AI
agent at your legacy estate and let it figure things out. But the
organizations running the most successful modernization programs
are doing something different. They're building factories."

[H2: First argument section - establish the key concept]
Define the framework, concept, or position. Make it concrete with
a specific example or scenario. Each paragraph should advance the
argument, not just add information.

[H2: Second argument section - deepen with evidence]
Support the thesis with industry patterns, real-world scenarios,
or data. Show why the conventional wisdom is incomplete.

[H2: Third argument section - address the costs honestly]
This is what separates good thought leadership from marketing.
Name the trade-offs, challenges, and counterarguments. Address
the strongest objection directly. This builds credibility.

[H2: Fourth argument section (optional) - the human element]
For topics involving process or organizational change, address
what changes for the people involved. How does their role shift?
What do they gain and what do they lose?

[Conclusion: 100-200 words]
Synthesize the argument. Acknowledge open questions where they
exist. Point forward. Light CTA if appropriate.
```

**Voice Notes for Thought Leadership**:
- Use the "Strategy/Advice Content" tone from brand-voice.md: Authoritative, substantive, frameworks-oriented
- Write as someone who has earned the perspective through years of experience
- Be willing to take a position that someone could disagree with - that's what makes it thought leadership
- Concrete examples and scenarios are essential - abstract arguments without grounding read as opinion, not insight
- Honest about difficulty. "This is hard because..." is stronger than pretending everything is solvable
- Avoid the "listicle disguised as thought leadership" pattern - 3-5 deeper sections beats 7 shallow ones
- Product mentions are optional. If the article stands stronger without them, leave them out

**How It Differs from SEO Content**:
| Dimension | SEO Content | Thought Leadership |
|-----------|-------------|-------------------|
| Starting point | Keyword / search intent | Idea / position / framework |
| Structure | Comprehensive topic coverage | Argument progression |
| Sections | 4-7 H2s covering breadth | 3-5 H2s with depth |
| Evidence | Statistics, SERP data, expert quotes | Experience, patterns, scenarios |
| Product mentions | Natural integration throughout | Optional, only if part of argument |
| Links | 3-5 internal, 2-3 external (required) | Only where genuinely relevant |
| Keyword optimization | 1-2% density, keyword in headings | Not a consideration |
| Word count | 2000-3000+ | 1500-2500 |
| Post-write agents | Full SEO pipeline | Argument reviewer + meta + repurposers |

---

## Common Patterns Across Examples

### Voice & Tone Patterns

- **Direct address to the reader's context**: Opens by acknowledging the reader's specific situation ("So, you need to make sense of a massive COBOL codebase," "At Swimm, we perform static code analysis")
- **Technical authority without condescension**: Explains complex concepts assuming intelligence, not ignorance ("For those who know COBOL, the real challenge isn't about understanding the language")
- **Conversational expertise**: Uses first-person ("I discovered," "we found") to share real experiences rather than abstract theories
- **Transparent about complexity**: Acknowledges difficulty upfront rather than oversimplifying ("Accurate Analysis of COBOL Code is Complex," "The task involves navigating a spectrum of complexities")
- **Invites reader participation**: Poses questions, presents puzzles, asks readers to think ("What output would you expect to see?" "Think about it for a moment")
- **Uses memorable metaphors**: "Armed mine," "black box into a blueprint," "make lying harder than telling the truth"

### Structural Patterns

- **Problem-first openings**: Every article starts with the challenge before introducing solutions
- **Layered explanations**: Moves from simple to complex (e.g., Level 1 → Level 3 complexity spectrum)
- **Step-by-step walkthroughs**: Numbered lists that trace execution or logic systematically
- **Visual learning cues**: References to flowcharts, diagrams, and visual representations (even when describing them textually)
- **"How it works" deep dives**: Technical implementation sections that go beyond surface-level explanations
- **Modular content**: Uses clear H2/H3 structure allowing readers to jump to relevant sections
- **Connecting articles**: References to related content ("In part 2, we dive into...") creating content clusters

### Content Patterns

- **Real-world context grounding**: Opens with statistics and real-world impact ("80% of credit card transactions," "95% of ATMs")
- **Concrete code examples**: Shows actual code rather than describing it abstractly
- **Before/after comparisons**: Demonstrates the same logic in different complexity levels
- **Framework-based thinking**: Introduces organizing frameworks (complexity spectrum, three main entities, Event-Condition-Action pattern)
- **Multiple solution approaches**: Shows failed attempts before successful ones, teaching through iteration
- **Technical precision with accessible language**: Balances exact terminology with explanatory clarity
- **Complementary techniques**: Emphasizes combining tools ("Static code analysis tools... complement LLMs")
- **Practical implications**: Connects technical details to real modernization/analysis work
- **Honest about limitations**: Acknowledges when something "still not be enough" or presents challenges

### SEO Patterns

- **Question-based headings**: Uses reader questions as H2/H3 headings ("What are business rules?" "How different is it?" "What about edge cases?")
- **Keyword-rich technical terms**: Naturally incorporates searchable phrases (COBOL PERFORM statement, business logic extraction, LLM hallucination)
- **Progressive disclosure**: Content structure mirrors likely search journey from basic to advanced
- **Specific use cases in headings**: "Level 3 example – multiple files, cryptic variable names" targets exact search intent
- **Long-form comprehensive coverage**: Articles range 2,000-3,800 words, thoroughly covering topics
- **Internal content linking**: References between articles create topic authority clusters
- **Code-heavy content**: Extensive code examples likely help with technical search queries
- **Numbered list structures**: "5 key areas," "4 attempts," easily scannable and shareable

### Unique Swimm Patterns

- **Education through iteration**: Shows failed attempts and learning process, not just final answers
- **Deep technical credibility**: CTO/founder byline writing about hands-on implementation experience
- **Niche technical audience**: Writes for legacy system experts, not beginners
- **Product integration without hard selling**: Mentions Swimm capabilities contextually within problem-solving narrative
- **Academic tone meets practical application**: Balances formal technical writing with pragmatic use cases

### Thought Leadership Patterns (Example 5)

- **Position-first structure**: States thesis early and builds argument through each section
- **Framework-oriented**: Gives the reader a mental model they can apply to their own situation
- **Honest about costs**: Addresses trade-offs and counterarguments directly rather than presenting one-sided case
- **Experience-grounded**: Uses industry patterns and real scenarios as evidence, not just statistics
- **Lighter product integration**: Swimm mentioned only when genuinely part of the argument
- **Fewer, deeper sections**: 3-5 H2s that each advance the argument vs. 4-7 H2s that cover breadth
