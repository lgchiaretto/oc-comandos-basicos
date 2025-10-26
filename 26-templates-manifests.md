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
```bash
# Templates do projeto atual
oc get templates
```

```bash
# Templates do openshift namespace
oc get templates -n openshift
```

```bash ignore-test
# Descrever template
oc describe template <template-name> -n openshift
```

```bash ignore-test
# Ver YAML do template
oc get template <template-name> -n openshift -o yaml
```

```bash ignore-test
# Buscar templates disponíveis
oc get templates -n openshift | grep <keyword>
```

### Criar Template
```bash ignore-test
# Template básico
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
```bash ignore-test
# Template com múltiplos recursos
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
```bash ignore-test
# Process e display (não cria recursos)
oc process <template-name>
```

```bash ignore-test
# Com parâmetros
oc process <template-name> -p APP_NAME=test-app -p REPLICAS=3
```

```bash ignore-test
# Process e create
oc process <template-name> -p APP_NAME=test-app | oc create -f -
```

```bash ignore-test
# De um template no openshift namespace
oc process -n openshift <template-name> -p PARAM=value | oc create -f -
```

```bash ignore-test
# De arquivo local
oc process -f template.yaml -p APP_NAME=test-app | oc create -f -
```

### Ver Parâmetros
```bash ignore-test
# Listar parâmetros de um template
oc process <template-name> --parameters
```

```bash ignore-test
# De template no openshift namespace
oc process -n openshift <template-name> --parameters
```

```bash ignore-test
# Formato mais legível
oc process -n openshift <template-name> --parameters | column -t
```

### Usar Arquivo de Parâmetros
```bash
# Criar arquivo de parâmetros
cat > /tmp/params.env << EOF
APP_NAME=test-app
IMAGE=nodejs-16
REPLICAS=3
DB_HOST=mongodb.database.svc
DB_NAME=production
EOF
```

```bash ignore-test
# Usar com template
oc process <template-name> --param-file=/tmp/params.env | oc create -f -
```

```bash ignore-test
# Ou combinar arquivo + override
oc process <template-name> --param-file=/tmp/params.env -p REPLICAS=5 | oc create -f -
```

---

## Parameters

### Tipos de Parâmetros
```bash ignore-test
# Parâmetro obrigatório
parameters:
- name: APP_NAME
  required: true
```

```bash ignore-test
# Com valor default
parameters:
- name: REPLICAS
  value: "1"
```

```bash ignore-test
# Com generate (senha aleatória, por exemplo)
parameters:
- name: DATABASE_PASSWORD
  displayName: "Database Password"
  description: "Password for the database"
  generate: expression
  from: "[a-zA-Z0-9]{16}"
```

```bash ignore-test
# Com validation regex
parameters:
- name: APP_NAME
  description: "Nome válido (alphanumeric)"
  required: true
  # (validation é aplicada no processing)
```

### Generate Values
```bash ignore-test
# Gerar valores aleatórios
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
```bash ignore-test
# oc get pod <resource-name>app -o yaml > /tmp/pod.yaml
oc get pod test-app -o yaml > /tmp/pod.yaml
```

```bash
# Export deployment
# oc get deployment <deployment-name> -o yaml > /tmp/deployment.yaml
oc get deployment test-app -o yaml > /tmp/deployment.yaml
```

```bash
# Export service
# oc get svc <service-name> -o yaml > /tmp/service.yaml> 
oc get svc test-app -o yaml > /tmp/service.yaml
```

```bash
# Export route
# oc get route <route-name> -o yaml > /tmp/route.yaml
oc get route test-app -o yaml > /tmp/route.yaml
```

```bash
# Export todos os recursos de um tipo
oc get deployments -o yaml > /tmp/all-deployments.yaml
```

### Criar Template de Recursos Existentes
```bash
# Export como template
oc get deployment,svc,route -l app=test-app -o yaml
```
```bash ignore-test
# oc create template <resource-name>template --dry-run=client -o yaml > /tmp/test-app-template.yaml
oc create template test-app-template --dry-run=client -o yaml > /tmp/test-app-template.yaml
```

```bash
# Ou manualmente
cat > /tmp/app-template.yaml << 'EOF'
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: test-app-template
objects:
EOF
```

```bash
# Adicionar recursos exportados
# oc get deployment <deployment-name> -o yaml | sed 's/^/  /' >> /tmp/app-template.yaml
oc get deployment test-app -o yaml | sed 's/^/  /' >> /tmp/app-template.yaml
echo "---" >> /tmp/app-template.yaml
# oc get svc <service-name> -o yaml | sed 's/^/  /' >> /tmp/app-template.yaml
oc get svc test-app -o yaml | sed 's/^/  /' >> /tmp/app-template.yaml
```

```bash
# Depois substituir valores fixos por parâmetros
# Ex: replicas: 2 -> replicas: ${REPLICAS}
```

### Manifests e Kustomize
```bash ignore-test
# Estrutura Kustomize
mkdir -p app/{base,overlays/{dev,prod}}
```

```bash ignore-test
# Base
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

---

## Navegação

- [← Anterior: Output e Formatação](25-output-formatacao.md)
- [→ Próximo: Backup e Disaster Recovery](27-backup-disaster-recovery.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
