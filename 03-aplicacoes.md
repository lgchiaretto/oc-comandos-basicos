# 🚀 Gerenciamento de Aplicações

Este documento contém comandos para criar e gerenciar aplicações no OpenShift.

---

## 📋 Índice

1. [Criação de Aplicações](#criação-de-aplicações)
2. [Gerenciamento](#gerenciamento)
3. [Informações e Status](#informações-e-status)
4. [Atualização de Imagens](#atualização-de-imagens)
5. [Permissões e Validações](#permissões-e-validações)
6. [Aguardar Condições](#aguardar-condições)

---

## 🆕 Criação de Aplicações

### A partir de Imagem Docker
```bash ignore
# Criar aplicação a partir de imagem
oc new-app <nome-da-imagem>
```

```bash ignore
# Exemplo com imagem pública
oc new-app nginx
```

```bash ignore
# Imagem de registry customizado
oc new-app myregistry.com/myapp:latest
```

```bash ignore
# Com nome personalizado
oc new-app nginx --name=meu-nginx
```

```bash
# Exemplo com httpd
oc new-app httpd:latest --name=test-app -n development
```

### A partir de Repositório Git
```bash ignore
# Criar aplicação a partir de repositório Git
oc new-app <url-do-repositorio-git>
```

```bash ignore
# Especificando branch
oc new-app <url-do-repositorio-git>#<branch>
```

```bash ignore
# Exemplo prático
oc new-app https://github.com/sclorg/django-ex
```

```bash ignore
# Branch específica
oc new-app https://github.com/sclorg/django-ex#develop
```

### Com Variáveis de Ambiente
```bash ignore
# Criar aplicação com variáveis
oc new-app <imagem> -e VAR1=valor1 -e VAR2=valor2
```

```bash ignore
# Exemplo
oc new-app mysql -e MYSQL_USER=user -e MYSQL_PASSWORD=pass
```

### A partir de Template
```bash
# Listar templates disponíveis
oc get templates -n openshift
```

```bash ignore
# Criar a partir de template
oc new-app --template=<nome-do-template>
```

```bash
# Com parâmetros
oc new-app --template=mysql-persistent -p MYSQL_USER=admin
```

### Com Estratégia de Build
```bash ignore
# Especificar estratégia de build
oc new-app <url-git> --strategy=docker
```
```bash  ignore
oc new-app <url-git> --strategy=source
```

```bash ignore
# A partir de código local
oc new-app . --name=test-app
```

---

## 🔧 Gerenciamento

### Listar Recursos
```bash
# Listar todas as aplicações
oc get all
```

```bash
# Listar recursos com labels
oc get all -l app=test-app
```

```bash
# Listar apenas deployments
oc get deployment
```

```bash
# Listar services
oc get svc
```

```bash
# Listar routes
oc get routes
```

```bash
# Listar routes em um namespace específico
oc get routes -n development
```

```bash
# Listar ImageStreams
oc get is
```

```bash
# Listar ImageStreams em um projeto
oc get is -n development
```

### Deletar Aplicações
```bash ignore
# Deletar aplicação e recursos relacionados
oc delete all -l app=test-app
```

```bash ignore
# Deletar por seletor
oc delete all --selector app=test-app
```

```bash ignore
# Deletar deployment específico
oc delete deployment test-app
```

### Expor Aplicação
```bash ignore
# Expor service como route
oc expose service test-app
```

```bash ignore
# Com hostname customizado
oc expose service test-app --hostname=app.example.com
```

```bash
# Com TLS
oc create route edge --service=test-app
```

---

## 📊 Informações e Status

### Status do Projeto
```bash
# Ver status geral do projeto
oc status
```

```bash
# Status de um projeto específico
oc status -n development
```

### Descrever Recursos
```bash
# Descrever deployment
oc describe deployment test-app
```

```bash
# Descrever deployment em namespace específico
oc describe deployment test-app -n development
```

---

## 🔄 Atualização de Imagens

### Atualizar Imagem do Deployment
```bash
# Atualizar imagem de um container
oc set image deployment/test-app httpd=httpd:2.4 -n development
```

```bash ignore
# Atualizar múltiplos containers
oc set image deployment/test-app container1=image1:tag container2=image2:tag
```

### Patch de Deployment
```bash
# Aplicar patch usando merge
oc patch deployment test-app -n development --type=merge -p '{"spec":{"replicas":3}}'
```

```bash
# Patch para atualizar imagem
oc patch deployment test-app -n development --type=merge -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "httpd",
          "image": "httpd:latest"
        }]
      }
    }
  }
}'
```

---

## 🔐 Permissões e Validações

### Verificar Permissões
```bash
# Verificar se pode criar deployments
oc auth can-i create deployments
```

```bash
# Verificar em namespace específico
oc auth can-i create deployments -n development
```

```bash
# Verificar outras ações
oc auth can-i delete pods -n development
oc auth can-i get secrets -n development
```

---

## ⏳ Aguardar Condições

### Wait para Deployment
```bash
# Aguardar deployment estar disponível
oc wait --for=condition=available deployment/test-app
```

```bash
# Com timeout
oc wait --for=condition=available --timeout=60s deployment/test-app
```

```bash
# Aguardar em namespace específico
oc wait --for=condition=available --timeout=60s deployment/test-app -n development
```
---

## 📖 Navegação

- [← Anterior: Projetos](02-projetos.md)
- [→ Próximo: Pods e Containers](04-pods-containers.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
