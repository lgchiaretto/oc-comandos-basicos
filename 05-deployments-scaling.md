# 📦 Deployments e Scaling

Este documento contém comandos para gerenciar deployments, scaling e rollouts no OpenShift.

---

## 📋 Índice

1. [Deployments](#deployments)
2. [Scaling](#scaling)
3. [Atualizações e Rollbacks](#atualizações-e-rollbacks)
4. [ReplicaSets](#replicasets)
5. [Autoscaling](#autoscaling)

---

## 🚀 Deployments

### Básico
```bash
# Listar deployments
oc get deployments
oc get deploy

# Descrever deployment
oc describe deployment <nome-do-deployment>

# Ver deployment em YAML
oc get deployment <nome-do-deployment> -o yaml

# Criar deployment
oc create deployment <nome> --image=<imagem>

# Editar deployment
oc edit deployment <nome-do-deployment>

# Deletar deployment
oc delete deployment <nome-do-deployment>
```

---

## 📏 Scaling

### Manual
```bash
# Escalar deployment manualmente
oc scale deployment <nome-do-deployment> --replicas=<numero>

# Escalar deployment config
oc scale dc <nome-do-dc> --replicas=<numero>

# Exemplo
oc scale deployment nginx --replicas=5
```

### Autoscaling (HPA)
```bash
# Criar Horizontal Pod Autoscaler
oc autoscale deployment <nome> --min=2 --max=10 --cpu-percent=80

# Ver autoscalers
oc get hpa

# Descrever HPA
oc describe hpa <nome>

# Deletar autoscaler
oc delete hpa <nome>

# Exemplo completo
oc autoscale deployment myapp --min=3 --max=20 --cpu-percent=75
```

---

## 🔄 Atualizações e Rollbacks

### Atualizar Imagem
```bash
# Atualizar imagem do deployment
oc set image deployment/<nome-do-deployment> <container>=<nova-imagem>

# Exemplo
oc set image deployment/nginx nginx=nginx:1.21

# Ver histórico de rollouts
oc rollout history deployment/<nome-do-deployment>

# Ver status do rollout
oc rollout status deployment/<nome-do-deployment>
```

### Pausar e Retomar
```bash
# Pausar rollout
oc rollout pause deployment/<nome-do-deployment>

# Retomar rollout
oc rollout resume deployment/<nome-do-deployment>

# Reiniciar deployment (recrear pods)
oc rollout restart deployment/<nome-do-deployment>
```

### Rollback
```bash
# Fazer rollback para revisão anterior
oc rollout undo deployment/<nome-do-deployment>

# Fazer rollback para revisão específica
oc rollout undo deployment/<nome-do-deployment> --to-revision=<numero>

# Ver detalhes de uma revisão
oc rollout history deployment/<nome> --revision=2
```

---

## 📦 ReplicaSets

```bash
# Listar replicasets
oc get replicasets
oc get rs

# Descrever replicaset
oc describe rs <nome-do-rs>

# Ver replica sets de um deployment
oc get rs -l app=<nome-da-app>

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
