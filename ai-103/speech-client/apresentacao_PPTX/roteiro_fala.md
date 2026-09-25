Oi, pessoal. Eu sou o Lucas e vou mostrar o lab de Azure Speech com agente, da certificação AI-103. A ideia: um agente de IA que fala e ouve.
Tem quatro peças. O agente é a IA, no caso o GPT-5. A ferramenta é o que ele usa pra fazer algo, aqui é fala. O Azure Speech transforma texto em áudio e áudio em texto. E o MCP é o plugue que liga o agente na ferramenta.
O fluxo é esse: meu programa manda o pedido, o agente recebe e decide usar o Speech. Se for pra gerar áudio, o arquivo vai pro Storage e volta um link. Meu programa não tem código de fala nenhum. Ele só conversa com o agente.
No Azure são três recursos: o Foundry, o projeto e um Storage pra guardar os áudios. O acesso ao Storage é por um link temporário, que vale só um dia.
Aqui é o agente: GPT-5, uma instrução simples e só a ferramenta de Speech ligada. Testei primeiro aqui no portal.
No Python são quatro trechos de código. O login é pelo Azure, então não tem senha no código. E eu só aponto pro agente pelo nome.
Funcionou nos dois testes. Pedi pra gerar uma frase em áudio e voltou o link do MP3. Pedi pra transcrever um áudio e voltou o texto.
Fiz também uma tela web por conta própria. Ela usa a mesma chamada e deixa ouvir o áudio direto na tela.
Deu problema em algumas coisas: o link do Storage tinha vencido e eu gerei outro. Tirei uma ferramenta que não era usada. E aprendi que mudança no agente só vale depois de salvar.
Resumindo: o agente decide quando usar a fala, e o programa não precisa saber nada de Speech. Um agente que fala e ouve, sem uma linha de Speech no client.