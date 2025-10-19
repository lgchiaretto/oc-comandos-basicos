# 📄 Templates e Manifests

Este documento contém comandos para trabalhar com templates e manifests do OpenShift.

---

## 📋 Índice

1. [Templates](#templates)
2. [Processing Templates](#processing-templates)
3. [Parameters](#parameters)
4. [Export e Manifests](#export-e-manifests)

---

## 📋 Templates

### Listar Templates
```bash
# Templates do projeto atual
oc get templates

# Templates do openshift namespace
oc get templates -n openshift

# Descrever template
oc describe template <template-name> -n openshift

# Ver YAML do template
oc get template <template-name> -n openshift -o yaml

# Buscar templates disponíveis
oc get templates -n openshift | grep <keyword>
```

### Criar Template
```bash
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
```bash
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

## ⚙️ Processing Templates

### Processar Template
```bash
# Process e display (não cria recursos)
oc process <template-name>

# Com parâmetros
oc process <template-name> -p APP_NAME=myapp -p REPLICAS=3

# Process e create
oc process <template-name> -p APP_NAME=myapp | oc create -f -

# De um template no openshift namespace
oc process -n openshift <template-name> -p PARAM=value | oc create -f -

# De arquivo local
oc process -f template.yaml -p APP_NAME=myapp | oc create -f -
```

### Ver Parâmetros
```bash
# Listar parâmetros de um template
oc process <template-name> --parameters

# De template no openshift namespace
oc process -n openshift <template-name> --parameters

# Formato mais legível
oc process -n openshift <template-name> --parameters | column -t
```

### Usar Arquivo de Parâmetros
```bash
# Criar arquivo de parâmetros
cat > params.env << EOF
APP_NAME=myapp
IMAGE=nodejs-16
REPLICAS=3
DB_HOST=mongodb.database.svc
DB_NAME=production
EOF

# Usar com template
oc process <template-name> --param-file=params.env | oc create -f -

# Ou combinar arquivo + override
oc process <template-name> --param-file=params.env -p REPLICAS=5 | oc create -f -
```

---

## 🔢 Parameters

### Tipos de Parâmetros
```bash
# Parâmetro obrigatório
parameters:
- name: APP_NAME
  required: true

# Com valor default
parameters:
- name: REPLICAS
  value: "1"

# Com generate (senha aleatória, por exemplo)
parameters:
- name: DATABASE_PASSWORD
  displayName: "Database Password"
  description: "Password for the database"
  generate: expression
  from: "[a-zA-Z0-9]{16}"

# Com validation regex
parameters:
- name: APP_NAME
  description: "Nome válido (alphanumeric)"
  required: true
  # (validation é aplicada no processing)
```

### Generate Values
```bash
# Gerar valores aleatórios
parameters:
- name: SECRET_KEY
  generate: expression
  from: "[a-zA-Z0-9]{32}"

- name: DATABASE_USER
  generate: expression
  from: "user[0-9]{4}"

- name: API_KEY
  generate: expression
  from: "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
```

---

## 📤 Export e Manifests

### Export de Recursos
```bash
# Export pod
oc get pod <nome> -o yaml --export > pod.yaml
# Nota: --export está deprecated, use:
oc get pod <nome> -o yaml > pod.yaml

# Limpar metadata desnecessário com yq
oc get pod <nome> -o yaml | yq 'del(.metadata.uid, .metadata.resourceVersion, .metadata.creationTimestamp, .status)' > pod-clean.yaml

# Export deployment
oc get deployment <nome> -o yaml > deployment.yaml

# Export service
oc get svc <nome> -o yaml > service.yaml

# Export route
oc get route <nome> -o yaml > route.yaml

# Export todos os recursos de um tipo
oc get deployments -o yaml > all-deployments.yaml
```

### Criar Template de Recursos Existentes
```bash
# Export como template
oc get deployment,svc,route -l app=myapp -o yaml | \
oc create template myapp-template --dry-run=client -o yaml > myapp-template.yaml

# Ou manualmente
cat > app-template.yaml << 'EOF'
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: myapp-template
objects:
EOF

# Adicionar recursos exportados
oc get deployment myapp -o yaml | sed 's/^/  /' >> app-template.yaml
echo "---" >> app-template.yaml
oc get svc myapp -o yaml | sed 's/^/  /' >> app-template.yaml

# Depois substituir valores fixos por parâmetros
# Ex: replicas: 2 -> replicas: ${REPLICAS}
```

### Manifests e Kustomize
```bash
# Estrutura Kustomize
mkdir -p app/{base,overlays/{dev,prod}}

# Base
cat > app/base/kustomization.yaml << EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
- service.yaml
- route.yaml
EOF

# Overlay dev
cat > app/overlays/dev/kustomization.yaml << EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: myapp-dev
bases:
- ../../base
replicas:
- name: myapp
  count: 1
EOF

# Aplicar
oc apply -k app/overlays/dev/
```

### Backup de Projeto Completo
```bash
# Script para backup de projeto
cat > /tmp/backup-project.sh << 'EOF'
#!/bin/bash
PROJECT=$1
BACKUP_DIR="project-backup-${PROJECT}-$(date +%Y%m%d)"

mkdir -p ${BACKUP_DIR}

# Export de cada tipo de recurso
for resource in dc deployment statefulset daemonset job cronjob \
                svc route pvc cm secret sa role rolebinding; do
  echo "Exporting ${resource}..."
  oc get ${resource} -n ${PROJECT} -o yaml > ${BACKUP_DIR}/${resource}.yaml 2>/dev/null
done

# Compress
tar czf ${BACKUP_DIR}.tar.gz ${BACKUP_DIR}/
echo "Backup saved to ${BACKUP_DIR}.tar.gz"
EOF

chmod +x /tmp/backup-project.sh
/tmp/backup-project.sh <project-name>
```

---

## 📖 Navegação

- [← Anterior: Output e Formatação](25-output-formatacao.md)
- [→ Próximo: Backup e Disaster Recovery](27-backup-disaster-recovery.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
