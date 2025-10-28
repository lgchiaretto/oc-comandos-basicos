# Templates e Manifests

Este documento contém comandos para trabalhar com templates e manifests do OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Templates](#templates)
3. [Processing Templates](#processing-templates)
4. [Parameters](#parameters)
5. [Export e Manifests](#export-e-manifests)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Templates

### Listar Templates
**Templates do projeto atual**

```bash
oc get templates
```

**Listar templates disponíveis no namespace openshift**

```bash
oc get templates -n openshift
```

**Descrever template**

```bash ignore-test
oc describe template <template-name> -n openshift
```

**Ver YAML do template**

```bash ignore-test
oc get template <template-name> -n openshift -o yaml
```

**Buscar templates disponíveis**

```bash ignore-test
oc get templates -n openshift | grep <keyword>
```

### Criar Template
**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
cat <<EOF | oc apply -f -
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: my-app-template
  annotations:
    description: "Template para minha aplicação"
    tags: "quickstart,nodejs"
objects:
- apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: \${APP_NAME}
  spec:
    replicas: \${REPLICAS}
    selector:
      matchLabels:
        app: \${APP_NAME}
    template:
      metadata:
        labels:
          app: \${APP_NAME}
      spec:
        containers:
        - name: \${APP_NAME}
          image: \${IMAGE}
          ports:
          - containerPort: 8080
parameters:
- name: APP_NAME
  description: "Nome da aplicação"
  required: true
- name: IMAGE
  description: "Imagem do container"
  value: "registry.access.redhat.com/ubi8/nodejs-16"
- name: REPLICAS
  description: "Número de réplicas"
  value: "1"
EOF
```

### Template Completo
**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
cat <<EOF | oc apply -f -
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: full-app-template
  annotations:
    description: "Template completo com deployment, service e route"
    iconClass: "icon-nodejs"
    tags: "nodejs,mongodb"
objects:
- apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: \${APP_NAME}
    labels:
      app: \${APP_NAME}
  spec:
    replicas: \${REPLICAS}
    selector:
      matchLabels:
        app: \${APP_NAME}
    template:
      metadata:
        labels:
          app: \${APP_NAME}
      spec:
        containers:
        - name: \${APP_NAME}
          image: \${IMAGE}:\${IMAGE_TAG}
          ports:
          - containerPort: 8080
          env:
          - name: DATABASE_HOST
            value: \${DB_HOST}
          - name: DATABASE_NAME
            value: \${DB_NAME}
          resources:
            limits:
              cpu: \${CPU_LIMIT}
              memory: \${MEMORY_LIMIT}
            requests:
              cpu: \${CPU_REQUEST}
              memory: \${MEMORY_REQUEST}
- apiVersion: v1
  kind: Service
  metadata:
    name: \${APP_NAME}
    labels:
      app: \${APP_NAME}
  spec:
    ports:
    - port: 8080
      targetPort: 8080
    selector:
      app: \${APP_NAME}
- apiVersion: route.openshift.io/v1
  kind: Route
  metadata:
    name: \${APP_NAME}
    labels:
      app: \${APP_NAME}
  spec:
    to:
      kind: Service
      name: \${APP_NAME}
    port:
      targetPort: 8080
parameters:
- name: APP_NAME
  displayName: "Application Name"
  description: "Nome da aplicação"
  required: true
- name: IMAGE
  displayName: "Docker Image"
  description: "Nome da imagem"
  value: "nodejs-app"
  required: true
- name: IMAGE_TAG
  displayName: "Image Tag"
  description: "Tag da imagem"
  value: "latest"
- name: REPLICAS
  displayName: "Replicas"
  description: "Número de réplicas"
  value: "2"
- name: DB_HOST
  displayName: "Database Host"
  description: "Hostname do banco"
  value: "mongodb"
- name: DB_NAME
  displayName: "Database Name"
  description: "Nome do banco"
  value: "mydb"
- name: CPU_REQUEST
  displayName: "CPU Request"
  value: "100m"
- name: CPU_LIMIT
  displayName: "CPU Limit"
  value: "500m"
- name: MEMORY_REQUEST
  displayName: "Memory Request"
  value: "128Mi"
- name: MEMORY_LIMIT
  displayName: "Memory Limit"
  value: "512Mi"
labels:
  template: full-app-template
EOF
```

---

## Processing Templates

### Processar Template
**Process e display (não cria recursos)**

```bash ignore-test
oc process <template-name>
```

**Com parâmetros**

```bash ignore-test
oc process <template-name> -p APP_NAME=test-app -p REPLICAS=3
```

**Process e create**

```bash ignore-test
oc process <template-name> -p APP_NAME=test-app | oc create -f -
```

**De um template no openshift namespace**

```bash ignore-test
oc process -n openshift <template-name> -p PARAM=value | oc create -f -
```

**Criar novo recurso**

```bash ignore-test
oc process -f template.yaml -p APP_NAME=test-app | oc create -f -
```

### Ver Parâmetros
**Listar parâmetros de um template**

```bash ignore-test
oc process <template-name> --parameters
```

**De template no openshift namespace**

```bash ignore-test
oc process -n openshift <template-name> --parameters
```

**Formato mais legível**

```bash ignore-test
oc process -n openshift <template-name> --parameters | column -t
```

### Usar Arquivo de Parâmetros
**Criar arquivo de parâmetros**

```bash
cat > /tmp/params.env << EOF
APP_NAME=test-app
IMAGE=nodejs-16
REPLICAS=3
DB_HOST=mongodb.database.svc
DB_NAME=production
EOF
```

**Usar com template**

```bash ignore-test
oc process <template-name> --param-file=/tmp/params.env | oc create -f -
```

**Ou combinar arquivo + override**

```bash ignore-test
oc process <template-name> --param-file=/tmp/params.env -p REPLICAS=5 | oc create -f -
```

---

## Parameters

### Tipos de Parâmetros
**Parâmetro obrigatório**

```bash ignore-test
parameters:
- name: APP_NAME
  required: true
```

**Com valor default**

```bash ignore-test
parameters:
- name: REPLICAS
  value: "1"
```

**Com generate (senha aleatória, por exemplo)**

```bash ignore-test
parameters:
- name: DATABASE_PASSWORD
  displayName: "Database Password"
  description: "Password for the database"
  generate: expression
  from: "[a-zA-Z0-9]{16}"
```

**Com validation regex**
* (validation é aplicada no processing)

```bash ignore-test
parameters:
- name: APP_NAME
  description: "Nome válido (alphanumeric)"
  required: true
```

### Generate Values
**Gerar valores aleatórios**

```bash ignore-test
parameters:
- name: SECRET_KEY
  generate: expression
  from: "[a-zA-Z0-9]{32}"
```

```bash ignore-test
- name: DATABASE_USER
  generate: expression
  from: "user[0-9]{4}"
```

```bash ignore-test
- name: API_KEY
  generate: expression
  from: "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
```

---

## Export e Manifests

### Export de Recursos
**oc get pod <resource-name>app -o yaml > /tmp/pod.yaml**

```bash ignore-test
oc get pod test-app -o yaml > /tmp/pod.yaml
```

**Exibir deployment em formato YAML completo**

```bash
oc get deployment test-app -o yaml > /tmp/deployment.yaml
```

**Exibir service "test-app" em formato YAML**

```bash
oc get svc test-app -o yaml > /tmp/service.yaml
```

**Exibir route "test-app" em formato YAML**

```bash
oc get route test-app -o yaml > /tmp/route.yaml
```

**Exibir deployments em formato YAML completo**

```bash
oc get deployments -o yaml > /tmp/all-deployments.yaml
```

### Criar Template de Recursos Existentes
**Listar recurso filtrados por label**

```bash
oc get deployment,svc,route -l app=test-app -o yaml
```
**oc create template <resource-name>template --dry-run=client -o yaml > /tmp/test-app-template.yaml**

```bash ignore-test
oc create template test-app-template --dry-run=client -o yaml > /tmp/test-app-template.yaml
```

**Ou manualmente**

```bash
cat > /tmp/app-template.yaml << 'EOF'
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: test-app-template
objects:
EOF
```

**Exibir recurso "test-app" em formato YAML**

**oc get svc <service-name> -o yaml | sed 's/^/  /' >> /tmp/app-template.yaml**

```bash
oc get deployment test-app -o yaml | sed 's/^/  /' >> /tmp/app-template.yaml
echo "---" >> /tmp/app-template.yaml
oc get svc test-app -o yaml | sed 's/^/  /' >> /tmp/app-template.yaml
```

```bash
# Depois substituir valores fixos por parâmetros
# Ex: replicas: 2 -> replicas: ${REPLICAS}
```

### Manifests e Kustomize
**Estrutura Kustomize**

```bash ignore-test
mkdir -p app/{base,overlays/{dev,prod}}
```

**Base**

```bash ignore-test
cat > app/base/kustomization.yaml << EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
- service.yaml
- route.yaml
EOF
```

```bash 
# Overlay dev
cat > app/overlays/dev/kustomization.yaml << EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: test-app-dev
bases:
- ../../base
replicas:
- name: test-app
  count: 1
EOF
```

```bash ignore-tests
# Aplicar
oc apply -k app/overlays/dev/
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images">Images - Using templates</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
---


## Navegação

- [← Anterior: Output e Formatação](25-output-formatacao.md)
- [→ Próximo: Backup e Disaster Recovery](27-backup-disaster-recovery.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
