# Citation Claim Audit

Project: AutoProgram Press Brake Thesis

Scope: Chapters 1 to 7, current working copy scanned on 2026-04-27.

Local source folder checked: `THD_MEng_Thesis/reference Papers`

## Summary

- Citation occurrences in chapter files: 76
- Unique cited keys in Chapters 1 to 7: 35
- Exact same-name PDFs available locally: 27
- Web-only or missing local PDFs: 8
- Chapters with no direct citation occurrences: Chapter 3, Chapter 6, Chapter 7
- Important equation issue found: FMEA RPN equation is uncited; vacuum force equation needs wording/citation cleanup; ROSAuth/SHA512 equation does not match the drag&bot document.

## Status Legend

- OK: The thesis claim is supported by the cited source.
- PARTLY OK: The source supports the general idea, but the thesis wording is too specific or needs an additional/better citation.
- PROBLEM: The citation does not support the thesis claim, or the cited source entry/source file is wrong.
- NOT LOCALLY VERIFIED: No matching PDF was available in the local reference folder. Web pages were checked where possible.

## Main Problems To Fix Before Submission

| Location | Current citation | Status | Reason | Recommended fix |
|---|---:|---|---|---|
| `ch5_implementation.tex:114-129` | `dragandbot_anyrobot_2025` | PROBLEM | The drag&bot AnyRobot PDF supports WebSocket/RosBridge access and ROSAuth-style fields, but it does not support the exact thesis formula `SHA-512(secret || id_string || dest || nonce || t || level)` or the Python listing fields currently shown. The PDF shows `op`, `client`, `dest`, `level`, `mac`, `rand`, and `t`; it also shows hashing the secret for ROSAuth. | Rewrite this paragraph/equation/listing to match the documented fields, or state it is an illustrative implementation parameter and not the official formula. |
| `code/sha512_auth.py` used by `ch5:125-129` | `dragandbot_anyrobot_2025` | PROBLEM | The listing uses `operation`, `nonce`, `timestamp`, and `role`; the drag&bot document uses `op`, `client`, `dest`, `rand`, `t`, `level`, and `mac`. | Replace the listing or remove it. |
| `ch5_implementation.tex:15` | `quigley2009ros` | PARTLY OK | Quigley supports ROS as open-source middleware/communication infrastructure, but not Ubuntu as the development platform or stable drag&bot integration. | Cite ROS/Ubuntu/drag&bot documentation, or remove the citation from the Ubuntu/drag&bot stability part. |
| `ch4_development_of_concepts.tex:160` | `UnityROS2Docs` | PROBLEM | Unity for ROS2 documentation supports a ROS2-Unity interface, but not automated trajectory generation, inverse kinematics, or constraint-aware motion planning. | Cite `quigley2009ros` and `Coleman2014MoveIt` for planning/IK/motion planning, and use `UnityROS2Docs` only for Unity-ROS2 communication. |
| `ch5_implementation.tex:488-511` | `vacuum_handling_standard` | PARTLY OK | The Schmalz source supports safety factors and theoretical holding-force calculations, and `VacuumGripperModeling` supports vacuum force, pressure difference, suction area, object/gripper interaction, mass, acceleration, and dynamic loading. The exact vector resultant equation in the thesis is an adapted implementation model, not the exact Schmalz equation. | Add `VacuumGripperModeling` to the citation and phrase the equation as an adapted conservative model used in this thesis. |
| `ch5_implementation.tex:748-755` | none | PROBLEM | The FMEA RPN equation `RPN = S x O x D` and 1-10 scoring have no citation. | Add a source such as IEC 60812 or AIAG/VDA FMEA handbook, or describe it as the thesis scoring convention. |
| `ch4_development_of_concepts.tex:86` | `Thramboulidis2013MDE` | PROBLEM | No matching local PDF was found, and the exact BibTeX entry could not be confirmed from available sources. The claim about separating planning logic and execution is also more directly supported by the thesis architecture and drag&bot interface than by the missing MDE survey. | Remove this citation, replace with a correct available MDE/automation source, or make it a thesis design statement. |
| `ch2_state_of_the_art.tex:100` | `Tao2019` | NOT LOCALLY VERIFIED | The exact Tao 2019 book PDF is not in the local folder. However, `Tao2021DigitalTwin.pdf` supports digital twin, smart manufacturing, and cyber-physical/virtual-physical integration. | Replace `Tao2019` with `Tao2021DigitalTwin`, unless you provide the book. |
| `ch2_state_of_the_art.tex:167` | `Biagiotti2008Trajectory` | NOT LOCALLY VERIFIED | No local PDF for the Biagiotti book was found. The thesis claim is also supported by the available `Gasparetto2012Trajectory` paper. | Replace or supplement with `Gasparetto2012Trajectory`. |
| `ch2_state_of_the_art.tex:17` | `Fabricator_RoboticPressBrake_2023` | NOT LOCALLY VERIFIED | No local PDF, and the web article was not accessible in this scan. The claim is mostly textbook press-brake/sheet-metal bending fundamentals. | Use `KalpakjianManufacturing2014` for the process fundamentals. Keep Fabricator only for industry context if accessible. |
| `ch1_introduction.tex:43` and `ch5_implementation.tex:223` | `universalrobots_ur5e` | PARTLY OK | The official UR page supports 6 DOF, 850 mm reach, 5 kg payload, repeatability, and communication items. It does not directly prove "reliable kinematic modelling" or drag&bot model availability. | Keep UR citation for robot specs. Phrase simulation availability as observed in your drag&bot environment or cite drag&bot documentation if available. |

## Missing Or Web-Only Sources

These cited keys do not have a same-name PDF in the local reference folder:

| Key | Local PDF? | Verification result |
|---|---:|---|
| `acieta_press_brake` | No | Web page checked. OK as source for the Acieta robotic bending figure/cell description. |
| `Biagiotti2008Trajectory` | No | Not locally verified. Use `Gasparetto2012Trajectory` if you want a verified local source for trajectory planning. |
| `Fabricator_RoboticPressBrake_2023` | No | Not locally verified in full. Use `KalpakjianManufacturing2014` for core press-brake fundamentals. |
| `RoboDK2024` | No | Web page checked. OK for RoboDK simulation/offline programming/product capability claims. |
| `Tao2019` | No | Not locally verified. `Tao2021DigitalTwin` is available and supports the thesis digital twin claim. |
| `Thramboulidis2013MDE` | No | Not verified; BibTeX entry should be checked or replaced. |
| `UnityROS2Docs` | No | Web page checked. OK only for ROS2 interface/utilities for Unity, not for motion planning/IK claims. |
| `universalrobots_ur5e` | No | Official UR web page checked. OK for UR5e payload, reach, DOF, repeatability, and communication specs. |

## Chapter-by-Chapter Claim Check

### Chapter 1

| Line | Citation | Status | Verification |
|---:|---|---|---|
| 9 | `Gupta1998SheetMetalBending`, `Aomura2002RoboticBending` | OK | Both sources support robotic/sheet-metal bending process planning, bend sequences, gripping, and process interdependence. |
| 11 | `Gupta1998SheetMetalBending`, `Aomura2002RoboticBending` | OK | Aomura explicitly discusses robots replacing skilled operators and the need for grasp/reposition planning; Gupta covers grippers, robot motion, kinematic limits, and collision checks. |
| 13 | `Pan2012Survey`, `Neto2013OLP` | OK | Pan supports robot programming effort/time overhead and OLP; Neto supports CAD-based OLP for robot-assisted sheet-metal bending. |
| 14 | `Pan2012Survey`, `Gupta1998SheetMetalBending`, `Aomura2002RoboticBending` | OK | Combined sources support manual programming effort, process planning, bend sequence/regrip complexity, and verification/simulation concerns. |
| 15 | `Pan2012Survey`, `Gupta1998SheetMetalBending` | OK | Supported for reducing manual programming and coordinating grip/motion/pose validation. |
| 20 | `Pan2012Survey`, `Neto2013OLP` | OK | Supported for programming effort, OLP, CAD/simulation, and production/test benefits. |
| 22 | `Gupta1998SheetMetalBending`, `Aomura2002RoboticBending` | OK | Supported for geometry changes affecting grasp/repositioning/bending sequence feasibility. |
| 24 | `Aomura2002RoboticBending`, `Gupta1998SheetMetalBending` | OK | Supported for regripping, reachability/kinematic limits, repositioning, and planning complexity. |
| 43 | `universalrobots_ur5e` | PARTLY OK | Official UR page verifies UR5e specs, but not every qualitative claim in this sentence. |

### Chapter 2

| Line | Citation | Status | Verification |
|---:|---|---|---|
| 7 | `ISO8373` | OK | ISO 8373 PDF defines industrial robots as automatically controlled, reprogrammable, multipurpose manipulators programmable in three or more axes. |
| 9 | `craig2005robotics` | OK | Craig supports joints, DOF, pose, end-effector/tool frame, base frame, kinematics, and workspace. |
| 11 | `Pan2012Survey`, `Kruger2019` | OK | Supported for manual/OLP programming and higher-level/task-level/skill-based programming. |
| 17 | `Fabricator_RoboticPressBrake_2023` | NOT LOCALLY VERIFIED | Better supported by `KalpakjianManufacturing2014` for press-brake/sheet-metal bending fundamentals. |
| 19 | `KalpakjianManufacturing2014` | OK | Supports sheet-metal forming and bending processes. |
| 26 | `acieta_press_brake` | OK | Web page supports the robotic bending system figure/source. |
| 30 | `Aomura2002RoboticBending` | OK | Supports press-brake robot handling, grasping positions, repositioning, and bending sequence generation. |
| 35 | `Gupta1998SheetMetalBending` | OK | Supports coordinated process planning, tooling, grasp positions, robot motion planning, and kinematic/collision constraints. |
| 44 | `Siciliano2016Robotics` | OK | Supports manual/teach-pendant style robot programming and robotics fundamentals. |
| 67 | `Pan2012Survey` | OK | Supports frequent reprogramming and manual programming limitations in flexible environments. |
| 81 | `Pan2012Survey` | OK | Supports CAD-based OLP, simulation, prechecking, reachability/error checking, and reduced production trial-and-error. |
| 92 | `RoboDK2024` | OK | Web page supports RoboDK simulation/offline programming environment. |
| 100 | `Tao2019` | NOT LOCALLY VERIFIED | Replace with `Tao2021DigitalTwin`, which locally supports the same digital-twin/cyber-physical manufacturing claim. |
| 115 | `LozanoPerez1983` | OK | Supports task-level robot programming and symbolic/higher-level task specifications. |
| 117 | `Kruger2019` | OK | Supports robot skills, motion primitives, reusable modules, and non-expert/task-level programming. |
| 122 | `Pan2012Survey` | PARTLY OK | Pan supports programming approaches, OLP, and planning/simulation, but the exact wording "rule-based planning is commonly applied" is broader than Pan alone. |
| 124 | `Pan2012Survey`, `Gupta1998SheetMetalBending` | OK | Supported for manual engineering effort and coupled bending process planning. |
| 126 | `bohg2014data` | OK | Supports grasp synthesis, object geometry, contact conditions, task constraints, reachability, and integrated grasp/manipulation concerns. |
| 138 | `Neto2013OLP` | OK | Supports the robotic sheet-metal bending/OLP figure source. |
| 142 | `Gupta1998SheetMetalBending` | OK | Supports geometry/grasp/tool/robot-motion coupling. |
| 149 | `wan2017regrasp` | OK | Supports regrasp planning using grasps, stable placements, graph search, IK/reachability, and object reorientation. |
| 151 | `Gupta1998SheetMetalBending` | OK | Supports regrip affecting subsequent process and motion planning. |
| 158 | `VacuumGripperModeling` | OK | Supports vacuum grippers for sheet-metal handling, suction force, holding force, gripper-object interaction, and dynamic loading. |
| 160 | `bohg2014data` | OK | Supports general grasp planning based on object geometry, contact and task constraints. |
| 167 | `Biagiotti2008Trajectory`, `Gupta1998SheetMetalBending` | PARTLY OK | Gupta supports bending complexity. Biagiotti is missing locally; available `Gasparetto2012Trajectory` supports smooth trajectory planning and should be used. |
| 190 | `Pan2012Survey` | OK | Supports OLP/simulation advantages and pre-execution verification. |
| 192 | `RoboDK2024` | PARTLY OK | RoboDK web source supports product features. The critique that OLP is not fully automatic should be cited with Pan or presented as thesis analysis. |
| 197 | `dragandbot_anyrobot_2025` | PARTLY OK | The AnyRobot document supports WebSocket/RosBridge robot access. It does not fully support broad claims about graphical modular user workflows unless another drag&bot source is supplied. |

### Chapter 3

No citation occurrences were found in the Chapter 3 `.tex` file.

### Chapter 4

| Line | Citation | Status | Verification |
|---:|---|---|---|
| 8 | `Pahl2007EngineeringDesign` | OK | Supports concept development, requirements, solution variants, and evaluation. |
| 12 | `Pan2012Survey`, `Siciliano2016Robotics` | OK | Supports manual programming, OLP, and robotics programming concepts. |
| 23 | `Siciliano2016Robotics` | OK | Supports manual/teach-pendant programming and robot trajectory/programming fundamentals. |
| 63 | `Pan2012Survey`, `Siciliano2016Robotics` | OK | Supports manual programming effort, path generation, setup effort, and robotics expertise. |
| 86 | `dragandbot_anyrobot_2025`, `Thramboulidis2013MDE` | PARTLY OK / PROBLEM | drag&bot supports WebSocket/AnyRobot communication. `Thramboulidis2013MDE` is not locally verified and should be replaced or removed. |
| 88 | `VacuumGripperModeling` | OK | Supports grip planning considerations involving suction cups, force, load, object/gripper interaction. |
| 90 | `Gupta1998SheetMetalBending` | PARTLY OK | Gupta supports regrip/repositioning/process planning generally, but not the exact automatic opposite-side flipping workflow. Phrase the workflow as your system design. |
| 92 | `Siciliano2016Robotics` | OK | Supports linear Cartesian/tool-based motion and trajectory fundamentals. |
| 136 | `Pan2012Survey`, `Lechler2019VirtualCommissioning` | OK | Supports OLP/simulation verification and virtual commissioning/early validation. |
| 138 | `quigley2009ros`, `Coleman2014MoveIt`, `UnityROS2Docs` | OK | ROS and MoveIt support planning/IK/collision/motion planning. Unity docs support ROS2-Unity communication/interface only. |
| 140 | `Cadena2016SLAM` | OK | Supports SLAM, mapping, perception, and reconstruction/mapping context. |
| 153 | `Siciliano2016Robotics`, `Pan2012Survey` | OK | Supports dependence on accurate models and mismatch/verification issues in simulation/OLP. |
| 160 | `UnityROS2Docs` | PROBLEM | Unity docs alone do not support automated trajectory generation, IK, or constraint-aware motion planning. |
| 191 | `Aomura2002RoboticBending`, `Gupta1998SheetMetalBending` | OK | Supports regripping/repositioning and multistage bending complexity. |

### Chapter 5

| Line | Citation | Status | Verification |
|---:|---|---|---|
| 15 | `quigley2009ros` | PARTLY OK | Supports ROS, but not Ubuntu/drag&bot integration. |
| 103 | `Pimentel2012`, `Crick2017` | OK | Pimentel supports WebSocket persistent/full-duplex/low-overhead real-time communication; Crick supports rosbridge socket/JSON access to ROS. |
| 110 | `dragandbot_anyrobot_2025` | OK | Supports AnyRobot/RosBridge/WebSocket communication architecture. |
| 114 | `dragandbot_anyrobot_2025` | PROBLEM | Authentication concept is supported, but the formula and fields do not match the document. |
| 125 | `dragandbot_anyrobot_2025` | PROBLEM | The implementation listing does not match the documented ROSAuth field names. |
| 129 | `dragandbot_anyrobot_2025` | PROBLEM | Caption says it follows the specification, but it does not match the PDF. |
| 217 | `dragandbot_anyrobot_2025`, `Tao2021DigitalTwin` | OK | drag&bot supports virtual/WebSocket runtime; Tao supports digital twin and virtual/physical manufacturing concepts. |
| 223 | `universalrobots_ur5e`, `dragandbot_anyrobot_2025` | PARTLY OK | UR official page supports UR5e specs. Local drag&bot document supports interface concepts, but not full proof of UR5e model availability in the platform. |
| 239 | `Siciliano2016Robotics` | OK | Supports pose, manipulation, frames, and robotic system modelling. |
| 277 | `Siciliano2016Robotics` | PARTLY OK | Supports kinematics/reachability concepts; safety validation thresholds are thesis implementation choices. |
| 328 | `Siciliano2016Robotics` | OK | Supports workspace/orientation/kinematic constraints generally. |
| 361 | `Siciliano2016Robotics`, `lynch2017modern` | OK | Supports ZYX Euler/rotation representation and extraction concepts. |
| 511 | `vacuum_handling_standard` | PARTLY OK | Standard force/safety-factor principle is supported, exact equation is thesis adaptation. Add `VacuumGripperModeling` and clarify. |
| 551 | `lynch2017modern` | OK | Supports workspace, joint limits, IK, and singularity constraints. |
| 639 | `lynch2017modern` | PARTLY OK | Lynch supports kinematic/workspace/singularity limits; the exact two-stage transfer preference is your design decision. |
| 689 | `Shoemake1985Slerp` | OK | The scanned paper was visually checked and supports SLERP in quaternion space with smooth/constant-speed orientation interpolation. |
| 698 | `Flash1985MinimumJerk`, `Gasparetto2012Trajectory` | OK | Flash supports minimum-jerk with zero velocity/acceleration boundary assumptions; Gasparetto supports smooth/jerk-limited trajectory planning. |
| 748-755 | none | PROBLEM | FMEA RPN method and 1-10 scoring have no citation. |

### Chapter 6

No citation occurrences were found in the Chapter 6 `.tex` file. However, Chapter 6 refers to FMEA from Chapter 5; the FMEA method citation should be fixed in Chapter 5.

### Chapter 7

No citation occurrences were found in the Chapter 7 `.tex` file.

## Equation Citation Check

| Equation/location | Status | Notes |
|---|---|---|
| ROSAuth SHA512 MAC, `ch5:116-119` | PROBLEM | Does not match the drag&bot AnyRobot source. |
| Fixture position deviation, `ch5:286-289` | OK as thesis implementation | Euclidean distance formula is basic mathematical definition; citation not strictly required if it is an implementation metric. |
| Fixture angular deviation, `ch5:293-296` | OK as thesis implementation | Max absolute Euler deviation is a design metric; citation not strictly required if stated as implementation choice. |
| Orientation transforms, `ch5:335-340`, `ch5:355-389` | OK as thesis implementation | These are your transformation rules; cite robotics sources only for rotation/Euler conventions, which is already done at `ch5:361`. |
| Euler composition/extraction, `ch5:363-372` | OK | Supported by Siciliano/Lynch. |
| Vacuum available force, `ch5:488-490` | PARTLY OK | Supported by vacuum sources in principle; add `VacuumGripperModeling` and clarify efficiency/safety factor terms. |
| Required holding force, `ch5:497-499` | PARTLY OK | Schmalz supports load cases with mass, gravity, acceleration, safety factor. The vector-resultant form is adapted by the thesis. |
| Vacuum feasibility criterion, `ch5:506-508` | OK with cleanup | Logical feasibility criterion is fine after force equation wording/citation cleanup. |
| Cartesian interpolation, `ch5:682-685` | OK as basic implementation | Basic linear interpolation; citation not strictly required. |
| Minimum-jerk scaling, `ch5:693-695` | OK | Supported by Flash and Gasparetto. |
| RPN equation, `ch5:750-753` | PROBLEM | Needs an FMEA source or wording as thesis scoring convention. |

## References Verified OK From Local PDFs

These cited sources were verified as correctly supporting the thesis claim ideas where used:

- `Aomura2002RoboticBending`
- `Gupta1998SheetMetalBending`
- `Pan2012Survey`
- `Neto2013OLP`
- `ISO8373`
- `craig2005robotics`
- `KalpakjianManufacturing2014`
- `Pahl2007EngineeringDesign`
- `Kruger2019`
- `LozanoPerez1983`
- `bohg2014data`
- `wan2017regrasp`
- `VacuumGripperModeling`
- `Lechler2019VirtualCommissioning`
- `quigley2009ros`
- `Coleman2014MoveIt`
- `Cadena2016SLAM`
- `Pimentel2012`
- `Crick2017`
- `Siciliano2016Robotics`
- `lynch2017modern`
- `Shoemake1985Slerp` (visually checked because text extraction was empty)
- `Flash1985MinimumJerk`
- `Gasparetto2012Trajectory`
- `Tao2021DigitalTwin`

## Recommended Fix Order

1. Fix the drag&bot ROSAuth equation/listing/caption in Chapter 5.
2. Add or replace the missing FMEA source for RPN.
3. Clean up the vacuum force wording and cite both Schmalz and `VacuumGripperModeling`.
4. Replace `Tao2019` with `Tao2021DigitalTwin`, unless the Tao 2019 book is provided.
5. Replace or supplement `Biagiotti2008Trajectory` with `Gasparetto2012Trajectory`.
6. Remove/replace `Thramboulidis2013MDE` unless the correct paper is supplied.
7. Fix `UnityROS2Docs` usage at Chapter 4 line 160 by citing MoveIt/ROS for planning and Unity only for simulation/communication.
8. Rephrase UR5e and drag&bot availability claims to distinguish official robot specifications from the observed simulation setup.
