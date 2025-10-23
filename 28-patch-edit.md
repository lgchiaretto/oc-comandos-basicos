# ✏️ Patch e Edit

Este documento contém comandos para editar e fazer patch em recursos do OpenShift.

---

## 📋 Índice

1. [Edit](#edit)
2. [Patch](#patch)
3. [Set Commands](#set-commands)
4. [Replace](#replace)

---

## ✏️ Edit

### Edit Básico
```bash ignore-test
# Editar deployment
oc edit deployment test-app
```

```bash ignore-test
# Editar service
oc edit svc test-app
```

```bash ignore-test
# Editar configmap
oc edit cm test-app
```

```bash ignore-test
# Editar com editor específico
EDITOR=nano oc edit deployment test-app
KUBE_EDITOR=vim oc edit deployment test-app
```

```bash ignore-test
# Editar em namespace específico
oc edit deployment test-app -n <namespace>
```

### Edit em Arquivo Temporário
```bash
# Export, edit, apply
oc get deployment test-app -o yaml > /tmp/deploy.yaml
vi /tmp/deploy.yaml
oc apply -f /tmp/deploy.yaml
```

```bash
# Ou com replace
oc replace -f /tmp/deploy.yaml
```

```bash
# Com force
oc replace -f /tmp/deploy.yaml --force
```

---

## 🔧 Patch

### Patch Types

#### Strategic Merge Patch
```bash
# Patch deployment replicas
oc patch deployment test-app -p '{"spec":{"replicas":3}}'
```

```bash
# Patch com type explicit
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

```bash
# Adicionar label
oc patch deployment test-app -p '{"metadata":{"labels":{"env":"production"}}}'
```

```bash
# Adicionar annotation
oc patch deployment test-app -p '{"metadata":{"annotations":{"description":"My app"}}}'
```

```bash ignore-test
# Atualizar imagem
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","image":"new-image:tag"}]}}}}'
```

```bash
# Múltiplos campos
oc patch deployment test-app --type merge -p '
{
  "spec": {
    "replicas": 3,
    "template": {
      "spec": {
        "containers": [{
          "name": "app",
          "resources": {
            "limits": {
              "cpu": "500m",
              "memory": "512Mi"
            }
          }
        }]
      }
    }
  }
}'
```

#### JSON Patch
```bash ignore-test
# Adicionar elemento a array
oc patch deployment test-app --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"NEW_VAR","value":"new_value"}}]'
```

```bash ignore-test
# Remover elemento
oc patch deployment test-app --type json -p='[{"op":"remove","path":"/spec/template/spec/containers/0/env/0"}]'
```

```bash ignore-test
# Replace elemento
oc patch deployment test-app --type json -p='[{"op":"replace","path":"/spec/replicas","value":5}]'
```

```bash
# Múltiplas operações
oc patch deployment test-app --type json -p='[
  {"op":"replace","path":"/spec/replicas","value":3},
  {"op":"add","path":"/metadata/labels/team","value":"backend"}
]'
```

#### JSON Merge Patch
```bash
# Merge simples (sobrescreve)
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

```bash
# Remover campo (set to null)
oc patch deployment test-app --type merge -p '{"metadata":{"annotations":{"old-annotation":null}}}'
```

### Patch de Recursos Comuns

#### Deployments
```bash
# Replicas
oc patch deployment test-app -p '{"spec":{"replicas":5}}'
```

```bash
# Strategy
oc patch deployment test-app -p '{"spec":{"strategy":{"type":"RollingUpdate","rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
```

```bash ignore-test
# Image
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container>","image":"new-image:v2"}]}}}}'
```

```bash ignore-test
# Resources
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","resources":{"limits":{"memory":"1Gi","cpu":"1000m"},"requests":{"memory":"512Mi","cpu":"500m"}}}]}}}}'
```

```bash ignore-test
# Environment variable
oc patch deployment test-app --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"LOG_LEVEL","value":"debug"}}]'
```

#### Services
```bash ignore-test
# Port
oc patch svc test-app -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
```

```bash
# Type
oc patch svc test-app -p '{"spec":{"type":"NodePort"}}'
```

```bash
# Selector
oc patch svc test-app -p '{"spec":{"selector":{"app":"new-app"}}}'
```

#### ConfigMaps
```bash
# Atualizar data
oc patch cm test-app -p '{"data":{"key1":"new-value"}}'
```

```bash
# Adicionar nova chave
oc patch cm test-app --type merge -p '{"data":{"new-key":"new-value"}}'
```

```bash ignore-test
# Remover chave
oc patch cm test-app --type json -p='[{"op":"remove","path":"/data/old-key"}]'
```

#### Routes
```bash
# Mudar host
oc patch route test-app -p '{"spec":{"host":"new-hostname.example.com"}}'
```

```bash
# Adicionar TLS
oc patch route test-app -p '{"spec":{"tls":{"termination":"edge"}}}'
```

```bash
# Mudar service target
oc patch route test-app -p '{"spec":{"to":{"name":"new-service"}}}'
```

#### HPA
```bash
# Min/Max replicas
oc patch hpa test-app -p '{"spec":{"minReplicas":2,"maxReplicas":10}}'
```

```bash
# Target CPU
oc patch hpa test-app -p '{"spec":{"targetCPUUtilizationPercentage":70}}'
```

### Patch em Lote
```bash
# Patch múltiplos deployments
for deploy in $(oc get deploy -o name); do
  oc patch $deploy -p '{"metadata":{"labels":{"env":"production"}}}'
done
```

```bash
# Patch todos os deployments com label
oc get deploy -l app=myapp -o name | xargs -I {} oc patch {} -p '{"spec":{"replicas":3}}'
```

```bash ignore-test
# Patch com filter
oc get deploy -o json | jq -r '.items[] | select(.spec.replicas < 2) | .metadata.name' | \
while read deploy; do
  oc patch deployment $deploy -p '{"spec":{"replicas":2}}'
done
```

---

## ⚙️ Set Commands

### Set Image
```bash ignore-test
# Deployment
oc set image deployment/test-app <container-name>=<new-image>:<tag>
```

```bash
# Exemplo
oc set image deployment/myapp myapp=myapp:v2.0
```

```bash
# Múltiplos containers
oc set image deployment/test-app container1=image1:v2 container2=image2:v2
```

```bash ignore-test
# DeploymentConfig
oc set image dc/test-app <container-name>=<new-image>
```

```bash ignore-test
# Verificar
oc get deployment/test-app -o jsonpath='{.spec.template.spec.containers[0].image}'
```

### Set Resources
```bash
# Requests e limits
oc set resources deployment/test-app --limits=cpu=500m,memory=512Mi --requests=cpu=250m,memory=256Mi
```

```bash
# Apenas limits
oc set resources deployment/test-app --limits=cpu=1,memory=1Gi
```

```bash
# Apenas requests
oc set resources deployment/test-app --requests=cpu=100m,memory=128Mi
```

```bash ignore-test
# Container específico
oc set resources deployment/test-app -c=<container-name> --limits=cpu=200m,memory=256Mi
```

```bash
# Remover limits
oc set resources deployment/test-app --limits=cpu=0,memory=0
```

### Set Env
```bash
# Adicionar variável
oc set env deployment/test-app KEY=value
```

```bash
# Múltiplas variáveis
oc set env deployment/test-app KEY1=value1 KEY2=value2
```

```bash ignore-test
# De ConfigMap
oc set env deployment/test-app --from=configmap/<cm-name>
```

```bash ignore-test
# De Secret
oc set env deployment/test-app --from=secret/<secret-name>
```

```bash ignore-test
# Chave específica de CM
oc set env deployment/test-app KEY --from=configmap/<cm-name> --keys=specific-key
```

```bash
# Remover variável
oc set env deployment/test-app KEY-
```

```bash
# Listar variáveis
oc set env deployment/test-app --list
```

### Set Volumes
```bash ignore-test
# Adicionar volume de ConfigMap
oc set volume deployment/test-app --add --name=config-vol --type=configmap --configmap-name=<cm-name> --mount-path=/etc/config
```

```bash ignore-test
# Adicionar volume de Secret
oc set volume deployment/test-app --add --name=secret-vol --type=secret --secret-name=<secret-name> --mount-path=/etc/secret
```

```bash ignore-test
# Adicionar PVC
oc set volume deployment/test-app --add --name=data-vol --type=persistentVolumeClaim --claim-name=<pvc-name> --mount-path=/data
```

```bash
# EmptyDir
oc set volume deployment/test-app --add --name=tmp-vol --type=emptyDir --mount-path=/tmp
```

```bash ignore-test
# Remover volume
oc set volume deployment/test-app --remove --name=<volume-name>
```

```bash
# Listar volumes
oc set volume deployment/test-app
```

### Set Probe
```bash
# Liveness probe
oc set probe deployment/test-app --liveness --get-url=http://:8080/health --initial-delay-seconds=30
```

```bash
# Readiness probe
oc set probe deployment/test-app --readiness --get-url=http://:8080/ready --period-seconds=10
```

```bash
# TCP probe
oc set probe deployment/test-app --liveness --open-tcp=8080 --timeout-seconds=1
```

```bash
# Exec probe
oc set probe deployment/test-app --liveness --exec -- cat /tmp/healthy
```

```bash
# Remover probe
oc set probe deployment/test-app --liveness --remove
oc set probe deployment/test-app --readiness --remove
```

### Set ServiceAccount
```bash ignore-test
# Definir ServiceAccount
oc set serviceaccount deployment/test-app <sa-name>
```

```bash
# Exemplo
oc set serviceaccount deployment/myapp mysa
```

### Set Selector
```bash
# Service selector
oc set selector svc/test-app app=myapp,tier=frontend
```

```bash
# Overwrite
oc set selector svc/test-app app=newapp --overwrite
```

---

## 🔄 Replace

### Replace vs Apply
```bash
# Apply (merge)
oc apply -f resource.yaml
```

```bash
# Replace (substitui completamente)
oc replace -f resource.yaml
```

```bash
# Replace com force (deleta e recria)
oc replace -f resource.yaml --force
```

```bash
# Replace de stdin
cat resource.yaml | oc replace -f -
```

```bash
# Get, edit, replace
oc get deployment/test-app -o yaml > /tmp/deploy.yaml
vi /tmp/deploy.yaml
oc replace -f /tmp/deploy.yaml
```

### Replace em Massa
```bash
# Replace múltiplos recursos
oc replace -f directory/
```

```bash
# Replace recursivo
oc replace -f directory/ -R
```

```bash
# Replace com dry-run
oc replace -f resource.yaml --dry-run=client
```

---

## 📖 Navegação

- [← Anterior: Backup e Disaster Recovery](27-backup-disaster-recovery.md)
- [→ Próximo: Jobs e CronJobs](29-jobs-cronjobs.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
