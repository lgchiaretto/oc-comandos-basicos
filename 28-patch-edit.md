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
**Abrir editor para modificar recurso interativamente**

```bash ignore-test
oc edit deployment test-app
```

**Abrir editor para modificar recurso interativamente**

```bash ignore-test
oc edit svc test-app
```

**Abrir editor para modificar recurso interativamente**

```bash ignore-test
oc edit cm test-app
```

**Abrir editor para modificar recurso interativamente**

```bash ignore-test
EDITOR=nano oc edit deployment test-app
KUBE_EDITOR=vim oc edit deployment test-app
```

**Abrir editor para modificar recurso interativamente**

```bash ignore-test
oc edit deployment test-app -n development
```

### Edit em Arquivo Temporário
**Exibir deployment em formato YAML completo**

```bash ignore-test
oc get deployment test-app -o yaml > /tmp/deploy.yaml
vi /tmp/deploy.yaml
oc apply -f /tmp/deploy.yaml
```

**Ou com replace**

```bash ignore-test
oc replace -f /tmp/deploy.yaml
```

**Com force**

```bash ignore-test
oc replace -f /tmp/deploy.yaml --force
```

---

## Patch

### Patch Types

#### Strategic Merge Patch
**Aplicar modificação parcial ao deployment usando patch**

```bash
oc patch deployment test-app -p '{"spec":{"replicas":3}}'
```

**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

**Aplicar modificação parcial ao deployment usando patch**

```bash
oc patch deployment test-app -p '{"metadata":{"labels":{"env":"production"}}}'
```

**Aplicar modificação parcial ao deployment usando patch**

```bash
oc patch deployment test-app -p '{"metadata":{"annotations":{"description":"My app"}}}'
```

**Aplicar modificação parcial ao deployment usando patch**

```bash ignore-test
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"new-image:tag"}]}}}}'
```

**Aplicar modificação parcial ao recurso usando patch**

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
**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch deployment test-app --type json -p='[{"op":"replace","path":"/spec/replicas","value":5}]'
```

**Aplicar modificação parcial ao recurso usando patch**

```bash ignore-test
oc patch deployment test-app --type json -p='[
  {"op":"replace","path":"/spec/replicas","value":3},
  {"op":"add","path":"/metadata/labels/team","value":"backend"}
]'
```

#### JSON Merge Patch
**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch deployment test-app --type merge -p '{"spec":{"replicas":3}}'
```

**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch deployment test-app --type merge -p '{"metadata":{"annotations":{"old-annotation":null}}}'
```

### Patch de Recursos Comuns

#### Deployments
**Aplicar modificação parcial ao deployment usando patch**

```bash
oc patch deployment test-app -p '{"spec":{"replicas":5}}'
```

**Aplicar modificação parcial ao deployment usando patch**

```bash
oc patch deployment test-app -p '{"spec":{"strategy":{"type":"RollingUpdate","rollingUpdate":{"maxSurge":1,"maxUnavailable":0}}}}'
```

**Image**

```bash ignore-test
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container>","image":"new-image:v2"}]}}}}'
```

**Aplicar modificação parcial ao deployment usando patch**

```bash ignore-test
oc patch deployment test-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"registry.redhat.io/rhel8/httpd-24","resources":{"limits":{"memory":"1Gi","cpu":"1000m"},"requests":{"memory":"512Mi","cpu":"500m"}}}]}}}}'
```

**Aplicar modificação parcial ao recurso usando patch**

```bash ignore-test
oc patch deployment test-app --type json -p='[{"op":"add","path":"/spec/template/spec/containers/0/env/-","value":{"name":"LOG_LEVEL","value":"debug"}}]'
```

#### Services
**Aplicar modificação parcial ao service usando patch**

```bash ignore-test
oc patch svc test-app -p '{"spec":{"ports":[{"port":8080,"targetPort":8080}]}}'
```

**Aplicar modificação parcial ao service usando patch**

```bash
oc patch svc test-app -p '{"spec":{"type":"NodePort"}}'
```

**Aplicar modificação parcial ao service usando patch**

```bash
oc patch svc test-app -p '{"spec":{"selector":{"app":"new-app"}}}'
```

#### ConfigMaps
**Aplicar modificação parcial ao cm usando patch**

```bash
oc patch cm test-app -p '{"data":{"key1":"new-value"}}'
```

**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch cm test-app --type merge -p '{"data":{"new-key":"new-value"}}'
```

**Aplicar modificação parcial ao recurso usando patch**

```bash ignore-test
oc patch cm test-app --type json -p='[{"op":"remove","path":"/data/old-key"}]'
```

#### Routes
**Aplicar modificação parcial ao route usando patch**

```bash
oc patch route test-app -p '{"spec":{"host":"new-hostname.example.com"}}'
```

**Aplicar modificação parcial ao route usando patch**

```bash
oc patch route test-app -p '{"spec":{"tls":{"termination":"edge"}}}'
```

**Aplicar modificação parcial ao route usando patch**

```bash
oc patch route test-app -p '{"spec":{"to":{"name":"new-service"}}}'
```

#### HPA
```bash inore-test
# Min/Max replicas
# oc patch hpa <resource-name>app -p '{"spec":{"minReplicas":2,"maxReplicas":10}}'
oc patch hpa test-app -p '{"spec":{"minReplicas":2,"maxReplicas":10}}'
```

**Aplicar modificação parcial ao horizontal pod autoscaler usando patch**

```bash ignore-test
oc patch hpa test-app -p '{"spec":{"targetCPUUtilizationPercentage":70}}'
```

### Patch em Lote
**Patch múltiplos deployments**

```bash ignore-test
for deploy in $(oc get deploy -o name); do
  oc patch $deploy -p '{"metadata":{"labels":{"env":"production"}}}'
done
```

**Listar deployment filtrados por label**

```bash
oc get deploy -l env=production -o name | xargs -I {} oc patch {} -p '{"spec":{"replicas":3}}'
```

**Exibir deploy em formato JSON completo**

```bash ignore-test
oc get deploy -o json | jq -r '.items[] | select(.spec.replicas < 2) | .metadata.name' | \
while read deploy; do
  oc patch deployment $deploy -p '{"spec":{"replicas":2}}'
done
```

---

## Set Commands

### Set Image
**Deployment**

```bash ignore-test
oc set image deployment/test-app httpd=<new-image>:<tag>
```

**Exemplo**

```bash ignore-test
oc set image deployment/test-app test-app=test-app:v2.0
```

**Atualizar imagem do container no deployment/pod**

```bash ignore-test
oc set image deployment/test-app container1=image1:v2 container2=image2:v2
```

**DeploymentConfig**

```bash ignore-test
oc set image dc/test-app httpd=<new-image>
```

**Exibir deployment/test-app em formato JSON**

```bash ignore-test
oc get deployment/test-app -o jsonpath='{.spec.template.spec.containers[0].image}'
```

### Set Resources
**Definir/atualizar requests e limits de recursos**

```bash
oc set resources deployment/test-app --limits=cpu=500m,memory=512Mi --requests=cpu=250m,memory=256Mi
```

**Definir/atualizar requests e limits de recursos**

```bash
oc set resources deployment/test-app --limits=cpu=1,memory=1Gi
```

**Definir/atualizar requests e limits de recursos**

```bash
oc set resources deployment/test-app --requests=cpu=100m,memory=128Mi
```

**Definir/atualizar requests e limits de recursos**

```bash ignore-test
oc set resources deployment/test-app -c=httpd --limits=cpu=200m,memory=256Mi
```

### Set Env
**Definir/atualizar variáveis de ambiente no recurso**

```bash
oc set env deployment/test-app KEY=value
```

**Definir/atualizar variáveis de ambiente no recurso**

```bash
oc set env deployment/test-app KEY1=value1 KEY2=value2
```

**De ConfigMap**

```bash ignore-test
oc set env deployment/test-app --from=configmap/<cm-name>
```

**De Secret**

```bash ignore-test
oc set env deployment/test-app --from=secret/<secret-name>
```

**Chave específica de CM**

```bash ignore-test
oc set env deployment/test-app KEY --from=configmap/<cm-name> --keys=specific-key
```

**Definir/atualizar variáveis de ambiente no recurso**

```bash
oc set env deployment/test-app KEY-
```

**Definir/atualizar variáveis de ambiente no recurso**

```bash
oc set env deployment/test-app --list
```

### Set Volumes
**Adicionar volume de ConfigMap**

```bash ignore-test
oc set volume deployment/test-app --add --name=config-vol --type=configmap --configmap-name=<cm-name> --mount-path=/etc/config
```

**Adicionar volume de Secret**

```bash ignore-test
oc set volume deployment/test-app --add --name=secret-vol --type=secret --secret-name=<secret-name> --mount-path=/etc/secret
```

**Adicionar PVC**

```bash ignore-test
oc set volume deployment/test-app --add --name=data-vol --type=persistentVolumeClaim --claim-name=test-app --mount-path=/data
```

**EmptyDir**

```bash
oc set volume deployment/test-app --add --name=data-vol --type=emptyDir --mount-path=/data
```

**Remover volume**

```bash
oc set volume deployment/test-app --remove --name=data-vol
```

**Listar volumes**

```bash
oc set volume deployment/test-app
```

### Set Probe
**Liveness probe**

```bash
oc set probe deployment/test-app --liveness --get-url=http://:8080/health --initial-delay-seconds=30
```

**Readiness probe**

```bash
oc set probe deployment/test-app --readiness --get-url=http://:8080/ready --period-seconds=10
```

**Exec probe**

```bash
oc set probe deployment/test-app --liveness -- cat /tmp/healthy
```

**TCP probe**

```bash
oc set probe deployment/test-app --liveness --open-tcp=8080 --timeout-seconds=1
```

**Remover probe**

**oc set probe <resource-name>/test-app --readiness --remove**

```bash
oc set probe deployment/test-app --liveness --remove
oc set probe deployment/test-app --readiness --remove
```

### Set ServiceAccount
**Definir ServiceAccount**

```bash ignore-test
oc set serviceaccount deployment/test-app test-app
```

**Exemplo**

```bash
oc set serviceaccount deployment/test-app test-app
```

### Set Selector
**Service selector**

```bash
oc set selector svc/test-app app=test-app,tier=frontend
```

**Overwrite**

```bash
oc set selector svc/test-app app=newapp
```

---

## Replace

### Replace vs Apply
**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
oc apply -f resource.yaml
```

**Replace (substitui completamente)**

```bash ignore-test
oc replace -f resource.yaml
```

**Replace com force (deleta e recria)**

```bash ignore-test
oc replace -f resource.yaml --force
```

**Replace de stdin**

```bash ignore-test
cat resource.yaml | oc replace -f -
```

**Exibir deployment/test-app em formato YAML**

```bash ignore-test
oc get deployment/test-app -o yaml > /tmp/deploy.yaml
vi /tmp/deploy.yaml
oc replace -f /tmp/deploy.yaml
```

### Replace em Massa
**Replace múltiplos recursos**

```bash ignore-test
oc replace -f directory/
```

**Replace recursivo**

```bash ignore-test
oc replace -f directory/ -R
```

**Replace com dry-run**

```bash ignore-test
oc replace -f resource.yaml --dry-run=client
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc">CLI Tools - OpenShift CLI (oc)</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
---


## Navegação

- [← Anterior: Backup e Disaster Recovery](27-backup-disaster-recovery.md)
- [→ Próximo: Jobs e CronJobs](29-jobs-cronjobs.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
