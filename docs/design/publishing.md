# Public documents

## 1. Responsibilities

- Defines what the public repository's README and license contain.
- Keeps the introduction and first-use instructions consistent with the available rules.

## 2. Public interface

### The README

The README is in English and covers five subjects:

- What plumbline is: rules for developing in three layers, intent, design and impl. An AI reads the rules and reproduces a setup for a project using the tools available there.
- How to start: choose a rules tag or commit and keep a copy outside the project; ask the project's AI to reproduce from that repository and version. On first use, confirm intent and the module map with the user, complete layer locations, git exclusions and role settings, and agree on the workflow before reproduction. Later changes to settings or the rules commit require reproduction again.
- What the setup provides: lead is the only built-in role; the project defines the other roles, their read and write zones, duties and models, and how work and the five checks are assigned. Zones can use paths, file-name patterns and file parts, and roles may share zones. The setup delivers role-specific instructions, the role guard, validate on user request, the design template and a setup record. Every non-lead role is forbidden to read intent or its copies and to change design. The project chooses zone enforcement and shell inspection. The record distinguishes tested mechanical coverage from instruction-only limits; a requested guard is not proof of coverage. Runners, connectors and renderers are chosen during reproduction for the available environment.
- How the repository is organized: where to find the rules, conformance cases, design and license.
- The license's name.

If role or workflow examples are included, identify them as project choices. They must not imply a default roster, fixed checking role, required lighter model or one workflow for every project. Explain only enough of the guard choices and recorded limits to distinguish the required permissions from the enforcement available in a particular setup; refer to the rules for the contracts.

### The license

- MIT-0.
- Copyright notice: Jonghyeok Eun, 2026.

## 3. Flow

None.

## 4. Invariants and contracts

- The README describes only what is available at the current commit.
- The README never points to plumbline's intent or copies its content. It may explain intent as a layer of a target project.
- The README presents reproduced project tools as outputs of the rules, not as a distributed executable or plugin.
- The README does not promise mechanical enforcement for every tool or operation. Role permissions remain instructions outside the checked coverage.

## 5. Decisions and reasons

- English serves visitors to the public repository.
- The introduction names the project's role and workflow choices because they must be settled before a usable setup can be reproduced.
- Stating enforcement limits avoids confusing a guard setting with a demonstrated tool restriction.
- MIT-0 permits carrying the rules into project files without requiring a copyright notice on those copies.

## 6. Verification criteria

- Every repository file and folder referenced in the README exists in the current commit.
- All five subjects are covered. First-use instructions include the confirmed module map, complete role settings and agreed workflow before reproduction.
- Role and workflow descriptions agree with Layers and settings, Roles and A change: only lead is built in, permissions and models are project-defined, and the five checks have project-assigned coverage.
- Descriptions of setup outputs and enforcement agree with Reproduction and Setup record. Examples do not introduce defaults or imply untested mechanical coverage. Validate is described as running on user request.
- The license contains the MIT-0 text and the copyright notice above.

## 7. Out of scope

None.
