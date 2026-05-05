from __future__ import annotations

import csv
import html
import zipfile
from io import StringIO
from pathlib import Path


CREATED = "2026-04-27"
OUT = Path(__file__).resolve().parents[1] / "950_LeLe" / "lessons_learned_thesis.xlsx"
ALT_OUT = Path(__file__).resolve().parents[1] / "950_LeLe" / "lessons_learned_thesis_master_level.xlsx"
CLEAN_OUT = Path(__file__).resolve().parents[1] / "950_LeLe" / "lessons_learned_thesis_master_level_cleaned.xlsx"


GUIDELINE_TSV = r"""Requirement from professor guideline	How this workbook addresses it	Workbook location / sheet	Notes
Create a lessons learned document	This workbook is a separate deliverable for the lessons learned reflection.	File: 950_LeLe/lessons_learned_thesis.xlsx	Created as Excel because the guideline references an XLSX template.
Keep it short and focused	The main sheet uses concise rows with direct future actions.	Sheet: Lessons Learned	Rows are written for discussion with the professor, not as thesis chapters.
Answer what was good and should be kept	The main matrix contains a dedicated column for successful practices.	Sheet: Lessons Learned, column D	Also summarized in the Keep Practices sheet.
Answer what was bad and needs to be changed	The main matrix contains a dedicated improvement column.	Sheet: Lessons Learned, column E	Also converted into corrective actions in the Improvement Plan sheet.
Support final discussion with professor	The workbook links lessons to thesis phases, artefacts, and future actions.	All sheets	Use this file during the final review or colloquium preparation.
Avoid personal/confidential detail	The content describes methods, project work, and engineering process learning.	All sheets	No confidential company data or personal data is included.
Make the file submission-ready	The workbook has filters, frozen headers, wrapped cells, and color-coded priority/status fields.	All sheets	Can be submitted as XLSX and exported to PDF if needed.
Show what was learned from literature	A dedicated sheet links key papers/sources to concrete technical learning and thesis application.	Sheet: Literature Learning	This makes the reflection stronger at master-thesis level.
"""


LESSONS_TSV = r"""No.	Thesis phase / area	Activity or situation	What was good and should be kept	What was difficult or should be improved	What I learned	Evidence from thesis work	Future action	Priority	Category
LL-01	Topic scoping and problem definition	Defining the thesis around automatic robot program generation for a robotic press brake cell.	The topic was linked to a clear industrial workflow problem: reducing manual programming effort while keeping validation before execution.	The scope initially touched many areas such as CAD, perception, trajectory generation, gripper design, and simulation.	A thesis topic becomes manageable only when the core technical contribution is sharply separated from supporting background.	Ch.1 objective, Ch.3 requirements, Ch.4 concept decision.	Keep the main contribution visible in every chapter and avoid adding unsupported side topics late in the work.	High	Keep and improve
LL-02	State of the art research	Reviewing robot programming, OLP, robotic bending, grasping, regrip planning, and digital simulation.	The review gave a strong basis for the selected system architecture and showed why manual programming is still a bottleneck.	Some references were initially too broad or not the best source for the exact claim.	Literature is not only a bibliography task; every citation must support the exact sentence where it is used.	Ch.2, citation_claim_audit.md, citation_claim_evidence_matrix.xlsx.	Start a claim-evidence matrix during literature review, not after writing most chapters.	High	Improve
LL-03	Citation verification	Checking claims against original papers and PDFs.	The final verification process improved the reliability of the thesis and reduced false-claim risk.	It took significant time because claim checking was done late and some PDFs were missing or mismatched.	Good technical writing requires traceability from claim to source, including correct paper, page, and claim scope.	citation_claim_audit.md and citation_claim_evidence_matrix.xlsx.	Maintain a source log with PDF filename, page, claim, and thesis location from the first week.	High	Improve
LL-04	Requirement management	Writing functional, non-functional, and software platform requirements.	Using requirement IDs made it easier to connect implementation, validation, and appendix traceability.	Some requirements became clearer only after implementation started.	Requirements should be specific enough for validation but flexible enough for engineering iteration.	Ch.3 requirements, Appendix requirement traceability matrix.	Freeze a first requirement baseline earlier, then explicitly record later changes.	High	Keep and improve
LL-05	Concept development	Comparing Concept A, B, and C using a weighted decision model.	The weighted sum model made the concept decision more objective and easier to defend.	Weighting criteria required careful explanation to avoid appearing arbitrary.	Concept selection is stronger when the decision is based on requirements and measurable criteria.	Ch.4 concept comparison and WSM table.	Define weights together with supervisors or stakeholders before scoring concepts.	Medium	Keep and improve
LL-06	Simulation-first implementation	Using the drag&bot virtual environment before physical deployment.	The virtual cell allowed safe testing of robot, press brake, orientation table, gripper, and object handling logic.	Simulation fidelity and interface assumptions still had to be checked carefully.	Simulation reduces risk, but it must be treated as an engineering model with limits, not as proof of physical performance.	Ch.5 development and simulation environment, test environment figure.	Build the virtual cell earlier and document all model assumptions explicitly.	High	Keep
LL-07	System architecture	Developing a layered architecture for configuration, geometry, planning, communication, and validation.	The layer separation improved maintainability and made the implementation easier to explain.	Some module boundaries had to be refined during writing to make data flow clearer.	Architecture is not only code organization; it is also a communication tool for the thesis reader.	Ch.5 system architecture and module overview table.	Keep architectural diagrams and module tables synchronized with the actual implementation.	High	Keep
LL-08	Configuration design	Using YAML configuration for workpiece, process, robot, gripper, and motion parameters.	The configuration-based approach supported adaptability without changing source code.	The configuration file required careful validation to prevent hidden inconsistency between related parameters.	Flexible systems need controlled parameter management and clear validation rules.	Ch.5 configuration architecture, YAML listing.	Add automatic consistency checks and a configuration version field in future projects.	Medium	Keep and improve
LL-09	WebSocket and AnyRobot communication	Implementing communication with the drag&bot runtime through WebSocket/AnyRobot.	Centralizing communication avoided duplicated message construction across modules.	The ROSAuth/SHA-512 description required exact matching with vendor documentation.	Interface documentation must be followed precisely; small field-order or naming differences can make a technical claim wrong.	Ch.5 communication architecture, SHA authentication listing.	Verify interface formulas and service fields directly against vendor documentation before finalizing text.	High	Improve
LL-10	Operator interface	Using an interactive 3D sheet bending viewer integrated into the operator cockpit.	The visual interface reduced reliance on abstract side labels and supported intuitive bend-side selection.	The interaction had to be limited during execution to avoid inconsistent operator input.	User interfaces in automation should minimize unnecessary choices while still supporting expert configuration when needed.	Ch.5 operator interface section.	Define basic and expert modes early and document which parameters are persistent.	Medium	Keep
LL-11	Pose and zone classification	Classifying the sheet position into workspace zones from tracked centroid coordinates.	The zone method made downstream decisions deterministic and simple to validate.	Thresholds are implementation parameters and must not be presented as universal theory.	Simple rule-based methods are acceptable when their assumptions and thresholds are clearly stated.	Ch.5 virtual cell layout and zone classification.	Keep thresholds configurable and record why each threshold value was selected.	Medium	Keep and improve
LL-12	Orientation strategy	Developing the three-level orientation selection strategy.	The structured fallback strategy ensured that a pickup orientation could be generated even under constraints.	The distinction between admissible orientation and fallback orientation required careful explanation.	Robotic decision logic must carry status information forward, not only return a pose.	Ch.5 workpiece orientation strategy and flow diagram.	Keep explicit result states such as valid, corrected, fallback, and not confirmed.	High	Keep
LL-13	Vacuum gripping model	Calculating feasible suction cup positions using geometry and an adapted conservative force model.	The combination of hole exclusion, edge clearance, cup spacing, and force checks made grip planning more robust.	The exact vacuum-force equation needed careful wording as an adapted conservative model, not a direct copied standard formula.	Engineering formulas can be adapted, but the thesis must clearly distinguish source principles from thesis-specific modelling choices.	Ch.5 vacuum holding force validation.	Keep adapted-model wording and document assumptions such as efficiency, safety factor, and acceleration.	High	Keep and improve
LL-14	Regrip planning	Handling cases where direct bending is not feasible from the current grasp.	Regrip logic made the automation concept more complete than a simple direct-pick-and-bend workflow.	Regrip planning adds complexity because it connects orientation, grip feasibility, reachability, and sequencing.	Regrip is a system-level problem; it cannot be solved by grip planning or trajectory generation alone.	Ch.5 regrip planning and execution.	Create smaller test cases for each regrip decision path before testing the complete workflow.	High	Keep and improve
LL-15	Opposite-side bending	Developing a flip-station workflow for bends on the opposite side.	The two-stage flip sequence avoids unrealistic in-gripper rotations and reuses existing validation logic.	The exact workflow is a thesis design decision and should not be over-cited as if it came directly from a paper.	Implemented workflows should be presented as own engineering design while citing only the general background.	Ch.5 opposite-side bending workflow.	Keep reuse of existing validation pipeline and clearly label thesis-specific process logic.	Medium	Keep
LL-16	Trajectory generation	Generating smooth waypoint-based motion with interpolation and minimum-jerk timing.	The trajectory section connects validated task poses to executable robot motion in a structured way.	Named mathematical methods need correct citations and clear boundary assumptions.	Equations should be introduced stepwise with purpose, variables, assumptions, and source when needed.	Ch.5 trajectory generation and equation audit.	For every equation, write source/own-design status during drafting.	High	Keep and improve
LL-17	Safety validation and FMEA	Using pre-execution checks and a simplified FMEA-style risk scoring convention.	The safety-first structure shows that motion generation is not allowed before validation.	The RPN formula needed to be reframed as a thesis scoring convention because no formal FMEA standard was used.	If a formal standard is not applied, the thesis should describe the method honestly as a local scoring convention.	Ch.5 safety validation and FMEA section.	Either obtain the formal standard early or explicitly define an internal scoring method.	High	Improve
LL-18	Validation and evaluation	Documenting functional validation and comparing manual versus automated workflow.	The evaluation connects implementation outcomes back to requirements and workflow-level benefits.	Some quantitative claims require careful separation between measured results, simulation observations, and expected benefits.	Evaluation should distinguish measured evidence from interpretation.	Ch.6 evaluation tables and appendix trial records.	Keep raw data, trial logs, and evaluation tables aligned from the beginning.	High	Keep and improve
LL-19	Figure and report quality	Adding figures, captions, references, and float placement controls.	Referencing every figure in text improved readability and compliance with the professor guideline.	LaTeX floats can move figures away from the intended section if not controlled.	Figure quality is not only image resolution; placement, caption, and text explanation matter equally.	Ch.2 to Ch.5 figures, preamble placeins section control.	Use section float barriers and check the compiled PDF after each major layout change.	Medium	Keep and improve
LL-20	Scientific writing	Rewriting claims to avoid overstatement and unsupported wording.	The final text became more defensible when claims were tied to what was actually implemented or verified.	Some early sentences used citations for claims that were broader than the source allowed.	Scientific writing should be precise, conservative, and source-aware.	Ch.1 to Ch.7 claim audit and final citation cleanup.	Use wording categories: literature-supported, implementation-specific, measured result, and future expectation.	High	Improve
LL-21	AI-assisted workflow	Using AI as a support tool for checking, restructuring, and technical questioning.	AI helped challenge claims, find inconsistencies, and improve wording when final responsibility remained with the author.	Every AI-assisted step needed transparency, prompt logging, and human verification.	AI is useful as a reviewer and assistant, but it does not replace author responsibility for correctness.	declaration_gpt.tex and appendix prompt log.	Keep prompt logs machine-readable and verify every technical output before use.	High	Keep and improve
LL-22	Project management	Managing development, writing, citation checking, formatting, and submission preparation.	The work benefited from breaking the thesis into phases and deliverables.	Final-stage citation checking, formatting, and evidence documentation took longer than expected.	The last part of a thesis is not only writing; it includes verification, formatting, traceability, and submission packaging.	Project files, citation matrices, compiled PDF checks.	Reserve the final two weeks only for verification, formatting, and submission documents.	High	Improve
"""


KEEP_TSV = r"""Practice to keep	Why it worked well	Where it helped in the thesis	How to standardize it next time
Requirement IDs with traceability	They connected problem definition, implementation, and validation.	Ch.3 requirements, Appendix traceability matrix.	Create requirement IDs before implementation and keep them stable.
Weighted concept decision	It made the selected concept easier to defend objectively.	Ch.4 weighted sum model.	Define criteria and weights before scoring alternatives.
Layered architecture	It made the system understandable and easier to maintain.	Ch.5 system architecture and module overview.	Use one architecture diagram plus one module responsibility table.
Simulation before hardware	It allowed safe testing of robot cell logic before physical execution.	Ch.5 simulation environment.	Create the virtual cell at the beginning of development.
Central communication module	It prevented duplicated WebSocket message logic.	Ch.5 communication architecture.	Route all runtime communication through one interface layer.
Configuration-driven parameters	It supported adaptation to different workpieces without code changes.	Ch.5 YAML configuration.	Use schema validation and versioned configuration files.
Explicit safety checks before execution	It reduced the risk of invalid motion commands.	Ch.5 pre-execution safety validation.	Place validation before planning and execution in the workflow.
Evidence matrix for citations	It reduced false citation and unsupported claim risk.	citation_claim_evidence_matrix.xlsx.	Maintain the matrix continuously during writing.
Compiled-PDF layout checks	They revealed float placement and formatting issues that were not visible in the .tex file.	Final LaTeX layout work.	Compile after each chapter-level edit and inspect figures/tables.
Clear AI declaration and prompt logging	It supports transparency and compliance with the professor guideline.	declaration_gpt.tex and appendix prompt log.	Keep prompts as machine-readable text during the work, not after.
"""


IMPROVEMENT_TSV = r"""Improvement area	Problem observed	Root cause	Corrective action	When to apply	Priority	Expected benefit
Citation verification	Some citations initially supported only part of the written claim.	Claim checking was concentrated near the end.	Check each citation immediately when a claim is written.	From first literature review onward.	High	Lower false-claim and plagiarism risk.
PDF/source management	Some references were missing, web-only, or mismatched with the cited key.	Source files were collected in several folders.	Use one controlled reference-paper folder with consistent filenames matching BibTeX keys.	Before writing Ch.2.	High	Faster verification and cleaner submission package.
Vendor interface documentation	The ROSAuth/SHA description required late correction.	Implementation and documentation were not compared field-by-field early enough.	Create an interface-contract table for service fields, message names, and formulas.	During communication-layer implementation.	High	Fewer technical documentation errors.
Equation documentation	Some equations required later source-status checking.	Equations were written before deciding whether they were sourced or thesis-specific.	Add a source-status note for each equation while drafting.	Whenever adding an equation.	High	Clear distinction between literature equations and own model.
Scope control	The topic could expand into CAD, SLAM, AI, hardware, and full digital twin areas.	Many adjacent robotics topics are relevant but not central.	Maintain an explicit out-of-scope list and update it after supervisor meetings.	During concept and methodology phases.	Medium	More focused thesis and less unnecessary citation work.
Simulation assumptions	Some simulation-based statements needed careful wording.	Simulation was used as the main validation environment.	Create a simulation-assumptions table with limits and validation scope.	Before Ch.5 and Ch.6 writing.	Medium	More defensible evaluation.
Test data organization	Validation evidence and trial records need consistent storage.	Test records were easier to interpret after tables were built.	Use a standard template for every trial: input, expected result, actual result, evidence file, status.	During evaluation.	High	Stronger reproducibility.
Figure workflow	Figures sometimes did not stay near the related text in the PDF.	LaTeX float placement was checked late.	Use section float barriers and inspect PDF layout after each figure insertion.	During writing.	Medium	Better readability and formatting compliance.
Supervisor discussion preparation	Lessons learned and supporting documents were not created early.	Focus was mainly on thesis text and implementation.	Maintain a deliverables checklist including paper, presentation, lessons learned, raw data, and final zip.	From midterm onward.	Medium	Lower submission stress.
Time planning	Final checking took longer than expected.	Citation, formatting, and verification work were underestimated.	Reserve final weeks for cleanup only, with no new feature development.	At initial Gantt planning.	High	More reliable submission schedule.
"""


SKILLS_TSV = r"""Skill area	Concrete skill learned	Thesis example	Benefit for future engineering work	Confidence
Scientific research	Matching exact claims to original sources instead of citing generally.	Citation claim audit and evidence matrix.	Improves technical credibility and reduces plagiarism risk.	High
System engineering	Translating an industrial automation problem into requirements, architecture, and validation logic.	Ch.3 requirements and Ch.5 layered architecture.	Supports structured development of complex mechatronic systems.	High
Robotics fundamentals	Applying pose, TCP, workspace, reachability, singularity, and trajectory concepts.	UR5e simulation, zone classification, trajectory generation.	Strengthens robot-programming and automation design capability.	High
Industrial automation integration	Using drag&bot, AnyRobot, WebSocket, IO, and object manager services as one workflow.	Ch.5 communication and gripper/object attachment logic.	Useful for integrating software with robot runtime environments.	High
Simulation-based validation	Using a virtual cell to test program logic before hardware deployment.	drag&bot virtual press brake environment.	Reduces commissioning risk and supports safer iteration.	High
Algorithm design	Designing deterministic rule-based strategies for orientation, grip, regrip, and flipping.	Three-level orientation strategy and grip planner.	Supports explainable automation methods.	High
Engineering modelling	Building an adapted conservative vacuum force feasibility model.	Vacuum holding force validation.	Improves ability to combine literature principles with practical assumptions.	Medium
Software architecture	Separating configuration, planning, validation, communication, and execution modules.	Module overview and architecture diagrams.	Improves maintainability and testability.	High
Validation thinking	Connecting requirements, FMEA, test scenarios, and evaluation tables.	Ch.6 evaluation and appendix traceability.	Improves evidence-based engineering reporting.	High
Technical writing	Writing precise, conservative, and source-aware technical explanations.	Final citation and equation cleanup.	Improves thesis/report quality and professional communication.	High
LaTeX/document control	Managing figures, captions, references, float placement, and compile checks.	Preamble float fix and figure insertion.	Improves final-document quality.	Medium
Responsible AI use	Using AI for checking and refinement while keeping author responsibility.	AI declaration and prompt log.	Supports transparent and compliant use of AI tools.	Medium
"""


LITERATURE_TSV = r"""No.	Reference / paper or source	Topic area	Key idea learned from the source	What I learned from the paper/source	How it influenced the thesis	Limitation / caution learned	Applied in thesis
PL-01	Gupta et al., Automated process planning for sheet metal bending operations	Sheet-metal bending process planning	Bending automation is not only a robot-motion problem; tooling, bend sequence, grasping, and feasibility constraints are coupled.	I learned that robotic bending must be treated as an integrated process-planning and manipulation problem.	This supported the thesis focus on automatic program generation with validation, grip planning, and regrip logic rather than isolated waypoint generation.	The source supports general process-planning complexity, not every implemented thesis workflow detail.	Ch.1 motivation, Ch.2 state of the art, Ch.5 regrip and feasibility logic.
PL-02	Aomura and Koguchi, Optimized bending sequences of sheet metal bending by robot	Robotic bending sequence and handling	Robot-assisted bending requires optimized bend sequences and workpiece handling decisions.	I learned that bend order and robot handling strongly affect whether a bending process can be executed automatically.	This justified treating reorientation and handling as part of the automated planning problem.	Specific algorithms in the paper are not directly copied; they provide background for the need for automation.	Ch.1 problem statement, Ch.2 robotic bending background, Ch.4 concept evaluation.
PL-03	Pan et al., Recent progress on programming methods for industrial robots	Robot programming methods	Manual programming, lead-through, offline programming, and automatic programming each have different effort, flexibility, and validation trade-offs.	I learned that reducing robot-programming effort requires more than generating poses; it requires a programming method matched to task complexity.	This shaped the comparison between manual drag&bot programming, automated generation, and CAD/OLP concepts.	The paper is broad; it supports programming-method context but not detailed implementation choices.	Ch.1 motivation, Ch.2 programming methods, Ch.4 concept comparison.
PL-04	Neto, Off-line programming and simulation from CAD drawings: robot-assisted sheet metal bending	CAD-based OLP for bending	Simulation and CAD-based OLP can support robot-assisted sheet-metal bending, but still need correct process and motion generation.	I learned that OLP is useful but does not automatically remove all engineering effort for task-specific bending workflows.	This helped position the thesis contribution between manual programming and full CAD-based automatic OLP.	The thesis does not implement full CAD-based OLP; the paper supports the alternative concept and background.	Ch.2 OLP background, Ch.4 Concept C discussion.
PL-05	Lozano-Perez, Robot Programming	Task-level robot programming	Task-level programming separates user intent from low-level robot commands.	I learned that automatic program generation should be described as a structured translation from task-level input to executable robot actions.	This influenced the thesis language around automatic robot program generation and modular planning layers.	The paper is foundational and conceptual; detailed modern software architecture is thesis-specific.	Ch.2 task-level programming, Ch.5 layered architecture.
PL-06	Pedersen/Kruger et al., Robot skills for manufacturing	Robot skills and reusable modules	Robot skills package reusable task knowledge into modules that can be composed for manufacturing tasks.	I learned that modularity is not only a software convenience; it is a practical way to make robot programming reusable and understandable.	This supported the module-based architecture for orientation, grip planning, regrip, communication, and validation.	The exact modules in this thesis are implementation-specific, not taken directly from the paper.	Ch.2 robot skills, Ch.5 module overview.
PL-07	Bohg et al., Data-driven grasp synthesis: A survey	Grasp planning	Grasp selection depends on object geometry, contact properties, constraints, and task context.	I learned that a valid grip is not simply a point on a surface; it must satisfy geometric and task-specific constraints.	This shaped the grip planner: edge clearance, hole exclusion, cup spacing, and force validation are all considered.	The paper is broad and includes data-driven methods; the thesis uses deterministic rule-based planning.	Ch.2 grasp planning, Ch.5 grip candidate search.
PL-08	Wan and Harada, Regrasp planning using 10,000s of grasps	Regrip and regrasp planning	Regrasp planning can be represented as search over possible grasps, placements, and feasible transitions.	I learned that regripping is naturally a planning problem connecting grasp feasibility, intermediate placement, and reachability.	This supported the thesis decision to implement automatic regrip planning instead of fixed manual regrip steps.	The paper uses a large-grasp planning approach; the thesis uses a simpler deterministic strategy suitable for the selected cell.	Ch.2 regrasp background, Ch.5 regrip planning.
PL-09	Gabriel et al., Modeling of vacuum grippers for energy efficient vacuum-based handling	Vacuum gripping	Vacuum gripper performance depends on pressure difference, suction area, leakage, contact quality, deformation, and dynamic loading.	I learned that suction gripping must be evaluated physically, not only geometrically.	This directly influenced the adapted conservative vacuum force model and the exclusion of unsuitable contact regions.	The thesis model is simplified and conservative; it should be described as adapted from principles, not as an exact reproduction.	Ch.2 vacuum gripping, Ch.5 vacuum holding force validation.
PL-10	Schmalz vacuum handling source	Vacuum force calculation practice	Practical vacuum design uses pressure, area, safety factors, and load-case thinking.	I learned that engineering calculations often require conservative assumptions because real contact, leakage, and acceleration vary.	This supported the safety-factor-based feasibility check used for suction cup selection.	The source is practical/technical guidance; exact product-specific values must come from selected hardware data.	Ch.5 vacuum equations and feasibility criterion.
PL-11	Craig, Introduction to Robotics	Robot kinematics and frames	Robot motion is described through joints, frames, end-effector pose, workspace, and kinematic transformations.	I learned that every generated target must be referenced consistently to the robot, tool, and world frames.	This supported the explanation of TCP, pose, DOF, and workspace concepts.	The book supports fundamentals, not thesis-specific threshold values or workflow rules.	Ch.2 robotics fundamentals, Ch.5 TCP and pose handling.
PL-12	Lynch and Park, Modern Robotics	Modern robotics, rotations, kinematics	Rotation representations, transformation matrices, inverse kinematics, joint limits, and singularities are core to robot motion feasibility.	I learned that orientation convention must be stated clearly because Euler-angle extraction depends on the selected rotation order.	This influenced the ZYX Euler convention, orientation extraction, and reachability/singularity discussion.	The source supports mathematical foundations; implementation thresholds remain thesis choices.	Ch.5 orientation equations, trajectory and feasibility sections.
PL-13	Siciliano et al., Robotics: Modelling, Planning and Control	Robotics modelling and planning	Robotics systems require modelling of kinematics, workspace, planning, and control constraints.	I learned how to connect general robot modelling concepts with the practical constraints of a press-brake cell.	This supported the general explanation of pose acquisition, workspace, kinematics, and robot programming.	Exact book pages should be recorded if the examiner asks for page-level verification.	Ch.2, Ch.4, Ch.5 robotics fundamentals.
PL-14	Quigley et al., ROS: an Open-Source Robot Operating System	ROS middleware	ROS provides a modular open-source robotics middleware with communication infrastructure.	I learned why middleware separation is important for robotics software integration.	This helped justify communication-layer separation and ROS-related interface assumptions.	The paper supports ROS middleware, not every claim about Ubuntu or drag&bot stability.	Ch.4 and Ch.5 communication context.
PL-15	Coleman et al., MoveIt! case study	Robot motion planning software	MoveIt provides planning, inverse kinematics, collision checking, and robot software integration capabilities.	I learned that constraint-aware motion planning is normally handled by specialized planning frameworks rather than ad hoc code alone.	This corrected the citation use: MoveIt supports planning claims, while Unity/ROS2 docs support interface/visualization claims only.	The thesis does not implement MoveIt directly; it uses the paper as state-of-art context for planning capabilities.	Ch.4 Concept C and planning discussion.
PL-16	Crick et al., rosbridge: ROS for Non-ROS Users	ROS bridge and JSON/socket access	rosbridge exposes ROS functionality to non-ROS clients through JSON/socket communication.	I learned how non-ROS applications can communicate with robot middleware through a bridge layer.	This supported the AnyRobot/WebSocket architecture where Python communicates through a RosBridge-style interface.	drag&bot AnyRobot documentation is still the primary source for exact service names and authentication.	Ch.5 communication architecture.
PL-17	Pimentel and Nickerson, Communicating and Displaying Real-Time Data with WebSocket	WebSocket communication	WebSocket supports persistent bidirectional communication suitable for real-time data exchange.	I learned why repeated HTTP-style communication is less suitable for continuous robot command/state interaction.	This supported the decision to describe a persistent WebSocket connection for runtime communication.	The paper supports WebSocket concepts generally, not drag&bot-specific service behavior.	Ch.5 communication architecture.
PL-18	Tao et al., Digital Twin in Industry / Digital Twin Driven Smart Manufacturing	Digital twin and virtual validation	Digital twins connect physical and virtual systems for monitoring, simulation, and smart manufacturing integration.	I learned that simulation-based validation must clearly state what is virtual, what is physical, and what assumptions connect them.	This improved wording around drag&bot simulation and digital manufacturing trends.	The thesis uses a virtual simulation environment; it should not overclaim a full closed-loop industrial digital twin.	Ch.2 digital twin background, Ch.5 simulation environment.
PL-19	Lechler et al., Virtual commissioning of production systems	Virtual commissioning	Virtual commissioning supports early validation of automation logic before physical commissioning.	I learned that simulation can reduce commissioning risk, but only if model fidelity and assumptions are clear.	This supported the value of testing the robotic bending workflow in a virtual cell.	The source supports virtual commissioning generally; exact drag&bot setup is thesis-specific.	Ch.4 simulation concept evaluation, Ch.5 virtual cell.
PL-20	Kalpakjian and Schmid, Manufacturing Engineering and Technology	Manufacturing fundamentals	Sheet-metal forming and bending depend on material, geometry, tooling, and process conditions.	I learned that manufacturing fundamentals are best supported by stable textbook sources rather than only web articles.	This helped strengthen basic press-brake and sheet-metal bending background.	The textbook supports process fundamentals, not robot-specific automation details.	Ch.2 press-brake and bending fundamentals.
PL-21	Pahl and Beitz, Engineering Design: A Systematic Approach	Engineering design methodology	Systematic design uses requirements, concept generation, evaluation, and decision-making.	I learned that concept development should be traceable from requirements to selected solution.	This supported the structured Concept A/B/C comparison and weighted sum model.	The source supports methodology; the scoring values are thesis decisions.	Ch.3 methodology, Ch.4 concept decision.
PL-22	Gasparetto et al., Trajectory Planning in Robotics	Trajectory planning	Smooth robot motion requires attention to velocity, acceleration, jerk, interpolation, and feasibility.	I learned that trajectory generation must be described as a controlled motion-planning stage, not only as a list of waypoints.	This supported the trajectory chapter and the use of smooth interpolation profiles.	The source supports general trajectory planning; exact waypoint reduction and thresholds are implementation choices.	Ch.5 trajectory generation.
PL-23	Flash and Hogan, Minimum-jerk model	Minimum-jerk motion	The minimum-jerk polynomial produces smooth motion with zero velocity and acceleration boundary assumptions.	I learned that named mathematical profiles require correct boundary-condition explanation and citation.	This supported the minimum-jerk scaling function in the trajectory section.	The source comes from human motor control; its use in robot trajectory generation should be linked through smooth-motion rationale and robotics trajectory literature.	Ch.5 minimum-jerk equation.
PL-24	Shoemake, Animating Rotation with Quaternion Curves	SLERP and quaternion rotation	Spherical linear interpolation provides smooth interpolation between orientations in quaternion space.	I learned that orientation interpolation should avoid naive Euler-angle interpolation where possible.	This supported the use of SLERP-style orientation interpolation in trajectory generation.	Page-level evidence may need manual recording from scanned source if required.	Ch.5 orientation interpolation.
PL-25	Cadena et al., Past, Present, and Future of SLAM	SLAM and mapping	SLAM concerns simultaneous localization and mapping for perception-based environment understanding.	I learned to separate SLAM/mapping claims from vision-to-control or grasp-learning claims.	This helped correct perception-related citations so Levine-type visuomotor claims were not used for SLAM mapping.	The paper supports mapping/perception background, not the thesis implementation, because SLAM is outside the final implemented scope.	Ch.4 perception-based concept discussion.
"""


MASTER_REFLECTION_TSV = r"""Reflection dimension	Master-level expectation	Evidence in this thesis	Critical learning gained	How I would apply it in the next engineering project
Scientific rigor	Claims must be precise, traceable, and supported by original sources.	Citation audit, reference evidence matrix, corrected citations in Ch.1 to Ch.7.	I learned that a correct reference list is not enough; the written claim must match the source statement and scope.	Create a live claim-source table during writing and verify every major claim before chapter review.
Engineering abstraction	A master thesis should show the ability to abstract an industrial problem into requirements, architecture, and validated functions.	Requirements in Ch.3, concept selection in Ch.4, layered implementation in Ch.5.	I learned to separate problem, requirement, concept, architecture, algorithm, and validation levels.	Use a systems-engineering structure from the start: stakeholder need, requirement, design decision, test evidence.
Implementation maturity	The implemented system should be modular, configurable, testable, and explainable.	YAML configuration, module overview, communication layer, validation layer, flow diagrams.	I learned that maintainability must be designed, not repaired at the end.	Define module boundaries, data ownership, and interface contracts before coding large workflows.
Model validity	Engineering models must state assumptions, limits, and source status.	Vacuum model wording, FMEA scoring convention, simulation-environment description.	I learned to distinguish literature equations, adapted conservative models, and own thesis scoring conventions.	For each model, document source, assumptions, calibration status, and valid operating range.
Simulation credibility	Simulation can support validation only when its scope and limits are clear.	drag&bot virtual environment, virtual test cell figure, Ch.6 simulation-based evaluation.	I learned that simulation evidence should not be written as physical proof unless physical measurement is performed.	State what was validated virtually, what remains for physical commissioning, and what assumptions connect the two.
Automation safety	Robot program generation must include checks before execution, not only motion generation.	Pre-execution safety validation, reachability, gripper feasibility, FMEA-style analysis.	I learned that safety and feasibility checks are part of program generation, not optional post-processing.	Place validation gates before every motion or process transition in future automation systems.
User-centered automation	Automation should reduce operator burden while keeping necessary control and clarity.	3D bending viewer, basic/expert mode concept, operator confirmations.	I learned that usability is a technical requirement in industrial automation, not only a visual interface issue.	Test operator workflows early and minimize unnecessary manual input.
Critical self-management	A thesis requires controlled planning, not only technical work.	Lessons learned, submission checklist, citation evidence files, final layout checks.	I learned that final quality depends heavily on documentation, evidence, formatting, and packaging.	Reserve dedicated time for verification, formatting, and deliverables instead of treating them as final-day tasks.
Professional transparency	Use of tools, AI, sources, and assumptions must be declared clearly.	AI declaration, prompt log, source matrix, rewritten unsupported claims.	I learned that transparency protects the credibility of the work and helps the examiner understand the process.	Record tool usage, source limitations, and decisions continuously.
Research-to-practice transfer	The thesis should convert literature learning into a concrete engineering implementation.	Grip planning, regrip strategy, trajectory generation, communication architecture.	I learned to use literature as design guidance, not as decoration for already-written text.	For each paper, record one concrete design consequence or reason why it is only background.
"""


SUBMISSION_TSV = r"""Deliverable item	Recommended filename / location	Status	Comment
Lessons learned Excel	950_LeLe/lessons_learned_thesis.xlsx	Created	This workbook.
Thesis PDF	900_upload_thesis/main.pdf	To prepare	Copy final compiled PDF during submission packaging.
Colloquium presentation	<submission folder>/presentation.pdf or .pptx	To prepare	Submit the final presentation to the professor.
Raw data and evidence	<submission folder>/raw_data or supporting files	To prepare	Include measurement, validation, and supporting files where required.
AI prompt log	Appendix / electronic submission	Already prepared / check	Keep machine-readable text, not screenshots.
Citation evidence matrix	AutoProgram_PressBrake_Thesis/citation_claim_evidence_matrix.xlsx	Created	Useful supporting file, even if not mandatory.
Reference PDFs	reference Papers folder	Created / check	Ensure only allowed and relevant source files are submitted.
"""


SHEETS = [
    ("Guideline Summary", GUIDELINE_TSV),
    ("Lessons Learned", LESSONS_TSV),
    ("Literature Learning", LITERATURE_TSV),
    ("Master Reflection", MASTER_REFLECTION_TSV),
    ("Keep Practices", KEEP_TSV),
    ("Improvement Plan", IMPROVEMENT_TSV),
    ("Skills Developed", SKILLS_TSV),
    ("Submission Checklist", SUBMISSION_TSV),
]


def parse_tsv(text: str) -> tuple[list[str], list[list[str]]]:
    rows = list(csv.reader(StringIO(text.strip()), delimiter="\t"))
    return rows[0], rows[1:]


def col_letter(n: int) -> str:
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out


def esc(value: object) -> str:
    return html.escape(str(value), quote=False)


def style_for(sheet: str, col: int, value: str) -> int:
    text = value.lower()
    if sheet == "Literature Learning":
        if col == 7:
            return 4
        if col in (5, 6, 8):
            return 3
    if sheet == "Master Reflection":
        if col in (4, 5):
            return 3
    if sheet == "Lessons Learned" and col == 9:
        if "high" in text:
            return 5
        if "medium" in text:
            return 4
    if sheet == "Lessons Learned" and col == 10:
        if "improve" in text and "keep" not in text:
            return 5
        if "keep and improve" in text:
            return 4
        if "keep" in text:
            return 3
    if sheet == "Improvement Plan" and col == 6:
        if "high" in text:
            return 5
        if "medium" in text:
            return 4
    if sheet == "Skills Developed" and col == 5:
        if "high" in text:
            return 3
        if "medium" in text:
            return 4
    if sheet == "Submission Checklist" and col == 3:
        if "created" in text or "prepared" in text:
            return 3
        if "to prepare" in text or "check" in text:
            return 4
    return 2


def width_for(header: str) -> int:
    h = header.lower()
    if h in ("no.", "status", "priority", "confidence", "category"):
        return 16
    if any(token in h for token in ("reference", "paper", "source")):
        return 36
    if any(token in h for token in ("what", "learned", "action", "comment", "benefit", "problem", "root", "evidence")):
        return 44
    if any(token in h for token in ("activity", "situation", "phase", "area", "requirement", "location")):
        return 32
    return 24


def row_height(sheet_name: str, row_index: int) -> int:
    if row_index == 1:
        return 34
    if sheet_name == "Literature Learning":
        return 112
    if sheet_name == "Master Reflection":
        return 104
    if sheet_name == "Lessons Learned":
        return 88
    return 78


def worksheet_xml(sheet_name: str, headers: list[str], rows: list[list[str]]) -> str:
    all_rows = [headers] + rows
    max_col = len(headers)
    max_row = len(all_rows)
    dim = f"A1:{col_letter(max_col)}{max_row}"
    cols = "".join(
        f'<col min="{idx}" max="{idx}" width="{width_for(header)}" customWidth="1"/>'
        for idx, header in enumerate(headers, 1)
    )

    xml = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
        f'<dimension ref="{dim}"/>',
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
        'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>',
        '<sheetFormatPr defaultRowHeight="18"/>',
        f"<cols>{cols}</cols>",
        "<sheetData>",
    ]

    for r_idx, row in enumerate(all_rows, 1):
        height = row_height(sheet_name, r_idx)
        xml.append(f'<row r="{r_idx}" ht="{height}" customHeight="1">')
        for c_idx, value in enumerate(row, 1):
            cell = f"{col_letter(c_idx)}{r_idx}"
            style = 1 if r_idx == 1 else style_for(sheet_name, c_idx, value)
            xml.append(f'<c r="{cell}" s="{style}" t="inlineStr"><is><t>{esc(value)}</t></is></c>')
        xml.append("</row>")

    xml.extend(
        [
            "</sheetData>",
            f'<autoFilter ref="{dim}"/>',
            '<pageMargins left="0.5" right="0.5" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>',
            '<pageSetup orientation="landscape"/>',
            "</worksheet>",
        ]
    )
    return "".join(xml)


def build_xlsx(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    parsed = [(name, *parse_tsv(tsv)) for name, tsv in SHEETS]
    workbook_sheets = []
    rels = []
    for i, (name, _headers, _rows) in enumerate(parsed, 1):
        workbook_sheets.append(f'<sheet name="{esc(name)}" sheetId="{i}" r:id="rId{i}"/>')
        rels.append(
            f'<Relationship Id="rId{i}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{i}.xml"/>'
        )
    rels.append(
        f'<Relationship Id="rId{len(parsed) + 1}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    )

    content = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for i in range(1, len(parsed) + 1):
        content.append(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content.extend(
        [
            '<Override PartName="/docProps/core.xml" '
            'ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
            '<Override PartName="/docProps/app.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
            "</Types>",
        ]
    )

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="2"><font><sz val="10"/><name val="Calibri"/></font><font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font></fonts>
<fills count="6"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFE2F0D9"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFF4CCCC"/></patternFill></fill></fills>
<borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border><border><left style="thin"><color rgb="FFD9E2F3"/></left><right style="thin"><color rgb="FFD9E2F3"/></right><top style="thin"><color rgb="FFD9E2F3"/></top><bottom style="thin"><color rgb="FFD9E2F3"/></bottom><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="6"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf><xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="0" fillId="5" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf></cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>"""

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        "<sheets>"
        + "".join(workbook_sheets)
        + "</sheets></workbook>"
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(rels)
        + "</Relationships>"
    )
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" '
        'Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
        'Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" '
        'Target="docProps/app.xml"/>'
        "</Relationships>"
    )
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<dc:title>Lessons Learned Thesis</dc:title>"
        "<dc:creator>Codex</dc:creator>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{CREATED}T00:00:00Z</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{CREATED}T00:00:00Z</dcterms:modified>'
        "</cp:coreProperties>"
    )
    app = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>Codex generated XLSX</Application>"
        "</Properties>"
    )

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", "".join(content))
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("docProps/core.xml", core)
        archive.writestr("docProps/app.xml", app)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        archive.writestr("xl/styles.xml", styles)
        for i, (name, headers, rows) in enumerate(parsed, 1):
            archive.writestr(f"xl/worksheets/sheet{i}.xml", worksheet_xml(name, headers, rows))


if __name__ == "__main__":
    for candidate in (OUT, ALT_OUT, CLEAN_OUT):
        try:
            build_xlsx(candidate)
            written = candidate
            break
        except PermissionError:
            continue
    else:
        raise PermissionError("All configured lessons-learned workbook paths are locked.")
    if written != OUT:
        print("Earlier workbook path was locked; wrote alternate file instead.")
    print(f"Wrote {written}")
    for name, tsv in SHEETS:
        _headers, rows = parse_tsv(tsv)
        print(f"{name}: {len(rows)} rows")
