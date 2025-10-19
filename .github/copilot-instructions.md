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
