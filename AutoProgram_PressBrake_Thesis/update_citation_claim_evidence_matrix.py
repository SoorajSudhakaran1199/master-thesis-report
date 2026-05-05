from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZIP_DEFLATED


OUT = Path("citation_claim_evidence_matrix.xlsx")
CREATED = "2026-05-02"


CLAIMS = [
    ["C001", "Ch.1 lines 9, 11, 22, 24", "Sheet-metal bending is common, and robotic bending requires coordinated bend sequence, tooling, grasping, repositioning and reachability planning.", "Gupta1998SheetMetalBending; Aomura2002RoboticBending", "Local PDFs available", "Both papers address robotic sheet-metal bending, bend sequence planning, robot handling, grasp/reposition planning and changing part geometry.", "OK", "Keep. Core bending-specific background sources.", "High"],
    ["C002", "Ch.1 lines 13-20", "Manual and offline robot programming still require significant effort, adaptation and expert knowledge for new workpieces.", "Pan2012Survey; Neto2013OLP", "Local PDFs available", "Pan surveys programming effort and OLP approaches. Neto presents CAD-based OLP for robot-assisted sheet-metal bending.", "OK", "Keep.", "High"],
    ["C003", "Ch.1 line 15", "Flexible manufacturing motivates reduction of manual programming and more systematic grip, pose, regrip, sequence and validation generation.", "Pan2012Survey; Gupta1998SheetMetalBending", "Local PDFs available", "Sources support programming-effort reduction and the coupling of bending process planning with grasping and motion constraints.", "OK", "Keep as synthesis of cited sources and thesis problem definition.", "High"],
    ["C004", "Ch.1 line 56", "UR5e provides six DOF, approx. 850 mm reach, 5 kg payload and high repeatability, and is used as the simulation reference manipulator.", "universalrobots_ur5e", "Official UR technical web source", "Manufacturer data supports measurable UR5e specifications. The use as reference model is an implementation decision.", "OK", "Keep. Do not overextend the citation beyond specifications.", "Medium"],
    ["C005", "Ch.2 line 7", "Industrial robots are reprogrammable, multipurpose manipulators with three or more programmable axes.", "ISO8373", "Local PDF exact match", "The ISO vocabulary definition supports the formal industrial-robot definition.", "OK", "Keep. Check bib year/version if it still says ISO 8373:2012 while the local PDF is 2021.", "High"],
    ["C006", "Ch.2 line 9", "Robot joints provide DOF to position and orient the end-effector/TCP in 3D space.", "craig2005robotics", "Local PDF exact match", "Craig supports joints, coordinate frames, end-effectors, TCP/pose and robot kinematics fundamentals.", "OK", "Keep.", "High"],
    ["C007", "Ch.2 line 11", "Robot programming spans low-level pose/trajectory programming and higher-level task/skill abstraction.", "Pan2012Survey; Kruger2019", "Local PDFs available", "Pan supports programming approaches and OLP; Kruger/Pedersen supports robot skills and modular task abstraction.", "OK", "Keep. Check key/year consistency for Kruger2019 if bib year is 2016.", "High"],
    ["C008", "Ch.2 line 17", "Sheet-metal bending is a plastic-deformation manufacturing process used for varied geometries.", "KalpakjianManufacturing2014", "Local PDF exact match", "Manufacturing textbook supports sheet-metal forming and bending fundamentals.", "OK", "Keep.", "High"],
    ["C009", "Ch.2 line 19", "Industrial robots are used for handling, processing and assembly to reduce direct human reliance.", "Groover2016", "Local PDF under non-key filename", "Manufacturing textbook supports general robot use in manufacturing tasks.", "OK", "Keep; optionally rename or document the local PDF alias.", "Medium"],
    ["C010", "Ch.2 line 25", "Robotic press-brake bending system figure source.", "acieta_press_brake", "Web source", "Citation is used for image/source attribution rather than as academic evidence.", "OK", "Keep if figure reuse requirements are satisfied.", "Medium"],
    ["C011", "Ch.2 lines 29, 34, 133, 142", "Automated press-brake cells require picking, positioning, support, reorientation, unloading, and integrated process/motion planning as geometry changes.", "Aomura2002RoboticBending; Gupta1998SheetMetalBending", "Local PDFs available", "Aomura supports robotic bending handling and bend sequences; Gupta supports geometric changes, tooling, grasping and robot-motion constraints.", "OK", "Keep.", "High"],
    ["C012", "Ch.2 lines 43, 66", "Teach-pendant/manual programming uses manually defined positions/waypoints and becomes inefficient with frequent workpiece changes.", "Siciliano2016Robotics; Pan2012Survey", "Local PDFs available", "Siciliano supports manual robot programming and robotics fundamentals; Pan supports programming effort and reprogramming burden.", "OK", "Keep.", "High"],
    ["C013", "Ch.2 line 80", "OLP allows robot programs to be prepared and validated virtually, reducing setup time and shop-floor trial-and-error.", "Pan2012Survey", "Local PDF exact match", "Pan supports OLP, simulation and reduced production interruption/setup effort.", "OK", "Keep.", "High"],
    ["C014", "Ch.2 line 91; Ch.5 line 191", "Digital twins link virtual representations with physical systems and support monitoring, validation, synchronization and smart manufacturing.", "Tao2021DigitalTwin", "Local PDF exact match", "The local Tao paper supports digital-twin-driven smart manufacturing, virtual-physical integration and validation concepts.", "OK", "Successfully updated from Tao2019. Replacement supports the current claim.", "High"],
    ["C015", "Ch.2 line 106", "Task-level robot programming separates task intent from low-level robot motion.", "LozanoPerez1983", "Local PDF exact match", "Classic task-level programming source supports symbolic/task abstraction above low-level motion commands.", "OK", "Keep. Fix author-name encoding in bib if needed.", "High"],
    ["C016", "Ch.2 line 108", "Robot skills, motion primitives and reusable task modules can be combined for complex robot programs.", "Kruger2019", "Local PDF exact match", "Paper supports manufacturing robot skills and modular reusable operation descriptions.", "OK", "Keep. Check bibliography key/year consistency.", "High"],
    ["C017", "Ch.2 line 113", "Rule-based and constraint-based planning uses predefined rules and feasibility checks for robot behavior.", "Pan2012Survey", "Local PDF exact match", "Pan supports robot programming/OLP context, but this broad rule-based formulation is partly thesis synthesis.", "Partly OK", "Add a stronger rule-/constraint-based planning source or phrase as synthesis.", "Medium"],
    ["C018", "Ch.2 line 117", "Grasp, regrip, trajectory and reachability planning are interdependent in complex manipulation tasks.", "bohg2014data", "Local PDF exact match", "Bohg supports grasp synthesis with geometry, contact, constraints and task context; the full multi-module integration claim is broader.", "Partly OK", "Keep for grasp context; add manipulation-planning/regrasp integration source if needed.", "Medium"],
    ["C019", "Ch.2 line 129", "Robotic sheet-metal bending system figure source.", "Neto2013OLP", "Local PDF exact match", "Citation is used as source attribution for the figure and OLP bending context.", "OK", "Keep.", "High"],
    ["C020", "Ch.2 line 140", "A valid regrip sequence considers grasp stability, reachability and intermediate placements.", "wan2017regrasp", "Local PDF exact match", "Wan and Harada support regrasp planning with grasps, stable placements and feasibility/reachability checks.", "OK", "Keep.", "High"],
    ["C021", "Ch.2 line 149; Ch.4 line 81; Ch.5 lines 429, 436", "Vacuum gripper feasibility depends on suction-cup placement, pressure/area, contact quality, holding force, load and safety factor.", "VacuumGripperModeling; vacuum_handling_standard", "Local PDFs available", "Sources support vacuum force principles, pressure difference, suction area, object/gripper interaction, safety margins and dynamic loading.", "OK", "Keep. Current wording correctly frames equations as an adapted conservative model.", "High"],
    ["C022", "Ch.2 line 151", "General grasp planning uses object geometry, contact conditions and task constraints; bending adds tool-access constraints.", "bohg2014data", "Local PDF exact match", "Bohg supports geometry/contact/task-context aspects of grasp planning. Bending-specific tool access is thesis application.", "OK", "Keep.", "High"],
    ["C023", "Ch.2 line 158; Ch.5 line 685", "Classical trajectory generation supports smooth continuous robot motion; robotic bending adds changing geometry and feasibility constraints.", "Gasparetto2012Trajectory; Gupta1998SheetMetalBending", "Local PDFs available", "Gasparetto supports trajectory planning and smooth profiles; Gupta supports bending-specific geometric and planning constraints.", "OK", "Successfully updated from Biagiotti2008Trajectory. Replacement supports the current claim.", "High"],
    ["C024", "Ch.2 lines 181, 183", "Simulation/OLP environments support virtual program development and validation; RoboDK is a practical OLP/simulation example.", "Pan2012Survey; RoboDK2024", "Pan local PDF; RoboDK web source", "Pan supports OLP and simulation benefits. RoboDK source supports product capability, while critique of manual configuration is thesis analysis.", "OK", "Keep. Product source is appropriate for product capability only.", "Medium"],
    ["C025", "Ch.2 lines 188, 190", "drag&bot provides graphical modular programming and AnyRobot/KEBA integration context.", "dragandbot_about_2026; dragandbot_anyrobot_2025; keba_dragandbot_2022", "AnyRobot local PDF; web/company sources", "Sources support platform capability and AnyRobot communication claims.", "OK", "Keep. Use company/web sources for product facts only.", "Medium"],
    ["C026", "Ch.4 line 8", "Concept development follows systematic engineering design and requirement-based evaluation.", "Pahl2007EngineeringDesign", "Local PDF exact match", "Pahl and Beitz support structured conceptual design and solution evaluation.", "OK", "Keep.", "High"],
    ["C027", "Ch.4 lines 12, 23, 56", "Manual, rule-based and CAD/OLP concepts are evaluated against programming effort and automation needs.", "Pan2012Survey; Siciliano2016Robotics", "Local PDFs available", "Sources support manual robot programming, OLP and robotics fundamentals; the comparison itself is thesis design.", "OK", "Keep.", "High"],
    ["C028", "Ch.4 line 79", "AnyRobot WebSocket communication separates planning logic from runtime command execution in the implemented architecture.", "dragandbot_anyrobot_2025", "Local PDF exact match", "AnyRobot documentation supports WebSocket/RosBridge interface and external communication. Planning/runtime separation is thesis architecture.", "OK", "Thramboulidis2013MDE was removed; remaining source supports the concrete interface claim.", "High"],
    ["C029", "Ch.4 line 83", "Opposite-side bending is handled through a thesis-specific flipping and repositioning workflow, with validation across process steps.", "Gupta1998SheetMetalBending", "Local PDF exact match", "Gupta supports regrip/repositioning and integrated process planning generally, but not the exact implemented workflow.", "Partly OK", "Keep only as general background; present exact flip workflow as thesis design.", "Medium"],
    ["C030", "Ch.4 line 85", "Linear Cartesian robot trajectories with smooth velocity profiles support stable and predictable execution.", "Siciliano2016Robotics", "Local PDF exact match", "Textbook supports Cartesian motion/trajectory fundamentals. Gasparetto would be stronger trajectory-specific support.", "Partly OK", "Optional: add Gasparetto2012Trajectory.", "Medium"],
    ["C031", "Ch.4 line 121", "Simulation-based evaluation enables collision/reachability validation and reduced commissioning effort; named OLP tools use similar methodologies.", "Pan2012Survey; Lechler2019VirtualCommissioning", "Local PDFs available", "Pan and Lechler support OLP/virtual commissioning. Named ABB/KUKA/FANUC tool claim needs vendor-specific sources if kept as factual product claim.", "Partly OK", "Add vendor sources or soften the named-tools sentence.", "Medium"],
    ["C032", "Ch.4 lines 123, 143", "ROS/MoveIt can provide automation, IK, trajectory generation and constraint-aware planning; Unity supports ROS2 simulation/visualisation interface.", "quigley2009ros; Coleman2014MoveIt; UnityROS2Docs; Cadena2016SLAM", "Local PDFs plus Unity web docs", "ROS and MoveIt support middleware and planning; Unity docs support interface; SLAM source supports perception/mapping context.", "OK", "Keep. Current wording separates MoveIt planning evidence from Unity visualisation evidence.", "High"],
    ["C033", "Ch.4 line 136", "Virtual/physical deviation and digital-model accuracy affect simulation-to-execution reliability.", "Siciliano2016Robotics; Pan2012Survey", "Local PDFs available", "Sources support kinematic modelling and OLP model-dependence.", "OK", "Keep.", "High"],
    ["C034", "Ch.4 line 171", "Automated regrip and opposite-side handling are evaluation criteria because they are complex bending operations.", "Aomura2002RoboticBending; Gupta1998SheetMetalBending", "Local PDFs available", "Both sources support complexity of robotic bending sequence, handling and regrip/repositioning.", "OK", "Keep.", "High"],
    ["C035", "Ch.5 line 17", "Ubuntu is used because of ROS compatibility and integration with drag&bot environment.", "quigley2009ros", "Local PDF exact match", "Quigley supports ROS as robotics middleware, but not Ubuntu choice or drag&bot stability.", "Partly OK", "Rewrite as implementation choice or add Ubuntu/drag&bot platform documentation.", "Medium"],
    ["C036", "Ch.5 lines 92, 128, 132", "AnyRobot enables external planning software to communicate with drag&bot runtime through RosBridge/WebSocket and ROSAuth handshake.", "dragandbot_anyrobot_2025", "Local PDF exact match", "AnyRobot documentation supports WebSocket/RosBridge interface and authentication concept. Current thesis no longer exposes a mismatching formula/listing.", "OK", "Keep.", "High"],
    ["C037", "Ch.5 line 96", "Persistent WebSocket communication is suitable for continuous command/state exchange and lower overhead than repeated HTTP.", "Pimentel2012; Crick2017", "Local PDFs available", "Pimentel supports WebSocket for real-time communication; Crick supports rosbridge JSON/socket access to ROS.", "OK", "Keep.", "High"],
    ["C038", "Ch.5 line 197", "UR5e specs and joint ranges support its use as simulated manipulator.", "universalrobots_ur5e", "Official UR technical web source", "Manufacturer source supports reach, payload, DOF, speed/range/specification facts. Suitability is thesis judgement.", "OK", "Keep.", "Medium"],
    ["C039", "Ch.5 line 204", "UR5e kinematic structure and coordinate-frame assignment figure source.", "zhang2025invertible", "Local PDF under non-key filename", "Potentially related to UR5e kinematics/dynamics, but weak as generic figure source unless directly adapted from it.", "Partly OK", "Verify figure provenance or replace with official/manual source or own diagram.", "Medium"],
    ["C040", "Ch.5 lines 235, 263, 325, 360", "Pose acquisition, safety pre-validation, workspace orientation constraints and ZYX Euler decomposition are robotics fundamentals.", "Siciliano2016Robotics; lynch2017modern", "Local PDFs available", "Textbooks support pose, coordinate frames, kinematics, joint limits, singularities and Euler rotations. Safety-standard strength is limited.", "Partly OK", "Keep for robotics fundamentals. For safety compliance claims, add safety standard or state as internal validation.", "High"],
    ["C041", "Ch.5 line 272", "Fixture positional deviation is computed using 3D Euclidean distance.", "OpenStaxCalculusVolume3", "Web source", "Source supports Euclidean distance formula. This is basic math and could also be left uncited.", "OK", "Keep or remove depending on citation style preference.", "Medium"],
    ["C042", "Ch.5 lines 527, 600", "Reachability limits, joint limits and singularity/workspace constraints motivate regrip planning and two-stage transfer rather than direct in-gripper rotation.", "lynch2017modern", "Local PDF exact match", "Modern Robotics supports workspace, joint limits, kinematics and singularity constraints. The specific two-stage transfer is thesis design.", "OK", "Keep with thesis-design wording.", "High"],
    ["C043", "Ch.5 line 667", "Cartesian translation between poses uses standard linear interpolation.", "LibreTextsLinearInterpolation", "Web source", "Source supports linear interpolation formula; it is basic mathematics.", "OK", "Keep or replace with textbook/trajectory source if stricter sourcing is required.", "Medium"],
    ["C044", "Ch.5 line 676", "SLERP provides smooth, constant-speed quaternion rotation interpolation.", "Shoemake1985Slerp", "Local PDF exact match", "Classic source introduces quaternion curves and spherical linear interpolation for rotations.", "OK", "Keep.", "High"],
    ["C045", "Ch.5 lines 678, 685", "Fifth-order minimum-jerk scaling gives smooth motion with zero velocity/acceleration at boundaries; such profiles are used in robot trajectory planning.", "Flash1985MinimumJerk; Sharkawy2021MinimumJerk; Gasparetto2012Trajectory", "Local PDFs available", "Sources support minimum-jerk/smooth trajectory use and boundary smoothness.", "OK", "Keep.", "High"],
    ["C046", "Ch.5 lines 726, 728", "Simplified FMEA-style scoring uses severity, occurrence and detectability combined into RPN.", "IEC60812_2018", "No exact local PDF found in reference Papers listing", "IEC 60812 is the relevant FMEA standard for failure-mode analysis terminology and S/O/D/RPN context.", "OK / Missing local file", "Add the IEC 60812 standard/source file to the reference folder if required.", "Medium"],
]


EQUATIONS = [
    ["Fixture position deviation", "Ch.5 line 272", "3D Euclidean distance", "OpenStaxCalculusVolume3", "Source supports Euclidean distance; formula is basic mathematics.", "OK", "No action."],
    ["Fixture orientation deviation", "Ch.5 safety validation section", "Maximum absolute Euler-angle deviation", "Thesis implementation rule", "Thresholding rule is system-specific and does not require external evidence if presented as design choice.", "OK", "No action."],
    ["Zone-based orientation correction", "Ch.5 orientation strategy section", "Yaw/roll wrapping and pitch inversion logic", "Siciliano2016Robotics; lynch2017modern nearby", "General rotation/Euler theory is supported; exact rule is thesis implementation logic.", "OK", "No action."],
    ["ZYX Euler composition/extraction", "Ch.5 line 360", "Rotation matrix to ZYX Euler angles", "Siciliano2016Robotics; lynch2017modern", "Sources support rotation matrices and Euler-angle decomposition conventions.", "OK", "Keep convention explicit."],
    ["Vacuum holding force", "Ch.5 line 429", "n * DeltaP * A * eta", "VacuumGripperModeling; vacuum_handling_standard", "Sources support pressure-area force principles and conservative vacuum feasibility modelling.", "OK", "Keep adapted-model wording."],
    ["Required holding force", "Ch.5 line 436", "Safety-factor-weighted gravitational/inertial resultant", "vacuum_handling_standard; VacuumGripperModeling", "Sources support force/load/safety-factor principles; exact resultant is thesis adaptation.", "OK", "Keep adapted-model wording."],
    ["Linear Cartesian interpolation", "Ch.5 line 667", "(1-lambda)p_s + lambda p_t", "LibreTextsLinearInterpolation", "Source supports linear interpolation; trajectory context also supported by Gasparetto.", "OK", "No action."],
    ["SLERP", "Ch.5 line 676", "Quaternion spherical linear interpolation", "Shoemake1985Slerp", "Classic source supports SLERP for rotations.", "OK", "No action."],
    ["Minimum-jerk scaling", "Ch.5 lines 678, 685", "10u^3 - 15u^4 + 6u^5", "Flash1985MinimumJerk; Sharkawy2021MinimumJerk; Gasparetto2012Trajectory", "Sources support minimum-jerk/smooth trajectory use and boundary smoothness.", "OK", "No action."],
    ["Risk Priority Number", "Ch.5 lines 726, 728", "RPN = S x O x D", "IEC60812_2018", "Citation is conceptually appropriate for FMEA/RPN terminology, but local file presence should be checked.", "OK / Missing local file", "Add IEC 60812 source file to reference folder if required."],
]


REFERENCES = [
    ["Aomura2002RoboticBending", "Ch.1; Ch.2; Ch.4", "Local PDF exact match", "Supports robotic bending, bend sequencing, workpiece handling and reorientation.", "Keep."],
    ["Cadena2016SLAM", "Ch.4", "Local PDF exact match", "Supports SLAM/perception/mapping context for alternative concept.", "Keep."],
    ["Coleman2014MoveIt", "Ch.4", "Local PDF exact match", "Supports MoveIt motion planning, IK and collision-aware planning.", "Keep."],
    ["Crick2017", "Ch.5", "Local PDF exact match", "Supports rosbridge/socket access to ROS.", "Keep."],
    ["Flash1985MinimumJerk", "Ch.5", "Local PDF exact match", "Supports minimum-jerk trajectory formulation.", "Keep."],
    ["Gasparetto2012Trajectory", "Ch.2; Ch.5", "Local PDF exact match", "Valid replacement for Biagiotti2008Trajectory.", "Keep."],
    ["Groover2016", "Ch.2", "Local PDF under non-key filename", "Supports manufacturing robot task background.", "Optionally rename PDF or note alias."],
    ["Gupta1998SheetMetalBending", "Ch.1; Ch.2; Ch.4", "Local PDF exact match", "Core evidence for bending process planning, grasping and motion constraints.", "Keep."],
    ["IEC60812_2018", "Ch.5", "No exact local PDF found", "Conceptually appropriate for FMEA/RPN terminology.", "Add standard/source file or document access route."],
    ["ISO8373", "Ch.2", "Local PDF exact match", "Supports industrial robot definition.", "Check bibliography year/version consistency."],
    ["KalpakjianManufacturing2014", "Ch.2", "Local PDF exact match", "Supports manufacturing/sheet-metal bending fundamentals.", "Keep."],
    ["Kruger2019", "Ch.2", "Local PDF exact match", "Supports robot skills/modular programming.", "Check key/year consistency."],
    ["Lechler2019VirtualCommissioning", "Ch.4", "Local PDF exact match", "Supports virtual commissioning and early validation.", "Keep."],
    ["LibreTextsLinearInterpolation", "Ch.5", "Web source", "Supports basic linear interpolation.", "Accept or replace with textbook source."],
    ["LozanoPerez1983", "Ch.2", "Local PDF exact match", "Supports task-level robot programming.", "Fix author encoding in bib if needed."],
    ["Neto2013OLP", "Ch.1; Ch.2", "Local PDF exact match", "Supports CAD/OLP for robot-assisted sheet-metal bending and figure source.", "Keep."],
    ["OpenStaxCalculusVolume3", "Ch.5", "Web source", "Supports Euclidean distance formula.", "Accept or remove if basic math citation not needed."],
    ["Pahl2007EngineeringDesign", "Ch.4", "Local PDF exact match", "Supports systematic concept development/evaluation.", "Keep."],
    ["Pan2012Survey", "Ch.1; Ch.2; Ch.4", "Local PDF exact match", "Supports programming methods, OLP and programming effort.", "Keep; add stronger source for broad rule-based planning if desired."],
    ["Pimentel2012", "Ch.5", "Local PDF exact match", "Supports WebSocket communication rationale.", "Keep."],
    ["RoboDK2024", "Ch.2", "Web/product source", "Supports RoboDK product capabilities.", "Use only for product facts."],
    ["Sharkawy2021MinimumJerk", "Ch.5", "Local PDF exact match", "Supports smooth/minimum-jerk trajectory context.", "Keep."],
    ["Shoemake1985Slerp", "Ch.5", "Local PDF exact match", "Supports quaternion SLERP.", "Keep."],
    ["Siciliano2016Robotics", "Ch.2; Ch.4; Ch.5", "Local PDF exact match", "Supports robot programming, kinematics, pose, workspace and trajectory fundamentals.", "Keep; use standards for safety-compliance claims."],
    ["Tao2021DigitalTwin", "Ch.2; Ch.5", "Local PDF exact match", "Valid replacement for Tao2019; supports digital twin/smart manufacturing concepts.", "Keep."],
    ["UnityROS2Docs", "Ch.4", "Web documentation", "Supports Unity-ROS2 simulation/interface claims.", "Keep for Unity interface only."],
    ["VacuumGripperModeling", "Ch.2; Ch.4; Ch.5", "Local PDF exact match", "Supports vacuum gripper force and feasibility principles.", "Keep."],
    ["acieta_press_brake", "Ch.2 figure", "Web/source attribution", "Supports figure/source attribution.", "Check reuse permission if required."],
    ["bohg2014data", "Ch.2", "Local PDF exact match", "Supports grasp planning geometry/contact/task constraints.", "Keep; add source if integrated-framework claim must be stronger."],
    ["craig2005robotics", "Ch.2", "Local PDF exact match", "Supports robot kinematics, DOF, frames and TCP.", "Keep."],
    ["dragandbot_about_2026", "Ch.2", "Web/company source", "Supports product/platform description.", "Use for product facts only."],
    ["dragandbot_anyrobot_2025", "Ch.2; Ch.4; Ch.5", "Local PDF exact match", "Supports AnyRobot WebSocket/RosBridge/interface and ROSAuth concept.", "Keep."],
    ["keba_dragandbot_2022", "Ch.2", "Web/company source", "Supports KEBA/drag&bot product context.", "Use for product facts only."],
    ["lynch2017modern", "Ch.5", "Local PDF exact match", "Supports kinematics, workspace, singularities and rotation math.", "Keep."],
    ["quigley2009ros", "Ch.4; Ch.5", "Local PDF exact match", "Supports ROS middleware, not Ubuntu/drag&bot stability.", "Keep; adjust Ch.5 wording/source if needed."],
    ["universalrobots_ur5e", "Ch.1; Ch.5", "Official web source", "Supports UR5e technical specifications.", "Keep."],
    ["vacuum_handling_standard", "Ch.5", "Local PDF exact match", "Supports practical vacuum handling force/safety-factor principles.", "Keep."],
    ["wan2017regrasp", "Ch.2", "Local PDF exact match", "Supports regrasp planning with stable placements/reachability.", "Keep."],
    ["zhang2025invertible", "Ch.5 figure", "Local PDF under non-key filename", "Potentially supports UR5e kinematics/dynamics, but weak as generic figure source unless directly adapted.", "Verify provenance or replace with official/manual source."],
]


ACTIONS = [
    ["Closed", "Ch.2 line 91", "Citation replacement", "Tao2019 is no longer cited; Tao2021DigitalTwin supports the current digital-twin claim.", "No further action unless removing unused bib entries."],
    ["Closed", "Ch.2 line 158", "Citation replacement", "Biagiotti2008Trajectory is no longer cited; Gasparetto2012Trajectory supports the current trajectory claim.", "No further action unless removing unused bib entries."],
    ["Closed", "Ch.4 line 79", "Missing PDF / weak citation", "Thramboulidis2013MDE is no longer cited; the sentence now relies on dragandbot_anyrobot_2025 and thesis architecture wording.", "No further action unless MDE literature is intentionally added."],
    ["High", "Ch.5 lines 726, 728", "Missing local file", "IEC60812_2018 is cited but no exact PDF appeared in the reference Papers folder listing.", "Add IEC 60812 standard/source file or document institutional access."],
    ["Medium", "Ch.5 line 17", "Weak support", "quigley2009ros supports ROS, but not Ubuntu choice or drag&bot stability.", "Rewrite as implementation choice or add Ubuntu/drag&bot platform documentation."],
    ["Medium", "Ch.5 line 204", "Weak/provenance issue", "zhang2025invertible is weak for a generic UR5e kinematic-structure figure unless the figure is directly adapted from that paper.", "Verify figure source; otherwise replace with official/manual source or own diagram."],
    ["Medium", "Ch.4 line 121", "Product claim support", "Named ABB/KUKA/FANUC OLP tools need vendor-specific support if kept as factual product claims.", "Add vendor sources or soften the sentence."],
    ["Medium", "Ch.2 line 113", "Broad planning claim", "Pan supports programming/OLP context, but broad rule-/constraint-based planning claim is partly synthesis.", "Add stronger source or make synthesis wording explicit."],
    ["Medium", "Ch.2 line 117", "Broad integrated-framework claim", "Bohg supports grasp planning but is narrower than the full integrated planning framework claim.", "Add manipulation-planning/regrasp integration source if needed."],
    ["Low", "references.bib", "Metadata consistency", "Some keys/file names suggest metadata mismatch: ISO8373 version/year, Kruger2019 key/year, Tao2021DigitalTwin key/year, Groover/Zhang local filenames.", "Clean bibliographic metadata before final submission."],
    ["Low", "references.bib", "Text encoding", "Lozano-Perez entry may contain encoding artefacts.", "Correct author spelling/encoding if present."],
]


HOW = [
    ["Workbook updated", f"Updated on {CREATED} against current chapter .tex citation usage."],
    ["Scope", "The matrix covers current in-text citation clusters found in Chapters 1, 2, 4 and 5. Chapters 3, 6 and 7 currently contain no direct citation keys in the chapter .tex files."],
    ["Status meanings", "OK = citation supports the claim; Partly OK = source supports only part of the claim or the claim is thesis synthesis; Missing local file = citation may be valid but source file was not found in the reference folder listing."],
    ["Academic-review focus", "Resolve High/Medium action items before submission, especially the missing IEC60812 source access and weak/provenance-sensitive figure/product claims."],
    ["Replacement audit", "Tao2019, Biagiotti2008Trajectory and Thramboulidis2013MDE are no longer current chapter citations; their handling is recorded as closed action history."],
]


SHEETS = [
    ("Claim Evidence Matrix", [["ID", "Thesis location", "Current report claim / citation use", "Citation key(s)", "Evidence source available", "Evidence summary / alignment check", "Claim match", "Matrix update / academic-review note", "Confidence"]] + CLAIMS),
    ("Equation Evidence", [["Equation / method", "Location", "Formula or method", "Citation link", "Evidence check", "Status", "Action"]] + EQUATIONS),
    ("Reference Coverage", [["Citation key", "Current chapter locations", "Local/source status", "Evidence alignment", "Action"]] + REFERENCES),
    ("Action Items", [["Priority", "Location", "Issue type", "Current status", "Recommendation"]] + ACTIONS),
    ("How To Use", [["Item", "Guidance"]] + HOW),
]


WIDTHS = {
    "Claim Evidence Matrix": [10, 24, 46, 30, 30, 58, 18, 46, 12],
    "Equation Evidence": [26, 22, 42, 34, 54, 18, 40],
    "Reference Coverage": [30, 30, 28, 56, 42],
    "Action Items": [12, 24, 28, 50, 58],
    "How To Use": [24, 90],
}


def col_name(n):
    name = ""
    while n:
        n, r = divmod(n - 1, 26)
        name = chr(65 + r) + name
    return name


def style_for(value, row):
    if row == 1:
        return 1
    text = str(value)
    if text == "OK" or text.startswith("OK "):
        return 3
    if "Partly OK" in text or "Missing local file" in text or text == "Medium":
        return 4
    if text == "High" or "Problem" in text:
        return 5
    if text == "Closed":
        return 6
    return 2


def sheet_xml(rows, widths):
    max_rows = len(rows)
    max_cols = max(len(row) for row in rows)
    dimension = f"A1:{col_name(max_cols)}{max_rows}"
    cols = "".join(
        f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>'
        for i, width in enumerate(widths, 1)
    )
    out = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
        f'<dimension ref="{dimension}"/>',
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
        'activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" '
        'activeCell="A2" sqref="A2"/></sheetView></sheetViews>',
        "<sheetFormatPr defaultRowHeight=\"15\"/>",
        f"<cols>{cols}</cols>",
        "<sheetData>",
    ]
    for r, row in enumerate(rows, 1):
        out.append(f'<row r="{r}" ht="{24 if r == 1 else 38}" customHeight="1">')
        for c, value in enumerate(row, 1):
            cell = f"{col_name(c)}{r}"
            out.append(
                f'<c r="{cell}" s="{style_for(value, r)}" t="inlineStr">'
                f"<is><t>{escape(str(value))}</t></is></c>"
            )
        out.append("</row>")
    out.extend(["</sheetData>", f'<autoFilter ref="{dimension}"/>', "</worksheet>"])
    return "".join(out)


def write_workbook():
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(1, len(SHEETS) + 1):
        content_types.append(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    content_types.append("</Types>")

    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
        + "".join(
            f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>'
            for i, (name, _) in enumerate(SHEETS, 1)
        )
        + "</sheets></workbook>"
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
            for i in range(1, len(SHEETS) + 1)
        )
        + f'<Relationship Id="rId{len(SHEETS) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        "</Relationships>"
    )
    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="3"><font><sz val="10"/><name val="Calibri"/></font><font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font><font><b/><sz val="10"/><name val="Calibri"/></font></fonts>
<fills count="6"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFE2F0D9"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FFF4CCCC"/><bgColor indexed="64"/></patternFill></fill></fills>
<borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border><border><left style="thin"><color rgb="FFD9E2F3"/></left><right style="thin"><color rgb="FFD9E2F3"/></right><top style="thin"><color rgb="FFD9E2F3"/></top><bottom style="thin"><color rgb="FFD9E2F3"/></bottom><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="7">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="2" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="2" fillId="5" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>"""
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<dc:title>Citation Claim Evidence Matrix</dc:title><dc:creator>Codex</dc:creator>"
        f'<cp:lastModifiedBy>Codex</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{CREATED}T00:00:00Z</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{CREATED}T00:00:00Z</dcterms:modified></cp:coreProperties>'
    )
    app = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
        "<Application>Codex XLSX writer</Application></Properties>"
    )

    with ZipFile(OUT, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "".join(content_types))
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/styles.xml", styles)
        zf.writestr("docProps/core.xml", core)
        zf.writestr("docProps/app.xml", app)
        for i, (name, rows) in enumerate(SHEETS, 1):
            zf.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(rows, WIDTHS[name]))


if __name__ == "__main__":
    write_workbook()
    print(f"Wrote {OUT}")
    print(f"Claim rows: {len(CLAIMS)}")
    print(f"Reference rows: {len(REFERENCES)}")
    print(f"Action rows: {len(ACTIONS)}")
