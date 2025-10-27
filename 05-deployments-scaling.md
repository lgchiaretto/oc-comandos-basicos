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
**Ajustar número de réplicas do deployment/replicaset**


```bash
oc scale deployment test-app --replicas=3
```

**Escalar deployment config**

```bash ignore-test
oc scale dc <nome-do-dc> --replicas=<numero>
```

### Autoscaling (HPA)
**Criar Horizontal Pod Autoscaler (HPA) para escalar automaticamente**


```bash
oc autoscale deployment test-app --min=2 --max=10 --cpu-percent=80
```

**Listar Horizontal Pod Autoscalers configurados**

```bash
oc get hpa
```

**Exibir detalhes completos do horizontal pod autoscaler**


```bash
oc describe hpa test-app
```

**Deletar o horizontal pod autoscaler especificado**


```bash
oc delete hpa test-app
```
---

## Atualizações e Rollbacks

### Atualizar Imagem
**Atualizar imagem do container no deployment/pod**


```bash
oc set image deployment/test-app httpd=httpd:2.4
```

**Exibir histórico de revisões do deployment**


```bash
oc rollout history deployment/test-app
```

**Verificar status do rollout em andamento**


```bash
oc rollout status deployment/test-app
```

### Pausar e Retomar
**Pausar rollout do deployment (impede novas atualizações)**


```bash
oc rollout pause deployment/test-app
```

**Retomar rollout pausado do deployment**


```bash
oc rollout resume deployment/test-app
```

**Reiniciar deployment (recria todos os pods)**


```bash
oc rollout restart deployment/test-app
```

### Rollback
**Fazer rollback para revisão anterior do deployment**


```bash
oc rollout undo deployment/test-app
```

**Fazer rollback para revisão específica**


```bash
oc rollout undo deployment/test-app --to-revision=1
```

**Exibir detalhes de revisão específica**


```bash
oc rollout history deployment/test-app --revision=3
```

---

## ReplicaSets

**Listar todos os ReplicaSets do namespace**

```bash
oc get replicasets
oc get rs
```

**Descrever replicaset**

```bash ignore-test
oc describe rs <nome-do-rs>
```

**Listar replicaset filtrados por label**

```bash
oc get rs -l app=test-app
```

**Deletar replicaset**

```bash ignore-test
oc delete rs <nome-do-rs>
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/deployments">Building applications - Deployments</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes - Autoscaling</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes - Managing pods</a>
---


## Navegação

- [← Anterior: Pods e Containers](04-pods-containers.md)
- [→ Próximo: Services e Routes](06-services-routes.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
