# 📦 Deployments e Scaling

Este documento contém comandos para gerenciar deployments, scaling e rollouts no OpenShift.

---

## 📋 Índice

- [📦 Deployments e Scaling](#-deployments-e-scaling)
  - [📋 Índice](#-índice)
  - [📏 Scaling](#-scaling)
    - [Manual](#manual)
    - [Autoscaling (HPA)](#autoscaling-hpa)
  - [🔄 Atualizações e Rollbacks](#-atualizações-e-rollbacks)
    - [Atualizar Imagem](#atualizar-imagem)
    - [Pausar e Retomar](#pausar-e-retomar)
    - [Rollback](#rollback)
  - [📦 ReplicaSets](#-replicasets)
  - [📖 Navegação](#-navegação)

---

## 📏 Scaling

### Manual
```bash
# Escalar deployment manualmente para 3
oc scale deployment test-app --replicas=3
```

```bash ignore-test
# Escalar deployment config
oc scale dc <nome-do-dc> --replicas=<numero>
```

### Autoscaling (HPA)
```bash
# Criar Horizontal Pod Autoscaler
oc autoscale deployment test-app --min=2 --max=10 --cpu-percent=80
```

```bash
# Ver autoscalers
oc get hpa
```

```bash
# Descrever HPA
oc describe hpa test-app
```

```bash
# Deletar autoscaler
oc delete hpa test-app
```
---

## 🔄 Atualizações e Rollbacks

### Atualizar Imagem
```bash
# Atualizar imagem do deployment (deployment/deploy-name container-name=image)
oc set image deployment/test-app httpd=httpd:2.4
```

```bash
# Ver histórico de rollouts
oc rollout history deployment/test-app
```

```bash
# Ver status do rollout
oc rollout status deployment/test-app
```

### Pausar e Retomar
```bash
# Pausar rollout
oc rollout pause deployment/test-app
```

```bash
# Retomar rollout
oc rollout resume deployment/test-app
```

```bash
# Reiniciar deployment (recrear pods)
oc rollout restart deployment/test-app
```

### Rollback
```bash
# Fazer rollback para revisão anterior
oc rollout undo deployment/test-app
```

```bash
# Fazer rollback para revisão específica
oc rollout undo deployment/test-app --to-revision=2
```

```bash
# Ver detalhes de uma revisão
oc rollout history deployment/test-app --revision=2
```

---

## 📦 ReplicaSets

```bash
# Listar replicasets
oc get replicasets
oc get rs
```

```bash ignore-test
# Descrever replicaset
oc describe rs <nome-do-rs>
```

```bash
# Ver replica sets de um deployment
oc get rs -l app=test-app
```

```bash ignore-test
# Deletar replicaset
oc delete rs <nome-do-rs>
```

---

## 📖 Navegação

- [← Anterior: Pods e Containers](04-pods-containers.md)
- [→ Próximo: Services e Routes](06-services-routes.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
