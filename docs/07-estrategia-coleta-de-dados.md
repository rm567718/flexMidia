# Estratégia de coleta de dados (Sprint 1)

## 1. Quais dados são coletados
Durante o uso do totem inteligente, serão coletados apenas **dados anônimos** e informações **necessárias para o funcionamento e análise de uso**.  
Os principais conjuntos de dados planejados são:

- **Interações do usuário:** toques na tela, comandos de voz, tempo de sessão, menus acessados.  
- **Solicitações de rota:** destino, tempo até a conclusão, escolha de alternativas.  
- **Engajamento com promoções:** promoções visualizadas, clicadas ou enviadas para o celular.  
- **Métricas de uso do sistema:** quantidade de sessões por dia, latência média de resposta, taxa de erros, eventos de reinício.  
- **Sensores auxiliares:** detecção de presença (PIR ou ToF) para ativação do sistema e ajuste de brilho/tela.

> Todos os dados são coletados sem identificação pessoal (sem CPF, nome, telefone ou dados sensíveis).

---

## 2. Forma de coleta (simulada ou planejada)
Nesta primeira fase, a coleta será **simulada**, representando o comportamento esperado de usuários em um ambiente real.

- **Simulação de uso:** registros artificiais gerados a partir de testes com os membros do grupo.  
- **Logs locais:** geração de eventos em arquivos `.csv` ou `.json` armazenados localmente para análise posterior.  
- **Coleta real futura:** na segunda fase do projeto (Sprint 2), será adicionada a coleta real dos sensores e interações físicas.

> Essa abordagem garante que o modelo conceitual possa ser validado antes de qualquer integração com hardware real.

---

## 3. Onde os dados são armazenados
A arquitetura prevê **dois níveis de armazenamento**:

| Camada | Local | Tipo de dados | Propósito |
|--------|--------|---------------|------------|
| **Local (borda)** | Dispositivo do totem (SD ou memória interna) | Logs temporários de interação e métricas | Operação imediata, offline |
| **Nuvem (dashboard)** | Serviço em cloud (Azure / Supabase / Firebase) | Dados agregados e anonimizados | Monitoramento e análise de engajamento |

> Apenas dados consolidados e anônimos serão enviados à nuvem, garantindo desempenho local e segurança.

---

## 4. Como proteger e descartar dados
- **Anonimização:** todos os registros usam identificadores aleatórios de sessão (ex.: `session_id`), sem vínculo com o usuário.  
- **Criptografia:** comunicação entre totem e nuvem feita via HTTPS/TLS.  
- **Retenção mínima:** logs locais são descartados automaticamente após 7 dias ou quando sincronizados com a nuvem.  
- **Consentimento:** caso futuramente sejam coletados dados pessoais (ex.: WhatsApp para envio de link), o consentimento explícito será solicitado na tela.  
- **Auditoria:** métricas de segurança e privacidade incluídas no dashboard para rastreabilidade e melhoria contínua.

---

✅ **Resumo**
A coleta de dados é **segura, anônima e simulada** nesta Sprint 1.  
Os registros servirão apenas para **validação de arquitetura e desempenho**, garantindo conformidade com **LGPD** e boas práticas de **IA ética**.

