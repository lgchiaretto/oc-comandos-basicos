# Deployments e Scaling

Este documento contém comandos para gerenciar deployments, scaling e rollouts no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Scaling](#scaling)
3. [Atualizações e Rollbacks](#atualizações-e-rollbacks)
4. [ReplicaSets](#replicasets)
5. [Documentação Oficial](#documentação-oficial)
6. [Navegação](#navegação)
---

## Scaling

### Manual
```bash
# Escalar deployment manualmente para 3
# oc scale deployment <deployment-name> --replicas=3
oc scale deployment test-app --replicas=3
```

```bash ignore-test
# Escalar deployment config
oc scale dc <nome-do-dc> --replicas=<numero>
```

### Autoscaling (HPA)
```bash
# Criar Horizontal Pod Autoscaler
# oc autoscale deployment <deployment-name> --min=2 --max=10 --cpu-percent=80
oc autoscale deployment test-app --min=2 --max=10 --cpu-percent=80
```

```bash
# Ver autoscalers
oc get hpa
```

```bash
# Descrever HPA
# oc describe hpa <resource-name>
oc describe hpa test-app
```

```bash
# Deletar autoscaler
# oc delete hpa <resource-name>
oc delete hpa test-app
```
---

## Atualizações e Rollbacks

### Atualizar Imagem
```bash
# Atualizar imagem do deployment (deployment/deploy-name container-name=image)
# oc set image <resource-name>/test-app httpd=httpd:2.4
oc set image deployment/test-app httpd=httpd:2.4
```

```bash
# Ver histórico de rollouts
# oc rollout history <resource-name>/test-app
oc rollout history deployment/test-app
```

```bash
# Ver status do rollout
# oc rollout status <resource-name>/test-app
oc rollout status deployment/test-app
```

### Pausar e Retomar
```bash
# Pausar rollout
# oc rollout pause <resource-name>/test-app
oc rollout pause deployment/test-app
```

```bash
# Retomar rollout
# oc rollout resume <resource-name>/test-app
oc rollout resume deployment/test-app
```

```bash
# Reiniciar deployment (recrear pods)
# oc rollout restart <resource-name>/test-app
oc rollout restart deployment/test-app
```

### Rollback
```bash
# Fazer rollback para revisão anterior
# oc rollout undo <resource-name>/test-app
oc rollout undo deployment/test-app
```

```bash
# Fazer rollback para revisão específica
# oc rollout undo <resource-name>/test-app --to-revision=1
oc rollout undo deployment/test-app --to-revision=1
```

```bash
# Ver detalhes de uma revisão
# oc rollout history <resource-name>/test-app --revision=3
oc rollout history deployment/test-app --revision=3
```

---

## ReplicaSets

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


## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/deployments" target="_blank">Building applications - Deployments</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/pods" target="_blank">Nodes - Working with pods</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration" target="_blank">Post-installation configuration</a>

---

## Navegação

- [← Anterior: Pods e Containers](04-pods-containers.md)
- [→ Próximo: Services e Routes](06-services-routes.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
