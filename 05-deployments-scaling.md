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
# Ajustar número de réplicas do deployment/replicaset
# oc scale deployment <deployment-name> --replicas=3
oc scale deployment test-app --replicas=3
```

```bash ignore-test
# Escalar deployment config
oc scale dc <nome-do-dc> --replicas=<numero>
```

### Autoscaling (HPA)
```bash
# Criar Horizontal Pod Autoscaler (HPA) para escalar automaticamente
# oc autoscale deployment <deployment-name> --min=2 --max=10 --cpu-percent=80
oc autoscale deployment test-app --min=2 --max=10 --cpu-percent=80
```

```bash
# Listar Horizontal Pod Autoscalers configurados
oc get hpa
```

```bash
# Exibir detalhes completos do horizontal pod autoscaler
# oc describe hpa <resource-name>
oc describe hpa test-app
```

```bash
# Deletar o horizontal pod autoscaler especificado
# oc delete hpa <resource-name>
oc delete hpa test-app
```
---

## Atualizações e Rollbacks

### Atualizar Imagem
```bash
# Atualizar imagem do container no deployment/pod
# oc set image <resource-name>/test-app httpd=httpd:2.4
oc set image deployment/test-app httpd=httpd:2.4
```

```bash
# Exibir histórico de revisões do deployment
# oc rollout history <resource-name>/test-app
oc rollout history deployment/test-app
```

```bash
# Verificar status do rollout em andamento
# oc rollout status <resource-name>/test-app
oc rollout status deployment/test-app
```

### Pausar e Retomar
```bash
# Pausar rollout do deployment (impede novas atualizações)
# oc rollout pause <resource-name>/test-app
oc rollout pause deployment/test-app
```

```bash
# Retomar rollout pausado do deployment
# oc rollout resume <resource-name>/test-app
oc rollout resume deployment/test-app
```

```bash
# Reiniciar deployment (recria todos os pods)
# oc rollout restart <resource-name>/test-app
oc rollout restart deployment/test-app
```

### Rollback
```bash
# Fazer rollback para revisão anterior do deployment
# oc rollout undo <resource-name>/test-app
oc rollout undo deployment/test-app
```

```bash
# Fazer rollback para revisão específica
# oc rollout undo <resource-name>/test-app --to-revision=1
oc rollout undo deployment/test-app --to-revision=1
```

```bash
# Exibir detalhes de revisão específica
# oc rollout history <resource-name>/test-app --revision=3
oc rollout history deployment/test-app --revision=3
```

---

## ReplicaSets

```bash
# Listar todos os ReplicaSets do namespace
oc get replicasets
oc get rs
```

```bash ignore-test
# Descrever replicaset
oc describe rs <nome-do-rs>
```

```bash
# Listar replicaset filtrados por label
oc get rs -l app=test-app
```

```bash ignore-test
# Deletar replicaset
oc delete rs <nome-do-rs>
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/deployments">Building applications - Deployments</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes - Autoscaling</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes - Managing pods</a>
---

---

## Navegação

- [← Anterior: Pods e Containers](04-pods-containers.md)
- [→ Próximo: Services e Routes](06-services-routes.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
