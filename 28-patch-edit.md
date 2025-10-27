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
**Ação:** Abrir editor para modificar recurso interativamente
**Exemplo:** `oc edit deployment <deployment-name>`

```bash ignore-test
oc edit deployment test-app
```

**Ação:** Abrir editor para modificar recurso interativamente
**Exemplo:** `oc edit svc <service-name>`

```bash ignore-test
oc edit svc test-app
```

**Ação:** Abrir editor para modificar recurso interativamente
**Exemplo:** `oc edit cm <configmap-name>`

```bash ignore-test
oc edit cm test-app
```

**Ação:** Abrir editor para modificar recurso interativamente

```bash ignore-test
EDITOR=nano oc edit deployment test-app
KUBE_EDITOR=vim oc edit deployment test-app
```

**Ação:** Abrir editor para modificar recurso interativamente
**Exemplo:** `oc edit deployment <deployment-name> -n <namespace>`

```bash ignore-test
oc edit deployment test-app -n development
```

### Edit em Arquivo Temporário
**Ação:** Exibir recurso "test-app" em formato YAML
**Exemplo:** `oc get deployment <deployment-name> -o yaml > /tmp/deploy.yaml`

```bash ignore-test
oc get deployment test-app -o yaml > /tmp/deploy.yaml
vi /tmp/deploy.yaml
oc apply -f /tmp/deploy.yaml
```

**Ação:** Ou com replace

```bash ignore-test
oc replace -f /tmp/deploy.yaml
```

**Ação:** Com force

```bash ignore-test
oc replace -f /tmp/deploy.yaml --force
```

---

## Patch

### Patch Types

#### Strategic Merge Patch
**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> -p '{"spec":{"replicas":3}}'`

```bash
oc patch deployment test-app -p '{"spec":{"replicas":3}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> --type merge -p '{"spec":{"replicas":3}}'`

```bash
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> -p '{"metadata":{"labels":{"env":"production"}}}'`

```bash
oc patch deployment test-app -p '{"metadata":{"labels":{"env":"production"}}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> -p '{"metadata":{"annotations":{"description":"My app"}}}'`

```bash
oc patch deployment test-app -p '{"metadata":{"annotations":{"description":"My app"}}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"new-image:tag"}]}}}}'`

```bash ignore-test
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"new-image:tag"}]}}}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> --type merge -p '`

```bash ignore-test
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
**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> --type json -p='[{"op":"replace","path":"/spec/replicas","value":5}]'`

```bash
oc patch deployment test-app --type json -p='[{"op":"replace","path":"/spec/replicas","value":5}]'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> --type json -p='[`

```bash ignore-test
oc patch deployment test-app --type json -p='[
  {"op":"replace","path":"/spec/replicas","value":3},
  {"op":"add","path":"/metadata/labels/team","value":"backend"}
]'
```

#### JSON Merge Patch
**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> --type merge -p '{"spec":{"replicas":3}}'`

```bash
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> --type merge -p '{"metadata":{"annotations":{"old-annotation":null}}}'`

```bash
oc patch deployment test-app --type merge -p '{"metadata":{"annotations":{"old-annotation":null}}}'
```

### Patch de Recursos Comuns

#### Deployments
**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> -p '{"spec":{"replicas":5}}'`

```bash
oc patch deployment test-app -p '{"spec":{"replicas":5}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> -p '{"spec":{"strategy":{"type":"RollingUpdate","rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'`

```bash
oc patch deployment test-app -p '{"spec":{"strategy":{"type":"RollingUpdate","rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
```

**Ação:** Image

```bash ignore-test
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container>","image":"new-image:v2"}]}}}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"registry.redhat.io/rhel8/httpd-24","resources":{"limits":{"memory":"1Gi","cpu":"1000m"},"requests":{"memory":"512Mi","cpu":"500m"}}}]}}}}'`

```bash ignore-test
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"registry.redhat.io/rhel8/httpd-24","resources":{"limits":{"memory":"1Gi","cpu":"1000m"},"requests":{"memory":"512Mi","cpu":"500m"}}}]}}}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch deployment <deployment-name> --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"LOG_LEVEL","value":"debug"}}]'`

```bash ignore-test
oc patch deployment test-app --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"LOG_LEVEL","value":"debug"}}]'
```

#### Services
**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch svc <service-name> -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'`

```bash ignore-test
oc patch svc test-app -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch svc <service-name> -p '{"spec":{"type":"NodePort"}}'`

```bash
oc patch svc test-app -p '{"spec":{"type":"NodePort"}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch svc <service-name> -p '{"spec":{"selector":{"app":"new-app"}}}'`

```bash
oc patch svc test-app -p '{"spec":{"selector":{"app":"new-app"}}}'
```

#### ConfigMaps
**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch cm <configmap-name> -p '{"data":{"key1":"new-value"}}'`

```bash
oc patch cm test-app -p '{"data":{"key1":"new-value"}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch cm <configmap-name> --type merge -p '{"data":{"new-key":"new-value"}}'`

```bash
oc patch cm test-app --type merge -p '{"data":{"new-key":"new-value"}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch cm <configmap-name> --type json -p='[{"op":"remove","path":"/data/old-key"}]'`

```bash ignore-test
oc patch cm test-app --type json -p='[{"op":"remove","path":"/data/old-key"}]'
```

#### Routes
**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch route <route-name> -p '{"spec":{"host":"new-hostname.example.com"}}'`

```bash
oc patch route test-app -p '{"spec":{"host":"new-hostname.example.com"}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch route <route-name> -p '{"spec":{"tls":{"termination":"edge"}}}'`

```bash
oc patch route test-app -p '{"spec":{"tls":{"termination":"edge"}}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch route <route-name> -p '{"spec":{"to":{"name":"new-service"}}}'`

```bash
oc patch route test-app -p '{"spec":{"to":{"name":"new-service"}}}'
```

#### HPA
```bash inore-test
# Min/Max replicas
# oc patch hpa <resource-name>app -p '{"spec":{"minReplicas":2,"maxReplicas":10}}'
oc patch hpa test-app -p '{"spec":{"minReplicas":2,"maxReplicas":10}}'
```

**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch hpa <resource-name>app -p '{"spec":{"targetCPUUtilizationPercentage":70}}'`

```bash ignore-test
oc patch hpa test-app -p '{"spec":{"targetCPUUtilizationPercentage":70}}'
```

### Patch em Lote
**Ação:** Patch múltiplos deployments

```bash ignore-test
for deploy in $(oc get deploy -o name); do
  oc patch $deploy -p '{"metadata":{"labels":{"env":"production"}}}'
done
```

**Ação:** Listar deployment filtrados por label

```bash
oc get deploy -l env=production -o name | xargs -I {} oc patch {} -p '{"spec":{"replicas":3}}'
```

**Ação:** Exibir deployment em formato JSON

```bash ignore-test
oc get deploy -o json | jq -r '.items[] | select(.spec.replicas < 2) | .metadata.name' | \
while read deploy; do
  oc patch deployment $deploy -p '{"spec":{"replicas":2}}'
done
```

---

## Set Commands

### Set Image
**Ação:** Deployment

```bash ignore-test
oc set image deployment/test-app httpd=<new-image>:<tag>
```

**Ação:** Exemplo
**Exemplo:** `oc set image <resource-name>/test-app test-app=test-app:v2.0`

```bash ignore-test
oc set image deployment/test-app test-app=test-app:v2.0
```

**Ação:** Atualizar imagem do container no deployment/pod
**Exemplo:** `oc set image <resource-name>/test-app container1=image1:v2 container2=image2:v2`

```bash ignore-test
oc set image deployment/test-app container1=image1:v2 container2=image2:v2
```

**Ação:** DeploymentConfig

```bash ignore-test
oc set image dc/test-app httpd=<new-image>
```

**Ação:** Exibir recurso em formato JSON
**Exemplo:** `oc get deployment/<deployment-name> -o jsonpath='{.spec.template.spec.containers[0].image}'`

```bash ignore-test
oc get deployment/test-app -o jsonpath='{.spec.template.spec.containers[0].image}'
```

### Set Resources
**Ação:** Definir/atualizar requests e limits de recursos
**Exemplo:** `oc set resources <resource-name>/test-app --limits=cpu=500m,memory=512Mi --requests=cpu=250m,memory=256Mi`

```bash
oc set resources deployment/test-app --limits=cpu=500m,memory=512Mi --requests=cpu=250m,memory=256Mi
```

**Ação:** Definir/atualizar requests e limits de recursos
**Exemplo:** `oc set resources <resource-name>/test-app --limits=cpu=1,memory=1Gi`

```bash
oc set resources deployment/test-app --limits=cpu=1,memory=1Gi
```

**Ação:** Definir/atualizar requests e limits de recursos
**Exemplo:** `oc set resources <resource-name>/test-app --requests=cpu=100m,memory=128Mi`

```bash
oc set resources deployment/test-app --requests=cpu=100m,memory=128Mi
```

**Ação:** Definir/atualizar requests e limits de recursos
**Exemplo:** `oc set resources <resource-name>/test-app -c=httpd --limits=cpu=200m,memory=256Mi`

```bash ignore-test
oc set resources deployment/test-app -c=httpd --limits=cpu=200m,memory=256Mi
```

### Set Env
**Ação:** Definir/atualizar variáveis de ambiente no recurso
**Exemplo:** `oc set env <resource-name>/test-app KEY=value`

```bash
oc set env deployment/test-app KEY=value
```

**Ação:** Definir/atualizar variáveis de ambiente no recurso
**Exemplo:** `oc set env <resource-name>/test-app KEY1=value1 KEY2=value2`

```bash
oc set env deployment/test-app KEY1=value1 KEY2=value2
```

**Ação:** De ConfigMap

```bash ignore-test
oc set env deployment/test-app --from=configmap/<cm-name>
```

**Ação:** De Secret

```bash ignore-test
oc set env deployment/test-app --from=secret/<secret-name>
```

**Ação:** Chave específica de CM

```bash ignore-test
oc set env deployment/test-app KEY --from=configmap/<cm-name> --keys=specific-key
```

**Ação:** Definir/atualizar variáveis de ambiente no recurso
**Exemplo:** `oc set env <resource-name>/test-app KEY-`

```bash
oc set env deployment/test-app KEY-
```

**Ação:** Definir/atualizar variáveis de ambiente no recurso
**Exemplo:** `oc set env <resource-name>/test-app --list`

```bash
oc set env deployment/test-app --list
```

### Set Volumes
**Ação:** Adicionar volume de ConfigMap

```bash ignore-test
oc set volume deployment/test-app --add --name=config-vol --type=configmap --configmap-name=<cm-name> --mount-path=/etc/config
```

**Ação:** Adicionar volume de Secret

```bash ignore-test
oc set volume deployment/test-app --add --name=secret-vol --type=secret --secret-name=<secret-name> --mount-path=/etc/secret
```

**Ação:** Adicionar PVC
**Exemplo:** `oc set volume <resource-name>/test-app --add --name=data-vol --type=persistentVolumeClaim --claim-name=test-app --mount-path=/data`

```bash ignore-test
oc set volume deployment/test-app --add --name=data-vol --type=persistentVolumeClaim --claim-name=test-app --mount-path=/data
```

**Ação:** EmptyDir
**Exemplo:** `oc set volume <resource-name>/test-app --add --name=data-vol --type=emptyDir --mount-path=/data`

```bash
oc set volume deployment/test-app --add --name=data-vol --type=emptyDir --mount-path=/data
```

**Ação:** Remover volume
**Exemplo:** `oc set volume <resource-name>/test-app --remove --name=data-vol`

```bash
oc set volume deployment/test-app --remove --name=data-vol
```

**Ação:** Listar volumes
**Exemplo:** `oc set volume <resource-name>/test-app`

```bash
oc set volume deployment/test-app
```

### Set Probe
**Ação:** Liveness probe
**Exemplo:** `oc set probe <resource-name>/test-app --liveness --get-url=http://:8080/health --initial-delay-seconds=30`

```bash
oc set probe deployment/test-app --liveness --get-url=http://:8080/health --initial-delay-seconds=30
```

**Ação:** Readiness probe
**Exemplo:** `oc set probe <resource-name>/test-app --readiness --get-url=http://:8080/ready --period-seconds=10`

```bash
oc set probe deployment/test-app --readiness --get-url=http://:8080/ready --period-seconds=10
```

**Ação:** Exec probe
**Exemplo:** `oc set probe <resource-name>/test-app --liveness -- cat /tmp/healthy`

```bash
oc set probe deployment/test-app --liveness -- cat /tmp/healthy
```

**Ação:** TCP probe
**Exemplo:** `oc set probe <resource-name>/test-app --liveness --open-tcp=8080 --timeout-seconds=1`

```bash
oc set probe deployment/test-app --liveness --open-tcp=8080 --timeout-seconds=1
```

**Ação:** Remover probe
**Exemplo:** `oc set probe <resource-name>/test-app --liveness --remove`
**Ação:** oc set probe <resource-name>/test-app --readiness --remove

```bash
oc set probe deployment/test-app --liveness --remove
oc set probe deployment/test-app --readiness --remove
```

### Set ServiceAccount
**Ação:** Definir ServiceAccount
**Exemplo:** `oc set serviceaccount <serviceaccount-name>/test-app test-app`

```bash ignore-test
oc set serviceaccount deployment/test-app test-app
```

**Ação:** Exemplo
**Exemplo:** `oc set serviceaccount <serviceaccount-name>/test-app test-app`

```bash
oc set serviceaccount deployment/test-app test-app
```

### Set Selector
**Ação:** Service selector
**Exemplo:** `oc set selector <resource-name>/test-app app=test-app,tier=frontend`

```bash
oc set selector svc/test-app app=test-app,tier=frontend
```

**Ação:** Overwrite
**Exemplo:** `oc set selector <resource-name>/test-app app=newapp`

```bash
oc set selector svc/test-app app=newapp
```

---

## Replace

### Replace vs Apply
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster

```bash ignore-test
oc apply -f resource.yaml
```

**Ação:** Replace (substitui completamente)

```bash ignore-test
oc replace -f resource.yaml
```

**Ação:** Replace com force (deleta e recria)

```bash ignore-test
oc replace -f resource.yaml --force
```

**Ação:** Replace de stdin

```bash ignore-test
cat resource.yaml | oc replace -f -
```

**Ação:** Exibir recurso em formato YAML
**Exemplo:** `oc get deployment/<deployment-name> -o yaml > /tmp/deploy.yaml`

```bash ignore-test
oc get deployment/test-app -o yaml > /tmp/deploy.yaml
vi /tmp/deploy.yaml
oc replace -f /tmp/deploy.yaml
```

### Replace em Massa
**Ação:** Replace múltiplos recursos

```bash ignore-test
oc replace -f directory/
```

**Ação:** Replace recursivo

```bash ignore-test
oc replace -f directory/ -R
```

**Ação:** Replace com dry-run

```bash ignore-test
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
