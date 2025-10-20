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
```bash
# Editar deployment
oc edit deployment <nome>
```

```bash
# Editar service
oc edit svc <nome>
```

```bash
# Editar configmap
oc edit cm <nome>
```

```bash
# Editar com editor específico
EDITOR=nano oc edit deployment <nome>
KUBE_EDITOR=vim oc edit deployment <nome>
```

```bash
# Editar em namespace específico
oc edit deployment <nome> -n <namespace>
```

### Edit em Arquivo Temporário
```bash
# Export, edit, apply
oc get deployment <nome> -o yaml > /tmp/deploy.yaml
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
oc patch deployment <nome> -p '{"spec":{"replicas":3}}'
```

```bash
# Patch com type explicit
oc patch deployment <nome> --type merge -p '{"spec":{"replicas":3}}'
```

```bash
# Adicionar label
oc patch deployment <nome> -p '{"metadata":{"labels":{"env":"production"}}}'
```

```bash
# Adicionar annotation
oc patch deployment <nome> -p '{"metadata":{"annotations":{"description":"My app"}}}'
```

```bash
# Atualizar imagem
oc patch deployment <nome> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","image":"new-image:tag"}]}}}}'
```

```bash
# Múltiplos campos
oc patch deployment <nome> --type merge -p '
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
```bash
# Adicionar elemento a array
oc patch deployment <nome> --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"NEW_VAR","value":"new_value"}}]'
```

```bash
# Remover elemento
oc patch deployment <nome> --type json -p='[{"op":"remove","path":"/spec/template/spec/containers/0/env/0"}]'
```

```bash
# Replace elemento
oc patch deployment <nome> --type json -p='[{"op":"replace","path":"/spec/replicas","value":5}]'
```

```bash
# Múltiplas operações
oc patch deployment <nome> --type json -p='[
  {"op":"replace","path":"/spec/replicas","value":3},
  {"op":"add","path":"/metadata/labels/team","value":"backend"}
]'
```

#### JSON Merge Patch
```bash
# Merge simples (sobrescreve)
oc patch deployment <nome> --type merge -p '{"spec":{"replicas":3}}'
```

```bash
# Remover campo (set to null)
oc patch deployment <nome> --type merge -p '{"metadata":{"annotations":{"old-annotation":null}}}'
```

### Patch de Recursos Comuns

#### Deployments
```bash
# Replicas
oc patch deployment <nome> -p '{"spec":{"replicas":5}}'
```

```bash
# Strategy
oc patch deployment <nome> -p '{"spec":{"strategy":{"type":"RollingUpdate","rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
```

```bash
# Image
oc patch deployment <nome> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container>","image":"new-image:v2"}]}}}}'
```

```bash
# Resources
oc patch deployment <nome> -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","resources":{"limits":{"memory":"1Gi","cpu":"1000m"},"requests":{"memory":"512Mi","cpu":"500m"}}}]}}}}'
```

```bash
# Environment variable
oc patch deployment <nome> --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"LOG_LEVEL","value":"debug"}}]'
```

#### Services
```bash
# Port
oc patch svc <nome> -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
```

```bash
# Type
oc patch svc <nome> -p '{"spec":{"type":"NodePort"}}'
```

```bash
# Selector
oc patch svc <nome> -p '{"spec":{"selector":{"app":"new-app"}}}'
```

#### ConfigMaps
```bash
# Atualizar data
oc patch cm <nome> -p '{"data":{"key1":"new-value"}}'
```

```bash
# Adicionar nova chave
oc patch cm <nome> --type merge -p '{"data":{"new-key":"new-value"}}'
```

```bash
# Remover chave
oc patch cm <nome> --type json -p='[{"op":"remove","path":"/data/old-key"}]'
```

#### Routes
```bash
# Mudar host
oc patch route <nome> -p '{"spec":{"host":"new-hostname.example.com"}}'
```

```bash
# Adicionar TLS
oc patch route <nome> -p '{"spec":{"tls":{"termination":"edge"}}}'
```

```bash
# Mudar service target
oc patch route <nome> -p '{"spec":{"to":{"name":"new-service"}}}'
```

#### HPA
```bash
# Min/Max replicas
oc patch hpa <nome> -p '{"spec":{"minReplicas":2,"maxReplicas":10}}'
```

```bash
# Target CPU
oc patch hpa <nome> -p '{"spec":{"targetCPUUtilizationPercentage":70}}'
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

```bash
# Patch com filter
oc get deploy -o json | jq -r '.items[] | select(.spec.replicas < 2) | .metadata.name' | \
while read deploy; do
  oc patch deployment $deploy -p '{"spec":{"replicas":2}}'
done
```

---

## ⚙️ Set Commands

### Set Image
```bash
# Deployment
oc set image deployment/<nome> <container-name>=<new-image>:<tag>
```

```bash
# Exemplo
oc set image deployment/myapp myapp=myapp:v2.0
```

```bash
# Múltiplos containers
oc set image deployment/<nome> container1=image1:v2 container2=image2:v2
```

```bash
# DeploymentConfig
oc set image dc/<nome> <container-name>=<new-image>
```

```bash
# Verificar
oc get deployment/<nome> -o jsonpath='{.spec.template.spec.containers[0].image}'
```

### Set Resources
```bash
# Requests e limits
oc set resources deployment/<nome> --limits=cpu=500m,memory=512Mi --requests=cpu=250m,memory=256Mi
```

```bash
# Apenas limits
oc set resources deployment/<nome> --limits=cpu=1,memory=1Gi
```

```bash
# Apenas requests
oc set resources deployment/<nome> --requests=cpu=100m,memory=128Mi
```

```bash
# Container específico
oc set resources deployment/<nome> -c=<container-name> --limits=cpu=200m,memory=256Mi
```

```bash
# Remover limits
oc set resources deployment/<nome> --limits=cpu=0,memory=0
```

### Set Env
```bash
# Adicionar variável
oc set env deployment/<nome> KEY=value
```

```bash
# Múltiplas variáveis
oc set env deployment/<nome> KEY1=value1 KEY2=value2
```

```bash
# De ConfigMap
oc set env deployment/<nome> --from=configmap/<cm-name>
```

```bash
# De Secret
oc set env deployment/<nome> --from=secret/<secret-name>
```

```bash
# Chave específica de CM
oc set env deployment/<nome> KEY --from=configmap/<cm-name> --keys=specific-key
```

```bash
# Remover variável
oc set env deployment/<nome> KEY-
```

```bash
# Listar variáveis
oc set env deployment/<nome> --list
```

### Set Volumes
```bash
# Adicionar volume de ConfigMap
oc set volume deployment/<nome> --add --name=config-vol --type=configmap --configmap-name=<cm-name> --mount-path=/etc/config
```

```bash
# Adicionar volume de Secret
oc set volume deployment/<nome> --add --name=secret-vol --type=secret --secret-name=<secret-name> --mount-path=/etc/secret
```

```bash
# Adicionar PVC
oc set volume deployment/<nome> --add --name=data-vol --type=persistentVolumeClaim --claim-name=<pvc-name> --mount-path=/data
```

```bash
# EmptyDir
oc set volume deployment/<nome> --add --name=tmp-vol --type=emptyDir --mount-path=/tmp
```

```bash
# Remover volume
oc set volume deployment/<nome> --remove --name=<volume-name>
```

```bash
# Listar volumes
oc set volume deployment/<nome>
```

### Set Probe
```bash
# Liveness probe
oc set probe deployment/<nome> --liveness --get-url=http://:8080/health --initial-delay-seconds=30
```

```bash
# Readiness probe
oc set probe deployment/<nome> --readiness --get-url=http://:8080/ready --period-seconds=10
```

```bash
# TCP probe
oc set probe deployment/<nome> --liveness --open-tcp=8080 --timeout-seconds=1
```

```bash
# Exec probe
oc set probe deployment/<nome> --liveness --exec -- cat /tmp/healthy
```

```bash
# Remover probe
oc set probe deployment/<nome> --liveness --remove
oc set probe deployment/<nome> --readiness --remove
```

### Set ServiceAccount
```bash
# Definir ServiceAccount
oc set serviceaccount deployment/<nome> <sa-name>
```

```bash
# Exemplo
oc set serviceaccount deployment/myapp mysa
```

### Set Selector
```bash
# Service selector
oc set selector svc/<nome> app=myapp,tier=frontend
```

```bash
# Overwrite
oc set selector svc/<nome> app=newapp --overwrite
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
oc get deployment/<nome> -o yaml > /tmp/deploy.yaml
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
