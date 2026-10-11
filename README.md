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
| `6_Testing_Practice` | Lab 4 (Vibe Coding): bug fix and new features for the Skyscraper Stack game, with before/after videos, updated code and chat history |

## Requirements summary

- FR-001: Generate seeded single/double elimination brackets
- FR-002: Team registration before deadline
- FR-003: Submit match score
- FR-004: Automatic winner advancement
- FR-005: Tiebreaker rules
- NFR-001: Standings update within 200 ms
- NFR-002: 99.5% uptime during tournament hours

## 6_Testing_Practice: Lab 4 (Vibe Coding)

Assigned repository: https://github.com/SETAPESU26/54_skyscrapper_stack

Skyscraper Stack is a Pygame tower stacking game. The assigned code had one bug and three features to add. Claude Code (in VS Code) was used to fix and extend it.

| Task | Change | File(s) |
|---|---|---|
| 1. Bug fix | The drop check was inverted (`overlap <= 0`), so good drops ended the game and misses kept going. Changed to `overlap > 0`. Restart now also works with Space, as the README says. | `game/game_engine.py` |
| 2. Perfect placement | A drop within a few pixels of the block below snaps into place without trimming, shows "PERFECT! +2", and restores some width after consecutive perfect drops. | `game/game_engine.py` |
| 3. Falling debris | The trimmed overhang becomes a piece that falls and spins off screen instead of disappearing. | `game/block.py`, `game/game_engine.py` |
| 4. Changing sky | The background is a gradient that shifts from day to sunset, twilight, night and space as the tower grows (every 8 floors). | `game/game_engine.py` |

Files:
- `Before_changes.mp4`: game running before any changes (10 s)
- `After_changes.mp4`: game running after the fix and all features (10 s)
- `main.py`, `game/`: updated code
- `Chat.pdf`: exported chat history with Claude Code

To run:

    cd 6_Testing_Practice
    pip install pygame
    python main.py

Controls: Space or left-click to drop a block, Space or R to restart after the tower collapses.
