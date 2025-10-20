# OpenShift Commands Reference Guide - AI Instructions

## Project Overview
This repository is a **comprehensive Portuguese-language reference guide** for OpenShift (OCP) commands, organized into 30 modular documentation files. It serves as a quick-reference manual for developers, administrators, and DevOps engineers working with OpenShift 4.x clusters.

## Repository Structure

### Documentation Organization
- **Numbered files (01-30)**: Topical command reference documents, each focusing on a specific OpenShift domain
- **README.md**: Main navigation index with categorized links and quick reference commands
- **ESTRUTURA.md**: Project structure documentation explaining the modular organization
- **INICIO-RAPIDO.md**: Quick-start guide with the top 20 most-used commands
- **comandos-openshift-ORIGINAL-COMPLETO.md**: Original monolithic reference (kept for historical purposes)

### Test Infrastructure (AUTO-GENERATED!)
- **tests/**: Modular test suite for validating all documented commands
  - **tests/lib/common.sh**: Shared functions library for all test modules
  - **tests/01-...-30-*/**: Individual test modules (one per documentation file) - **AUTO-GENERATED**
  - **tests/README.md**: Complete testing documentation
- **test-commands.sh**: Main test orchestrator script
- **generate-all-tests.py**: 🤖 **Auto-generator script** - Regenerates ALL test modules from markdown files
- **GENERATE-TESTS-README.md**: Complete documentation for the auto-generator

### Content Categories
1. **Essential Commands (01-03)**: Authentication, projects, applications
2. **Resources & Workloads (04-06)**: Pods, deployments, services, routes
3. **Configuration (07-08)**: ConfigMaps, Secrets, Storage
4. **Build & CI/CD (09-10)**: BuildConfigs, ImageStreams, Registry
5. **Observability (11-12)**: Monitoring, logs, must-gather
6. **Troubleshooting (13-15)**: Pods, networking, storage issues
7. **Security & RBAC (16-18)**: Permissions, groups, SCC
8. **Advanced Admin (19-22)**: Cluster operators, nodes, certificates, networking
9. **Utilities (23-26)**: Custom commands with awk/jq, field selectors, formatting, templates
10. **Operations (27-30)**: Backup/restore, patching, jobs, operators

## Content Conventions

### Document Structure Pattern
Every numbered document follows this template:
```markdown
# 🎯 [Topic Title]

Brief description of the topic

---

## 📋 Índice
[Table of contents with anchor links]

---

## 🔧 [Section Title]

### [Subsection]
```bash
# Comment explaining the command
oc command --flags args

# Practical example
oc specific-example
```
```

### Key Patterns
- **Language**: All documentation is in Portuguese (Brazil)
- **Emojis**: Used consistently for visual navigation (🔐 for auth, 🐳 for pods, 🛠️ for utilities, etc.)
- **Code blocks**: Always use triple backticks with `bash` language identifier
- **Comments**: Every command includes explanatory comments starting with `#`
- **Examples**: "Exemplo" or "Exemplo prático" labels practical use cases
- **Navigation**: Footer links to previous/next documents (when applicable)

### Command Presentation Style
- Show basic command first, then variations with increasing complexity
- Group related commands in subsections
- Include both simple flags (`-A`) and long flags (`--all-namespaces`) for clarity
- Demonstrate pipes with Unix tools (grep, awk, jq) in appropriate sections

## Working with This Codebase

### When Adding New Commands
1. Identify the correct numbered document based on topic (refer to ESTRUTURA.md categories)
2. Place command under the most specific relevant section heading
3. Add explanatory comment above the command
4. Provide a practical example with real-world context
5. Maintain consistent emoji usage and formatting

### When Creating New Documents
1. Follow the numbering scheme (01-30) established in README.md
2. Use the standard document template (see "Document Structure Pattern" above)
3. Update README.md index to link to the new document
4. Add navigation footer with links to previous/next topics
5. Include "Última atualização" and "Versão" footer

### When Referencing Commands
- The most frequently used commands are in **INICIO-RAPIDO.md**
- Advanced automation patterns (awk/jq/pipes) are in **23-comandos-customizados.md**
- Field selectors and filtering techniques are in **24-field-selectors.md**
- JSONPath and output formatting are in **25-output-formatacao.md**

### Troubleshooting Command Patterns
Common troubleshooting workflows are distributed across specialized docs:
- **13-troubleshooting-pods.md**: Pod issues (CrashLoopBackOff, OOMKilled, ImagePullBackOff)
- **14-troubleshooting-rede.md**: Network connectivity, DNS, service discovery
- **15-troubleshooting-storage.md**: PVC binding issues, storage class problems
- **12-must-gather.md**: Diagnostic data collection for Red Hat support

### OpenShift-Specific Knowledge
- This is **OpenShift CLI (`oc`)**, not vanilla Kubernetes (`kubectl`)
- OpenShift-specific concepts: Projects (vs namespaces), Routes (vs Ingress), BuildConfigs, ImageStreams
- Commands often reference cluster operators (`oc get co`), Machine API, and OLM (Operator Lifecycle Manager)
- Security Context Constraints (SCC) are OpenShift's alternative to Pod Security Policies
- CSR (Certificate Signing Request) approval is a common admin task: `oc get csr | grep Pending | awk '{print $1}' | xargs oc adm certificate approve`

## AI Agent Guidance

When assisting users:
1. **Respect the Portuguese language** - maintain all text in Portuguese unless explicitly asked otherwise
2. **Preserve existing formatting** - keep emojis, code block styles, and structural patterns
3. **Cross-reference appropriately** - mention related documents when commands span multiple topics
4. **Real-world context** - commands in this guide are production-tested; preserve practical examples
5. **Modular mindset** - avoid creating massive single files; distribute content across the 30-document structure
6. **Test-driven updates** - when adding/modifying commands in documentation, also update the corresponding test module

## Test Suite Workflow

### 🤖 AUTOMATED TEST GENERATION (RECOMMENDED)

**The preferred workflow is to use the auto-generator:**

1. **Edit markdown files (01-30)** - Add/modify/remove commands
2. **Run the auto-generator:**
   ```bash
   python3 generate-all-tests.py
   ```
3. **Validate changes:**
   ```bash
   ./test-commands.sh --module XX  # Test specific module
   ./test-commands.sh              # Test everything
   ```
4. **Commit both files** - The `.md` and the auto-generated `test.sh`

**Key Benefits:**
- ✅ Perfect synchronization between docs and tests
- ✅ Automatic command sanitization (error handling)
- ✅ Automatic filtering of invalid commands (placeholders)
- ✅ Saves hours of manual work
- ✅ Reduces human error

**Read GENERATE-TESTS-README.md for complete documentation.**

### Manual Test Updates (Legacy Method)

Only use manual editing when the auto-generator doesn't produce the desired result:


1. Add the command to the appropriate markdown file (01-30)
2. Update the corresponding test script in `tests/XX-topic/test.sh`
3. Run the specific test module: `./test-commands.sh --module XX`
4. Fix any issues and run full suite: `./test-commands.sh`

### When Modifying Commands
1. Update the markdown documentation
2. Update the test script with the new command syntax
3. Test the specific module first
4. Run full validation suite

### Test Script Structure
Each test module (`tests/XX-topic/test.sh`) follows this pattern:
```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "XX - TOPIC NAME"

run_test "Test description" \
    "oc command to execute"
```

### Regenerating All Test Modules
If you make bulk changes to commands:
```bash
python3 generate-all-tests.py
```

### Running Tests
- All tests: `./test-commands.sh`
- Specific module: `./test-commands.sh --module 05`
- Verbose mode: `./test-commands.sh --verbose`
- Stop on first error: `./test-commands.sh --stop-on-error`

## Critical Maintenance Rules

1. **Documentation + Tests = One Change**
   - Never update docs without updating tests
   - Never update tests without validating against cluster
   
2. **Validation Before Commit**
   - Always run `./test-commands.sh` before committing
   - Target success rate: >95%
   
3. **Modular Organization**
   - Keep tests in their respective module directories
   - Use `tests/lib/common.sh` for shared functions
   - Don't create monolithic test files

4. **Error Handling**
   - Use `|| true` for commands that may legitimately fail
   - Use `2>/dev/null` to suppress expected errors
   - Document why certain tests are skipped

   ## Additional Notes
   - Remove all scripts generated by Copilot after use
   - run ./test-commands.sh with no parameter to validate all changes (it will take time)
