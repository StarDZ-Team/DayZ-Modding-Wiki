# Capítulo 7.5: Sistemas de Permissão

[<< Anterior: Persistência de Config](04-config-persistence.md) | [Início](../../README.md) | [Próximo: Arquitetura Orientada a Eventos >>](06-events.md)

---

## Introdução

Toda ferramenta admin, toda ação privilegiada e toda feature de moderação no DayZ precisa de um sistema de permissão. A questão não é se verificar permissões mas como estruturá-las. A comunidade de modding DayZ se estabeleceu em três padrões principais: permissões hierárquicas separadas por ponto (MyMod), atribuição de grupos de usuário por função (VPP) e acesso baseado em função em nível de framework (CF/COT). Cada um tem diferentes trade-offs em granularidade, complexidade e experiência do dono do servidor.

Este capítulo cobre os três padrões, o fluxo de verificação de permissão, formatos de armazenamento e tratamento de wildcard/superadmin.

---

## Por que Permissões Importam

Sem um sistema de permissão, você tem duas opções: ou todo jogador pode fazer tudo (caos), ou você hardcoda Steam64 IDs nos seus scripts (insustentável). Um sistema de permissão permite que donos de servidor definam quem pode fazer o quê, sem modificar código.

As três regras de segurança:

1. **Nunca confie no cliente.** O cliente envia uma requisição; o servidor decide se a honra.
2. **Negação padrão.** Se um jogador não recebeu explicitamente uma permissão, ele não a tem.
3. **Falhe fechado.** Se a própria verificação de permissão falhar (identidade null, dados corrompidos), negue a ação.

---

## Hierárquica Separada por Ponto (Padrão MyMod)

MyMod usa strings de permissão separadas por ponto organizadas em uma hierarquia de árvore. Cada permissão é um caminho como `"MyMod.Admin.Teleport"` ou `"MyMod.Missions.Start"`. Wildcards permitem conceder subárvores inteiras.

### Formato de Permissão

```
MyMod                           (namespace raiz)
├── Admin                        (ferramentas admin)
│   ├── Panel                    (abrir painel admin)
│   ├── Teleport                 (teleportar self/outros)
│   ├── Kick                     (kickar jogadores)
│   ├── Ban                      (banir jogadores)
│   └── Weather                  (mudar clima)
├── Missions                     (sistema de missões)
│   ├── Start                    (iniciar missões manualmente)
│   └── Stop                     (parar missões)
└── AI                           (sistema de IA)
    ├── Spawn                    (spawnar IA manualmente)
    └── Config                   (editar config de IA)
```

### Verificação de Permissão

A verificação percorre as permissões concedidas do jogador e suporta três tipos de match: match exato, wildcard total (`"*"`) e wildcard de prefixo (`"MyMod.Admin.*"`):

```c
bool HasPermission(string plainId, string permission)
{
    if (plainId == "" || permission == "")
        return false;

    TStringArray perms;
    if (!m_Permissions.Find(plainId, perms))
        return false;

    for (int i = 0; i < perms.Count(); i++)
    {
        string granted = perms[i];

        // Wildcard total: superadmin
        if (granted == "*")
            return true;

        // Match exato
        if (granted == permission)
            return true;

        // Wildcard de prefixo: "MyMod.Admin.*" corresponde a "MyMod.Admin.Teleport"
        if (granted.IndexOf("*") > 0)
        {
            string prefix = granted.Substring(0, granted.Length() - 1);
            if (permission.IndexOf(prefix) == 0)
                return true;
        }
    }

    return false;
}
```

### Armazenamento JSON

```json
{
    "Admins": {
        "76561198000000001": ["*"],
        "76561198000000002": ["MyMod.Admin.Panel", "MyMod.Admin.Teleport"],
        "76561198000000003": ["MyMod.Missions.*"],
        "76561198000000004": ["MyMod.Admin.Kick", "MyMod.Admin.Ban"]
    }
}
```

---

## Padrão UserGroup do VPP

VPP Admin Tools usa um sistema baseado em grupos. Você define grupos nomeados (funções) com conjuntos de permissões, depois atribui jogadores a grupos.

### Conceito

```
Grupos:
  "SuperAdmin"  → [todas as permissões]
  "Moderator"   → [kick, ban, mute, teleport]
  "Builder"     → [spawn objects, teleport, ESP]

Jogadores:
  "76561198000000001" → "SuperAdmin"
  "76561198000000002" → "Moderator"
  "76561198000000003" → "Builder"
```

---

## Padrão Baseado em Função do CF (COT)

Community Framework / COT usa um sistema de funções e permissões onde funções são definidas com conjuntos explícitos de permissão, e jogadores são atribuídos a funções.

CF representa permissões como uma estrutura de árvore, onde cada nó pode ser explicitamente permitido, negado ou herdar do pai:

```
Root
├── Admin [ALLOW]
│   ├── Kick [INHERIT → ALLOW]
│   ├── Ban [INHERIT → ALLOW]
│   └── Teleport [DENY]        ← Explicitamente negado mesmo com Admin sendo ALLOW
└── ESP [ALLOW]
```

Este sistema de três estados (allow/deny/inherit) é mais expressivo que os sistemas binários (concedido/não-concedido) usados por MyMod e VPP.

---

## Fluxo de Verificação de Permissão

Independentemente de qual sistema você usa, a verificação server-side segue o mesmo padrão:

```
Cliente envia requisição RPC
        │
        ▼
Handler RPC do servidor recebe
        │
        ▼
    ┌─────────────────────────────────┐
    │ Identidade do sender é não-null? │
    └───────────┬─────────────────────┘
                │ Não → return (descartar silenciosamente)
                │ Sim ▼
    ┌─────────────────────────────────┐
    │ Sender tem a permissão          │
    │ necessária para esta ação?      │
    └───────────┬─────────────────────┘
                │ Não → log warning, opcionalmente enviar erro ao cliente, return
                │ Sim ▼
    ┌─────────────────────────────────┐
    │ Validar dados da requisição     │
    │ (ler params, verificar limites) │
    └───────────┬─────────────────────┘
                │ Inválido → enviar erro ao cliente, return
                │ Válido ▼
    ┌─────────────────────────────────┐
    │ Executar a ação privilegiada    │
    │ Fazer log da ação com ID admin  │
    │ Enviar resposta de sucesso      │
    └─────────────────────────────────┘
```

---

## Padrões de Wildcard e Superadmin

### Wildcard Total: `"*"`

Concede todas as permissões. Este é o padrão superadmin. Um jogador com `"*"` pode fazer qualquer coisa.

**Convenção:** Todo sistema de permissão na comunidade de modding DayZ usa `"*"` para superadmin. Não invente uma convenção diferente.

### Wildcard de Prefixo: `"MyMod.Admin.*"`

Concede todas as permissões que começam com `"MyMod.Admin."`. Permite conceder um subsistema inteiro sem listar cada permissão.

---

## Melhores Práticas

1. **Negação padrão.** Se uma permissão não é explicitamente concedida, a resposta é "não".
2. **Verifique no servidor, nunca no cliente.** Verificações de permissão no cliente são apenas para conveniência de UI (esconder botões). O servidor deve sempre re-verificar.
3. **Use `"*"` para superadmin.** É a convenção universal. Não invente `"all"`, `"admin"` ou `"root"`.
4. **Faça log de toda ação privilegiada negada.** Esta é sua trilha de auditoria de segurança.
5. **Forneça um arquivo de permissões padrão com placeholder.**
6. **Namespaceie suas permissões.** Use `"YourMod.Category.Action"` para evitar colisões com outros mods.
7. **Suporte wildcards de prefixo.** Donos de servidor devem poder conceder `"YourMod.Admin.*"` ao invés de listar cada permissão admin individualmente.
8. **Mantenha o arquivo de permissões editável por humanos.** Donos de servidor vão editá-lo à mão.
9. **Implemente migração desde o primeiro dia.** Quando seu formato de permissão mudar (e vai), migração automática previne tickets de suporte.
10. **Sincronize permissões para o cliente no connect.** O cliente precisa saber suas próprias permissões para fins de UI.

---

[<< Anterior: Persistência de Config](04-config-persistence.md) | [Início](../../README.md) | [Próximo: Arquitetura Orientada a Eventos >>](06-events.md)
