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
# oc edit deployment <deployment-name>
oc edit deployment test-app
```

```bash ignore-test
# Editar service
# oc edit svc <service-name>
oc edit svc test-app
```

```bash ignore-test
# Editar configmap
# oc edit cm <configmap-name>
oc edit cm test-app
```

```bash ignore-test
# Editar com editor específico
EDITOR=nano oc edit deployment test-app
KUBE_EDITOR=vim oc edit deployment test-app
```

```bash ignore-test
# Editar em namespace específico
# oc edit deployment <deployment-name> -n <namespace>
oc edit deployment test-app -n development
```

### Edit em Arquivo Temporário
```bash ignore-test
# Export, edit, apply
# oc get deployment <deployment-name> -o yaml > /tmp/deploy.yaml
oc get deployment test-app -o yaml > /tmp/deploy.yaml
vi /tmp/deploy.yaml
oc apply -f /tmp/deploy.yaml
```

```bash ignore-test
# Ou com replace
oc replace -f /tmp/deploy.yaml
```

```bash ignore-test
# Com force
oc replace -f /tmp/deploy.yaml --force
```

---

## 🔧 Patch

### Patch Types

#### Strategic Merge Patch
```bash
# Patch deployment replicas
# oc patch deployment <deployment-name> -p '{"spec":{"replicas":3}}'
oc patch deployment test-app -p '{"spec":{"replicas":3}}'
```

```bash
# Patch com type explicit
# oc patch deployment <deployment-name> --type merge -p '{"spec":{"replicas":3}}'
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

```bash
# Adicionar label
# oc patch deployment <deployment-name> -p '{"metadata":{"labels":{"env":"production"}}}'
oc patch deployment test-app -p '{"metadata":{"labels":{"env":"production"}}}'
```

```bash
# Adicionar annotation
# oc patch deployment <deployment-name> -p '{"metadata":{"annotations":{"description":"My app"}}}'
oc patch deployment test-app -p '{"metadata":{"annotations":{"description":"My app"}}}'
```

```bash ignore-test
# Atualizar imagem
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"new-image:tag"}]}}}}'
```

```bash ignore-test
# Múltiplos campos
# oc patch deployment <deployment-name> --type merge -p '
oc patch deployment test-app --type merge -p '
{
  "spec": {
    "replicas": 3,
    "template": {
      "spec": {
        "containers": [{
          "name": "httpd",
          "image": "registry.redhat.io/rhel8/httpd-24",
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
# Replace elemento
# oc patch deployment <deployment-name> --type json -p='[{"op":"replace","path":"/spec/replicas","value":5}]'
oc patch deployment test-app --type json -p='[{"op":"replace","path":"/spec/replicas","value":5}]'
```

```bash ignore-test
# Múltiplas operações
# oc patch deployment <deployment-name> --type json -p='[
oc patch deployment test-app --type json -p='[
  {"op":"replace","path":"/spec/replicas","value":3},
  {"op":"add","path":"/metadata/labels/team","value":"backend"}
]'
```

#### JSON Merge Patch
```bash
# Merge simples (sobrescreve)
# oc patch deployment <deployment-name> --type merge -p '{"spec":{"replicas":3}}'
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

```bash
# Remover campo (set to null)
# oc patch deployment <deployment-name> --type merge -p '{"metadata":{"annotations":{"old-annotation":null}}}'
oc patch deployment test-app --type merge -p '{"metadata":{"annotations":{"old-annotation":null}}}'
```

### Patch de Recursos Comuns

#### Deployments
```bash
# Replicas
# oc patch deployment <deployment-name> -p '{"spec":{"replicas":5}}'
oc patch deployment test-app -p '{"spec":{"replicas":5}}'
```

```bash
# Strategy
# oc patch deployment <deployment-name> -p '{"spec":{"strategy":{"type":"RollingUpdate","rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
oc patch deployment test-app -p '{"spec":{"strategy":{"type":"RollingUpdate","rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
```

```bash ignore-test
# Image
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container>","image":"new-image:v2"}]}}}}'
```

```bash ignore-test
# Resources
# oc patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"registry.redhat.io/rhel8/httpd-24","resources":{"limits":{"memory":"1Gi","cpu":"1000m"},"requests":{"memory":"512Mi","cpu":"500m"}}}]}}}}'
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"registry.redhat.io/rhel8/httpd-24","resources":{"limits":{"memory":"1Gi","cpu":"1000m"},"requests":{"memory":"512Mi","cpu":"500m"}}}]}}}}'
```

```bash ignore-test
# Environment variable
# oc patch deployment <deployment-name> --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"LOG_LEVEL","value":"debug"}}]'
oc patch deployment test-app --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"LOG_LEVEL","value":"debug"}}]'
```

#### Services
```bash ignore-test
# Port
# oc patch svc <service-name> -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
oc patch svc test-app -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
```

```bash
# Type
# oc patch svc <service-name> -p '{"spec":{"type":"NodePort"}}'
oc patch svc test-app -p '{"spec":{"type":"NodePort"}}'
```

```bash
# Selector
# oc patch svc <service-name> -p '{"spec":{"selector":{"app":"new-app"}}}'
oc patch svc test-app -p '{"spec":{"selector":{"app":"new-app"}}}'
```

#### ConfigMaps
```bash
# Atualizar data
# oc patch cm <configmap-name> -p '{"data":{"key1":"new-value"}}'
oc patch cm test-app -p '{"data":{"key1":"new-value"}}'
```

```bash
# Adicionar nova chave
# oc patch cm <configmap-name> --type merge -p '{"data":{"new-key":"new-value"}}'
oc patch cm test-app --type merge -p '{"data":{"new-key":"new-value"}}'
```

```bash ignore-test
# Remover chave
# oc patch cm <configmap-name> --type json -p='[{"op":"remove","path":"/data/old-key"}]'
oc patch cm test-app --type json -p='[{"op":"remove","path":"/data/old-key"}]'
```

#### Routes
```bash
# Mudar host
# oc patch route <route-name> -p '{"spec":{"host":"new-hostname.example.com"}}'
oc patch route test-app -p '{"spec":{"host":"new-hostname.example.com"}}'
```

```bash
# Adicionar TLS
# oc patch route <route-name> -p '{"spec":{"tls":{"termination":"edge"}}}'
oc patch route test-app -p '{"spec":{"tls":{"termination":"edge"}}}'
```

```bash
# Mudar service target
# oc patch route <route-name> -p '{"spec":{"to":{"name":"new-service"}}}'
oc patch route test-app -p '{"spec":{"to":{"name":"new-service"}}}'
```

#### HPA
```bash inore-test
# Min/Max replicas
# oc patch hpa <resource-name>app -p '{"spec":{"minReplicas":2,"maxReplicas":10}}'
oc patch hpa test-app -p '{"spec":{"minReplicas":2,"maxReplicas":10}}'
```

```bash ignore-test
# Target CPU
# oc patch hpa <resource-name>app -p '{"spec":{"targetCPUUtilizationPercentage":70}}'
oc patch hpa test-app -p '{"spec":{"targetCPUUtilizationPercentage":70}}'
```

### Patch em Lote
```bash ignore-test
# Patch múltiplos deployments
for deploy in $(oc get deploy -o name); do
  oc patch $deploy -p '{"metadata":{"labels":{"env":"production"}}}'
done
```

```bash
# Patch todos os deployments com label
oc get deploy -l env=production -o name | xargs -I {} oc patch {} -p '{"spec":{"replicas":3}}'
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
oc set image deployment/test-app httpd=<new-image>:<tag>
```

```bash ignore-test
# Exemplo
# oc set image <resource-name>/test-app test-app=test-app:v2.0
oc set image deployment/test-app test-app=test-app:v2.0
```

```bash ignore-test
# Múltiplos containers
# oc set image <resource-name>/test-app container1=image1:v2 container2=image2:v2
oc set image deployment/test-app container1=image1:v2 container2=image2:v2
```

```bash ignore-test
# DeploymentConfig
oc set image dc/test-app httpd=<new-image>
```

```bash ignore-test
# Verificar
oc get deployment/test-app -o jsonpath='{.spec.template.spec.containers[0].image}'
```

### Set Resources
```bash
# Requests e limits
# oc set resources <resource-name>/test-app --limits=cpu=500m,memory=512Mi --requests=cpu=250m,memory=256Mi
oc set resources deployment/test-app --limits=cpu=500m,memory=512Mi --requests=cpu=250m,memory=256Mi
```

```bash
# Apenas limits
# oc set resources <resource-name>/test-app --limits=cpu=1,memory=1Gi
oc set resources deployment/test-app --limits=cpu=1,memory=1Gi
```

```bash
# Apenas requests
# oc set resources <resource-name>/test-app --requests=cpu=100m,memory=128Mi
oc set resources deployment/test-app --requests=cpu=100m,memory=128Mi
```

```bash ignore-test
# Container específico
oc set resources deployment/test-app -c=httpd --limits=cpu=200m,memory=256Mi
```

### Set Env
```bash
# Adicionar variável
# oc set env <resource-name>/test-app KEY=value
oc set env deployment/test-app KEY=value
```

```bash
# Múltiplas variáveis
# oc set env <resource-name>/test-app KEY1=value1 KEY2=value2
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
# oc set env <resource-name>/test-app KEY-
oc set env deployment/test-app KEY-
```

```bash
# Listar variáveis
# oc set env <resource-name>/test-app --list
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
# oc set volume <resource-name>/test-app --add --name=data-vol --type=persistentVolumeClaim --claim-name=test-app --mount-path=/data
oc set volume deployment/test-app --add --name=data-vol --type=persistentVolumeClaim --claim-name=test-app --mount-path=/data
```

```bash
# EmptyDir
# oc set volume <resource-name>/test-app --add --name=data-vol --type=emptyDir --mount-path=/data
oc set volume deployment/test-app --add --name=data-vol --type=emptyDir --mount-path=/data
```

```bash
# Remover volume
oc set volume deployment/test-app --remove --name=data-vol
```

```bash
# Listar volumes
# oc set volume <resource-name>/test-app
oc set volume deployment/test-app
```

### Set Probe
```bash
# Liveness probe
# oc set probe <resource-name>/test-app --liveness --get-url=http://:8080/health --initial-delay-seconds=30
oc set probe deployment/test-app --liveness --get-url=http://:8080/health --initial-delay-seconds=30
```

```bash
# Readiness probe
# oc set probe <resource-name>/test-app --readiness --get-url=http://:8080/ready --period-seconds=10
oc set probe deployment/test-app --readiness --get-url=http://:8080/ready --period-seconds=10
```

```bash
# Exec probe
# oc set probe <resource-name>/test-app --liveness -- cat /tmp/healthy
oc set probe deployment/test-app --liveness -- cat /tmp/healthy
```

```bash
# TCP probe
# oc set probe <resource-name>/test-app --liveness --open-tcp=8080 --timeout-seconds=1
oc set probe deployment/test-app --liveness --open-tcp=8080 --timeout-seconds=1
```

```bash
# Remover probe
# oc set probe <resource-name>/test-app --liveness --remove
oc set probe deployment/test-app --liveness --remove
# oc set probe <resource-name>/test-app --readiness --remove
oc set probe deployment/test-app --readiness --remove
```

### Set ServiceAccount
```bash ignore-test
# Definir ServiceAccount
oc set serviceaccount deployment/test-app test-app
```

```bash
# Exemplo
# oc set serviceaccount <serviceaccount-name>/test-app test-app
oc set serviceaccount deployment/test-app test-app
```

### Set Selector
```bash
# Service selector
# oc set selector <resource-name>/test-app app=test-app,tier=frontend
oc set selector svc/test-app app=test-app,tier=frontend
```

```bash
# Overwrite
# oc set selector <resource-name>/test-app app=newapp
oc set selector svc/test-app app=newapp
```

---

## 🔄 Replace

### Replace vs Apply
```bash ignore-test
# Apply (merge)
oc apply -f resource.yaml
```

```bash ignore-test
# Replace (substitui completamente)
oc replace -f resource.yaml
```

```bash ignore-test
# Replace com force (deleta e recria)
oc replace -f resource.yaml --force
```

```bash ignore-test
# Replace de stdin
cat resource.yaml | oc replace -f -
```

```bash ignore-test
# Get, edit, replace
oc get deployment/test-app -o yaml > /tmp/deploy.yaml
vi /tmp/deploy.yaml
oc replace -f /tmp/deploy.yaml
```

### Replace em Massa
```bash ignore-test
# Replace múltiplos recursos
oc replace -f directory/
```

```bash ignore-test
# Replace recursivo
oc replace -f directory/ -R
```

```bash ignore-test
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
