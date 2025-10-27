# Patch e Edit

Este documento contém comandos para editar e fazer patch em recursos do OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Edit](#edit)
3. [Patch](#patch)
4. [Set Commands](#set-commands)
5. [Replace](#replace)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Edit

### Edit Básico
```bash ignore-test
# Abrir editor para modificar recurso interativamente
# oc edit deployment <deployment-name>
oc edit deployment test-app
```

```bash ignore-test
# Abrir editor para modificar recurso interativamente
# oc edit svc <service-name>
oc edit svc test-app
```

```bash ignore-test
# Abrir editor para modificar recurso interativamente
# oc edit cm <configmap-name>
oc edit cm test-app
```

```bash ignore-test
# Abrir editor para modificar recurso interativamente
EDITOR=nano oc edit deployment test-app
KUBE_EDITOR=vim oc edit deployment test-app
```

```bash ignore-test
# Abrir editor para modificar recurso interativamente
# oc edit deployment <deployment-name> -n <namespace>
oc edit deployment test-app -n development
```

### Edit em Arquivo Temporário
```bash ignore-test
# Exibir recurso "test-app" em formato YAML
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

## Patch

### Patch Types

#### Strategic Merge Patch
```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> -p '{"spec":{"replicas":3}}'
oc patch deployment test-app -p '{"spec":{"replicas":3}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> --type merge -p '{"spec":{"replicas":3}}'
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> -p '{"metadata":{"labels":{"env":"production"}}}'
oc patch deployment test-app -p '{"metadata":{"labels":{"env":"production"}}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> -p '{"metadata":{"annotations":{"description":"My app"}}}'
oc patch deployment test-app -p '{"metadata":{"annotations":{"description":"My app"}}}'
```

```bash ignore-test
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"new-image:tag"}]}}}}'
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"new-image:tag"}]}}}}'
```

```bash ignore-test
# Aplicar modificação parcial ao recurso usando patch
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
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> --type json -p='[{"op":"replace","path":"/spec/replicas","value":5}]'
oc patch deployment test-app --type json -p='[{"op":"replace","path":"/spec/replicas","value":5}]'
```

```bash ignore-test
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> --type json -p='[
oc patch deployment test-app --type json -p='[
  {"op":"replace","path":"/spec/replicas","value":3},
  {"op":"add","path":"/metadata/labels/team","value":"backend"}
]'
```

#### JSON Merge Patch
```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> --type merge -p '{"spec":{"replicas":3}}'
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> --type merge -p '{"metadata":{"annotations":{"old-annotation":null}}}'
oc patch deployment test-app --type merge -p '{"metadata":{"annotations":{"old-annotation":null}}}'
```

### Patch de Recursos Comuns

#### Deployments
```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> -p '{"spec":{"replicas":5}}'
oc patch deployment test-app -p '{"spec":{"replicas":5}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> -p '{"spec":{"strategy":{"type":"RollingUpdate","rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
oc patch deployment test-app -p '{"spec":{"strategy":{"type":"RollingUpdate","rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
```

```bash ignore-test
# Image
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container>","image":"new-image:v2"}]}}}}'
```

```bash ignore-test
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"registry.redhat.io/rhel8/httpd-24","resources":{"limits":{"memory":"1Gi","cpu":"1000m"},"requests":{"memory":"512Mi","cpu":"500m"}}}]}}}}'
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"registry.redhat.io/rhel8/httpd-24","resources":{"limits":{"memory":"1Gi","cpu":"1000m"},"requests":{"memory":"512Mi","cpu":"500m"}}}]}}}}'
```

```bash ignore-test
# Aplicar modificação parcial ao recurso usando patch
# oc patch deployment <deployment-name> --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"LOG_LEVEL","value":"debug"}}]'
oc patch deployment test-app --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"LOG_LEVEL","value":"debug"}}]'
```

#### Services
```bash ignore-test
# Aplicar modificação parcial ao recurso usando patch
# oc patch svc <service-name> -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
oc patch svc test-app -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch svc <service-name> -p '{"spec":{"type":"NodePort"}}'
oc patch svc test-app -p '{"spec":{"type":"NodePort"}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch svc <service-name> -p '{"spec":{"selector":{"app":"new-app"}}}'
oc patch svc test-app -p '{"spec":{"selector":{"app":"new-app"}}}'
```

#### ConfigMaps
```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch cm <configmap-name> -p '{"data":{"key1":"new-value"}}'
oc patch cm test-app -p '{"data":{"key1":"new-value"}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch cm <configmap-name> --type merge -p '{"data":{"new-key":"new-value"}}'
oc patch cm test-app --type merge -p '{"data":{"new-key":"new-value"}}'
```

```bash ignore-test
# Aplicar modificação parcial ao recurso usando patch
# oc patch cm <configmap-name> --type json -p='[{"op":"remove","path":"/data/old-key"}]'
oc patch cm test-app --type json -p='[{"op":"remove","path":"/data/old-key"}]'
```

#### Routes
```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch route <route-name> -p '{"spec":{"host":"new-hostname.example.com"}}'
oc patch route test-app -p '{"spec":{"host":"new-hostname.example.com"}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
# oc patch route <route-name> -p '{"spec":{"tls":{"termination":"edge"}}}'
oc patch route test-app -p '{"spec":{"tls":{"termination":"edge"}}}'
```

```bash
# Aplicar modificação parcial ao recurso usando patch
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
# Aplicar modificação parcial ao recurso usando patch
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
# Listar deployment filtrados por label
oc get deploy -l env=production -o name | xargs -I {} oc patch {} -p '{"spec":{"replicas":3}}'
```

```bash ignore-test
# Exibir deployment em formato JSON
oc get deploy -o json | jq -r '.items[] | select(.spec.replicas < 2) | .metadata.name' | \
while read deploy; do
  oc patch deployment $deploy -p '{"spec":{"replicas":2}}'
done
```

---

## Set Commands

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
# Atualizar imagem do container no deployment/pod
# oc set image <resource-name>/test-app container1=image1:v2 container2=image2:v2
oc set image deployment/test-app container1=image1:v2 container2=image2:v2
```

```bash ignore-test
# DeploymentConfig
oc set image dc/test-app httpd=<new-image>
```

```bash ignore-test
# Exibir recurso em formato JSON
# oc get deployment/<deployment-name> -o jsonpath='{.spec.template.spec.containers[0].image}'
oc get deployment/test-app -o jsonpath='{.spec.template.spec.containers[0].image}'
```

### Set Resources
```bash
# Definir/atualizar requests e limits de recursos
# oc set resources <resource-name>/test-app --limits=cpu=500m,memory=512Mi --requests=cpu=250m,memory=256Mi
oc set resources deployment/test-app --limits=cpu=500m,memory=512Mi --requests=cpu=250m,memory=256Mi
```

```bash
# Definir/atualizar requests e limits de recursos
# oc set resources <resource-name>/test-app --limits=cpu=1,memory=1Gi
oc set resources deployment/test-app --limits=cpu=1,memory=1Gi
```

```bash
# Definir/atualizar requests e limits de recursos
# oc set resources <resource-name>/test-app --requests=cpu=100m,memory=128Mi
oc set resources deployment/test-app --requests=cpu=100m,memory=128Mi
```

```bash ignore-test
# Definir/atualizar requests e limits de recursos
# oc set resources <resource-name>/test-app -c=httpd --limits=cpu=200m,memory=256Mi
oc set resources deployment/test-app -c=httpd --limits=cpu=200m,memory=256Mi
```

### Set Env
```bash
# Definir/atualizar variáveis de ambiente no recurso
# oc set env <resource-name>/test-app KEY=value
oc set env deployment/test-app KEY=value
```

```bash
# Definir/atualizar variáveis de ambiente no recurso
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
# Definir/atualizar variáveis de ambiente no recurso
# oc set env <resource-name>/test-app KEY-
oc set env deployment/test-app KEY-
```

```bash
# Definir/atualizar variáveis de ambiente no recurso
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
# oc set volume <resource-name>/test-app --remove --name=data-vol
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
# oc set serviceaccount <serviceaccount-name>/test-app test-app
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

## Replace

### Replace vs Apply
```bash ignore-test
# Aplicar configuração do arquivo YAML/JSON ao cluster
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
# Exibir recurso em formato YAML
# oc get deployment/<deployment-name> -o yaml > /tmp/deploy.yaml
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

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc">CLI Tools - OpenShift CLI (oc)</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
---

---

## Navegação

- [← Anterior: Backup e Disaster Recovery](27-backup-disaster-recovery.md)
- [→ Próximo: Jobs e CronJobs](29-jobs-cronjobs.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
