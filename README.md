# BE HUMBLE Bot

## Introdução

Bem-vindo ao BE HUMBLE bot, personalizado para o gerenciamento de membros em seu servidor! Este bot foi desenvolvido para facilitar o processo de integração de novos membros, coletando informações importantes e automatizando algumas tarefas administrativas.

## Funcionalidades

### 1. Processo de Registro

**Atribuição de Cargo e Mensagem de Boas-Vindas:**
- Um cargo inicial é atribuído ao novo membro, restringindo o acesso a um canal específico com instruções.
- Uma mensagem de boas-vindas é enviada à DM do usuário.

**Coleta de Informações:**
- Quatro perguntas são feitas na DM do usuário (Nickname, Nome Pessoal, Data de Aniversário e Horários Disponíveis).

**Envio de Dados para Moderadores:**
- Após as respostas, o bot envia uma mensagem a um canal exclusivo para moderadores, contendo todas as informações coletadas.

**Registro em Planilha XLSX:**
- As informações do usuário são salvas em uma planilha XLSX para referência futura.

**Atualização de Cargo e Nome:**
- O bot renomeia o usuário com o nickname fornecido, remove o cargo inicial e atribui um novo cargo para acesso total ao servidor.

### 2. Verificação de Aniversários

Diariamente, o bot verifica na planilha se algum membro está completando ano. Se sim, ele envia uma mensagem embed no canal geral desejando feliz aniversário e marca o usuário correspondente.

### 3. Comandos de Slash

O bot possui quatro comandos de slash para interações rápidas:

- `/Ping:` Mostra o ping atual do bot.
- `/Limpar:` Limpa uma quantidade específica de mensagens no canal (apenas para moderadores).
- `/Embed:` Cria uma mensagem embed personalizada.
- `/Registro:` Inicia o processo de registro (não renomeia nem atribui cargo, pois consideramos que, caso a pessoa já esteja no servidor, ela terá o nome e o cargo corretos).

## Configuração

Antes de executar o bot, certifique-se de seguir estes passos:

1. **Token do Bot:**
   - Substitua `bot_token` em `config.py` pelo token real do seu bot.

2. **IDs dos canais e do Servidor**
3. - Substitua os IDs de canais desejados e o ID do servidor no código.

4. **Requisitos Python:**
   - Certifique-se de ter todas as bibliotecas Python instaladas. Você pode instalá-las usando `pip install -r requirements.txt`.

5. **Arquivo de Dados:**
   - Crie uma planilha Excel `teste.xlsx` para armazenar os dados dos usuários.

6. **Permissões do Bot:**
   - Certifique-se de que o bot tem permissões necessárias, como leitura de mensagens, envio de mensagens, e gerenciamento de membros.

7. **Comandos de Slash:**
   - Certifique-se de registrar os comandos de slash usando a biblioteca discord.py.

## Execução

Após realizar as configurações necessárias, execute o bot usando uma IDE de sua preferência ou digite seguinte comando:

```bash
python bot.py
```

**Nota:** Antes de executar o programa, lembre-se de modificar o código conforme necessário, especialmente no que diz respeito a tokens e configurações específicas do seu servidor Discord.

Agora, seu bot está pronto para operar e facilitar a administração do seu servidor Discord! Para mais informações sobre comandos e personalizações, consulte a documentação do Discord.py.
