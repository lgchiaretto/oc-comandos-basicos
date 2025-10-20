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
```bash
# Criar aplicação a partir de imagem
oc new-app <nome-da-imagem>
```

```bash
# Exemplo com imagem pública
oc new-app nginx
```

```bash
# Imagem de registry customizado
oc new-app myregistry.com/myapp:latest
```

```bash
# Com nome personalizado
oc new-app nginx --name=meu-nginx
```

```bash
# Exemplo com httpd
oc new-app httpd:latest --name=test-app -n <nome-do-projeto>
```

### A partir de Repositório Git
```bash
# Criar aplicação a partir de repositório Git
oc new-app <url-do-repositorio-git>
```

```bash
# Especificando branch
oc new-app <url-do-repositorio-git>#<branch>
```

```bash
# Exemplo prático
oc new-app https://github.com/sclorg/django-ex
```

```bash
# Branch específica
oc new-app https://github.com/sclorg/django-ex#develop
```

### Com Variáveis de Ambiente
```bash
# Criar aplicação com variáveis
oc new-app <imagem> -e VAR1=valor1 -e VAR2=valor2
```

```bash
# Exemplo
oc new-app mysql -e MYSQL_USER=user -e MYSQL_PASSWORD=pass
```

### A partir de Template
```bash
# Listar templates disponíveis
oc get templates -n openshift
```

```bash
# Criar a partir de template
oc new-app --template=<nome-do-template>
```

```bash
# Com parâmetros
oc new-app --template=mysql-persistent -p MYSQL_USER=admin
```

### Com Estratégia de Build
```bash
# Especificar estratégia de build
oc new-app <url-git> --strategy=docker
oc new-app <url-git> --strategy=source
```

```bash
# A partir de código local
oc new-app . --name=<nome-da-app>
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
oc get all -l app=<nome-da-app>
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
oc get routes -n <nome-do-projeto>
```

```bash
# Listar ImageStreams
oc get is
```

```bash
# Listar ImageStreams em um projeto
oc get is -n <nome-do-projeto>
```

### Deletar Aplicações
```bash
# Deletar aplicação e recursos relacionados
oc delete all -l app=<nome-da-app>
```

```bash
# Deletar por seletor
oc delete all --selector app=<nome-da-app>
```

```bash
# Deletar deployment específico
oc delete deployment <nome>
```

### Expor Aplicação
```bash
# Expor service como route
oc expose service <nome-do-service>
```

```bash
# Com hostname customizado
oc expose service <nome> --hostname=app.example.com
```

```bash
# Com TLS
oc create route edge --service=<nome>
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
oc status -n <nome-do-projeto>
```

### Descrever Recursos
```bash
# Descrever deployment
oc describe deployment <nome-do-deployment>
```

```bash
# Descrever deployment em namespace específico
oc describe deployment <nome-do-deployment> -n <nome-do-projeto>
```

```bash
# Exemplo prático
oc describe deployment test-app -n meu-projeto
```

---

## 🔄 Atualização de Imagens

### Atualizar Imagem do Deployment
```bash
# Atualizar imagem de um container
oc set image deployment/<nome-do-deployment> <nome-do-container>=<nova-imagem>
```

```bash
# Exemplo prático
oc set image deployment/test-app httpd=httpd:2.4 -n <nome-do-projeto>
```

```bash
# Atualizar múltiplos containers
oc set image deployment/<nome> container1=image1:tag container2=image2:tag
```

### Patch de Deployment
```bash
# Aplicar patch usando merge
oc patch deployment <nome> -n <projeto> --type=merge -p '{"spec":{"replicas":3}}'
```

```bash
# Patch para atualizar imagem
oc patch deployment <nome> -n <projeto> --type=merge -p '{
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
oc auth can-i create deployments -n <nome-do-projeto>
```

```bash
# Verificar outras ações
oc auth can-i delete pods -n <nome-do-projeto>
oc auth can-i get secrets -n <nome-do-projeto>
```

---

## ⏳ Aguardar Condições

### Wait para Deployment
```bash
# Aguardar deployment estar disponível
oc wait --for=condition=available deployment/<nome>
```

```bash
# Com timeout
oc wait --for=condition=available --timeout=60s deployment/<nome>
```

```bash
# Aguardar em namespace específico
oc wait --for=condition=available --timeout=60s deployment/<nome> -n <nome-do-projeto>
```

```bash
# Exemplo prático
oc wait --for=condition=available --timeout=60s deployment/test-app -n meu-projeto
```

---

## 📖 Navegação

- [← Anterior: Projetos](02-projetos.md)
- [→ Próximo: Pods e Containers](04-pods-containers.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
