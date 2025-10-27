# Gerenciamento de Aplicações

Este documento contém comandos para criar e gerenciar aplicações no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Criação de Aplicações](#criação-de-aplicações)
3. [Gerenciamento](#gerenciamento)
4. [Informações e Status](#informações-e-status)
5. [Atualização de Imagens](#atualização-de-imagens)
6. [Permissões e Validações](#permissões-e-validações)
7. [⏳ Aguardar Condições](#⏳-aguardar-condições)
8. [Documentação Oficial](#documentação-oficial)
9. [Navegação](#navegação)
---

## Criação de Aplicações

### A partir de Imagem Docker
**Criar aplicação a partir de imagem**

```bash ignore-test
oc new-app <nome-da-imagem>
```

**Exemplo com imagem pública**

```bash ignore-test
oc new-app nginx
```

**Criar nova aplicação a partir de imagem ou código fonte**

```bash ignore-test
oc new-app myregistry.com/myapp:latest
```

**Criar aplicação com nome customizado**

```bash ignore-test
oc new-app nginx --name=meu-nginx
```

**Exemplo com httpd**

```bash
oc new-app httpd:latest --name=test-app -n development
```

### A partir de Repositório Git
**Criar aplicação a partir de repositório Git**

```bash ignore-test
oc new-app <url-do-repositorio-git>
```

**Especificando branch**

```bash ignore-test
oc new-app <url-do-repositorio-git>#<branch>
```

**Exemplo prático de new-app usando s2i**

```bash
oc new-app https://github.com/lgchiaretto/s2i-chiaretto.git --name=s2i-chiaretto
```

### Com Variáveis de Ambiente
**Criar aplicação com variáveis**

```bash ignore-test
oc new-app <imagem> -e VAR1=valor1 -e VAR2=valor2
```

**Exemplo**

```bash ignore-test
oc new-app mysql -e MYSQL_USER=user -e MYSQL_PASSWORD=pass
```

### A partir de Template
**Listar templates disponíveis no namespace openshift**

```bash
oc get templates -n openshift
```

**Criar a partir de template**

```bash ignore-test
oc new-app --template=<nome-do-template>
```

**Criar aplicação a partir de template**

```bash ignore-test
oc new-app --template=mysql-persistent -p MYSQL_USER=admin
```

### Com Estratégia de Build
**Especificar estratégia de build**

```bash ignore-test
oc new-app <url-git> --strategy=docker
```
```bash  ignore
oc new-app <url-git> --strategy=source
```

**Criar aplicação com nome customizado**

```bash ignore-test
oc new-app . --name=test-app
```

---

## Gerenciamento

### Listar Recursos
**Listar todos os recursos principais do namespace**

```bash
oc get all
```

**Listar recurso filtrados por label**

```bash
oc get all -l app=test-app
```

**Listar todos os deployments do namespace**

```bash
oc get deployment
```

**Listar todos os services do namespace atual**

```bash
oc get svc
```

**Listar todas as routes expostas no namespace**

```bash
oc get routes
```

**Listar routes em um namespace específico**

```bash
oc get routes -n development
```

**Listar todas as ImageStreams do projeto**

```bash
oc get is
```

**Listar ImageStreams em um projeto**

```bash
oc get is -n development
```

### Deletar Aplicações
**Deletar recurso que correspondem ao seletor de label**

```bash ignore-test
oc delete all -l app=test-app
```

**Deletar recurso que correspondem ao seletor de label**

```bash ignore-test
oc delete all --selector app=test-app
```

**Deletar o recurso especificado**

```bash ignore-test
oc delete deployment test-app
```

### Expor Aplicação
**Criar route para expor service externamente**

```bash ignore-test
oc expose service test-app
```

**Criar route com hostname customizado para o service**

```bash ignore-test
oc expose service test-app --hostname=app.example.com
```

**Criar route com terminação TLS edge (TLS terminado no router)**

```bash
oc create route edge --service=test-app
```

---

## Informações e Status

### Status do Projeto
**Exibir visão geral dos recursos do projeto atual**

```bash
oc status
```

**Status de um projeto específico**

```bash
oc status -n development
```

### Descrever Recursos
**Exibir detalhes completos do recurso**

```bash
oc describe deployment test-app
```

**Exibir detalhes completos do recurso**

```bash
oc describe deployment test-app -n development
```

---

## Atualização de Imagens

### Atualizar Imagem do Deployment
**Atualizar imagem do container no deployment/pod**

```bash
oc set image deployment/test-app httpd=httpd:2.4 -n development
```

**Atualizar imagem do container no deployment/pod**

```bash ignore-test
oc set image deployment/test-app container1=image1:tag container2=image2:tag
```

### Patch de Deployment
**Aplicar merge patch ao recurso (mescla alterações)**

```bash
oc patch deployment test-app -n development --type=merge -p '{"spec":{"replicas":3}}'
```

**Aplicar merge patch ao recurso (mescla alterações)**

```bash
oc patch deployment test-app -n development --type=merge -p '{"spec":{"template":{"spec":{"containers":[{"name":"httpd","image":"httpd:latest"}]}}}}'
```

---

## Permissões e Validações

### Verificar Permissões
**Verificar se usuário tem permissão para executar ação específica**

```bash
oc auth can-i create deployments
```

**Verificar se usuário tem permissão para executar ação específica**

```bash
oc auth can-i create deployments -n development
```

**Verificar se usuário tem permissão para executar ação específica**

**oc auth can-i get secrets -n <namespace>**

```bash
oc auth can-i delete pods -n development
oc auth can-i get secrets -n development
```

---

## ⏳ Aguardar Condições

### Wait para Deployment
**Aguardar deployment ficar disponível**

```bash
oc wait --for=condition=available deployment/test-app
```

**Aguardar deployment ficar disponível**

```bash
oc wait --for=condition=available --timeout=60s deployment/test-app
```

**Aguardar deployment ficar disponível**

```bash
oc wait --for=condition=available --timeout=60s deployment/test-app -n development
```
## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/developer-cli-odo">Developer CLI (odo)</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications/deployments">Deployments</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images">Images - Using templates</a>
---


## Navegação

- [← Anterior: Projetos](02-projetos.md)
- [→ Próximo: Pods e Containers](04-pods-containers.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
