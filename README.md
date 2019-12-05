# Download-Bot

___

## Introdução:

  O conceito fundamental por trás de qualquer implementação com o intuito de automatizar um processo é a eficiência.
  
  De um modo bem amplo, automatizar é fazer um processo mais eficiente, seja essa eficiência baseada no consumo de matérias primas e energia, na complexidade de realizar determinada etapa de um processo ou o tempo que um processo leva para reiniciar (pensando em um processo cíclico).
  
   Faz parte do senso-comum pensar em automatização em linhas de produção de grandes indústrias, processos de grandes empresas e serviços de larga escala no geral em diversos setores. Além disso, é comum pensar em automatização de uma visão negativa, associando a corte de gastos e desempregos por causa da substituição do trabalho humano, sendo algo indesejado e que somente beneficia grandes corporações.
   
   Entretanto a automatização não é um inimigo da sociedade mas sim uma ferramenta para levar a mesma mais longe, podendo ser aplicada nos mais diversos problemas e situações, buscando não a substituição do trabalho humano, mas sim a redução de esforço para um indivíduo, melhor condições de trabalho, redução de riscos e potenciais problemas futuros que podem ser por vezes fatais para um ser humano.
   
   Neste trabalho, o razão que motiva a automação  não é redução de custos e de riscos, nem nada a ponto de modificar uma sociedade inteira mas que não deixa de ser menos válida e é ainda positiva: realizar uma tarefa entediante, cíclica, monótona e estressante no lugar de um ser humano.
   
   Essa tarefa é algo muito comum e que provavelmente muitas pessoas praticam: baixar filmes ou episódios de uma determinada série. O processo de baixar um filme tem várias etapas problemáticas que podem ser divididas em três categorias (ou etapas). São elas:
   
**1. Navegação**

Nessa etapa são incluídas todos as dificuldades entre abrir o navegador e iniciar o *download* do arquivo, como por exemplo:
* clicar em cada link de cada episódio
* Lidar com:
    * ads e pop-ups
    * redirecionamentos para sites incorretos e/ou mal intencionados
    * Verificações diversar para evitar *bots*
    
**2. Monitoramento**

Nessa etapa são incluídas as dificuldades durante o processo de *download*, como por exemplo:
* Baixar vários arquivos de uma vez
* Falha de conexão com a rede (geralmente causado pelo problema acima)
* Geração de um arquivo corrompido ou imcompleto (geralmente causado pelo problema acima)


**3. Gestão**

Nessa etapa são incluídas as dificuldades após o processo de *download*, como por exemplo:
* Manter o diretório *Downloads* do computador organizado, ordenando corretamente cada arquivo na pasta correspondente
* Lidar com arquivos incompletos ou corrompidos (deletar o arquivo e reiniciar o processo)

___

## Objetivos:

O projeto tem como **objetivo  principal** acessar um site definido para baixar automaticamente episódios de uma determinada série ou filme.

Também existem tem alguns **objetivos secundários** relativos à eficiência (em termos de tempo e redução de recursos),  autonomia, controle e geração de relatórios. São eles:

* **Eficiência:** Fazer todos os passos que um usuário faria mais rapidamente (e consequentemente reduzir o trabalho do usuário)

* **Autonomia:** Conseguir rodar sozinho por longos períodos e estar pronto pra lidar com problemas externos (queda de conexão, por exemplo)

* **Controle:** Capaz de monitorar qual *download* está sendo executado (evitar baixar diversos episódios de uma vez e acabar reduzindo a velocidade de conexão da rede)

* **Geração de Relatórios:** registrar medidas para posterior análise como, por exemplo, quais episódios já foram baixados, tempo para concluir o *download*, velocidade média de *download*, se o *download* precisou ser reiniciado e quantas vezes isso ocorreu, etc.

Por fim, existem **objetivos bônus** relacionados a usabilidade:

* **Biblioteca:** Estruturar o código para que ele funcione como uma biblioteca (estrutura `Class`)

* **Navegadores:** Rodar o programa em qualquer navegador (Google Chrome, FireFox, Safari etc.) de forma '*headless*'

* **Interface:** Elaborar uma interface com a qual o usuário possa interagir sem a necessidade de alterar o código e/ou fazer *inputs* no console

* **WhatsApp:** Ser capaz de avisar remotamente o usuário sobre a fim do processo através de mensagens pelo WhatsApp

___

## Limitações:

A biblioteca `Selenium` do Python será utilizada, funcionando em conjunto com um WebDriver, assume o controle de uma janela do navegador e navega através da estrutura (HTML) do *site* (baseando-se nos elementos em HTML e os parâmetros atribuídos a eles). Como cada *site* possui uma estrutura, elementos e atributos distintos o programa será elaborado baseando-se em um apenas um.

O *site* escolhido para esse projeto será o https://saikoanimes.com pelos seguintes motivos:

* Páginas bem organizadas, com pouca propaganda e com estrutura base bem definida
* Páginas de fácil reconhecimento dos elementos
* Os links redirecionam diretamente para a página de download, sem precisar lidar com pop-ups ou verificações anti-bots

Além disso, outra limitação que deve ser comentada é o navegador. O `Selenium` necessita de um WebDriver específico para cada navegador e que também precisa ser salvo em uma localização específica, onde cada qual possui dificuldades específicas de instalação. Por tanto, não será necessário que o programa rode em diferentes navegadores por não haver necessidade para tal.

Esse projeto foi desenvolvido no Ubuntu 18 e, por comodidade, será testado no navegador Mozilla FireFox. Para baixar o WebDriver correspondente basta baixar o arquivo correspondente ao seu sistema no link a seguir: https://github.com/mozilla/geckodriver/releases

Após baixar e descompactar o arquivo, abra o terminal e acesse o diretório onde se encontra o WebDriver e execute o seguinte comando:
> `sudo cp geckodriver /usr/local/bin`

___

## Estrutura do *Database*:

O programa contará com dois *databases* distintos em um mesmo arquivo elaborado em **JSON** (um dos formatos de dados mais comuns, pois diversas linguagens de programação possuem suporte para ler e manipular esse formato de dado). Cada uma dessas duas partes terá funções e comandos para interação específicos. Abaixo da descrição dos *databases* há exemplos da estrutura dos arquivos, para melhor entendimentimento e consulta durante a elaboração dos códigos (quando necessário).

* ***anime_data*:** Armazenamento dos dados extraídos através do `Selenium` de forma organizada, escalável e replicável (uma vez que serão vários animes diferentes que serão armazenados baseando-se na mesma estrutura)

>```
>anime_data = {
>    'anime_name': {'page_url':'anime_page.com',
>                   'episodes':{
>                               '01':{'link': 'anime_ep_01.com', 'status': 'downloaded'},
>                               '02':{'link': 'anime_ep_02.com', 'status': 'not downloaded'},
>                               '03':{'link': 'anime_ep_03.com', 'status': 'not downloaded'}
>                              }
>                  }
>             }
>```


* ***analysis_data:*** Armazenamento de dados para posterior análise e monitoria sobre o funcionamento e eficiência do programa

>```
>analysis_data = {{'anime_pages_extracted': 0,
>                   'anime_pages_acessed': 0,
>                   'links_extracted': 0,
>                   'links_acessed': 0,
>                   'completed_downloads': 0,
>                   'restarted_downloads': 0,
>                   'errors_detected': 0,
>                  }
>                }
>```

___
