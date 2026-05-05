from __future__ import annotations

import csv
import html
import zipfile
from io import StringIO
from pathlib import Path


OUT = Path("citation_claim_evidence_matrix.xlsx")
CREATED = "2026-04-27"


CLAIMS_TSV = r"""ID	Thesis location	Thesis claim / citation use	Citation key(s)	Source PDF / URL	Source section / PDF page	Evidence from source (paraphrased)	Claim match	How it helps the thesis	What I learned from the paper/source	Action needed	Confidence
C001	Ch.1 line 9	Sheet metal bending is a common manufacturing process, and bending sequence, tooling and handling are interconnected.	Gupta1998SheetMetalBending; Aomura2002RoboticBending	Gupta1998SheetMetalBending.pdf; Aomura2002RoboticBending.pdf	Gupta PDF pp. 1, 4-6; Aomura PDF pp. 1-4	Gupta discusses bending process planning with tooling, grasping and robot-motion constraints. Aomura discusses bend sequence optimization and robotic sheet handling.	OK	Justifies the manufacturing background and why robotic bending needs integrated planning.	Bending automation is a coupled process, grasping and motion-planning problem.	Keep citation.	High
C002	Ch.1 lines 11, 22, 24	Robotic bending reduces human effort but requires grip, repositioning, reachability and bend-sequence planning.	Gupta1998SheetMetalBending; Aomura2002RoboticBending	Gupta1998SheetMetalBending.pdf; Aomura2002RoboticBending.pdf	Gupta PDF pp. 1, 4-6; Aomura PDF pp. 1-4	Both sources support robotic bending, grasp/reposition planning and geometry changes affecting process feasibility.	OK	Supports the problem statement and motivation for automatic planning.	Part variation propagates into grasp, reach and sequence decisions.	Keep citation.	High
C003	Ch.1 lines 13-20	Manual/OLP robot programming requires considerable effort and adaptation for new parts.	Pan2012Survey; Neto2013OLP	Pan2012Survey.pdf; Neto2013OLP.pdf	Pan PDF pp. 1-3, 7; Neto PDF pp. 1-4	Pan surveys programming effort and OLP methods. Neto presents CAD-based OLP for robot-assisted sheet-metal bending.	OK	Supports the thesis goal of reducing programming effort.	OLP helps, but still requires engineering work for paths and process logic.	Keep citation.	High
C004	Ch.1 line 43	UR5e has 6 DOF, 850 mm reach, 5 kg payload and high repeatability; used as simulation reference manipulator.	universalrobots_ur5e	Official UR5e technical specification web page	Official web specification page	The UR specification verifies DOF, reach, payload and repeatability. Simulation-model use is the thesis setup, not a UR claim.	OK after wording	Supports hardware-model choice without overclaiming modelling reliability.	Manufacturer specs should support measurable facts only.	Keep current wording.	Medium
C005	Ch.2 line 7	Industrial robots are automatically controlled, reprogrammable and multipurpose manipulators with three or more axes.	ISO8373	ISO8373.pdf	PDF p. 8; vocabulary definition	ISO 8373 defines industrial robots using reprogrammable, multipurpose manipulator wording and programmable axes.	OK	Provides the formal definition used in the state of the art.	Use the correct standard for definitions; ISO 9283 would be the wrong source.	Keep citation.	High
C006	Ch.2 line 9	Robot joints provide DOF to position/orient the end-effector/TCP in workspace.	craig2005robotics	craig2005robotics.pdf	PDF pp. 6-13 found by keyword scan	Craig supports joints, degrees of freedom, end-effector frames, kinematics and workspace.	OK	Supports robotics fundamentals used throughout the thesis.	TCP and pose definitions must be consistent because all generated targets depend on them.	Keep citation.	High
C007	Ch.2 line 11	Robot programming ranges from low-level pose/program specification to higher-level task/skill programming.	Pan2012Survey; Kruger2019	Pan2012Survey.pdf; Kruger2019.pdf	Pan PDF pp. 1-3, 7; Kruger PDF pp. 1-4	Pan surveys programming approaches; Kruger/Pedersen discusses robot skills and reusable task-level modules.	OK	Positions the thesis between manual programming and automatic program generation.	Skill/task abstraction reduces low-level programming but still needs feasibility validation.	Keep citation.	High
C008	Ch.2 line 17	Press-brake bending process fundamentals: sheet, punch, die, material/tooling/force dependence.	Fabricator_RoboticPressBrake_2023	Web article; no local PDF	No local PDF; web-only/not fully locally verified	The claim is standard manufacturing knowledge and is better supported by Kalpakjian locally.	Not locally verified	Process background should rely on a stable source.	Textbook sources are stronger than web articles for basic manufacturing fundamentals.	Replace or supplement with KalpakjianManufacturing2014.	Low
C009	Ch.2 line 19	Sheet-metal bending is widely used for simple and complex fabricated parts.	KalpakjianManufacturing2014	KalpakjianManufacturing2014.pdf	PDF pp. 10-15 found by bending/tooling scan	Kalpakjian covers manufacturing processes including sheet-metal forming and bending fundamentals.	OK	Supports manufacturing process background with a textbook source.	Use textbooks for core process fundamentals.	Keep citation; optionally also cite at Ch.2 line 17.	Medium
C010	Ch.2 lines 30, 35, 142, 151	Automated press-brake cells need handling, support, reorientation, regrip and integrated process/motion planning.	Aomura2002RoboticBending; Gupta1998SheetMetalBending	Aomura2002RoboticBending.pdf; Gupta1998SheetMetalBending.pdf	Aomura PDF pp. 1-4; Gupta PDF pp. 1, 4-6	Aomura supports robot handling and bend sequences. Gupta supports process planning, tooling, grasp positions, robot motion and kinematic/collision constraints.	OK	Supports the core state-of-the-art argument for integrated planning.	Robotic bending must coordinate process planning and manipulation constraints.	Keep citation.	High
C011	Ch.2 lines 44, 67, 81, 190; Ch.4 line 136	Manual programming and OLP/simulation: programming effort, pre-execution validation and reduced trial-and-error.	Pan2012Survey; Siciliano2016Robotics	Pan2012Survey.pdf; Siciliano2016Robotics.pdf	Pan PDF pp. 1-3, 7; Siciliano keyword hits pp. 6-7, 14, 38	Pan supports programming and OLP claims. Siciliano supports robotics/programming fundamentals.	OK	Supports baseline manual programming and OLP comparison.	OLP reduces shop-floor interruption but does not solve all planning decisions automatically.	Keep citation.	High
C012	Ch.2 line 92	RoboDK is an offline programming/simulation tool.	RoboDK2024	RoboDK web page	Web page checked; no local PDF	Product page supports RoboDK as simulation and offline programming software.	OK for product capability	Provides an industrial OLP example.	Product pages support capability, but critique needs literature or thesis analysis.	Keep product citation; support critique separately if needed.	Medium
C013	Ch.2 line 100	Digital twin links virtual and physical manufacturing systems for monitoring/validation/cyber-physical integration.	Tao2019	Tao2019 book not local; Tao2021DigitalTwin.pdf is local	Tao2021DigitalTwin PDF pp. 1-4 supports this topic	The available Tao digital-twin paper supports smart manufacturing and cyber-physical/virtual-physical integration; the cited Tao 2019 book is not locally verified.	Not locally verified for Tao2019	Supports digital-twin motivation in state of the art.	Use the available verified paper unless the book is supplied.	Replace Tao2019 with Tao2021DigitalTwin or provide Tao 2019 book.	Medium
C014	Ch.2 line 115	Task-level robot programming separates task intent from low-level robot motion.	LozanoPerez1983	LozanoPerez1983.pdf	PDF pp. 1-4	Lozano-Perez discusses robot-programming abstractions and task-level programming concepts.	OK	Supports the theoretical basis for automatic task/program generation.	Task-level programming is a long-standing way to reduce explicit motion coding.	Keep citation.	High
C015	Ch.2 line 117	Robot skills/motion primitives provide reusable modules for task-level programming.	Kruger2019	Kruger2019.pdf	PDF pp. 1-4	The paper discusses robot skills for manufacturing, reusable modules and non-expert/task-level programming.	OK	Supports modular system design and reusable planning components.	Skills bridge low-level robot commands and user-level tasks.	Keep citation.	High
C016	Ch.2 line 122	Rule/constraint-based planning executes robot behavior using predefined rules and feasibility checks.	Pan2012Survey	Pan2012Survey.pdf	PDF pp. 1-3, 7	Pan supports robot programming and OLP/planning approaches, but the exact broad rule-based claim is a synthesis.	Partly OK	Provides background for rule-based automatic generation.	This claim should be worded as thesis analysis or supported by an additional rule-based planning source.	Consider adding stronger rule-based planning source.	Medium
C017	Ch.2 line 126; Ch.2 line 160	Grasp planning considers object geometry, contact, task constraints and integrated manipulation feasibility.	bohg2014data	bohg2014data.pdf	PDF pp. 1-4	Bohg et al. discuss grasp synthesis with object geometry, contact, constraints and task context.	OK	Supports geometry- and constraint-based grip selection.	Grasp quality cannot be judged only from object geometry; task context matters.	Keep citation.	High
C018	Ch.2 line 149	Regrip planning must consider grasp stability, reachability and intermediate placements.	wan2017regrasp	wan2017regrasp.pdf	PDF pp. 1-4	Wan and Harada discuss regrasp planning using many grasps, stable placements, search and feasibility/reachability checks.	OK	Supports the thesis regrip-planning module.	Regrasping can be represented as a planning/search problem over grasps and placements.	Keep citation.	High
C019	Ch.2 line 158; Ch.4 line 88; Ch.5 line 486	Vacuum gripper performance depends on pressure difference, suction area, seal/contact, holding force and dynamic loading.	VacuumGripperModeling; vacuum_handling_standard	VacuumGripperModeling.pdf; vacuum_handling_standard.pdf	VacuumGripperModeling PDF pp. 1-4 and model Eq. 1/2 section; Schmalz searchable text limited	Gabriel et al. support holding force, pressure difference, suction area, safety margin, gripper-object interaction and dynamic loading. Schmalz supports practical force/safety-factor principles.	OK after wording	Supports the adapted conservative vacuum feasibility model.	Vacuum design is conservative because leakage, seal quality and dynamic loading are uncertain.	Keep current adapted-model wording.	High
C020	Ch.2 line 167	Classical trajectory generation provides foundations for smooth continuous robot motion.	Biagiotti2008Trajectory; Gupta1998SheetMetalBending	Biagiotti book not local; Gasparetto2012Trajectory.pdf local alternative	Gasparetto PDF pp. 1-4 and minimum-jerk section	Gasparetto defines trajectory planning and discusses smooth trajectories, acceleration continuity and jerk limitation. Biagiotti book was not locally verified.	Not locally verified for Biagiotti	Supports trajectory-generation background.	The available Gasparetto survey is enough for the general trajectory planning claim.	Replace/supplement Biagiotti2008Trajectory with Gasparetto2012Trajectory.	Medium
C021	Ch.2 line 197; Ch.5 line 217	drag&bot/AnyRobot provides a WebSocket/RosBridge interface for robot-related operations.	dragandbot_anyrobot_2025	dragandbot_anyrobot_2025.pdf	PDF pp. 1, 3-5	AnyRobot documentation describes a WebSocket-based protocol using RosBridge to access robot operations and IO services.	OK for interface	Supports the implemented runtime communication architecture.	AnyRobot strongly supports communication-interface claims, but not all GUI/workflow claims.	Keep for WebSocket/RosBridge/API claims.	High
C022	Ch.4 line 8	Concept development compares solution principles against requirements before implementation.	Pahl2007EngineeringDesign	Pahl2007EngineeringDesign.pdf	PDF pp. 6, 10-12 found by concept/evaluation scan	Pahl and Beitz describe systematic engineering design, conceptual design, solution principles and evaluation.	OK	Supports the methodology for concept generation and selection.	Structured concept evaluation reduces arbitrary design choices.	Keep citation.	High
C023	Ch.4 line 86	AnyRobot WebSocket communication enables execution-system integration; MDE source used for planning/execution separation.	dragandbot_anyrobot_2025; Thramboulidis2013MDE	dragandbot_anyrobot_2025.pdf; no Thramboulidis local PDF	drag&bot PDF pp. 1, 3-5; Thramboulidis not local	drag&bot supports the interface part. The MDE survey was not locally verified and is not necessary for the thesis-specific architecture claim.	Partly OK / Problem	Identifies a citation that should be cleaned before final submission.	Do not cite a missing paper for a thesis architecture choice.	Remove Thramboulidis citation or provide/verify PDF.	Medium
C024	Ch.4 line 90	Opposite-side bending uses a structured flipping and repositioning workflow.	Gupta1998SheetMetalBending	Gupta1998SheetMetalBending.pdf	PDF pp. 1, 4-6	Gupta supports regrip/repositioning and process planning generally, but not the exact thesis flip workflow.	Partly OK	Supports general regrip/repositioning context.	The exact implemented flip sequence should be presented as thesis design.	Phrase as thesis design; keep Gupta only for general context.	Medium
C025	Ch.4 lines 136, 153	Simulation/OLP enables early validation and depends on accurate digital/kinematic models.	Pan2012Survey; Lechler2019VirtualCommissioning; Siciliano2016Robotics	Pan2012Survey.pdf; Lechler2019VirtualCommissioning.pdf; Siciliano2016Robotics.pdf	Pan PDF pp. 1-3, 7; Lechler PDF pp. 1-4; Siciliano robotics fundamentals	Pan supports OLP/simulation validation; Lechler supports virtual commissioning and early validation; robotics text supports kinematic model dependence.	OK	Supports comparison of simulation-heavy concepts and risks.	Simulation reduces commissioning effort only when model fidelity is sufficient.	Keep citation.	High
C026	Ch.4 lines 138, 160	ROS/MoveIt provides planning, IK and constraint-aware motion; Unity provides ROS2 simulation/interface.	quigley2009ros; Coleman2014MoveIt; UnityROS2Docs	quigley2009ros.pdf; Coleman2014MoveIt.pdf; Unity docs web	Quigley PDF pp. 1-4; Coleman PDF pp. 1, 3-5; Unity docs web	ROS supports middleware; MoveIt supports planning, IK and collision-aware robotics; Unity docs support ROS2-Unity communication/interface.	OK after fix	Correctly separates planning evidence from visualization/interface evidence.	Unity docs should not support motion planning; MoveIt is the correct source.	Keep current wording.	High
C027	Ch.4 line 140	Perception modules can support mapping and scene reconstruction.	Cadena2016SLAM	Cadena2016SLAM.pdf	PDF pp. 1-4	Cadena et al. review SLAM, simultaneous localization and mapping, and mapping/perception foundations.	OK	Supports perception-based alternative concept while keeping it outside scope.	SLAM is relevant for mapping, not for generic vision-to-control claims.	Keep citation.	High
C028	Ch.4 line 191	Regripping and opposite-side bending are complex operations usually handled manually or through predefined operations.	Aomura2002RoboticBending; Gupta1998SheetMetalBending	Aomura2002RoboticBending.pdf; Gupta1998SheetMetalBending.pdf	Aomura PDF pp. 1-4; Gupta PDF pp. 1, 4-6	Both papers support bending sequence, regrip and repositioning complexity in robotic sheet-metal bending.	OK	Supports evaluation criterion for complex-operation automation.	Automating regrip has value because it is a major source of manual programming effort.	Keep citation.	High
C029	Ch.5 line 15	Ubuntu is used due to ROS compatibility and stable drag&bot integration.	quigley2009ros	quigley2009ros.pdf	PDF pp. 1-4	Quigley supports ROS as an open-source robot operating system/middleware, but not Ubuntu platform choice or drag&bot stability.	Partly OK	Highlights a sentence where citation coverage is too broad.	A citation may support ROS compatibility but not platform/vendor-integration claims.	Rewrite as thesis implementation choice or add Ubuntu/drag&bot documentation.	Medium
C030	Ch.5 line 103	Persistent WebSocket communication supports continuous command/state exchange and lower overhead than repeated HTTP.	Pimentel2012; Crick2017	Pimentel2012.pdf; Crick2017.pdf	Pimentel PDF pp. 1-4; Crick PDF pp. 1-4	Pimentel discusses WebSocket for real-time data communication; Crick describes rosbridge JSON/socket access to ROS for non-ROS users.	OK	Supports the communication-layer design.	WebSocket is appropriate for repeated runtime state/command exchange.	Keep citation.	High
C031	Ch.5 lines 114-129	ROSAuth/SHA-512 equation and Python listing follow the drag&bot AnyRobot specification.	dragandbot_anyrobot_2025	dragandbot_anyrobot_2025.pdf	PDF pp. 4-5; ROSAuth/hash/auth-service example	The document shows hashing the secret and an auth service with fields op, client, dest, end, level, mac, rand and t. The thesis equation/listing currently use different fields/order.	Problem	Main remaining equation/citation mismatch.	Implementation examples must match vendor documentation or be labelled illustrative/thesis-specific.	Fix equation/listing/caption to match documented fields or state illustrative.	High
C032	Ch.5 line 223	UR5e 6 DOF, reach and payload are sufficient for simulated workpieces.	universalrobots_ur5e	Official UR5e technical specification web page	Web spec page	Official UR data supports 6 DOF, 850 mm reach, 5 kg payload and repeatability.	OK after wording	Supports manipulator model selection without unsupported qualitative claims.	Use manufacturer specs only for measurable facts.	Keep current wording.	Medium
C033	Ch.5 lines 239, 277, 328, 551, 639	Pose acquisition, reachability, workspace, joint limits and singularity constraints are core robotics concepts.	Siciliano2016Robotics; lynch2017modern	Siciliano2016Robotics.pdf; lynch2017modern.pdf	Siciliano keyword hits pp. 6-7, 14, 38; Lynch pp. 3-4, 7, 9 and appendix B.1	Robotics sources support coordinate frames, workspace, kinematics, joint limits, IK and singularities.	OK / Partly OK for design-specific preferences	Supports validation and reachability reasoning.	Textbooks support general constraints; thresholds and two-stage transfer choices are thesis design decisions.	Keep citations; phrase exact choices as implementation decisions.	High
C034	Ch.5 line 361	Rotation matrix is decomposed into ZYX Euler angles using stated composition/extraction equations.	Siciliano2016Robotics; lynch2017modern	Siciliano2016Robotics.pdf; lynch2017modern.pdf	Lynch appendix B.1, text pp. 575-577; Siciliano orientation sections	Lynch gives ZYX Euler composition and extraction using atan2 relations; Siciliano supports rotation/Euler representations.	OK	Supports mathematical orientation convention used in report/code.	Euler extraction depends on convention; the thesis must state ZYX clearly.	Keep citation.	High
C035	Ch.5 lines 486-508	Vacuum holding force model estimates available force and compares it with safety-factor-weighted load.	vacuum_handling_standard; VacuumGripperModeling	vacuum_handling_standard.pdf; VacuumGripperModeling.pdf	VacuumGripperModeling PDF pp. 1-4 and Eq. 1/2 section; Schmalz supports practical force principles	Sources support pressure difference, suction area, number of cups, efficiency/safety factors and dynamic loading. Thesis formula is adapted.	OK after fix	Supports grip feasibility filtering.	Conservative adapted models are acceptable if clearly labelled and linked to standard principles.	Keep current wording.	High
C036	Ch.5 line 689	SLERP provides smooth constant-speed rotation in quaternion space.	Shoemake1985Slerp	Shoemake1985Slerp.pdf	Scanned/visual PDF; exact page pending	Shoemake introduced quaternion curves and spherical linear interpolation for rotations; visual audit confirmed relevance.	OK	Supports orientation interpolation choice.	Quaternions avoid many Euler interpolation problems; SLERP is the classical rotation interpolation method.	Keep; optionally manually record printed page.	Medium
C037	Ch.5 line 698	Minimum-jerk polynomial gives zero velocity/acceleration at motion boundaries and smooth robot motion.	Flash1985MinimumJerk; Gasparetto2012Trajectory	Flash1985MinimumJerk.pdf; Gasparetto2012Trajectory.pdf	Flash PDF pp. 2, 4, 11-12; Gasparetto PDF pp. 1-4 and minimum-jerk section	Flash supports fifth-order minimum-jerk with zero velocity/acceleration boundaries; Gasparetto supports jerk-limited smooth robot trajectory planning.	OK	Supports waypoint timing profile and smooth motion rationale.	Minimum-jerk is a practical way to reduce dynamic excitation.	Keep citation.	High
C038	Ch.5 lines 746-755	FMEA RPN = S x O x D uses a simplified thesis scoring convention.	No external citation used	Thesis implementation convention	Ch.5 System Reliability section	Text now states RPN is an internal qualitative FMEA-style scoring convention used in this thesis.	OK after rewrite	Avoids false standards citation while documenting risk ranking.	If no FMEA standard is available, frame method as internal scoring convention.	No citation required unless formal FMEA standard is required.	High
"""


EQUATIONS_TSV = r"""Equation ID	Location	Formula / method	Citation need	Current source	Evidence / reason	Status	Action
eq:sha512-mac	Ch.5 lines 116-119	MAC = SHA-512(secret || id_string || dest || nonce || t || level)	Required because it claims vendor authentication formula	dragandbot_anyrobot_2025.pdf pp. 4-5	Source shows ROSAuth fields op, client, dest, end, level, mac, rand, t and hashed secret; current equation/listing do not match.	Problem	Fix to match source or label as illustrative thesis-specific implementation.
eq:fixture-position-deviation	Ch.5 lines 286-289	Euclidean 3D distance	No external citation strictly required	Basic mathematical definition	Common distance metric used as thesis implementation threshold.	OK	No action.
eq:fixture-orientation-deviation	Ch.5 lines 293-296	Maximum absolute Euler-angle deviation	No external citation strictly required	Thesis implementation rule	Max-deviation criterion and thresholds are thesis design choices.	OK	No action.
eq:zone-based-opposite-orientation	Ch.5 lines 335-340	Orientation correction by wrapping RZ/RX and negating RY	No external citation strictly required	Thesis transformation rule; Euler convention supported nearby	Exact rule is system-specific; general Euler convention is cited nearby.	OK	No action.
eq:bend-face-corrected-rotation	Ch.5 lines 355-358	R_new = R_raw * Rz(-d_face)	No external citation strictly required	Thesis reference-face normalization	Matrix multiplication/rotation offset is a system-specific implementation rule.	OK	No action.
eq:euler-rotation-composition	Ch.5 lines 363-365	R = Rz(alpha) Ry(beta) Rx(gamma)	Yes, convention should be cited	Siciliano2016Robotics; lynch2017modern	Lynch appendix B.1 gives ZYX Euler-angle composition; Siciliano supports rotation representations.	OK	No action.
eq:euler-angle-extraction	Ch.5 lines 368-372	RZ/RY/RX from atan2/arcsin matrix entries	Yes, convention should be cited	Siciliano2016Robotics; lynch2017modern	Lynch appendix B.1 gives extraction relations for ZYX Euler angles.	OK	No action.
eq:fallback-opposite-orientation	Ch.5 lines 385-389	Fallback RZ/RX/RY orientation inversion	No external citation strictly required	Thesis fallback rule	Exact fallback is a system-specific feasibility strategy.	OK	No action.
eq:cup-area	Ch.5 lines 481-483	A = pi(d/2)^2	No external citation strictly required	Basic circle area; vacuum model sources nearby	Basic geometry; nearby vacuum citations support the broader model.	OK	No action.
eq:vacuum-force	Ch.5 lines 488-490	F_vacuum = n DeltaP A eta	Yes, model principle should be cited	VacuumGripperModeling; vacuum_handling_standard	Vacuum sources support pressure-difference, suction-area, number-of-cups, efficiency/safety-factor force modelling; thesis says adapted conservative model.	OK after fix	No action.
eq:required-force	Ch.5 lines 497-499	F_required = SF*m*sqrt(a_xy^2+(g+a_z)^2)	Yes, model principle should be cited	VacuumGripperModeling; vacuum_handling_standard	Sources support mass, gravity, acceleration and safety factor load cases; vector resultant is thesis adaptation.	OK after fix	No action.
eq:vacuum-feasibility-criterion	Ch.5 lines 506-508	F_vacuum >= F_required	No separate citation required	Logical feasibility criterion based on previous equations	Direct decision logic after cited force model.	OK	No action.
eq:linear-cartesian-interpolation	Ch.5 lines 682-685	p(lambda) = (1-lambda)p_s + lambda p_t	No external citation strictly required	Basic linear interpolation; trajectory sources nearby	Basic interpolation formula; general trajectory planning context is supported by Gasparetto.	OK	No action.
eq:minimum-jerk-scaling	Ch.5 lines 693-695	s(u)=10u^3-15u^4+6u^5	Yes, named trajectory profile should be cited	Flash1985MinimumJerk; Gasparetto2012Trajectory	Flash supports fifth-order minimum-jerk under zero velocity/acceleration boundaries; Gasparetto supports jerk-limited smooth robot trajectory planning.	OK	No action.
eq:risk-priority-number	Ch.5 lines 750-752	RPN = S x O x D	No external citation needed after rewrite	Thesis scoring convention	Text now states it is a simplified FMEA-style internal qualitative scoring method.	OK after rewrite	No action unless a formal FMEA standard is required.
"""


REFERENCES_TSV = r"""Citation key	Local source / URL	Where used	Evidence pages / section	Verification status	Evidence summary	Main thesis value	Action
Aomura2002RoboticBending	Aomura2002RoboticBending.pdf	Ch.1, Ch.2, Ch.4	PDF pp. 1-4	OK	Robotic sheet-metal bending, bend sequence, grasp/reposition handling.	Bending-specific automation complexity.	Keep.
Gupta1998SheetMetalBending	Gupta1998SheetMetalBending.pdf	Ch.1, Ch.2, Ch.4	PDF pp. 1, 4-6	OK	Automated process planning for bending, tooling, grippers, robot motion and kinematic/collision constraints.	Core source for integrated process/manipulation planning.	Keep.
Pan2012Survey	Pan2012Survey.pdf	Ch.1, Ch.2, Ch.4	PDF pp. 1-3, 7	OK / one Partly OK broad rule-based claim	Robot programming, OLP, manual effort and simulation.	Main programming-method and OLP source.	Keep; consider stronger source for rule-based planning.
Neto2013OLP	Neto2013OLP.pdf	Ch.1, Ch.2	PDF pp. 1-4	OK	CAD/OLP and robot-assisted sheet-metal bending.	CAD-based OLP bending background.	Keep.
ISO8373	ISO8373.pdf	Ch.2	PDF p. 8	OK	Industrial robot vocabulary definition.	Formal definition.	Keep.
craig2005robotics	craig2005robotics.pdf	Ch.2	PDF pp. 6-13 found	OK	DOF, joints, end-effector, pose, workspace and kinematics.	Robotics fundamentals.	Keep.
KalpakjianManufacturing2014	KalpakjianManufacturing2014.pdf	Ch.2	PDF pp. 10-15 found	OK	Sheet-metal bending/forming fundamentals.	Manufacturing process source.	Keep; use also for Ch.2 line 17 if replacing Fabricator.
Fabricator_RoboticPressBrake_2023	Web only; no local PDF	Ch.2	Not locally verified	Not locally verified	Industry article not locally archived.	Industry context only.	Replace/supplement with Kalpakjian for fundamentals.
RoboDK2024	Web only	Ch.2 figure/product	Web page checked earlier	OK for product capability	RoboDK simulation and offline programming software.	Industrial OLP example.	Keep product claims.
Tao2019	Book not local	Ch.2	No local PDF	Not locally verified	Digital twin claim is supported by available Tao2021DigitalTwin paper instead.	Digital twin background.	Replace with Tao2021DigitalTwin or provide book.
Tao2021DigitalTwin	Tao2021DigitalTwin.pdf	Ch.5; recommended for Ch.2	PDF pp. 1-4	OK	Digital twin, smart manufacturing and cyber-physical integration.	Digital manufacturing validation context.	Use for Ch.2 digital twin claim.
LozanoPerez1983	LozanoPerez1983.pdf	Ch.2	PDF pp. 1-4	OK	Task-level robot programming and abstraction.	Program-generation theory.	Keep.
Kruger2019	Kruger2019.pdf	Ch.2	PDF pp. 1-4	OK	Robot skills, reusable modules, task-level programming and non-expert concepts.	Modular task abstraction.	Keep.
bohg2014data	bohg2014data.pdf	Ch.2	PDF pp. 1-4	OK	Grasp synthesis, object geometry, task constraints and contact/stability issues.	Grip planning theory.	Keep.
wan2017regrasp	wan2017regrasp.pdf	Ch.2	PDF pp. 1-4	OK	Regrasp planning using grasps and stable placements with reachability/IK checks.	Regrip planning state of art.	Keep.
VacuumGripperModeling	VacuumGripperModeling.pdf	Ch.2, Ch.4, Ch.5	PDF pp. 1-4; model equations later	OK	Vacuum gripper holding force, pressure difference, suction area, seal/contact and dynamic loading.	Vacuum feasibility model.	Keep.
vacuum_handling_standard	vacuum_handling_standard.pdf	Ch.5	Searchable text limited	OK for practical principle	Practical vacuum force/safety-factor guidance.	Engineering calculation principle.	Keep with adapted-model wording.
Lechler2019VirtualCommissioning	Lechler2019VirtualCommissioning.pdf	Ch.4	PDF pp. 1-4	OK	Virtual commissioning and simulation-based early validation.	Concept C validation discussion.	Keep.
quigley2009ros	quigley2009ros.pdf	Ch.4, Ch.5	PDF pp. 1-4	OK for ROS; Partly OK for Ubuntu/drag&bot statement	ROS as open-source robotics middleware with communication infrastructure.	ROS framework claims.	Fix Ch.5 line 15 or add source.
Coleman2014MoveIt	Coleman2014MoveIt.pdf	Ch.4	PDF pp. 1, 3-5	OK	MoveIt planning, IK and collision-aware robot software.	Planning/IK/constraint-aware motion.	Keep.
UnityROS2Docs	Web only	Ch.4	Web documentation	OK after fix	ROS2-Unity interface, not planning.	Unity visualization/simulation interface only.	Keep current limited wording.
Cadena2016SLAM	Cadena2016SLAM.pdf	Ch.4	PDF pp. 1-4	OK	SLAM, mapping, localization and perception context.	Perception/mapping alternative concept.	Keep.
Pimentel2012	Pimentel2012.pdf	Ch.5	PDF pp. 1-4	OK	WebSocket real-time data communication.	Persistent communication choice.	Keep.
Crick2017	Crick2017.pdf	Ch.5	PDF pp. 1-4	OK	rosbridge JSON/socket access to ROS for non-ROS users.	Non-ROS Python client connection to ROS.	Keep.
dragandbot_anyrobot_2025	dragandbot_anyrobot_2025.pdf	Ch.2, Ch.4, Ch.5	PDF pp. 1, 3-5	OK for interface; Problem for current SHA equation/listing	AnyRobot WebSocket/RosBridge interface, robot operations, IO operations and ROSAuth example fields.	Primary communication architecture source.	Fix ROSAuth equation/listing.
Siciliano2016Robotics	Siciliano2016Robotics.pdf	Ch.2, Ch.4, Ch.5	PDF pp. 6-7, 14, 38 found	OK	Robotics fundamentals, programming, kinematics, workspace, rotations and trajectories.	General robotics theory.	Keep; add exact book pages if required.
lynch2017modern	lynch2017modern.pdf	Ch.5	PDF pp. 3-4, 7, 9; appendix B.1 text pp. 575-577	OK	Rotation matrices, ZYX Euler algorithm, singularities and kinematics.	Pose/orientation and reachability claims.	Keep.
Shoemake1985Slerp	Shoemake1985Slerp.pdf	Ch.5	Scanned/visual PDF; exact page pending	OK	Quaternion curves and SLERP for smooth rotation interpolation.	Orientation interpolation method.	Keep; optionally record printed page manually.
Flash1985MinimumJerk	Flash1985MinimumJerk.pdf	Ch.5	PDF pp. 2, 4, 11-12	OK	Minimum-jerk trajectory with zero velocity/acceleration boundary assumptions.	Minimum-jerk polynomial.	Keep.
Gasparetto2012Trajectory	Gasparetto2012Trajectory.pdf	Ch.5; recommended for Ch.2	PDF pp. 1-4 and minimum-jerk section	OK	Trajectory planning, smooth trajectories, jerk limitation and robotics trajectory methods.	Smooth trajectory planning context.	Use also to replace/supplement Biagiotti.
Biagiotti2008Trajectory	No local PDF	Ch.2	No local PDF	Not locally verified	Book unavailable locally; claim can be supported by Gasparetto.	Trajectory planning background.	Replace/supplement with Gasparetto or provide book.
Thramboulidis2013MDE	No local PDF	Ch.4	No local PDF	Problem/not verified	Not needed for thesis-specific separation claim unless paper is provided.	Architecture/design context only.	Remove or provide source.
universalrobots_ur5e	Official UR web page	Ch.1, Ch.5	Web spec page	OK after wording	Verifies UR5e DOF/reach/payload/repeatability.	Robot model specifications.	Keep spec-only wording.
"""


ACTIONS_TSV = r"""Priority	Location	Issue	Recommended action	Current status
High	Ch.5 lines 114-129 and code/sha512_auth.py	ROSAuth SHA-512 equation/listing does not match drag&bot AnyRobot PDF fields.	Rewrite equation/listing to match documented op/client/dest/end/level/mac/rand/t fields, or state it is illustrative/thesis-specific.	Open
Medium	Ch.5 line 15	quigley2009ros supports ROS but not Ubuntu platform choice or stable drag&bot integration.	Rewrite as implementation choice or add Ubuntu/drag&bot documentation.	Open
Medium	Ch.4 line 86	Thramboulidis2013MDE not locally verified and unnecessary for planning/execution separation claim.	Remove citation or provide verified paper; phrase separation as thesis architecture decision.	Open
Medium	Ch.2 line 100	Tao2019 book not locally verified.	Replace citation with Tao2021DigitalTwin or provide Tao 2019 book PDF.	Open
Medium	Ch.2 line 167	Biagiotti2008Trajectory book not locally verified.	Replace/supplement with Gasparetto2012Trajectory.	Open
Low	Ch.2 line 17	Fabricator web article not locally verified for basic press-brake fundamentals.	Use KalpakjianManufacturing2014 for process fundamentals; keep Fabricator only as industry context if needed.	Open
Done	Ch.5 lines 486-508	Vacuum equation needed adapted-model wording and VacuumGripperModeling citation.	Already rewritten as adapted conservative model and cited with VacuumGripperModeling plus vacuum standard.	Closed
Done	Ch.4 line 160	UnityROS2Docs was used for planning/IK claims.	Already fixed: ROS/MoveIt cite planning; Unity docs cite interface/simulation only.	Closed
Done	Ch.5 lines 746-755	FMEA RPN equation lacked source.	Already rewritten as simplified thesis scoring convention.	Closed
"""


HOW_TSV = r"""Topic	Guidance
Purpose	This workbook is an evidence matrix linking each important thesis citation/claim to the source that supports it.
How to read Claim Evidence Matrix	Each row is one thesis claim or citation-use cluster. Check the status, evidence page/section and action needed.
How to use before submission	Resolve every Open action in the Action Items sheet. For OK rows, keep the citation unless the thesis wording changes.
Page numbers	PDF page numbers are from local PDF scans where searchable text was available. Scanned/image PDFs and web-only sources are marked accordingly.
Plagiarism/false-claim safety	The evidence text is paraphrased. Use the source to support claims, but do not copy source wording directly into the thesis unless quoted properly.
Main remaining risk	The ROSAuth/SHA-512 equation/listing is the main remaining technical citation mismatch.
"""


def parse_tsv(text: str) -> tuple[list[str], list[list[str]]]:
    rows = list(csv.reader(StringIO(text.strip()), delimiter="\t"))
    return rows[0], rows[1:]


SHEETS = [
    ("Claim Evidence Matrix", *parse_tsv(CLAIMS_TSV)),
    ("Equation Evidence", *parse_tsv(EQUATIONS_TSV)),
    ("Reference Coverage", *parse_tsv(REFERENCES_TSV)),
    ("Action Items", *parse_tsv(ACTIONS_TSV)),
    ("How To Use", *parse_tsv(HOW_TSV)),
]


def col_letter(n: int) -> str:
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(65 + rem) + out
    return out


def esc(value: object) -> str:
    return html.escape(str(value), quote=False)


def status_style(sheet: str, col: int, value: str) -> int:
    if sheet == "Claim Evidence Matrix" and col == 8:
        v = value.lower()
    elif sheet == "Equation Evidence" and col == 7:
        v = value.lower()
    elif sheet == "Reference Coverage" and col == 5:
        v = value.lower()
    elif sheet == "Action Items" and col in (1, 5):
        v = value.lower()
    else:
        return 2
    if "problem" in v or "not locally" in v or "open" in v or "high" in v:
        return 5
    if "partly" in v or "medium" in v:
        return 4
    if "ok" in v or "done" in v or "closed" in v:
        return 3
    return 2


def worksheet_xml(sheet: str, headers: list[str], rows: list[list[str]]) -> str:
    all_rows = [headers] + rows
    max_col = len(headers)
    max_row = len(all_rows)
    dim = f"A1:{col_letter(max_col)}{max_row}"
    col_xml = []
    for i, header in enumerate(headers, 1):
        h = header.lower()
        width = 46 if any(k in h for k in ("claim", "evidence", "learned", "action", "guidance", "issue")) else 24
        if h in ("id", "priority", "status", "confidence"):
            width = 14
        col_xml.append(f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>')

    xml = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
        f'<dimension ref="{dim}"/>',
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>',
        '<sheetFormatPr defaultRowHeight="15"/>',
        '<cols>' + "".join(col_xml) + "</cols>",
        "<sheetData>",
    ]
    for r_idx, row in enumerate(all_rows, 1):
        height = 30 if r_idx == 1 else 64
        xml.append(f'<row r="{r_idx}" ht="{height}" customHeight="1">')
        for c_idx, value in enumerate(row, 1):
            cell = f"{col_letter(c_idx)}{r_idx}"
            style = 1 if r_idx == 1 else status_style(sheet, c_idx, value)
            xml.append(f'<c r="{cell}" s="{style}" t="inlineStr"><is><t>{esc(value)}</t></is></c>')
        xml.append("</row>")
    xml += [
        "</sheetData>",
        f'<autoFilter ref="{dim}"/>',
        '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>',
        "</worksheet>",
    ]
    return "".join(xml)


def build_xlsx(path: Path) -> None:
    workbook_sheets = []
    rels = []
    for i, (name, _headers, _rows) in enumerate(SHEETS, 1):
        workbook_sheets.append(f'<sheet name="{esc(name)}" sheetId="{i}" r:id="rId{i}"/>')
        rels.append(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        )
    rels.append(
        f'<Relationship Id="rId{len(SHEETS)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )

    content = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for i in range(1, len(SHEETS) + 1):
        content.append(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content += [
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
        "</Types>",
    ]

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
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
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
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<dc:title>Citation Claim Evidence Matrix</dc:title><dc:creator>Codex</dc:creator>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{CREATED}T00:00:00Z</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{CREATED}T00:00:00Z</dcterms:modified>'
        "</cp:coreProperties>"
    )
    app = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>Codex generated XLSX</Application></Properties>"
    )

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", "".join(content))
        archive.writestr("_rels/.rels", root_rels)
        archive.writestr("docProps/core.xml", core)
        archive.writestr("docProps/app.xml", app)
        archive.writestr("xl/workbook.xml", workbook_xml)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        archive.writestr("xl/styles.xml", styles)
        for i, (name, headers, rows) in enumerate(SHEETS, 1):
            archive.writestr(f"xl/worksheets/sheet{i}.xml", worksheet_xml(name, headers, rows))


if __name__ == "__main__":
    build_xlsx(OUT)
    print(f"Wrote {OUT.resolve()}")
    for name, _headers, rows in SHEETS:
        print(f"{name}: {len(rows)} rows")
