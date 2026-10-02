# MyProject_BracketManager

**Local Sports Tournament & Bracket Manager** (Problem Statement #54, Media, Events & Community)

Sushanth S Rao | PES1UG24CS485 | BPS54
PES University, Dept. of CSE, Software Engineering (UE24CS341A)

A tournament platform that generates single and double-elimination brackets, records live match scores, computes tiebreakers and publishes updated standings. Actors: Team Captain, Tournament Director (and Spectator for read-only views).

## Repository contents

| Folder | Contents |
|---|---|
| `1_RE` | Requirements table (5 FR, 2 NFR), use case diagram, UC-04 flow specification, Requirements Traceability Matrix |
| `2_Architecture` | Architecture diagram (layered architecture with MVC) |
| `3_Project_Creation_Screenshots` | GitHub repo creation, Jira Kanban and Scrum boards |
| `4_SRS_and_WBS` | Software Requirements Specification (IEEE 830 format) and Work Breakdown Structure |
| `5_Copilot_Code` | GitHub Copilot generated `validate_score` function and prompt screenshot |
| `6_Testing_Practice` | Bug report and testing exercise |

## Requirements summary

- FR-001: Generate seeded single/double elimination brackets
- FR-002: Team registration before deadline
- FR-003: Submit match score
- FR-004: Automatic winner advancement
- FR-005: Tiebreaker rules
- NFR-001: Standings update within 200 ms
- NFR-002: 99.5% uptime during tournament hours
